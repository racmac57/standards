# Cleanup completion status
_Exported on 12/21/2025 at 20:29:33 EST from Cursor (2.2.43)_

---

**User**

when I log into my laptop the attached two windows load.  I assum they are needed to process chunked files.  However, I have limited space on my taskbar.  Can the something be done? Maybe have the files opened in the background

---

**Cursor**

Checking what launches these processes on login so we can run them in the background.


Checking for startup scripts and how these processes are launched:


The `Start-Watcher.ps1` script launches both processes with visible windows. Creating a background version that runs them without taskbar windows:


Creating a background version that runs these processes without visible windows. Using `pythonw.exe` for the watcher (no console) and running Streamlit hidden with output redirected to log files.


```powershell
param(
  [string]$RepoRoot = "$PSScriptRoot\.."
)

Set-Location $RepoRoot
$env:PYTHONUNBUFFERED = "1"

Write-Host "Initializing Enterprise RAG Pipeline (Background Mode)..." -ForegroundColor Cyan

# Check for OneDrive path
$oneDriveRoot = Join-Path $env:OneDriveCommercial "KB_Shared"
if (-not (Test-Path $oneDriveRoot)) {
  Write-Host "OneDrive KB_Shared missing." -ForegroundColor Red
  exit 1
}

# Ensure logs directory exists
$logsDir = Join-Path $RepoRoot "05_logs"
if (-not (Test-Path $logsDir)) {
  New-Item -ItemType Directory -Path $logsDir -Force | Out-Null
}

# Check if watcher is already running
$pidFile = Join-Path $RepoRoot "watcher_pid.txt"
$skipWatcherStart = $false
if (Test-Path $pidFile) {
  $watcherPid = Get-Content $pidFile | Select-Object -First 1
  if ($watcherPid -and (Get-Process -Id $watcherPid -ErrorAction SilentlyContinue)) {
    Write-Host "Watcher already running. PID=$watcherPid" -ForegroundColor Yellow
    Write-Host "Starting Dashboard only..." -ForegroundColor Green
    $skipWatcherStart = $true
  }
}

# Check if dashboard is already running
$dashboard = Get-WmiObject Win32_Process -ErrorAction SilentlyContinue | Where-Object { $_.CommandLine -like "*streamlit run dashboard_kb_monitoring.py*" }
if ($dashboard) {
  Write-Host "Dashboard already running. PID=$($dashboard.ProcessId)" -ForegroundColor Yellow
}

# 1. Activate the Virtual Environment (if available)
$VenvPath = Join-Path $RepoRoot ".venv\Scripts\Activate.ps1"
$PythonExe = "python"
$PythonwExe = "pythonw"
$PipExe = "pip"
if (Test-Path $VenvPath) {
    . $VenvPath
    $PythonExe = Join-Path $RepoRoot ".venv\Scripts\python.exe"
    $PythonwExe = Join-Path $RepoRoot ".venv\Scripts\pythonw.exe"
    $PipExe = Join-Path $RepoRoot ".venv\Scripts\pip.exe"
    Write-Host "Virtual environment activated." -ForegroundColor Gray
} else {
    Write-Warning "Virtual environment not found at $VenvPath. Attempting to run with system Python..."
}

# Check and install missing dependencies (especially plotly for dashboard)
Write-Host "Checking dependencies..." -ForegroundColor Gray
$requirementsFile = Join-Path $RepoRoot "requirements.txt"
if (Test-Path $requirementsFile) {
    try {
        # Quick check if plotly is installed (required for dashboard)
        $plotlyCheck = & $PythonExe -c "import plotly" 2>&1
        if ($LASTEXITCODE -ne 0) {
            Write-Host "Installing missing dependencies (plotly required for dashboard)..." -ForegroundColor Yellow
            & $PipExe install -q -r $requirementsFile
            if ($LASTEXITCODE -eq 0) {
                Write-Host "Dependencies installed successfully." -ForegroundColor Green
            } else {
                Write-Warning "Some dependencies may have failed to install. Dashboard may not work correctly."
            }
        } else {
            Write-Host "Dependencies check passed." -ForegroundColor Gray
        }
    } catch {
        Write-Warning "Could not verify dependencies. Dashboard may fail if plotly is missing."
    }
} else {
    Write-Warning "requirements.txt not found. Dashboard may fail if dependencies are missing."
}

# 2. Start the Watcher (The Core Processor) - Skip if already running
# This handles File Splitting AND Automatic KB Insertion
# Using pythonw.exe to run without console window
if (-not $skipWatcherStart) {
    Write-Host "Starting Watcher Service (Splitter + KB Auto-Insert) in background..." -ForegroundColor Green
    
    # Use pythonw.exe if available, otherwise fall back to python.exe with hidden window
    $watcherLogFile = Join-Path $logsDir "watcher_background.log"
    if (Test-Path $PythonwExe) {
        # pythonw.exe runs without console window
        $WatcherProcess = Start-Process -FilePath $PythonwExe `
            -ArgumentList "watcher_splitter.py" `
            -WorkingDirectory $RepoRoot `
            -WindowStyle Hidden `
            -PassThru
    } else {
        # Fallback: use python.exe but redirect output and hide window
        $WatcherProcess = Start-Process -FilePath $PythonExe `
            -ArgumentList "watcher_splitter.py" `
            -WorkingDirectory $RepoRoot `
            -WindowStyle Hidden `
            -RedirectStandardOutput $watcherLogFile `
            -RedirectStandardError $watcherLogFile `
            -PassThru
    }

    Start-Sleep -Seconds 2
    $watcherPid = $WatcherProcess.Id

    if ($null -ne $watcherPid -and (Get-Process -Id $watcherPid -ErrorAction SilentlyContinue)) {
      $watcherPid | Out-File -Encoding ascii -FilePath $pidFile -Force
      Write-Host "Watcher started in background. PID=$watcherPid" -ForegroundColor Green
      Write-Host "Logs: $watcherLogFile" -ForegroundColor Gray
    } else {
      Write-Host "Watcher process not found after start attempt." -ForegroundColor Red
      exit 1
    }

    # Optional: Health check (if KB-Health.ps1 exists)
    if (Test-Path "$RepoRoot\scripts\KB-Health.ps1") {
      $health = & "$RepoRoot\scripts\KB-Health.ps1" -RepoRoot $RepoRoot -OD $env:OneDriveCommercial
      if ($health -is [System.Array]) {
        $health = $health[0]
      }
      if ($health.Watcher -notlike "Running*") {
        Write-Host "Watcher health check failed: $($health.Watcher)" -ForegroundColor Red
        if ($null -ne $watcherPid -and (Get-Process -Id $watcherPid -ErrorAction SilentlyContinue)) {
          Stop-Process -Id $watcherPid -Force
        }
        if (Test-Path $pidFile) {
          Remove-Item $pidFile -ErrorAction SilentlyContinue
        }
        exit 1
      }
    }
}

# 3. Start the Monitoring Dashboard
# This allows you to view the Database and Real-time stats
# Running in hidden mode - access via browser at http://localhost:8501
if (-not $dashboard) {
  Write-Host "Starting KB Monitoring Dashboard in background..." -ForegroundColor Green
  $StreamlitExe = Join-Path $RepoRoot ".venv\Scripts\streamlit.exe"
  if (-not (Test-Path $StreamlitExe)) {
      $StreamlitExe = "streamlit"
  }
  
  $dashboardLogFile = Join-Path $logsDir "dashboard_background.log"
  Start-Process -FilePath $StreamlitExe `
      -ArgumentList "run dashboard_kb_monitoring.py" `
      -WorkingDirectory $RepoRoot `
      -WindowStyle Hidden `
      -RedirectStandardOutput $dashboardLogFile `
      -RedirectStandardError $dashboardLogFile `
      -PassThru | Out-Null
  
  Write-Host "Dashboard starting in background..." -ForegroundColor Gray
  Write-Host "Access dashboard at: http://localhost:8501" -ForegroundColor Cyan
  Write-Host "Logs: $dashboardLogFile" -ForegroundColor Gray
} else {
  Write-Host "Dashboard already running." -ForegroundColor Gray
}

Write-Host ""
Write-Host "All systems operational (running in background)." -ForegroundColor Cyan
Write-Host "1. Drop files into '02_data' to process." -ForegroundColor White
Write-Host "2. Access dashboard at: http://localhost:8501" -ForegroundColor White
Write-Host "3. Check logs in: $logsDir" -ForegroundColor White
Write-Host ""
Write-Host "To stop services, run: scripts\Stop-Watcher.ps1" -ForegroundColor Yellow

```

```vb
' VBScript wrapper to run Start-Watcher-Background.ps1 silently
' This ensures no console windows appear at all

Set objShell = CreateObject("WScript.Shell")
Set objFSO = CreateObject("Scripting.FileSystemObject")

' Get the script directory
strScriptPath = objFSO.GetParentFolderName(WScript.ScriptFullName)
strRepoRoot = objFSO.GetParentFolderName(strScriptPath)
strPowerShellScript = objFSO.BuildPath(strScriptPath, "Start-Watcher-Background.ps1")

' Run PowerShell script silently (no window)
objShell.Run "powershell.exe -ExecutionPolicy Bypass -WindowStyle Hidden -File """ & strPowerShellScript & """", 0, False

```

Checking for startup configuration and creating a quick reference guide:


```markdown
# Running Watcher in Background Mode

## Problem
When the watcher and dashboard start, they create console windows that take up space on your taskbar. This can be annoying if you have limited taskbar space.

## Solution
Use the background versions of the startup scripts that run processes without visible windows.

## Usage

### Option 1: PowerShell Script (Recommended)
Run the background PowerShell script:
```powershell
.\scripts\Start-Watcher-Background.ps1
```

### Option 2: VBScript Wrapper (Completely Silent)
Double-click or run:
```powershell
.\scripts\Start-Watcher-Background.vbs
```

This runs the PowerShell script with no console window at all.

## What's Different?

### Background Mode:
- **Watcher**: Runs using `pythonw.exe` (no console window) or `python.exe` with hidden window
- **Dashboard**: Runs with hidden window, accessible via browser at http://localhost:8501
- **Logs**: All output redirected to log files in `05_logs/`:
  - `watcher_background.log` - Watcher output
  - `dashboard_background.log` - Streamlit dashboard output

### Normal Mode:
- **Watcher**: Minimized console window (still visible in taskbar)
- **Dashboard**: Normal console window (visible in taskbar)

## Accessing the Dashboard

Even though the dashboard runs in the background, you can still access it:
1. Open your browser
2. Navigate to: http://localhost:8501
3. The dashboard will load normally

## Checking Status

To check if services are running:
```powershell
.\scripts\KB-Health.ps1
```

Or check the log files:
```powershell
Get-Content .\05_logs\watcher_background.log -Tail 20
Get-Content .\05_logs\dashboard_background.log -Tail 20
```

## Stopping Services

To stop the background services:
```powershell
.\scripts\Stop-Watcher.ps1
```

## Setting Up Auto-Start on Login

If you want these to start automatically when you log in:

1. **Create a shortcut** to `scripts\Start-Watcher-Background.vbs`
2. **Copy the shortcut** to your Windows Startup folder:
   - Press `Win+R`
   - Type: `shell:startup`
   - Press Enter
   - Paste the shortcut there

Now the services will start automatically in the background when you log in, without any visible windows!

## Troubleshooting

### Dashboard not accessible?
- Check if Streamlit is running: `Get-Process | Where-Object {$_.ProcessName -like "*streamlit*"}`
- Check the dashboard log: `Get-Content .\05_logs\dashboard_background.log`
- Try accessing: http://localhost:8501

### Watcher not processing files?
- Check the watcher log: `Get-Content .\05_logs\watcher_background.log -Tail 50`
- Verify watcher is running: `Get-Content .\watcher_pid.txt` then check if that PID exists

### Need to see console output?
- Switch back to the normal script: `.\scripts\Start-Watcher.ps1`
- Or check the log files in `05_logs/`

```

Created a background version that runs without visible windows. Here's what was added:

## New Files Created

1. **`scripts\Start-Watcher-Background.ps1`** — Background version that:
   - Uses `pythonw.exe` for the watcher (no console window)
   - Runs Streamlit with a hidden window
   - Redirects all output to log files in `05_logs/`
   - Dashboard accessible at http://localhost:8501

2. **`scripts\Start-Watcher-Background.vbs`** — VBScript wrapper for silent execution (no PowerShell window)

3. **`scripts\README-Background.md`** — Documentation

## How to Use

### To run in background mode:
```powershell
.\scripts\Start-Watcher-Background.ps1
```

Or double-click:
```
scripts\Start-Watcher-Background.vbs
```

### To set up auto-start on login (no visible windows):

1. Create a shortcut to `scripts\Start-Watcher-Background.vbs`
2. Press `Win+R`, type `shell:startup`, press Enter
3. Copy the shortcut into that folder

The services will start automatically in the background when you log in, with no taskbar windows.

## Accessing the Dashboard

Even though it runs in the background, you can still access the dashboard:
- Open your browser and go to: **http://localhost:8501**

## Checking Logs

If you need to see what's happening:
```powershell
Get-Content .\05_logs\watcher_background.log -Tail 20
Get-Content .\05_logs\dashboard_background.log -Tail 20
```

The background version keeps the same functionality but runs without visible console windows, freeing up your taskbar space.

```powershell
.\scripts\Start-Watcher-Background.ps1
```

```plaintext
scripts\Start-Watcher-Background.vbs
```

```powershell
Get-Content .\05_logs\watcher_background.log -Tail 20
Get-Content .\05_logs\dashboard_background.log -Tail 20
```

---

**User**

can i close the two windows now? and if i run@scripts/Start-Watcher.ps1 to start it back up with both windows running in the background?

---

**Cursor**

Checking the stop script, then clarifying:


To run them in the background, use the background script, not the regular one.

1. Stop the current processes:
```powershell
.\scripts\Stop-Watcher.ps1
```

2. Start them in background mode:
```powershell
.\scripts\Start-Watcher-Background.ps1
```

Important: Use `Start-Watcher-Background.ps1`, not `Start-Watcher.ps1`. The regular script still shows windows:
- Watcher: `-WindowStyle Minimized` (still appears in taskbar)
- Dashboard: `-WindowStyle Normal` (shows console window)

The background version runs both without visible windows.

Updating the regular script to also support a background mode option:


```powershell
.\scripts\Stop-Watcher.ps1
```

```powershell
.\scripts\Start-Watcher-Background.ps1
```

## Quick Answer

**Yes, you can close the windows**, but:

1. Stop them properly first (don't just close the windows):
   ```powershell
   .\scripts\Stop-Watcher.ps1
   ```

2. Then start in background mode:
   ```powershell
   .\scripts\Start-Watcher-Background.ps1
   ```

**Note:** `Start-Watcher.ps1` will still show windows. Use `Start-Watcher-Background.ps1` for background mode.

## Summary

- Close windows? Yes, but stop the processes first with `Stop-Watcher.ps1`
- Use `Start-Watcher.ps1`? No — that still shows windows
- Use `Start-Watcher-Background.ps1`? Yes — that runs in the background

After starting in background mode:
- No windows will appear in your taskbar
- Dashboard is still accessible at http://localhost:8501
- Logs are in `05_logs\watcher_background.log` and `05_logs\dashboard_background.log`

Should I add a `-Background` switch to `Start-Watcher.ps1` so you can use one script with an option?

```powershell
   .\scripts\Stop-Watcher.ps1
```

```powershell
   .\scripts\Start-Watcher-Background.ps1
```

```powershell
   .\scripts\Stop-Watcher.ps1
```

```powershell
   .\scripts\Start-Watcher-Background.ps1
```

---

**User**

C:\_chunker\2025_12_21__chunker_directory_tree.json
please review the directory tree.  The directory is too cluttered, can we clean up the logs, archive the old files/scripts.  Move files in the root to the correct directories?

---

**Cursor**

Reviewing the directory tree to identify cleanup and reorganization opportunities.


Reviewing the structure and drafting a cleanup plan:


Creating a cleanup script to organize the directory. Identifying files to move:


Creating a cleanup script to organize the directory:


```powershell
# Directory Cleanup Script
# Organizes files in the root directory into appropriate subdirectories

param(
    [string]$RepoRoot = "$PSScriptRoot\..",
    [switch]$WhatIf = $false,
    [switch]$ArchiveOld = $true
)

Set-Location $RepoRoot

Write-Host "=== Directory Cleanup Script ===" -ForegroundColor Cyan
Write-Host "Repository Root: $RepoRoot" -ForegroundColor Gray
if ($WhatIf) {
    Write-Host "DRY RUN MODE - No files will be moved" -ForegroundColor Yellow
}
Write-Host ""

$movedCount = 0
$errors = @()

# Ensure target directories exist
$targetDirs = @(
    "05_logs",
    "05_logs\legacy",
    "scripts",
    "99_doc",
    "99_doc\archive",
    "99_doc\archive\old_scripts",
    "03_archive\old_backups",
    "tests\archive"
)

foreach ($dir in $targetDirs) {
    $fullPath = Join-Path $RepoRoot $dir
    if (-not (Test-Path $fullPath)) {
        if (-not $WhatIf) {
            New-Item -ItemType Directory -Path $fullPath -Force | Out-Null
        }
        Write-Host "Created directory: $dir" -ForegroundColor Gray
    }
}

# Function to safely move files
function Move-FileSafely {
    param(
        [string]$Source,
        [string]$Destination,
        [string]$Category
    )
    
    if (-not (Test-Path $Source)) {
        return $false
    }
    
    $destDir = Split-Path $Destination -Parent
    if (-not (Test-Path $destDir)) {
        if (-not $WhatIf) {
            New-Item -ItemType Directory -Path $destDir -Force | Out-Null
        }
    }
    
    if (Test-Path $Destination) {
        # File exists - create unique name with timestamp
        $name = [System.IO.Path]::GetFileNameWithoutExtension($Source)
        $ext = [System.IO.Path]::GetExtension($Source)
        $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
        $Destination = Join-Path $destDir "${name}_${timestamp}${ext}"
    }
    
    try {
        if ($WhatIf) {
            Write-Host "  [WOULD MOVE] $Source -> $Destination" -ForegroundColor Yellow
        } else {
            Move-Item -Path $Source -Destination $Destination -Force
            Write-Host "  ✓ Moved: $([System.IO.Path]::GetFileName($Source)) -> $Category" -ForegroundColor Green
        }
        return $true
    } catch {
        $script:errors += "Failed to move $Source : $_"
        Write-Host "  ✗ Error moving $Source : $_" -ForegroundColor Red
        return $false
    }
}

# 1. Move log files from root to 05_logs
Write-Host "1. Moving log files to 05_logs..." -ForegroundColor Cyan
$logFiles = @(
    "watcher_error.log",
    "watcher_live.log",
    "watcher_live_error.log",
    "watcher_test.log",
    "test_output.log",
    "last_1500_lines.log",
    "tree_report_error.log"
)

foreach ($logFile in $logFiles) {
    $source = Join-Path $RepoRoot $logFile
    $dest = Join-Path $RepoRoot "05_logs\$logFile"
    if (Move-FileSafely -Source $source -Destination $dest -Category "05_logs") {
        $movedCount++
    }
}

# 2. Move PowerShell scripts from root to scripts/
Write-Host ""
Write-Host "2. Moving PowerShell scripts to scripts/..." -ForegroundColor Cyan
$psScripts = @(
    "copy_files_for_processing.ps1",
    "copy_files_back_to_source.ps1",
    "move_files_for_processing.ps1",
    "create_mapping_for_existing_files.ps1",
    "Chunker_MoveOptimized.ps1",
    "prepare_claude_files.ps1",
    "prepare_grok_review.ps1"
)

foreach ($script in $psScripts) {
    $source = Join-Path $RepoRoot $script
    $dest = Join-Path $RepoRoot "scripts\$script"
    if (Move-FileSafely -Source $source -Destination $dest -Category "scripts/") {
        $movedCount++
    }
}

# 3. Move documentation files to 99_doc/
Write-Host ""
Write-Host "3. Moving documentation files to 99_doc/..." -ForegroundColor Cyan
$docFiles = @(
    "2025_11_07_CHATGPT_tagging_fix.md",
    "2025_11_09_claude_code_prompt_chunker.txt",
    "2025_12_21__chunker_directory_tree.json",
    "2025_12_21__chunker_directory_tree.md",
    "CLAUDE_CODE_TASK_PROMPT.md",
    "CLAUDE_GUI_COLLABORATION_PROMPT.md",
    "CLAUDE_IMPLEMENTATION_GUIDE.md",
    "CURSOR_FIX_PROMPT.md",
    "DATABASE_IMPROVEMENTS.md",
    "DESKTOP_SYNC.md",
    "FAILED_FILES_CLARIFICATION.md",
    "FIX_DESKTOP_SYNC.md",
    "FIXES_APPLIED_SUMMARY.md",
    "FINAL_STATUS.md",
    "GIT_SETUP_STATUS.md",
    "GROK_COLLABORATION_PROMPT.md",
    "GROK_FEEDBACK_001.md",
    "GROK_HNSW_FIX_PROMPT.md",
    "GROK_REFERENCE_PACKAGE.md",
    "GROK_REVIEW_PACKAGE.md",
    "GROK_SIMPLIFICATION_RECOMMENDATIONS.md",
    "grok_review_prompt.md",
    "HANDOFF_PROMPT.md",
    "handoff_brief.md",
    "IMPLEMENTATION_STATUS.md",
    "IMPLEMENTATION_SUMMARY.md",
    "KB_INTEGRATION_GUIDE.md",
    "LOG_REVIEW_AND_FIXES.md",
    "MONITOR_DB_LOCKS.md",
    "MOVE_WORKFLOW_IMPLEMENTATION.md",
    "PROMPT_KB_INTEGRATION.md",
    "QUICK_START_PROMPT.md",
    "RECOVERY_SUCCESS.md",
    "REPROCESSING_RUN_PLAN.md",
    "SYNC_INSTRUCTIONS.md",
    "TASK_PROGRESS_REPORT.md",
    "UPDATE_SUMMARY_2025-11-08.md",
    "VERIFICATION_REPORT.md"
)

foreach ($doc in $docFiles) {
    $source = Join-Path $RepoRoot $doc
    $dest = Join-Path $RepoRoot "99_doc\$doc"
    if (Move-FileSafely -Source $source -Destination $dest -Category "99_doc/") {
        $movedCount++
    }
}

# 4. Move test files to tests/archive
Write-Host ""
Write-Host "4. Moving test files to tests/archive..." -ForegroundColor Cyan
$testFiles = @(
    "test_celery_integration.py",
    "test_origin_tracking.py",
    "test_processing_workflow.py",
    "test_python_demo.py",
    "test_search.py",
    "simple_rag_test.py",
    "rag_test.py",
    "test_queries.json"
)

foreach ($testFile in $testFiles) {
    $source = Join-Path $RepoRoot $testFile
    $dest = Join-Path $RepoRoot "tests\archive\$testFile"
    if (Move-FileSafely -Source $source -Destination $dest -Category "tests/archive/") {
        $movedCount++
    }
}

# 5. Move utility/analysis scripts to appropriate locations
Write-Host ""
Write-Host "5. Organizing utility scripts..." -ForegroundColor Cyan
$utilityMoves = @{
    "_analyze_remaining.py" = "tools"
    "_check_py_files.py" = "tools"
    "_check_remaining.py" = "tools"
    "analyze_empty_folders.py" = "tools"
    "analyze_failed_files.py" = "tools"
    "check_collection_dim.py" = "tools"
    "diagnose_issues.py" = "tools"
    "verify_backfill.py" = "tools"
    "verify_chunk_completeness.py" = "tools"
    "verify_enhancements.py" = "tools"
}

foreach ($file in $utilityMoves.Keys) {
    $source = Join-Path $RepoRoot $file
    $destDir = $utilityMoves[$file]
    $dest = Join-Path $RepoRoot "$destDir\$file"
    if (Move-FileSafely -Source $source -Destination $dest -Category "$destDir/") {
        $movedCount++
    }
}

# 6. Archive old backup directories
if ($ArchiveOld) {
    Write-Host ""
    Write-Host "6. Archiving old backup directories..." -ForegroundColor Cyan
    $backupDirs = @(
        "backup_20251107",
        "archive"
    )
    
    foreach ($backupDir in $backupDirs) {
        $source = Join-Path $RepoRoot $backupDir
        if (Test-Path $source) {
            $dest = Join-Path $RepoRoot "03_archive\old_backups\$backupDir"
            try {
                if ($WhatIf) {
                    Write-Host "  [WOULD MOVE] $backupDir -> 03_archive\old_backups\" -ForegroundColor Yellow
                } else {
                    Move-Item -Path $source -Destination $dest -Force
                    Write-Host "  ✓ Archived: $backupDir" -ForegroundColor Green
                    $movedCount++
                }
            } catch {
                $errors += "Failed to archive $backupDir : $_"
                Write-Host "  ✗ Error archiving $backupDir : $_" -ForegroundColor Red
            }
        }
    }
}

# 7. Clean up odd files (10, 240, 90, bool, python, nul, Tuple[bool, etc.)
Write-Host ""
Write-Host "7. Cleaning up odd files..." -ForegroundColor Cyan
$oddFiles = @("10", "240", "90", "bool", "python", "nul", "Tuple[bool")

foreach ($oddFile in $oddFiles) {
    $source = Join-Path $RepoRoot $oddFile
    if (Test-Path $source) {
        try {
            if ($WhatIf) {
                Write-Host "  [WOULD DELETE] $oddFile" -ForegroundColor Yellow
            } else {
                Remove-Item -Path $source -Force -ErrorAction Stop
                Write-Host "  ✓ Deleted odd file: $oddFile" -ForegroundColor Green
                $movedCount++
            }
        } catch {
            $errors += "Failed to delete $oddFile : $_"
            Write-Host "  ✗ Error deleting $oddFile : $_" -ForegroundColor Red
        }
    }
}

# 8. Move old release files to archive
Write-Host ""
Write-Host "8. Archiving old release files..." -ForegroundColor Cyan
$releaseFiles = @(
    "release_docs_v2025.11.09.zip",
    "release_log.txt"
)

foreach ($releaseFile in $releaseFiles) {
    $source = Join-Path $RepoRoot $releaseFile
    $dest = Join-Path $RepoRoot "03_archive\old_backups\$releaseFile"
    if (Move-FileSafely -Source $source -Destination $dest -Category "03_archive/old_backups/") {
        $movedCount++
    }
}

# 9. Move old config backups
Write-Host ""
Write-Host "9. Organizing config backups..." -ForegroundColor Cyan
$configBackups = Get-ChildItem -Path $RepoRoot -Filter "config.json.backup_*" -ErrorAction SilentlyContinue
foreach ($backup in $configBackups) {
    $dest = Join-Path $RepoRoot "06_config\backups\$($backup.Name)"
    if (Move-FileSafely -Source $backup.FullName -Destination $dest -Category "06_config/backups/") {
        $movedCount++
    }
}

# 10. Move reprocess config to 06_config
Write-Host ""
Write-Host "10. Organizing config files..." -ForegroundColor Cyan
$reprocessConfig = Join-Path $RepoRoot "reprocess_config.json"
if (Test-Path $reprocessConfig) {
    $dest = Join-Path $RepoRoot "06_config\reprocess_config.json"
    if (Move-FileSafely -Source $reprocessConfig -Destination $dest -Category "06_config/") {
        $movedCount++
    }
}

# Summary
Write-Host ""
Write-Host "=== Cleanup Summary ===" -ForegroundColor Cyan
Write-Host "Files processed: $movedCount" -ForegroundColor $(if ($movedCount -gt 0) { "Green" } else { "Gray" })
if ($errors.Count -gt 0) {
    Write-Host "Errors: $($errors.Count)" -ForegroundColor Red
    foreach ($error in $errors) {
        Write-Host "  - $error" -ForegroundColor Red
    }
} else {
    Write-Host "No errors encountered." -ForegroundColor Green
}

if ($WhatIf) {
    Write-Host ""
    Write-Host "This was a DRY RUN. Run without -WhatIf to perform actual moves." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Cleanup complete!" -ForegroundColor Cyan

```

Created a cleanup script. Reviewing what it will do, then running it:


Fixing the syntax error in the script:


Fixing special character issues in the script:


```powershell
# Directory Cleanup Script
# Organizes files in the root directory into appropriate subdirectories

param(
    [string]$RepoRoot = "$PSScriptRoot\..",
    [switch]$WhatIf = $false,
    [switch]$ArchiveOld = $true
)

Set-Location $RepoRoot

Write-Host "=== Directory Cleanup Script ===" -ForegroundColor Cyan
Write-Host "Repository Root: $RepoRoot" -ForegroundColor Gray
if ($WhatIf) {
    Write-Host "DRY RUN MODE - No files will be moved" -ForegroundColor Yellow
}
Write-Host ""

$movedCount = 0
$errors = @()

# Ensure target directories exist
$targetDirs = @(
    "05_logs",
    "05_logs\legacy",
    "scripts",
    "99_doc",
    "99_doc\archive",
    "99_doc\archive\old_scripts",
    "03_archive\old_backups",
    "tests\archive"
)

foreach ($dir in $targetDirs) {
    $fullPath = Join-Path $RepoRoot $dir
    if (-not (Test-Path $fullPath)) {
        if (-not $WhatIf) {
            New-Item -ItemType Directory -Path $fullPath -Force | Out-Null
        }
        Write-Host "Created directory: $dir" -ForegroundColor Gray
    }
}

# Function to safely move files
function Move-FileSafely {
    param(
        [string]$Source,
        [string]$Destination,
        [string]$Category
    )
    
    if (-not (Test-Path $Source)) {
        return $false
    }
    
    $destDir = Split-Path $Destination -Parent
    if (-not (Test-Path $destDir)) {
        if (-not $WhatIf) {
            New-Item -ItemType Directory -Path $destDir -Force | Out-Null
        }
    }
    
    if (Test-Path $Destination) {
        # File exists - create unique name with timestamp
        $name = [System.IO.Path]::GetFileNameWithoutExtension($Source)
        $ext = [System.IO.Path]::GetExtension($Source)
        $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
        $Destination = Join-Path $destDir "${name}_${timestamp}${ext}"
    }
    
    try {
        if ($WhatIf) {
            Write-Host "  [WOULD MOVE] $Source -> $Destination" -ForegroundColor Yellow
        } else {
            Move-Item -Path $Source -Destination $Destination -Force
            Write-Host "  [OK] Moved: $([System.IO.Path]::GetFileName($Source)) -> $Category" -ForegroundColor Green
        }
        return $true
    } catch {
        $script:errors += "Failed to move $Source : $_"
        Write-Host "  ✗ Error moving $Source : $_" -ForegroundColor Red
        return $false
    }
}

# 1. Move log files from root to 05_logs
Write-Host "1. Moving log files to 05_logs..." -ForegroundColor Cyan
$logFiles = @(
    "watcher_error.log",
    "watcher_live.log",
    "watcher_live_error.log",
    "watcher_test.log",
    "test_output.log",
    "last_1500_lines.log",
    "tree_report_error.log"
)

foreach ($logFile in $logFiles) {
    $source = Join-Path $RepoRoot $logFile
    $dest = Join-Path $RepoRoot "05_logs\$logFile"
    if (Move-FileSafely -Source $source -Destination $dest -Category "05_logs") {
        $movedCount++
    }
}

# 2. Move PowerShell scripts from root to scripts/
Write-Host ""
Write-Host "2. Moving PowerShell scripts to scripts/..." -ForegroundColor Cyan
$psScripts = @(
    "copy_files_for_processing.ps1",
    "copy_files_back_to_source.ps1",
    "move_files_for_processing.ps1",
    "create_mapping_for_existing_files.ps1",
    "Chunker_MoveOptimized.ps1",
    "prepare_claude_files.ps1",
    "prepare_grok_review.ps1"
)

foreach ($script in $psScripts) {
    $source = Join-Path $RepoRoot $script
    $dest = Join-Path $RepoRoot "scripts\$script"
    if (Move-FileSafely -Source $source -Destination $dest -Category "scripts/") {
        $movedCount++
    }
}

# 3. Move documentation files to 99_doc/
Write-Host ""
Write-Host "3. Moving documentation files to 99_doc/..." -ForegroundColor Cyan
$docFiles = @(
    "2025_11_07_CHATGPT_tagging_fix.md",
    "2025_11_09_claude_code_prompt_chunker.txt",
    "2025_12_21__chunker_directory_tree.json",
    "2025_12_21__chunker_directory_tree.md",
    "CLAUDE_CODE_TASK_PROMPT.md",
    "CLAUDE_GUI_COLLABORATION_PROMPT.md",
    "CLAUDE_IMPLEMENTATION_GUIDE.md",
    "CURSOR_FIX_PROMPT.md",
    "DATABASE_IMPROVEMENTS.md",
    "DESKTOP_SYNC.md",
    "FAILED_FILES_CLARIFICATION.md",
    "FIX_DESKTOP_SYNC.md",
    "FIXES_APPLIED_SUMMARY.md",
    "FINAL_STATUS.md",
    "GIT_SETUP_STATUS.md",
    "GROK_COLLABORATION_PROMPT.md",
    "GROK_FEEDBACK_001.md",
    "GROK_HNSW_FIX_PROMPT.md",
    "GROK_REFERENCE_PACKAGE.md",
    "GROK_REVIEW_PACKAGE.md",
    "GROK_SIMPLIFICATION_RECOMMENDATIONS.md",
    "grok_review_prompt.md",
    "HANDOFF_PROMPT.md",
    "handoff_brief.md",
    "IMPLEMENTATION_STATUS.md",
    "IMPLEMENTATION_SUMMARY.md",
    "KB_INTEGRATION_GUIDE.md",
    "LOG_REVIEW_AND_FIXES.md",
    "MONITOR_DB_LOCKS.md",
    "MOVE_WORKFLOW_IMPLEMENTATION.md",
    "PROMPT_KB_INTEGRATION.md",
    "QUICK_START_PROMPT.md",
    "RECOVERY_SUCCESS.md",
    "REPROCESSING_RUN_PLAN.md",
    "SYNC_INSTRUCTIONS.md",
    "TASK_PROGRESS_REPORT.md",
    "UPDATE_SUMMARY_2025-11-08.md",
    "VERIFICATION_REPORT.md"
)

foreach ($doc in $docFiles) {
    $source = Join-Path $RepoRoot $doc
    $dest = Join-Path $RepoRoot "99_doc\$doc"
    if (Move-FileSafely -Source $source -Destination $dest -Category "99_doc/") {
        $movedCount++
    }
}

# 4. Move test files to tests/archive
Write-Host ""
Write-Host "4. Moving test files to tests/archive..." -ForegroundColor Cyan
$testFiles = @(
    "test_celery_integration.py",
    "test_origin_tracking.py",
    "test_processing_workflow.py",
    "test_python_demo.py",
    "test_search.py",
    "simple_rag_test.py",
    "rag_test.py",
    "test_queries.json"
)

foreach ($testFile in $testFiles) {
    $source = Join-Path $RepoRoot $testFile
    $dest = Join-Path $RepoRoot "tests\archive\$testFile"
    if (Move-FileSafely -Source $source -Destination $dest -Category "tests/archive/") {
        $movedCount++
    }
}

# 5. Move utility/analysis scripts to appropriate locations
Write-Host ""
Write-Host "5. Organizing utility scripts..." -ForegroundColor Cyan
$utilityMoves = @{
    "_analyze_remaining.py" = "tools"
    "_check_py_files.py" = "tools"
    "_check_remaining.py" = "tools"
    "analyze_empty_folders.py" = "tools"
    "analyze_failed_files.py" = "tools"
    "check_collection_dim.py" = "tools"
    "diagnose_issues.py" = "tools"
    "verify_backfill.py" = "tools"
    "verify_chunk_completeness.py" = "tools"
    "verify_enhancements.py" = "tools"
}

foreach ($file in $utilityMoves.Keys) {
    $source = Join-Path $RepoRoot $file
    $destDir = $utilityMoves[$file]
    $dest = Join-Path $RepoRoot "$destDir\$file"
    if (Move-FileSafely -Source $source -Destination $dest -Category "$destDir/") {
        $movedCount++
    }
}

# 6. Archive old backup directories
if ($ArchiveOld) {
    Write-Host ""
    Write-Host "6. Archiving old backup directories..." -ForegroundColor Cyan
    $backupDirs = @(
        "backup_20251107",
        "archive"
    )
    
    foreach ($backupDir in $backupDirs) {
        $source = Join-Path $RepoRoot $backupDir
        if (Test-Path $source) {
            $dest = Join-Path $RepoRoot "03_archive\old_backups\$backupDir"
            try {
                if ($WhatIf) {
                    Write-Host "  [WOULD MOVE] $backupDir -> 03_archive\old_backups\" -ForegroundColor Yellow
                } else {
                    Move-Item -Path $source -Destination $dest -Force
                    Write-Host "  ✓ Archived: $backupDir" -ForegroundColor Green
                    $movedCount++
                }
            } catch {
                $errors += "Failed to archive $backupDir : $_"
                Write-Host "  ✗ Error archiving $backupDir : $_" -ForegroundColor Red
            }
        }
    }
}

# 7. Clean up odd files (10, 240, 90, bool, python, nul, Tuple[bool, etc.)
Write-Host ""
Write-Host "7. Cleaning up odd files..." -ForegroundColor Cyan
$oddFiles = @("10", "240", "90", "bool", "python", "nul", "Tuple[bool")

foreach ($oddFile in $oddFiles) {
    $source = Join-Path $RepoRoot $oddFile
    if (Test-Path $source) {
        try {
            if ($WhatIf) {
                Write-Host "  [WOULD DELETE] $oddFile" -ForegroundColor Yellow
            } else {
                Remove-Item -Path $source -Force -ErrorAction Stop
                Write-Host "  ✓ Deleted odd file: $oddFile" -ForegroundColor Green
                $movedCount++
            }
        } catch {
            $errors += "Failed to delete $oddFile : $_"
            Write-Host "  ✗ Error deleting $oddFile : $_" -ForegroundColor Red
        }
    }
}

# 8. Move old release files to archive
Write-Host ""
Write-Host "8. Archiving old release files..." -ForegroundColor Cyan
$releaseFiles = @(
    "release_docs_v2025.11.09.zip",
    "release_log.txt"
)

foreach ($releaseFile in $releaseFiles) {
    $source = Join-Path $RepoRoot $releaseFile
    $dest = Join-Path $RepoRoot "03_archive\old_backups\$releaseFile"
    if (Move-FileSafely -Source $source -Destination $dest -Category "03_archive/old_backups/") {
        $movedCount++
    }
}

# 9. Move old config backups
Write-Host ""
Write-Host "9. Organizing config backups..." -ForegroundColor Cyan
$configBackups = Get-ChildItem -Path $RepoRoot -Filter "config.json.backup_*" -ErrorAction SilentlyContinue
foreach ($backup in $configBackups) {
    $dest = Join-Path $RepoRoot "06_config\backups\$($backup.Name)"
    if (Move-FileSafely -Source $backup.FullName -Destination $dest -Category "06_config/backups/") {
        $movedCount++
    }
}

# 10. Move reprocess config to 06_config
Write-Host ""
Write-Host "10. Organizing config files..." -ForegroundColor Cyan
$reprocessConfig = Join-Path $RepoRoot "reprocess_config.json"
if (Test-Path $reprocessConfig) {
    $dest = Join-Path $RepoRoot "06_config\reprocess_config.json"
    if (Move-FileSafely -Source $reprocessConfig -Destination $dest -Category "06_config/") {
        $movedCount++
    }
}

# Summary
Write-Host ""
Write-Host "=== Cleanup Summary ===" -ForegroundColor Cyan
Write-Host "Files processed: $movedCount" -ForegroundColor $(if ($movedCount -gt 0) { "Green" } else { "Gray" })
if ($errors.Count -gt 0) {
    Write-Host "Errors: $($errors.Count)" -ForegroundColor Red
    foreach ($error in $errors) {
        Write-Host "  - $error" -ForegroundColor Red
    }
} else {
    Write-Host "No errors encountered." -ForegroundColor Green
}

if ($WhatIf) {
    Write-Host ""
    Write-Host "This was a DRY RUN. Run without -WhatIf to perform actual moves." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Cleanup complete!" -ForegroundColor Cyan


```

```powershell
# Directory Cleanup Script
# Organizes files in the root directory into appropriate subdirectories

param(
    [string]$RepoRoot = "$PSScriptRoot\..",
    [switch]$WhatIf = $false,
    [switch]$ArchiveOld = $true
)

Set-Location $RepoRoot

Write-Host "=== Directory Cleanup Script ===" -ForegroundColor Cyan
Write-Host "Repository Root: $RepoRoot" -ForegroundColor Gray
if ($WhatIf) {
    Write-Host "DRY RUN MODE - No files will be moved" -ForegroundColor Yellow
}
Write-Host ""

$movedCount = 0
$errors = @()

# Ensure target directories exist
$targetDirs = @(
    "05_logs",
    "05_logs\legacy",
    "scripts",
    "99_doc",
    "99_doc\archive",
    "99_doc\archive\old_scripts",
    "03_archive\old_backups",
    "tests\archive"
)

foreach ($dir in $targetDirs) {
    $fullPath = Join-Path $RepoRoot $dir
    if (-not (Test-Path $fullPath)) {
        if (-not $WhatIf) {
            New-Item -ItemType Directory -Path $fullPath -Force | Out-Null
        }
        Write-Host "Created directory: $dir" -ForegroundColor Gray
    }
}

# Function to safely move files
function Move-FileSafely {
    param(
        [string]$Source,
        [string]$Destination,
        [string]$Category
    )
    
    if (-not (Test-Path $Source)) {
        return $false
    }
    
    $destDir = Split-Path $Destination -Parent
    if (-not (Test-Path $destDir)) {
        if (-not $WhatIf) {
            New-Item -ItemType Directory -Path $destDir -Force | Out-Null
        }
    }
    
    if (Test-Path $Destination) {
        # File exists - create unique name with timestamp
        $name = [System.IO.Path]::GetFileNameWithoutExtension($Source)
        $ext = [System.IO.Path]::GetExtension($Source)
        $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
        $Destination = Join-Path $destDir "${name}_${timestamp}${ext}"
    }
    
    try {
        if ($WhatIf) {
            Write-Host "  [WOULD MOVE] $Source -> $Destination" -ForegroundColor Yellow
        } else {
            Move-Item -Path $Source -Destination $Destination -Force
            Write-Host "  [OK] Moved: $([System.IO.Path]::GetFileName($Source)) -> $Category" -ForegroundColor Green
        }
        return $true
    } catch {
        $script:errors += "Failed to move $Source : $_"
            Write-Host "  [ERROR] Error moving $Source : $_" -ForegroundColor Red
        return $false
    }
}

# 1. Move log files from root to 05_logs
Write-Host "1. Moving log files to 05_logs..." -ForegroundColor Cyan
$logFiles = @(
    "watcher_error.log",
    "watcher_live.log",
    "watcher_live_error.log",
    "watcher_test.log",
    "test_output.log",
    "last_1500_lines.log",
    "tree_report_error.log"
)

foreach ($logFile in $logFiles) {
    $source = Join-Path $RepoRoot $logFile
    $dest = Join-Path $RepoRoot "05_logs\$logFile"
    if (Move-FileSafely -Source $source -Destination $dest -Category "05_logs") {
        $movedCount++
    }
}

# 2. Move PowerShell scripts from root to scripts/
Write-Host ""
Write-Host "2. Moving PowerShell scripts to scripts/..." -ForegroundColor Cyan
$psScripts = @(
    "copy_files_for_processing.ps1",
    "copy_files_back_to_source.ps1",
    "move_files_for_processing.ps1",
    "create_mapping_for_existing_files.ps1",
    "Chunker_MoveOptimized.ps1",
    "prepare_claude_files.ps1",
    "prepare_grok_review.ps1"
)

foreach ($script in $psScripts) {
    $source = Join-Path $RepoRoot $script
    $dest = Join-Path $RepoRoot "scripts\$script"
    if (Move-FileSafely -Source $source -Destination $dest -Category "scripts/") {
        $movedCount++
    }
}

# 3. Move documentation files to 99_doc/
Write-Host ""
Write-Host "3. Moving documentation files to 99_doc/..." -ForegroundColor Cyan
$docFiles = @(
    "2025_11_07_CHATGPT_tagging_fix.md",
    "2025_11_09_claude_code_prompt_chunker.txt",
    "2025_12_21__chunker_directory_tree.json",
    "2025_12_21__chunker_directory_tree.md",
    "CLAUDE_CODE_TASK_PROMPT.md",
    "CLAUDE_GUI_COLLABORATION_PROMPT.md",
    "CLAUDE_IMPLEMENTATION_GUIDE.md",
    "CURSOR_FIX_PROMPT.md",
    "DATABASE_IMPROVEMENTS.md",
    "DESKTOP_SYNC.md",
    "FAILED_FILES_CLARIFICATION.md",
    "FIX_DESKTOP_SYNC.md",
    "FIXES_APPLIED_SUMMARY.md",
    "FINAL_STATUS.md",
    "GIT_SETUP_STATUS.md",
    "GROK_COLLABORATION_PROMPT.md",
    "GROK_FEEDBACK_001.md",
    "GROK_HNSW_FIX_PROMPT.md",
    "GROK_REFERENCE_PACKAGE.md",
    "GROK_REVIEW_PACKAGE.md",
    "GROK_SIMPLIFICATION_RECOMMENDATIONS.md",
    "grok_review_prompt.md",
    "HANDOFF_PROMPT.md",
    "handoff_brief.md",
    "IMPLEMENTATION_STATUS.md",
    "IMPLEMENTATION_SUMMARY.md",
    "KB_INTEGRATION_GUIDE.md",
    "LOG_REVIEW_AND_FIXES.md",
    "MONITOR_DB_LOCKS.md",
    "MOVE_WORKFLOW_IMPLEMENTATION.md",
    "PROMPT_KB_INTEGRATION.md",
    "QUICK_START_PROMPT.md",
    "RECOVERY_SUCCESS.md",
    "REPROCESSING_RUN_PLAN.md",
    "SYNC_INSTRUCTIONS.md",
    "TASK_PROGRESS_REPORT.md",
    "UPDATE_SUMMARY_2025-11-08.md",
    "VERIFICATION_REPORT.md"
)

foreach ($doc in $docFiles) {
    $source = Join-Path $RepoRoot $doc
    $dest = Join-Path $RepoRoot "99_doc\$doc"
    if (Move-FileSafely -Source $source -Destination $dest -Category "99_doc/") {
        $movedCount++
    }
}

# 4. Move test files to tests/archive
Write-Host ""
Write-Host "4. Moving test files to tests/archive..." -ForegroundColor Cyan
$testFiles = @(
    "test_celery_integration.py",
    "test_origin_tracking.py",
    "test_processing_workflow.py",
    "test_python_demo.py",
    "test_search.py",
    "simple_rag_test.py",
    "rag_test.py",
    "test_queries.json"
)

foreach ($testFile in $testFiles) {
    $source = Join-Path $RepoRoot $testFile
    $dest = Join-Path $RepoRoot "tests\archive\$testFile"
    if (Move-FileSafely -Source $source -Destination $dest -Category "tests/archive/") {
        $movedCount++
    }
}

# 5. Move utility/analysis scripts to appropriate locations
Write-Host ""
Write-Host "5. Organizing utility scripts..." -ForegroundColor Cyan
$utilityMoves = @{
    "_analyze_remaining.py" = "tools"
    "_check_py_files.py" = "tools"
    "_check_remaining.py" = "tools"
    "analyze_empty_folders.py" = "tools"
    "analyze_failed_files.py" = "tools"
    "check_collection_dim.py" = "tools"
    "diagnose_issues.py" = "tools"
    "verify_backfill.py" = "tools"
    "verify_chunk_completeness.py" = "tools"
    "verify_enhancements.py" = "tools"
}

foreach ($file in $utilityMoves.Keys) {
    $source = Join-Path $RepoRoot $file
    $destDir = $utilityMoves[$file]
    $dest = Join-Path $RepoRoot "$destDir\$file"
    if (Move-FileSafely -Source $source -Destination $dest -Category "$destDir/") {
        $movedCount++
    }
}

# 6. Archive old backup directories
if ($ArchiveOld) {
    Write-Host ""
    Write-Host "6. Archiving old backup directories..." -ForegroundColor Cyan
    $backupDirs = @(
        "backup_20251107",
        "archive"
    )
    
    foreach ($backupDir in $backupDirs) {
        $source = Join-Path $RepoRoot $backupDir
        if (Test-Path $source) {
            $dest = Join-Path $RepoRoot "03_archive\old_backups\$backupDir"
            try {
                if ($WhatIf) {
                    Write-Host "  [WOULD MOVE] $backupDir -> 03_archive\old_backups\" -ForegroundColor Yellow
                } else {
                    Move-Item -Path $source -Destination $dest -Force
                    Write-Host "  ✓ Archived: $backupDir" -ForegroundColor Green
                    $movedCount++
                }
            } catch {
                $errors += "Failed to archive $backupDir : $_"
                Write-Host "  ✗ Error archiving $backupDir : $_" -ForegroundColor Red
            }
        }
    }
}

# 7. Clean up odd files (10, 240, 90, bool, python, nul, Tuple[bool, etc.)
Write-Host ""
Write-Host "7. Cleaning up odd files..." -ForegroundColor Cyan
$oddFiles = @("10", "240", "90", "bool", "python", "nul", "Tuple[bool")

foreach ($oddFile in $oddFiles) {
    $source = Join-Path $RepoRoot $oddFile
    if (Test-Path $source) {
        try {
            if ($WhatIf) {
                Write-Host "  [WOULD DELETE] $oddFile" -ForegroundColor Yellow
            } else {
                Remove-Item -Path $source -Force -ErrorAction Stop
                Write-Host "  ✓ Deleted odd file: $oddFile" -ForegroundColor Green
                $movedCount++
            }
        } catch {
            $errors += "Failed to delete $oddFile : $_"
            Write-Host "  ✗ Error deleting $oddFile : $_" -ForegroundColor Red
        }
    }
}

# 8. Move old release files to archive
Write-Host ""
Write-Host "8. Archiving old release files..." -ForegroundColor Cyan
$releaseFiles = @(
    "release_docs_v2025.11.09.zip",
    "release_log.txt"
)

foreach ($releaseFile in $releaseFiles) {
    $source = Join-Path $RepoRoot $releaseFile
    $dest = Join-Path $RepoRoot "03_archive\old_backups\$releaseFile"
    if (Move-FileSafely -Source $source -Destination $dest -Category "03_archive/old_backups/") {
        $movedCount++
    }
}

# 9. Move old config backups
Write-Host ""
Write-Host "9. Organizing config backups..." -ForegroundColor Cyan
$configBackups = Get-ChildItem -Path $RepoRoot -Filter "config.json.backup_*" -ErrorAction SilentlyContinue
foreach ($backup in $configBackups) {
    $dest = Join-Path $RepoRoot "06_config\backups\$($backup.Name)"
    if (Move-FileSafely -Source $backup.FullName -Destination $dest -Category "06_config/backups/") {
        $movedCount++
    }
}

# 10. Move reprocess config to 06_config
Write-Host ""
Write-Host "10. Organizing config files..." -ForegroundColor Cyan
$reprocessConfig = Join-Path $RepoRoot "reprocess_config.json"
if (Test-Path $reprocessConfig) {
    $dest = Join-Path $RepoRoot "06_config\reprocess_config.json"
    if (Move-FileSafely -Source $reprocessConfig -Destination $dest -Category "06_config/") {
        $movedCount++
    }
}

# Summary
Write-Host ""
Write-Host "=== Cleanup Summary ===" -ForegroundColor Cyan
Write-Host "Files processed: $movedCount" -ForegroundColor $(if ($movedCount -gt 0) { "Green" } else { "Gray" })
if ($errors.Count -gt 0) {
    Write-Host "Errors: $($errors.Count)" -ForegroundColor Red
    foreach ($error in $errors) {
        Write-Host "  - $error" -ForegroundColor Red
    }
} else {
    Write-Host "No errors encountered." -ForegroundColor Green
}

if ($WhatIf) {
    Write-Host ""
    Write-Host "This was a DRY RUN. Run without -WhatIf to perform actual moves." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Cleanup complete!" -ForegroundColor Cyan


```

```powershell
# Directory Cleanup Script
# Organizes files in the root directory into appropriate subdirectories

param(
    [string]$RepoRoot = "$PSScriptRoot\..",
    [switch]$WhatIf = $false,
    [switch]$ArchiveOld = $true
)

Set-Location $RepoRoot

Write-Host "=== Directory Cleanup Script ===" -ForegroundColor Cyan
Write-Host "Repository Root: $RepoRoot" -ForegroundColor Gray
if ($WhatIf) {
    Write-Host "DRY RUN MODE - No files will be moved" -ForegroundColor Yellow
}
Write-Host ""

$movedCount = 0
$errors = @()

# Ensure target directories exist
$targetDirs = @(
    "05_logs",
    "05_logs\legacy",
    "scripts",
    "99_doc",
    "99_doc\archive",
    "99_doc\archive\old_scripts",
    "03_archive\old_backups",
    "tests\archive"
)

foreach ($dir in $targetDirs) {
    $fullPath = Join-Path $RepoRoot $dir
    if (-not (Test-Path $fullPath)) {
        if (-not $WhatIf) {
            New-Item -ItemType Directory -Path $fullPath -Force | Out-Null
        }
        Write-Host "Created directory: $dir" -ForegroundColor Gray
    }
}

# Function to safely move files
function Move-FileSafely {
    param(
        [string]$Source,
        [string]$Destination,
        [string]$Category
    )
    
    if (-not (Test-Path $Source)) {
        return $false
    }
    
    $destDir = Split-Path $Destination -Parent
    if (-not (Test-Path $destDir)) {
        if (-not $WhatIf) {
            New-Item -ItemType Directory -Path $destDir -Force | Out-Null
        }
    }
    
    if (Test-Path $Destination) {
        # File exists - create unique name with timestamp
        $name = [System.IO.Path]::GetFileNameWithoutExtension($Source)
        $ext = [System.IO.Path]::GetExtension($Source)
        $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
        $Destination = Join-Path $destDir "${name}_${timestamp}${ext}"
    }
    
    try {
        if ($WhatIf) {
            Write-Host "  [WOULD MOVE] $Source -> $Destination" -ForegroundColor Yellow
        } else {
            Move-Item -Path $Source -Destination $Destination -Force
            Write-Host "  [OK] Moved: $([System.IO.Path]::GetFileName($Source)) -> $Category" -ForegroundColor Green
        }
        return $true
    } catch {
        $script:errors += "Failed to move $Source : $_"
            Write-Host "  [ERROR] Error moving $Source : $_" -ForegroundColor Red
        return $false
    }
}

# 1. Move log files from root to 05_logs
Write-Host "1. Moving log files to 05_logs..." -ForegroundColor Cyan
$logFiles = @(
    "watcher_error.log",
    "watcher_live.log",
    "watcher_live_error.log",
    "watcher_test.log",
    "test_output.log",
    "last_1500_lines.log",
    "tree_report_error.log"
)

foreach ($logFile in $logFiles) {
    $source = Join-Path $RepoRoot $logFile
    $dest = Join-Path $RepoRoot "05_logs\$logFile"
    if (Move-FileSafely -Source $source -Destination $dest -Category "05_logs") {
        $movedCount++
    }
}

# 2. Move PowerShell scripts from root to scripts/
Write-Host ""
Write-Host "2. Moving PowerShell scripts to scripts/..." -ForegroundColor Cyan
$psScripts = @(
    "copy_files_for_processing.ps1",
    "copy_files_back_to_source.ps1",
    "move_files_for_processing.ps1",
    "create_mapping_for_existing_files.ps1",
    "Chunker_MoveOptimized.ps1",
    "prepare_claude_files.ps1",
    "prepare_grok_review.ps1"
)

foreach ($script in $psScripts) {
    $source = Join-Path $RepoRoot $script
    $dest = Join-Path $RepoRoot "scripts\$script"
    if (Move-FileSafely -Source $source -Destination $dest -Category "scripts/") {
        $movedCount++
    }
}

# 3. Move documentation files to 99_doc/
Write-Host ""
Write-Host "3. Moving documentation files to 99_doc/..." -ForegroundColor Cyan
$docFiles = @(
    "2025_11_07_CHATGPT_tagging_fix.md",
    "2025_11_09_claude_code_prompt_chunker.txt",
    "2025_12_21__chunker_directory_tree.json",
    "2025_12_21__chunker_directory_tree.md",
    "CLAUDE_CODE_TASK_PROMPT.md",
    "CLAUDE_GUI_COLLABORATION_PROMPT.md",
    "CLAUDE_IMPLEMENTATION_GUIDE.md",
    "CURSOR_FIX_PROMPT.md",
    "DATABASE_IMPROVEMENTS.md",
    "DESKTOP_SYNC.md",
    "FAILED_FILES_CLARIFICATION.md",
    "FIX_DESKTOP_SYNC.md",
    "FIXES_APPLIED_SUMMARY.md",
    "FINAL_STATUS.md",
    "GIT_SETUP_STATUS.md",
    "GROK_COLLABORATION_PROMPT.md",
    "GROK_FEEDBACK_001.md",
    "GROK_HNSW_FIX_PROMPT.md",
    "GROK_REFERENCE_PACKAGE.md",
    "GROK_REVIEW_PACKAGE.md",
    "GROK_SIMPLIFICATION_RECOMMENDATIONS.md",
    "grok_review_prompt.md",
    "HANDOFF_PROMPT.md",
    "handoff_brief.md",
    "IMPLEMENTATION_STATUS.md",
    "IMPLEMENTATION_SUMMARY.md",
    "KB_INTEGRATION_GUIDE.md",
    "LOG_REVIEW_AND_FIXES.md",
    "MONITOR_DB_LOCKS.md",
    "MOVE_WORKFLOW_IMPLEMENTATION.md",
    "PROMPT_KB_INTEGRATION.md",
    "QUICK_START_PROMPT.md",
    "RECOVERY_SUCCESS.md",
    "REPROCESSING_RUN_PLAN.md",
    "SYNC_INSTRUCTIONS.md",
    "TASK_PROGRESS_REPORT.md",
    "UPDATE_SUMMARY_2025-11-08.md",
    "VERIFICATION_REPORT.md"
)

foreach ($doc in $docFiles) {
    $source = Join-Path $RepoRoot $doc
    $dest = Join-Path $RepoRoot "99_doc\$doc"
    if (Move-FileSafely -Source $source -Destination $dest -Category "99_doc/") {
        $movedCount++
    }
}

# 4. Move test files to tests/archive
Write-Host ""
Write-Host "4. Moving test files to tests/archive..." -ForegroundColor Cyan
$testFiles = @(
    "test_celery_integration.py",
    "test_origin_tracking.py",
    "test_processing_workflow.py",
    "test_python_demo.py",
    "test_search.py",
    "simple_rag_test.py",
    "rag_test.py",
    "test_queries.json"
)

foreach ($testFile in $testFiles) {
    $source = Join-Path $RepoRoot $testFile
    $dest = Join-Path $RepoRoot "tests\archive\$testFile"
    if (Move-FileSafely -Source $source -Destination $dest -Category "tests/archive/") {
        $movedCount++
    }
}

# 5. Move utility/analysis scripts to appropriate locations
Write-Host ""
Write-Host "5. Organizing utility scripts..." -ForegroundColor Cyan
$utilityMoves = @{
    "_analyze_remaining.py" = "tools"
    "_check_py_files.py" = "tools"
    "_check_remaining.py" = "tools"
    "analyze_empty_folders.py" = "tools"
    "analyze_failed_files.py" = "tools"
    "check_collection_dim.py" = "tools"
    "diagnose_issues.py" = "tools"
    "verify_backfill.py" = "tools"
    "verify_chunk_completeness.py" = "tools"
    "verify_enhancements.py" = "tools"
}

foreach ($file in $utilityMoves.Keys) {
    $source = Join-Path $RepoRoot $file
    $destDir = $utilityMoves[$file]
    $dest = Join-Path $RepoRoot "$destDir\$file"
    if (Move-FileSafely -Source $source -Destination $dest -Category "$destDir/") {
        $movedCount++
    }
}

# 6. Archive old backup directories
if ($ArchiveOld) {
    Write-Host ""
    Write-Host "6. Archiving old backup directories..." -ForegroundColor Cyan
    $backupDirs = @(
        "backup_20251107",
        "archive"
    )
    
    foreach ($backupDir in $backupDirs) {
        $source = Join-Path $RepoRoot $backupDir
        if (Test-Path $source) {
            $dest = Join-Path $RepoRoot "03_archive\old_backups\$backupDir"
            try {
                if ($WhatIf) {
                    Write-Host "  [WOULD MOVE] $backupDir -> 03_archive\old_backups\" -ForegroundColor Yellow
                } else {
                    Move-Item -Path $source -Destination $dest -Force
                    Write-Host "  [OK] Archived: $backupDir" -ForegroundColor Green
                    $movedCount++
                }
            } catch {
                $errors += "Failed to archive $backupDir : $_"
                Write-Host "  ✗ Error archiving $backupDir : $_" -ForegroundColor Red
            }
        }
    }
}

# 7. Clean up odd files (10, 240, 90, bool, python, nul, Tuple[bool, etc.)
Write-Host ""
Write-Host "7. Cleaning up odd files..." -ForegroundColor Cyan
$oddFiles = @("10", "240", "90", "bool", "python", "nul", "Tuple[bool")

foreach ($oddFile in $oddFiles) {
    $source = Join-Path $RepoRoot $oddFile
    if (Test-Path $source) {
        try {
            if ($WhatIf) {
                Write-Host "  [WOULD DELETE] $oddFile" -ForegroundColor Yellow
            } else {
                Remove-Item -Path $source -Force -ErrorAction Stop
                Write-Host "  ✓ Deleted odd file: $oddFile" -ForegroundColor Green
                $movedCount++
            }
        } catch {
            $errors += "Failed to delete $oddFile : $_"
            Write-Host "  ✗ Error deleting $oddFile : $_" -ForegroundColor Red
        }
    }
}

# 8. Move old release files to archive
Write-Host ""
Write-Host "8. Archiving old release files..." -ForegroundColor Cyan
$releaseFiles = @(
    "release_docs_v2025.11.09.zip",
    "release_log.txt"
)

foreach ($releaseFile in $releaseFiles) {
    $source = Join-Path $RepoRoot $releaseFile
    $dest = Join-Path $RepoRoot "03_archive\old_backups\$releaseFile"
    if (Move-FileSafely -Source $source -Destination $dest -Category "03_archive/old_backups/") {
        $movedCount++
    }
}

# 9. Move old config backups
Write-Host ""
Write-Host "9. Organizing config backups..." -ForegroundColor Cyan
$configBackups = Get-ChildItem -Path $RepoRoot -Filter "config.json.backup_*" -ErrorAction SilentlyContinue
foreach ($backup in $configBackups) {
    $dest = Join-Path $RepoRoot "06_config\backups\$($backup.Name)"
    if (Move-FileSafely -Source $backup.FullName -Destination $dest -Category "06_config/backups/") {
        $movedCount++
    }
}

# 10. Move reprocess config to 06_config
Write-Host ""
Write-Host "10. Organizing config files..." -ForegroundColor Cyan
$reprocessConfig = Join-Path $RepoRoot "reprocess_config.json"
if (Test-Path $reprocessConfig) {
    $dest = Join-Path $RepoRoot "06_config\reprocess_config.json"
    if (Move-FileSafely -Source $reprocessConfig -Destination $dest -Category "06_config/") {
        $movedCount++
    }
}

# Summary
Write-Host ""
Write-Host "=== Cleanup Summary ===" -ForegroundColor Cyan
Write-Host "Files processed: $movedCount" -ForegroundColor $(if ($movedCount -gt 0) { "Green" } else { "Gray" })
if ($errors.Count -gt 0) {
    Write-Host "Errors: $($errors.Count)" -ForegroundColor Red
    foreach ($error in $errors) {
        Write-Host "  - $error" -ForegroundColor Red
    }
} else {
    Write-Host "No errors encountered." -ForegroundColor Green
}

if ($WhatIf) {
    Write-Host ""
    Write-Host "This was a DRY RUN. Run without -WhatIf to perform actual moves." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Cleanup complete!" -ForegroundColor Cyan


```

```powershell
# Directory Cleanup Script
# Organizes files in the root directory into appropriate subdirectories

param(
    [string]$RepoRoot = "$PSScriptRoot\..",
    [switch]$WhatIf = $false,
    [switch]$ArchiveOld = $true
)

Set-Location $RepoRoot

Write-Host "=== Directory Cleanup Script ===" -ForegroundColor Cyan
Write-Host "Repository Root: $RepoRoot" -ForegroundColor Gray
if ($WhatIf) {
    Write-Host "DRY RUN MODE - No files will be moved" -ForegroundColor Yellow
}
Write-Host ""

$movedCount = 0
$errors = @()

# Ensure target directories exist
$targetDirs = @(
    "05_logs",
    "05_logs\legacy",
    "scripts",
    "99_doc",
    "99_doc\archive",
    "99_doc\archive\old_scripts",
    "03_archive\old_backups",
    "tests\archive"
)

foreach ($dir in $targetDirs) {
    $fullPath = Join-Path $RepoRoot $dir
    if (-not (Test-Path $fullPath)) {
        if (-not $WhatIf) {
            New-Item -ItemType Directory -Path $fullPath -Force | Out-Null
        }
        Write-Host "Created directory: $dir" -ForegroundColor Gray
    }
}

# Function to safely move files
function Move-FileSafely {
    param(
        [string]$Source,
        [string]$Destination,
        [string]$Category
    )
    
    if (-not (Test-Path $Source)) {
        return $false
    }
    
    $destDir = Split-Path $Destination -Parent
    if (-not (Test-Path $destDir)) {
        if (-not $WhatIf) {
            New-Item -ItemType Directory -Path $destDir -Force | Out-Null
        }
    }
    
    if (Test-Path $Destination) {
        # File exists - create unique name with timestamp
        $name = [System.IO.Path]::GetFileNameWithoutExtension($Source)
        $ext = [System.IO.Path]::GetExtension($Source)
        $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
        $Destination = Join-Path $destDir "${name}_${timestamp}${ext}"
    }
    
    try {
        if ($WhatIf) {
            Write-Host "  [WOULD MOVE] $Source -> $Destination" -ForegroundColor Yellow
        } else {
            Move-Item -Path $Source -Destination $Destination -Force
            Write-Host "  [OK] Moved: $([System.IO.Path]::GetFileName($Source)) -> $Category" -ForegroundColor Green
        }
        return $true
    } catch {
        $script:errors += "Failed to move $Source : $_"
            Write-Host "  [ERROR] Error moving $Source : $_" -ForegroundColor Red
        return $false
    }
}

# 1. Move log files from root to 05_logs
Write-Host "1. Moving log files to 05_logs..." -ForegroundColor Cyan
$logFiles = @(
    "watcher_error.log",
    "watcher_live.log",
    "watcher_live_error.log",
    "watcher_test.log",
    "test_output.log",
    "last_1500_lines.log",
    "tree_report_error.log"
)

foreach ($logFile in $logFiles) {
    $source = Join-Path $RepoRoot $logFile
    $dest = Join-Path $RepoRoot "05_logs\$logFile"
    if (Move-FileSafely -Source $source -Destination $dest -Category "05_logs") {
        $movedCount++
    }
}

# 2. Move PowerShell scripts from root to scripts/
Write-Host ""
Write-Host "2. Moving PowerShell scripts to scripts/..." -ForegroundColor Cyan
$psScripts = @(
    "copy_files_for_processing.ps1",
    "copy_files_back_to_source.ps1",
    "move_files_for_processing.ps1",
    "create_mapping_for_existing_files.ps1",
    "Chunker_MoveOptimized.ps1",
    "prepare_claude_files.ps1",
    "prepare_grok_review.ps1"
)

foreach ($script in $psScripts) {
    $source = Join-Path $RepoRoot $script
    $dest = Join-Path $RepoRoot "scripts\$script"
    if (Move-FileSafely -Source $source -Destination $dest -Category "scripts/") {
        $movedCount++
    }
}

# 3. Move documentation files to 99_doc/
Write-Host ""
Write-Host "3. Moving documentation files to 99_doc/..." -ForegroundColor Cyan
$docFiles = @(
    "2025_11_07_CHATGPT_tagging_fix.md",
    "2025_11_09_claude_code_prompt_chunker.txt",
    "2025_12_21__chunker_directory_tree.json",
    "2025_12_21__chunker_directory_tree.md",
    "CLAUDE_CODE_TASK_PROMPT.md",
    "CLAUDE_GUI_COLLABORATION_PROMPT.md",
    "CLAUDE_IMPLEMENTATION_GUIDE.md",
    "CURSOR_FIX_PROMPT.md",
    "DATABASE_IMPROVEMENTS.md",
    "DESKTOP_SYNC.md",
    "FAILED_FILES_CLARIFICATION.md",
    "FIX_DESKTOP_SYNC.md",
    "FIXES_APPLIED_SUMMARY.md",
    "FINAL_STATUS.md",
    "GIT_SETUP_STATUS.md",
    "GROK_COLLABORATION_PROMPT.md",
    "GROK_FEEDBACK_001.md",
    "GROK_HNSW_FIX_PROMPT.md",
    "GROK_REFERENCE_PACKAGE.md",
    "GROK_REVIEW_PACKAGE.md",
    "GROK_SIMPLIFICATION_RECOMMENDATIONS.md",
    "grok_review_prompt.md",
    "HANDOFF_PROMPT.md",
    "handoff_brief.md",
    "IMPLEMENTATION_STATUS.md",
    "IMPLEMENTATION_SUMMARY.md",
    "KB_INTEGRATION_GUIDE.md",
    "LOG_REVIEW_AND_FIXES.md",
    "MONITOR_DB_LOCKS.md",
    "MOVE_WORKFLOW_IMPLEMENTATION.md",
    "PROMPT_KB_INTEGRATION.md",
    "QUICK_START_PROMPT.md",
    "RECOVERY_SUCCESS.md",
    "REPROCESSING_RUN_PLAN.md",
    "SYNC_INSTRUCTIONS.md",
    "TASK_PROGRESS_REPORT.md",
    "UPDATE_SUMMARY_2025-11-08.md",
    "VERIFICATION_REPORT.md"
)

foreach ($doc in $docFiles) {
    $source = Join-Path $RepoRoot $doc
    $dest = Join-Path $RepoRoot "99_doc\$doc"
    if (Move-FileSafely -Source $source -Destination $dest -Category "99_doc/") {
        $movedCount++
    }
}

# 4. Move test files to tests/archive
Write-Host ""
Write-Host "4. Moving test files to tests/archive..." -ForegroundColor Cyan
$testFiles = @(
    "test_celery_integration.py",
    "test_origin_tracking.py",
    "test_processing_workflow.py",
    "test_python_demo.py",
    "test_search.py",
    "simple_rag_test.py",
    "rag_test.py",
    "test_queries.json"
)

foreach ($testFile in $testFiles) {
    $source = Join-Path $RepoRoot $testFile
    $dest = Join-Path $RepoRoot "tests\archive\$testFile"
    if (Move-FileSafely -Source $source -Destination $dest -Category "tests/archive/") {
        $movedCount++
    }
}

# 5. Move utility/analysis scripts to appropriate locations
Write-Host ""
Write-Host "5. Organizing utility scripts..." -ForegroundColor Cyan
$utilityMoves = @{
    "_analyze_remaining.py" = "tools"
    "_check_py_files.py" = "tools"
    "_check_remaining.py" = "tools"
    "analyze_empty_folders.py" = "tools"
    "analyze_failed_files.py" = "tools"
    "check_collection_dim.py" = "tools"
    "diagnose_issues.py" = "tools"
    "verify_backfill.py" = "tools"
    "verify_chunk_completeness.py" = "tools"
    "verify_enhancements.py" = "tools"
}

foreach ($file in $utilityMoves.Keys) {
    $source = Join-Path $RepoRoot $file
    $destDir = $utilityMoves[$file]
    $dest = Join-Path $RepoRoot "$destDir\$file"
    if (Move-FileSafely -Source $source -Destination $dest -Category "$destDir/") {
        $movedCount++
    }
}

# 6. Archive old backup directories
if ($ArchiveOld) {
    Write-Host ""
    Write-Host "6. Archiving old backup directories..." -ForegroundColor Cyan
    $backupDirs = @(
        "backup_20251107",
        "archive"
    )
    
    foreach ($backupDir in $backupDirs) {
        $source = Join-Path $RepoRoot $backupDir
        if (Test-Path $source) {
            $dest = Join-Path $RepoRoot "03_archive\old_backups\$backupDir"
            try {
                if ($WhatIf) {
                    Write-Host "  [WOULD MOVE] $backupDir -> 03_archive\old_backups\" -ForegroundColor Yellow
                } else {
                    Move-Item -Path $source -Destination $dest -Force
                    Write-Host "  [OK] Archived: $backupDir" -ForegroundColor Green
                    $movedCount++
                }
            } catch {
                $errors += "Failed to archive $backupDir : $_"
                Write-Host "  [ERROR] Error archiving $backupDir : $_" -ForegroundColor Red
            }
        }
    }
}

# 7. Clean up odd files (10, 240, 90, bool, python, nul, Tuple[bool, etc.)
Write-Host ""
Write-Host "7. Cleaning up odd files..." -ForegroundColor Cyan
$oddFiles = @("10", "240", "90", "bool", "python", "nul", "Tuple[bool")

foreach ($oddFile in $oddFiles) {
    $source = Join-Path $RepoRoot $oddFile
    if (Test-Path $source) {
        try {
            if ($WhatIf) {
                Write-Host "  [WOULD DELETE] $oddFile" -ForegroundColor Yellow
            } else {
                Remove-Item -Path $source -Force -ErrorAction Stop
                Write-Host "  ✓ Deleted odd file: $oddFile" -ForegroundColor Green
                $movedCount++
            }
        } catch {
            $errors += "Failed to delete $oddFile : $_"
            Write-Host "  ✗ Error deleting $oddFile : $_" -ForegroundColor Red
        }
    }
}

# 8. Move old release files to archive
Write-Host ""
Write-Host "8. Archiving old release files..." -ForegroundColor Cyan
$releaseFiles = @(
    "release_docs_v2025.11.09.zip",
    "release_log.txt"
)

foreach ($releaseFile in $releaseFiles) {
    $source = Join-Path $RepoRoot $releaseFile
    $dest = Join-Path $RepoRoot "03_archive\old_backups\$releaseFile"
    if (Move-FileSafely -Source $source -Destination $dest -Category "03_archive/old_backups/") {
        $movedCount++
    }
}

# 9. Move old config backups
Write-Host ""
Write-Host "9. Organizing config backups..." -ForegroundColor Cyan
$configBackups = Get-ChildItem -Path $RepoRoot -Filter "config.json.backup_*" -ErrorAction SilentlyContinue
foreach ($backup in $configBackups) {
    $dest = Join-Path $RepoRoot "06_config\backups\$($backup.Name)"
    if (Move-FileSafely -Source $backup.FullName -Destination $dest -Category "06_config/backups/") {
        $movedCount++
    }
}

# 10. Move reprocess config to 06_config
Write-Host ""
Write-Host "10. Organizing config files..." -ForegroundColor Cyan
$reprocessConfig = Join-Path $RepoRoot "reprocess_config.json"
if (Test-Path $reprocessConfig) {
    $dest = Join-Path $RepoRoot "06_config\reprocess_config.json"
    if (Move-FileSafely -Source $reprocessConfig -Destination $dest -Category "06_config/") {
        $movedCount++
    }
}

# Summary
Write-Host ""
Write-Host "=== Cleanup Summary ===" -ForegroundColor Cyan
Write-Host "Files processed: $movedCount" -ForegroundColor $(if ($movedCount -gt 0) { "Green" } else { "Gray" })
if ($errors.Count -gt 0) {
    Write-Host "Errors: $($errors.Count)" -ForegroundColor Red
    foreach ($error in $errors) {
        Write-Host "  - $error" -ForegroundColor Red
    }
} else {
    Write-Host "No errors encountered." -ForegroundColor Green
}

if ($WhatIf) {
    Write-Host ""
    Write-Host "This was a DRY RUN. Run without -WhatIf to perform actual moves." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Cleanup complete!" -ForegroundColor Cyan


```

```powershell
# Directory Cleanup Script
# Organizes files in the root directory into appropriate subdirectories

param(
    [string]$RepoRoot = "$PSScriptRoot\..",
    [switch]$WhatIf = $false,
    [switch]$ArchiveOld = $true
)

Set-Location $RepoRoot

Write-Host "=== Directory Cleanup Script ===" -ForegroundColor Cyan
Write-Host "Repository Root: $RepoRoot" -ForegroundColor Gray
if ($WhatIf) {
    Write-Host "DRY RUN MODE - No files will be moved" -ForegroundColor Yellow
}
Write-Host ""

$movedCount = 0
$errors = @()

# Ensure target directories exist
$targetDirs = @(
    "05_logs",
    "05_logs\legacy",
    "scripts",
    "99_doc",
    "99_doc\archive",
    "99_doc\archive\old_scripts",
    "03_archive\old_backups",
    "tests\archive"
)

foreach ($dir in $targetDirs) {
    $fullPath = Join-Path $RepoRoot $dir
    if (-not (Test-Path $fullPath)) {
        if (-not $WhatIf) {
            New-Item -ItemType Directory -Path $fullPath -Force | Out-Null
        }
        Write-Host "Created directory: $dir" -ForegroundColor Gray
    }
}

# Function to safely move files
function Move-FileSafely {
    param(
        [string]$Source,
        [string]$Destination,
        [string]$Category
    )
    
    if (-not (Test-Path $Source)) {
        return $false
    }
    
    $destDir = Split-Path $Destination -Parent
    if (-not (Test-Path $destDir)) {
        if (-not $WhatIf) {
            New-Item -ItemType Directory -Path $destDir -Force | Out-Null
        }
    }
    
    if (Test-Path $Destination) {
        # File exists - create unique name with timestamp
        $name = [System.IO.Path]::GetFileNameWithoutExtension($Source)
        $ext = [System.IO.Path]::GetExtension($Source)
        $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
        $Destination = Join-Path $destDir "${name}_${timestamp}${ext}"
    }
    
    try {
        if ($WhatIf) {
            Write-Host "  [WOULD MOVE] $Source -> $Destination" -ForegroundColor Yellow
        } else {
            Move-Item -Path $Source -Destination $Destination -Force
            Write-Host "  [OK] Moved: $([System.IO.Path]::GetFileName($Source)) -> $Category" -ForegroundColor Green
        }
        return $true
    } catch {
        $script:errors += "Failed to move $Source : $_"
            Write-Host "  [ERROR] Error moving $Source : $_" -ForegroundColor Red
        return $false
    }
}

# 1. Move log files from root to 05_logs
Write-Host "1. Moving log files to 05_logs..." -ForegroundColor Cyan
$logFiles = @(
    "watcher_error.log",
    "watcher_live.log",
    "watcher_live_error.log",
    "watcher_test.log",
    "test_output.log",
    "last_1500_lines.log",
    "tree_report_error.log"
)

foreach ($logFile in $logFiles) {
    $source = Join-Path $RepoRoot $logFile
    $dest = Join-Path $RepoRoot "05_logs\$logFile"
    if (Move-FileSafely -Source $source -Destination $dest -Category "05_logs") {
        $movedCount++
    }
}

# 2. Move PowerShell scripts from root to scripts/
Write-Host ""
Write-Host "2. Moving PowerShell scripts to scripts/..." -ForegroundColor Cyan
$psScripts = @(
    "copy_files_for_processing.ps1",
    "copy_files_back_to_source.ps1",
    "move_files_for_processing.ps1",
    "create_mapping_for_existing_files.ps1",
    "Chunker_MoveOptimized.ps1",
    "prepare_claude_files.ps1",
    "prepare_grok_review.ps1"
)

foreach ($script in $psScripts) {
    $source = Join-Path $RepoRoot $script
    $dest = Join-Path $RepoRoot "scripts\$script"
    if (Move-FileSafely -Source $source -Destination $dest -Category "scripts/") {
        $movedCount++
    }
}

# 3. Move documentation files to 99_doc/
Write-Host ""
Write-Host "3. Moving documentation files to 99_doc/..." -ForegroundColor Cyan
$docFiles = @(
    "2025_11_07_CHATGPT_tagging_fix.md",
    "2025_11_09_claude_code_prompt_chunker.txt",
    "2025_12_21__chunker_directory_tree.json",
    "2025_12_21__chunker_directory_tree.md",
    "CLAUDE_CODE_TASK_PROMPT.md",
    "CLAUDE_GUI_COLLABORATION_PROMPT.md",
    "CLAUDE_IMPLEMENTATION_GUIDE.md",
    "CURSOR_FIX_PROMPT.md",
    "DATABASE_IMPROVEMENTS.md",
    "DESKTOP_SYNC.md",
    "FAILED_FILES_CLARIFICATION.md",
    "FIX_DESKTOP_SYNC.md",
    "FIXES_APPLIED_SUMMARY.md",
    "FINAL_STATUS.md",
    "GIT_SETUP_STATUS.md",
    "GROK_COLLABORATION_PROMPT.md",
    "GROK_FEEDBACK_001.md",
    "GROK_HNSW_FIX_PROMPT.md",
    "GROK_REFERENCE_PACKAGE.md",
    "GROK_REVIEW_PACKAGE.md",
    "GROK_SIMPLIFICATION_RECOMMENDATIONS.md",
    "grok_review_prompt.md",
    "HANDOFF_PROMPT.md",
    "handoff_brief.md",
    "IMPLEMENTATION_STATUS.md",
    "IMPLEMENTATION_SUMMARY.md",
    "KB_INTEGRATION_GUIDE.md",
    "LOG_REVIEW_AND_FIXES.md",
    "MONITOR_DB_LOCKS.md",
    "MOVE_WORKFLOW_IMPLEMENTATION.md",
    "PROMPT_KB_INTEGRATION.md",
    "QUICK_START_PROMPT.md",
    "RECOVERY_SUCCESS.md",
    "REPROCESSING_RUN_PLAN.md",
    "SYNC_INSTRUCTIONS.md",
    "TASK_PROGRESS_REPORT.md",
    "UPDATE_SUMMARY_2025-11-08.md",
    "VERIFICATION_REPORT.md"
)

foreach ($doc in $docFiles) {
    $source = Join-Path $RepoRoot $doc
    $dest = Join-Path $RepoRoot "99_doc\$doc"
    if (Move-FileSafely -Source $source -Destination $dest -Category "99_doc/") {
        $movedCount++
    }
}

# 4. Move test files to tests/archive
Write-Host ""
Write-Host "4. Moving test files to tests/archive..." -ForegroundColor Cyan
$testFiles = @(
    "test_celery_integration.py",
    "test_origin_tracking.py",
    "test_processing_workflow.py",
    "test_python_demo.py",
    "test_search.py",
    "simple_rag_test.py",
    "rag_test.py",
    "test_queries.json"
)

foreach ($testFile in $testFiles) {
    $source = Join-Path $RepoRoot $testFile
    $dest = Join-Path $RepoRoot "tests\archive\$testFile"
    if (Move-FileSafely -Source $source -Destination $dest -Category "tests/archive/") {
        $movedCount++
    }
}

# 5. Move utility/analysis scripts to appropriate locations
Write-Host ""
Write-Host "5. Organizing utility scripts..." -ForegroundColor Cyan
$utilityMoves = @{
    "_analyze_remaining.py" = "tools"
    "_check_py_files.py" = "tools"
    "_check_remaining.py" = "tools"
    "analyze_empty_folders.py" = "tools"
    "analyze_failed_files.py" = "tools"
    "check_collection_dim.py" = "tools"
    "diagnose_issues.py" = "tools"
    "verify_backfill.py" = "tools"
    "verify_chunk_completeness.py" = "tools"
    "verify_enhancements.py" = "tools"
}

foreach ($file in $utilityMoves.Keys) {
    $source = Join-Path $RepoRoot $file
    $destDir = $utilityMoves[$file]
    $dest = Join-Path $RepoRoot "$destDir\$file"
    if (Move-FileSafely -Source $source -Destination $dest -Category "$destDir/") {
        $movedCount++
    }
}

# 6. Archive old backup directories
if ($ArchiveOld) {
    Write-Host ""
    Write-Host "6. Archiving old backup directories..." -ForegroundColor Cyan
    $backupDirs = @(
        "backup_20251107",
        "archive"
    )
    
    foreach ($backupDir in $backupDirs) {
        $source = Join-Path $RepoRoot $backupDir
        if (Test-Path $source) {
            $dest = Join-Path $RepoRoot "03_archive\old_backups\$backupDir"
            try {
                if ($WhatIf) {
                    Write-Host "  [WOULD MOVE] $backupDir -> 03_archive\old_backups\" -ForegroundColor Yellow
                } else {
                    Move-Item -Path $source -Destination $dest -Force
                    Write-Host "  [OK] Archived: $backupDir" -ForegroundColor Green
                    $movedCount++
                }
            } catch {
                $errors += "Failed to archive $backupDir : $_"
                Write-Host "  [ERROR] Error archiving $backupDir : $_" -ForegroundColor Red
            }
        }
    }
}

# 7. Clean up odd files (10, 240, 90, bool, python, nul, Tuple[bool, etc.)
Write-Host ""
Write-Host "7. Cleaning up odd files..." -ForegroundColor Cyan
$oddFiles = @("10", "240", "90", "bool", "python", "nul", "Tuple[bool")

foreach ($oddFile in $oddFiles) {
    $source = Join-Path $RepoRoot $oddFile
    if (Test-Path $source) {
        try {
            if ($WhatIf) {
                Write-Host "  [WOULD DELETE] $oddFile" -ForegroundColor Yellow
            } else {
                Remove-Item -Path $source -Force -ErrorAction Stop
                Write-Host "  [OK] Deleted odd file: $oddFile" -ForegroundColor Green
                $movedCount++
            }
        } catch {
            $errors += "Failed to delete $oddFile : $_"
            Write-Host "  ✗ Error deleting $oddFile : $_" -ForegroundColor Red
        }
    }
}

# 8. Move old release files to archive
Write-Host ""
Write-Host "8. Archiving old release files..." -ForegroundColor Cyan
$releaseFiles = @(
    "release_docs_v2025.11.09.zip",
    "release_log.txt"
)

foreach ($releaseFile in $releaseFiles) {
    $source = Join-Path $RepoRoot $releaseFile
    $dest = Join-Path $RepoRoot "03_archive\old_backups\$releaseFile"
    if (Move-FileSafely -Source $source -Destination $dest -Category "03_archive/old_backups/") {
        $movedCount++
    }
}

# 9. Move old config backups
Write-Host ""
Write-Host "9. Organizing config backups..." -ForegroundColor Cyan
$configBackups = Get-ChildItem -Path $RepoRoot -Filter "config.json.backup_*" -ErrorAction SilentlyContinue
foreach ($backup in $configBackups) {
    $dest = Join-Path $RepoRoot "06_config\backups\$($backup.Name)"
    if (Move-FileSafely -Source $backup.FullName -Destination $dest -Category "06_config/backups/") {
        $movedCount++
    }
}

# 10. Move reprocess config to 06_config
Write-Host ""
Write-Host "10. Organizing config files..." -ForegroundColor Cyan
$reprocessConfig = Join-Path $RepoRoot "reprocess_config.json"
if (Test-Path $reprocessConfig) {
    $dest = Join-Path $RepoRoot "06_config\reprocess_config.json"
    if (Move-FileSafely -Source $reprocessConfig -Destination $dest -Category "06_config/") {
        $movedCount++
    }
}

# Summary
Write-Host ""
Write-Host "=== Cleanup Summary ===" -ForegroundColor Cyan
Write-Host "Files processed: $movedCount" -ForegroundColor $(if ($movedCount -gt 0) { "Green" } else { "Gray" })
if ($errors.Count -gt 0) {
    Write-Host "Errors: $($errors.Count)" -ForegroundColor Red
    foreach ($error in $errors) {
        Write-Host "  - $error" -ForegroundColor Red
    }
} else {
    Write-Host "No errors encountered." -ForegroundColor Green
}

if ($WhatIf) {
    Write-Host ""
    Write-Host "This was a DRY RUN. Run without -WhatIf to perform actual moves." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Cleanup complete!" -ForegroundColor Cyan


```

```powershell
# Directory Cleanup Script
# Organizes files in the root directory into appropriate subdirectories

param(
    [string]$RepoRoot = "$PSScriptRoot\..",
    [switch]$WhatIf = $false,
    [switch]$ArchiveOld = $true
)

Set-Location $RepoRoot

Write-Host "=== Directory Cleanup Script ===" -ForegroundColor Cyan
Write-Host "Repository Root: $RepoRoot" -ForegroundColor Gray
if ($WhatIf) {
    Write-Host "DRY RUN MODE - No files will be moved" -ForegroundColor Yellow
}
Write-Host ""

$movedCount = 0
$errors = @()

# Ensure target directories exist
$targetDirs = @(
    "05_logs",
    "05_logs\legacy",
    "scripts",
    "99_doc",
    "99_doc\archive",
    "99_doc\archive\old_scripts",
    "03_archive\old_backups",
    "tests\archive"
)

foreach ($dir in $targetDirs) {
    $fullPath = Join-Path $RepoRoot $dir
    if (-not (Test-Path $fullPath)) {
        if (-not $WhatIf) {
            New-Item -ItemType Directory -Path $fullPath -Force | Out-Null
        }
        Write-Host "Created directory: $dir" -ForegroundColor Gray
    }
}

# Function to safely move files
function Move-FileSafely {
    param(
        [string]$Source,
        [string]$Destination,
        [string]$Category
    )
    
    if (-not (Test-Path $Source)) {
        return $false
    }
    
    $destDir = Split-Path $Destination -Parent
    if (-not (Test-Path $destDir)) {
        if (-not $WhatIf) {
            New-Item -ItemType Directory -Path $destDir -Force | Out-Null
        }
    }
    
    if (Test-Path $Destination) {
        # File exists - create unique name with timestamp
        $name = [System.IO.Path]::GetFileNameWithoutExtension($Source)
        $ext = [System.IO.Path]::GetExtension($Source)
        $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
        $Destination = Join-Path $destDir "${name}_${timestamp}${ext}"
    }
    
    try {
        if ($WhatIf) {
            Write-Host "  [WOULD MOVE] $Source -> $Destination" -ForegroundColor Yellow
        } else {
            Move-Item -Path $Source -Destination $Destination -Force
            Write-Host "  [OK] Moved: $([System.IO.Path]::GetFileName($Source)) -> $Category" -ForegroundColor Green
        }
        return $true
    } catch {
        $script:errors += "Failed to move $Source : $_"
            Write-Host "  [ERROR] Error moving $Source : $_" -ForegroundColor Red
        return $false
    }
}

# 1. Move log files from root to 05_logs
Write-Host "1. Moving log files to 05_logs..." -ForegroundColor Cyan
$logFiles = @(
    "watcher_error.log",
    "watcher_live.log",
    "watcher_live_error.log",
    "watcher_test.log",
    "test_output.log",
    "last_1500_lines.log",
    "tree_report_error.log"
)

foreach ($logFile in $logFiles) {
    $source = Join-Path $RepoRoot $logFile
    $dest = Join-Path $RepoRoot "05_logs\$logFile"
    if (Move-FileSafely -Source $source -Destination $dest -Category "05_logs") {
        $movedCount++
    }
}

# 2. Move PowerShell scripts from root to scripts/
Write-Host ""
Write-Host "2. Moving PowerShell scripts to scripts/..." -ForegroundColor Cyan
$psScripts = @(
    "copy_files_for_processing.ps1",
    "copy_files_back_to_source.ps1",
    "move_files_for_processing.ps1",
    "create_mapping_for_existing_files.ps1",
    "Chunker_MoveOptimized.ps1",
    "prepare_claude_files.ps1",
    "prepare_grok_review.ps1"
)

foreach ($script in $psScripts) {
    $source = Join-Path $RepoRoot $script
    $dest = Join-Path $RepoRoot "scripts\$script"
    if (Move-FileSafely -Source $source -Destination $dest -Category "scripts/") {
        $movedCount++
    }
}

# 3. Move documentation files to 99_doc/
Write-Host ""
Write-Host "3. Moving documentation files to 99_doc/..." -ForegroundColor Cyan
$docFiles = @(
    "2025_11_07_CHATGPT_tagging_fix.md",
    "2025_11_09_claude_code_prompt_chunker.txt",
    "2025_12_21__chunker_directory_tree.json",
    "2025_12_21__chunker_directory_tree.md",
    "CLAUDE_CODE_TASK_PROMPT.md",
    "CLAUDE_GUI_COLLABORATION_PROMPT.md",
    "CLAUDE_IMPLEMENTATION_GUIDE.md",
    "CURSOR_FIX_PROMPT.md",
    "DATABASE_IMPROVEMENTS.md",
    "DESKTOP_SYNC.md",
    "FAILED_FILES_CLARIFICATION.md",
    "FIX_DESKTOP_SYNC.md",
    "FIXES_APPLIED_SUMMARY.md",
    "FINAL_STATUS.md",
    "GIT_SETUP_STATUS.md",
    "GROK_COLLABORATION_PROMPT.md",
    "GROK_FEEDBACK_001.md",
    "GROK_HNSW_FIX_PROMPT.md",
    "GROK_REFERENCE_PACKAGE.md",
    "GROK_REVIEW_PACKAGE.md",
    "GROK_SIMPLIFICATION_RECOMMENDATIONS.md",
    "grok_review_prompt.md",
    "HANDOFF_PROMPT.md",
    "handoff_brief.md",
    "IMPLEMENTATION_STATUS.md",
    "IMPLEMENTATION_SUMMARY.md",
    "KB_INTEGRATION_GUIDE.md",
    "LOG_REVIEW_AND_FIXES.md",
    "MONITOR_DB_LOCKS.md",
    "MOVE_WORKFLOW_IMPLEMENTATION.md",
    "PROMPT_KB_INTEGRATION.md",
    "QUICK_START_PROMPT.md",
    "RECOVERY_SUCCESS.md",
    "REPROCESSING_RUN_PLAN.md",
    "SYNC_INSTRUCTIONS.md",
    "TASK_PROGRESS_REPORT.md",
    "UPDATE_SUMMARY_2025-11-08.md",
    "VERIFICATION_REPORT.md"
)

foreach ($doc in $docFiles) {
    $source = Join-Path $RepoRoot $doc
    $dest = Join-Path $RepoRoot "99_doc\$doc"
    if (Move-FileSafely -Source $source -Destination $dest -Category "99_doc/") {
        $movedCount++
    }
}

# 4. Move test files to tests/archive
Write-Host ""
Write-Host "4. Moving test files to tests/archive..." -ForegroundColor Cyan
$testFiles = @(
    "test_celery_integration.py",
    "test_origin_tracking.py",
    "test_processing_workflow.py",
    "test_python_demo.py",
    "test_search.py",
    "simple_rag_test.py",
    "rag_test.py",
    "test_queries.json"
)

foreach ($testFile in $testFiles) {
    $source = Join-Path $RepoRoot $testFile
    $dest = Join-Path $RepoRoot "tests\archive\$testFile"
    if (Move-FileSafely -Source $source -Destination $dest -Category "tests/archive/") {
        $movedCount++
    }
}

# 5. Move utility/analysis scripts to appropriate locations
Write-Host ""
Write-Host "5. Organizing utility scripts..." -ForegroundColor Cyan
$utilityMoves = @{
    "_analyze_remaining.py" = "tools"
    "_check_py_files.py" = "tools"
    "_check_remaining.py" = "tools"
    "analyze_empty_folders.py" = "tools"
    "analyze_failed_files.py" = "tools"
    "check_collection_dim.py" = "tools"
    "diagnose_issues.py" = "tools"
    "verify_backfill.py" = "tools"
    "verify_chunk_completeness.py" = "tools"
    "verify_enhancements.py" = "tools"
}

foreach ($file in $utilityMoves.Keys) {
    $source = Join-Path $RepoRoot $file
    $destDir = $utilityMoves[$file]
    $dest = Join-Path $RepoRoot "$destDir\$file"
    if (Move-FileSafely -Source $source -Destination $dest -Category "$destDir/") {
        $movedCount++
    }
}

# 6. Archive old backup directories
if ($ArchiveOld) {
    Write-Host ""
    Write-Host "6. Archiving old backup directories..." -ForegroundColor Cyan
    $backupDirs = @(
        "backup_20251107",
        "archive"
    )
    
    foreach ($backupDir in $backupDirs) {
        $source = Join-Path $RepoRoot $backupDir
        if (Test-Path $source) {
            $dest = Join-Path $RepoRoot "03_archive\old_backups\$backupDir"
            try {
                if ($WhatIf) {
                    Write-Host "  [WOULD MOVE] $backupDir -> 03_archive\old_backups\" -ForegroundColor Yellow
                } else {
                    Move-Item -Path $source -Destination $dest -Force
                    Write-Host "  [OK] Archived: $backupDir" -ForegroundColor Green
                    $movedCount++
                }
            } catch {
                $errors += "Failed to archive $backupDir : $_"
                Write-Host "  [ERROR] Error archiving $backupDir : $_" -ForegroundColor Red
            }
        }
    }
}

# 7. Clean up odd files (10, 240, 90, bool, python, nul, Tuple[bool, etc.)
Write-Host ""
Write-Host "7. Cleaning up odd files..." -ForegroundColor Cyan
$oddFiles = @("10", "240", "90", "bool", "python", "nul", "Tuple[bool")

foreach ($oddFile in $oddFiles) {
    $source = Join-Path $RepoRoot $oddFile
    if (Test-Path $source) {
        try {
            if ($WhatIf) {
                Write-Host "  [WOULD DELETE] $oddFile" -ForegroundColor Yellow
            } else {
                Remove-Item -Path $source -Force -ErrorAction Stop
                Write-Host "  [OK] Deleted odd file: $oddFile" -ForegroundColor Green
                $movedCount++
            }
        } catch {
            $errors += "Failed to delete $oddFile : $_"
            Write-Host "  [ERROR] Error deleting $oddFile : $_" -ForegroundColor Red
        }
    }
}

# 8. Move old release files to archive
Write-Host ""
Write-Host "8. Archiving old release files..." -ForegroundColor Cyan
$releaseFiles = @(
    "release_docs_v2025.11.09.zip",
    "release_log.txt"
)

foreach ($releaseFile in $releaseFiles) {
    $source = Join-Path $RepoRoot $releaseFile
    $dest = Join-Path $RepoRoot "03_archive\old_backups\$releaseFile"
    if (Move-FileSafely -Source $source -Destination $dest -Category "03_archive/old_backups/") {
        $movedCount++
    }
}

# 9. Move old config backups
Write-Host ""
Write-Host "9. Organizing config backups..." -ForegroundColor Cyan
$configBackups = Get-ChildItem -Path $RepoRoot -Filter "config.json.backup_*" -ErrorAction SilentlyContinue
foreach ($backup in $configBackups) {
    $dest = Join-Path $RepoRoot "06_config\backups\$($backup.Name)"
    if (Move-FileSafely -Source $backup.FullName -Destination $dest -Category "06_config/backups/") {
        $movedCount++
    }
}

# 10. Move reprocess config to 06_config
Write-Host ""
Write-Host "10. Organizing config files..." -ForegroundColor Cyan
$reprocessConfig = Join-Path $RepoRoot "reprocess_config.json"
if (Test-Path $reprocessConfig) {
    $dest = Join-Path $RepoRoot "06_config\reprocess_config.json"
    if (Move-FileSafely -Source $reprocessConfig -Destination $dest -Category "06_config/") {
        $movedCount++
    }
}

# Summary
Write-Host ""
Write-Host "=== Cleanup Summary ===" -ForegroundColor Cyan
Write-Host "Files processed: $movedCount" -ForegroundColor $(if ($movedCount -gt 0) { "Green" } else { "Gray" })
if ($errors.Count -gt 0) {
    Write-Host "Errors: $($errors.Count)" -ForegroundColor Red
    foreach ($error in $errors) {
        Write-Host "  - $error" -ForegroundColor Red
    }
} else {
    Write-Host "No errors encountered." -ForegroundColor Green
}

if ($WhatIf) {
    Write-Host ""
    Write-Host "This was a DRY RUN. Run without -WhatIf to perform actual moves." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Cleanup complete!" -ForegroundColor Cyan


```

```powershell
$oddFiles = @("10", "240", "90", "bool", "python", "nul", "Tuple[bool")
```

Testing the script again:


---

**User**

is the clean up complete?

---

**Cursor**


Checking if the cleanup has been run. We only did a dry run (`-WhatIf`). Verifying the current state:



Cleanup hasn't been run yet; we only did a dry run. Running the cleanup script now:



Cleanup complete. Summary:



Cleanup complete. Summary:

## Cleanup results

- 81 files processed
- 7 log files moved to `05_logs/`
- 7 PowerShell scripts moved to `scripts/`
- 40 documentation files moved to `99_doc/`
- 8 test files moved to `tests/archive/`
- 10 utility scripts moved to `tools/`
- 2 backup directories archived to `03_archive/old_backups/`
- 5 odd files deleted (10, 240, 90, bool, python)
- 2 release files archived
- 1 config backup moved to `06_config/backups/`
- 1 reprocess config moved to `06_config/`

## Remaining items in root

A few items remain:
1. `nul` — Windows reserved filename (may require special handling)
2. `Tuple[bool` — file with bracket in name (script had an issue with this)
3. `holding/` — directory (check if it's needed)
4. `logs/` — directory (may be redundant with `05_logs/`)
5. `watcher_test_output.txt` — test output file

The root directory is much cleaner. Core Python modules, config files, and essential directories remain. Should I clean up the remaining items?

---

**User**

all of the below files need to stay in the root?watcher_splitter.py
watchdog_system.py
watch_events.py
reprocess_output.py
rag_search.py
rag_integration.py
rag_evaluation.py
query_cache.py
performance_test.py
orchestrator.py
ollama_integration.py
ollama_client.py
notification_system.py
monitoring_system.py
migrate_to_onedrive.py
metadata_enrichment.py
manual_process_files.py
langsmith_integration.py
langchain_rag_handler.py
kb_ask_ollama.py
install_rag_dependencies.py
incremental_updates.py
gui_app.py
file_processors.py
failed_file_tracker.py
enhanced_watchdog.py
embedding_helpers.py
deduplication.py
dashboard_kb_monitoring.py
conftest.py
comprehensive_eval.py
cleanup_recursive_manifests.py
chunker_db.py
chunker_core.py
chunker_cleanup.py
chromadb_crud.py
celery_tasks.py
batch_reprocess_failed.py
backup_manager.py
backfill_tags.py
backfill_knowledge_base.py
automated_eval.py
ask.py
api_server.py
analytics_cli.py
advanced_celery_config.py

---

**Cursor**


Many of these can be organized into subdirectories. Checking import dependencies to ensure we don't break anything:



These files use direct imports (e.g., `from metadata_enrichment import ...`), so moving them requires updating imports. Creating a reorganization plan that preserves functionality:


```powershell
# Organize Python Modules Script
# Moves Python files into organized subdirectories while preserving import compatibility

param(
    [string]$RepoRoot = "$PSScriptRoot\..",
    [switch]$WhatIf = $false
)

Set-Location $RepoRoot

Write-Host "=== Python Modules Organization Script ===" -ForegroundColor Cyan
Write-Host "Repository Root: $RepoRoot" -ForegroundColor Gray
if ($WhatIf) {
    Write-Host "DRY RUN MODE - No files will be moved" -ForegroundColor Yellow
}
Write-Host ""

# Create organized directory structure
$targetDirs = @(
    "core",              # Core chunker functionality
    "rag",               # RAG/search related
    "integrations",      # External service integrations
    "monitoring",        # Watchdog and monitoring
    "utils",             # Utility modules
    "processing",        # File processing utilities
    "api",              # API and CLI interfaces
    "gui",              # GUI applications
    "migration",        # Migration and backup scripts
    "backfill"          # Backfill scripts
)

foreach ($dir in $targetDirs) {
    $fullPath = Join-Path $RepoRoot $dir
    if (-not (Test-Path $fullPath)) {
        if (-not $WhatIf) {
            New-Item -ItemType Directory -Path $fullPath -Force | Out-Null
            # Create __init__.py to make it a Python package
            $initFile = Join-Path $fullPath "__init__.py"
            if (-not (Test-Path $initFile)) {
                New-Item -ItemType File -Path $initFile -Force | Out-Null
            }
        }
        Write-Host "Created directory: $dir" -ForegroundColor Gray
    }
}

# Function to safely move files
function Move-FileSafely {
    param(
        [string]$Source,
        [string]$Destination,
        [string]$Category
    )
    
    if (-not (Test-Path $Source)) {
        return $false
    }
    
    $destDir = Split-Path $Destination -Parent
    if (-not (Test-Path $destDir)) {
        if (-not $WhatIf) {
            New-Item -ItemType Directory -Path $destDir -Force | Out-Null
        }
    }
    
    if (Test-Path $Destination) {
        $name = [System.IO.Path]::GetFileNameWithoutExtension($Source)
        $ext = [System.IO.Path]::GetExtension($Source)
        $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
        $Destination = Join-Path $destDir "${name}_${timestamp}${ext}"
    }
    
    try {
        if ($WhatIf) {
            Write-Host "  [WOULD MOVE] $Source -> $Destination" -ForegroundColor Yellow
        } else {
            Move-Item -Path $Source -Destination $Destination -Force
            Write-Host "  [OK] Moved: $([System.IO.Path]::GetFileName($Source)) -> $Category" -ForegroundColor Green
        }
        return $true
    } catch {
        Write-Host "  [ERROR] Error moving $Source : $_" -ForegroundColor Red
        return $false
    }
}

$movedCount = 0
$errors = @()

# CORE MODULES - Keep in root (these are main entry points or heavily imported)
# These should stay:
# - watcher_splitter.py (main entry point)
# - chunker_core.py (core functionality)
# - chunker_db.py (database - heavily imported)
# - file_processors.py (heavily imported)
# - metadata_enrichment.py (heavily imported)
# - watch_events.py (heavily imported)

# RAG MODULES - Move to rag/
Write-Host "1. Organizing RAG modules to rag/..." -ForegroundColor Cyan
$ragFiles = @(
    "rag_search.py",
    "rag_integration.py",
    "rag_evaluation.py",
    "query_cache.py"
)

foreach ($file in $ragFiles) {
    $source = Join-Path $RepoRoot $file
    $dest = Join-Path $RepoRoot "rag\$file"
    if (Move-FileSafely -Source $source -Destination $dest -Category "rag/") {
        $movedCount++
    }
}

# INTEGRATION MODULES - Move to integrations/
Write-Host ""
Write-Host "2. Organizing integration modules to integrations/..." -ForegroundColor Cyan
$integrationFiles = @(
    "ollama_integration.py",
    "ollama_client.py",
    "langsmith_integration.py",
    "langchain_rag_handler.py"
)

foreach ($file in $integrationFiles) {
    $source = Join-Path $RepoRoot $file
    $dest = Join-Path $RepoRoot "integrations\$file"
    if (Move-FileSafely -Source $source -Destination $dest -Category "integrations/") {
        $movedCount++
    }
}

# MONITORING MODULES - Move to monitoring/
Write-Host ""
Write-Host "3. Organizing monitoring modules to monitoring/..." -ForegroundColor Cyan
$monitoringFiles = @(
    "watchdog_system.py",
    "enhanced_watchdog.py",
    "monitoring_system.py",
    "notification_system.py"
)

foreach ($file in $monitoringFiles) {
    $source = Join-Path $RepoRoot $file
    $dest = Join-Path $RepoRoot "monitoring\$file"
    if (Move-FileSafely -Source $source -Destination $dest -Category "monitoring/") {
        $movedCount++
    }
}

# UTILITY MODULES - Move to utils/
Write-Host ""
Write-Host "4. Organizing utility modules to utils/..." -ForegroundColor Cyan
$utilityFiles = @(
    "embedding_helpers.py",
    "deduplication.py",
    "incremental_updates.py",
    "failed_file_tracker.py"
)

foreach ($file in $utilityFiles) {
    $source = Join-Path $RepoRoot $file
    $dest = Join-Path $RepoRoot "utils\$file"
    if (Move-FileSafely -Source $source -Destination $dest -Category "utils/") {
        $movedCount++
    }
}

# PROCESSING MODULES - Move to processing/
Write-Host ""
Write-Host "5. Organizing processing modules to processing/..." -ForegroundColor Cyan
$processingFiles = @(
    "reprocess_output.py",
    "batch_reprocess_failed.py",
    "manual_process_files.py",
    "cleanup_recursive_manifests.py"
)

foreach ($file in $processingFiles) {
    $source = Join-Path $RepoRoot $file
    $dest = Join-Path $RepoRoot "processing\$file"
    if (Move-FileSafely -Source $source -Destination $dest -Category "processing/") {
        $movedCount++
    }
}

# API/CLI MODULES - Move to api/
Write-Host ""
Write-Host "6. Organizing API/CLI modules to api/..." -ForegroundColor Cyan
$apiFiles = @(
    "api_server.py",
    "analytics_cli.py",
    "ask.py",
    "kb_ask_ollama.py"
)

foreach ($file in $apiFiles) {
    $source = Join-Path $RepoRoot $file
    $dest = Join-Path $RepoRoot "api\$file"
    if (Move-FileSafely -Source $source -Destination $dest -Category "api/") {
        $movedCount++
    }
}

# GUI MODULES - Move to gui/
Write-Host ""
Write-Host "7. Organizing GUI modules to gui/..." -ForegroundColor Cyan
$guiFiles = @(
    "gui_app.py",
    "dashboard_kb_monitoring.py"
)

foreach ($file in $guiFiles) {
    $source = Join-Path $RepoRoot $file
    $dest = Join-Path $RepoRoot "gui\$file"
    if (Move-FileSafely -Source $source -Destination $dest -Category "gui/") {
        $movedCount++
    }
}

# MIGRATION MODULES - Move to migration/
Write-Host ""
Write-Host "8. Organizing migration modules to migration/..." -ForegroundColor Cyan
$migrationFiles = @(
    "migrate_to_onedrive.py",
    "backup_manager.py"
)

foreach ($file in $migrationFiles) {
    $source = Join-Path $RepoRoot $file
    $dest = Join-Path $RepoRoot "migration\$file"
    if (Move-FileSafely -Source $source -Destination $dest -Category "migration/") {
        $movedCount++
    }
}

# BACKFILL MODULES - Move to backfill/
Write-Host ""
Write-Host "9. Organizing backfill modules to backfill/..." -ForegroundColor Cyan
$backfillFiles = @(
    "backfill_knowledge_base.py",
    "backfill_tags.py"
)

foreach ($file in $backfillFiles) {
    $source = Join-Path $RepoRoot $file
    $dest = Join-Path $RepoRoot "backfill\$file"
    if (Move-FileSafely -Source $source -Destination $dest -Category "backfill/") {
        $movedCount++
    }
}

# OTHER MODULES - Move to appropriate locations
Write-Host ""
Write-Host "10. Organizing other modules..." -ForegroundColor Cyan

$otherMoves = @{
    "chunker_cleanup.py" = "core"
    "chromadb_crud.py" = "rag"
    "celery_tasks.py" = "core"
    "advanced_celery_config.py" = "core"
    "orchestrator.py" = "core"
    "comprehensive_eval.py" = "rag"
    "automated_eval.py" = "rag"
    "performance_test.py" = "tests"
    "install_rag_dependencies.py" = "utils"
}

foreach ($file in $otherMoves.Keys) {
    $destDir = $otherMoves[$file]
    $source = Join-Path $RepoRoot $file
    $dest = Join-Path $RepoRoot "$destDir\$file"
    if (Move-FileSafely -Source $source -Destination $dest -Category "$destDir/") {
        $movedCount++
    }
}

# Summary
Write-Host ""
Write-Host "=== Organization Summary ===" -ForegroundColor Cyan
Write-Host "Files moved: $movedCount" -ForegroundColor $(if ($movedCount -gt 0) { "Green" } else { "Gray" })

if ($WhatIf) {
    Write-Host ""
    Write-Host "This was a DRY RUN. Run without -WhatIf to perform actual moves." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "IMPORTANT: After moving files, you will need to:" -ForegroundColor Yellow
    Write-Host "  1. Update import statements in all Python files" -ForegroundColor Yellow
    Write-Host "  2. Update any scripts that reference these files" -ForegroundColor Yellow
    Write-Host "  3. Test that everything still works" -ForegroundColor Yellow
} else {
    Write-Host ""
    Write-Host "WARNING: Import statements need to be updated!" -ForegroundColor Red
    Write-Host "  Example: 'from rag_search import ...' instead of 'from rag_search import ...'" -ForegroundColor Yellow
    Write-Host "  You may need to add the new directories to PYTHONPATH or update sys.path" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Organization complete!" -ForegroundColor Cyan

```


No, they don't all need to stay in root. Moving them will break imports unless we update them. Here's a safer approach:

## Recommendation

**Keep in root (critical/core modules):**
- `watcher_splitter.py` - Main entry point
- `chunker_core.py` - Core functionality
- `chunker_db.py` - Heavily imported
- `file_processors.py` - Heavily imported
- `metadata_enrichment.py` - Heavily imported
- `watch_events.py` - Heavily imported
- `dashboard_kb_monitoring.py` - Streamlit entry point (if run as `streamlit run dashboard_kb_monitoring.py`)
- `gui_app.py` - Streamlit entry point

**Can be organized into subdirectories:**
- RAG modules → `rag/`
- Integration modules → `integrations/`
- Monitoring modules → `monitoring/`
- Utility modules → `utils/`
- Processing scripts → `processing/`
- API/CLI → `api/`
- Backfill scripts → `backfill/`

I created `scripts\Organize-Python-Modules.ps1` to organize them, but it will require updating imports.

**Options:**
1. Run the organization script and I'll create a script to update all imports automatically.
2. Keep critical files in root and only move standalone/utility scripts.
3. Create a package structure with `__init__.py` files to make imports work from subdirectories.

Which approach do you prefer? Option 3 is safest but requires more setup.

---

**User**

can the following be moved 
requirements.txt
requirements_api_gui.txt
requirements_rag.txt
watcher_pid.txt
watcher_test_output.txt

---

**Cursor**


Checking where these files are referenced before moving them:



Yes, they can be moved. Here's the plan and a script to move them and update references:


```powershell
# Move Configuration and Runtime Files
# Moves requirements files, PID file, and test output to organized locations

param(
    [string]$RepoRoot = "$PSScriptRoot\..",
    [switch]$WhatIf = $false
)

Set-Location $RepoRoot

Write-Host "=== Moving Configuration and Runtime Files ===" -ForegroundColor Cyan
Write-Host "Repository Root: $RepoRoot" -ForegroundColor Gray
if ($WhatIf) {
    Write-Host "DRY RUN MODE - No files will be moved" -ForegroundColor Yellow
}
Write-Host ""

# Create target directories
$targetDirs = @(
    "06_config\requirements",
    "05_logs\runtime"
)

foreach ($dir in $targetDirs) {
    $fullPath = Join-Path $RepoRoot $dir
    if (-not (Test-Path $fullPath)) {
        if (-not $WhatIf) {
            New-Item -ItemType Directory -Path $fullPath -Force | Out-Null
        }
        Write-Host "Created directory: $dir" -ForegroundColor Gray
    }
}

$movedCount = 0
$updatedCount = 0

# Function to safely move files
function Move-FileSafely {
    param(
        [string]$Source,
        [string]$Destination,
        [string]$Category
    )
    
    if (-not (Test-Path $Source)) {
        return $false
    }
    
    $destDir = Split-Path $Destination -Parent
    if (-not (Test-Path $destDir)) {
        if (-not $WhatIf) {
            New-Item -ItemType Directory -Path $destDir -Force | Out-Null
        }
    }
    
    try {
        if ($WhatIf) {
            Write-Host "  [WOULD MOVE] $Source -> $Destination" -ForegroundColor Yellow
        } else {
            Move-Item -Path $Source -Destination $Destination -Force
            Write-Host "  [OK] Moved: $([System.IO.Path]::GetFileName($Source)) -> $Category" -ForegroundColor Green
        }
        return $true
    } catch {
        Write-Host "  [ERROR] Error moving $Source : $_" -ForegroundColor Red
        return $false
    }
}

# Function to update file references
function Update-FileReferences {
    param(
        [string]$OldPath,
        [string]$NewPath,
        [string[]]$FilesToUpdate
    )
    
    $oldPathEscaped = [regex]::Escape($OldPath)
    $newPathEscaped = [regex]::Escape($NewPath)
    
    foreach ($file in $FilesToUpdate) {
        $fullPath = Join-Path $RepoRoot $file
        if (Test-Path $fullPath) {
            try {
                if ($WhatIf) {
                    Write-Host "  [WOULD UPDATE] $file" -ForegroundColor Yellow
                } else {
                    $content = Get-Content $fullPath -Raw
                    $updated = $content -replace $oldPathEscaped, $newPathEscaped
                    if ($content -ne $updated) {
                        Set-Content -Path $fullPath -Value $updated -NoNewline
                        Write-Host "  [OK] Updated references in: $file" -ForegroundColor Green
                        $script:updatedCount++
                    }
                }
            } catch {
                Write-Host "  [ERROR] Failed to update $file : $_" -ForegroundColor Red
            }
        }
    }
}

# 1. Move requirements files to 06_config/requirements/
Write-Host "1. Moving requirements files to 06_config/requirements/..." -ForegroundColor Cyan
$requirementsFiles = @(
    "requirements.txt",
    "requirements_api_gui.txt",
    "requirements_rag.txt"
)

foreach ($file in $requirementsFiles) {
    $source = Join-Path $RepoRoot $file
    $dest = Join-Path $RepoRoot "06_config\requirements\$file"
    if (Move-FileSafely -Source $source -Destination $dest -Category "06_config/requirements/") {
        $movedCount++
    }
}

# Update references to requirements.txt in scripts
Write-Host ""
Write-Host "2. Updating references to requirements files..." -ForegroundColor Cyan
$filesToUpdate = @(
    "scripts\Start-Watcher.ps1",
    "scripts\Start-Watcher-Background.ps1"
)

foreach ($reqFile in $requirementsFiles) {
    $oldPath = $reqFile
    $newPath = "06_config\requirements\$reqFile"
    Update-FileReferences -OldPath $oldPath -NewPath $newPath -FilesToUpdate $filesToUpdate
}

# 2. Move watcher_pid.txt to 05_logs/runtime/
Write-Host ""
Write-Host "3. Moving runtime files to 05_logs/runtime/..." -ForegroundColor Cyan
$pidFile = Join-Path $RepoRoot "watcher_pid.txt"
$pidDest = Join-Path $RepoRoot "05_logs\runtime\watcher_pid.txt"
if (Move-FileSafely -Source $pidFile -Destination $pidDest -Category "05_logs/runtime/") {
    $movedCount++
}

# Update references to watcher_pid.txt
Write-Host ""
Write-Host "4. Updating references to watcher_pid.txt..." -ForegroundColor Cyan
$pidFilesToUpdate = @(
    "scripts\Start-Watcher.ps1",
    "scripts\Start-Watcher-Background.ps1",
    "scripts\Stop-Watcher.ps1",
    "scripts\KB-Health.ps1"
)

Update-FileReferences -OldPath "watcher_pid.txt" -NewPath "05_logs\runtime\watcher_pid.txt" -FilesToUpdate $pidFilesToUpdate

# 3. Move watcher_test_output.txt to 05_logs/
Write-Host ""
Write-Host "5. Moving test output files..." -ForegroundColor Cyan
$testOutput = Join-Path $RepoRoot "watcher_test_output.txt"
$testDest = Join-Path $RepoRoot "05_logs\watcher_test_output.txt"
if (Move-FileSafely -Source $testOutput -Destination $testDest -Category "05_logs/") {
    $movedCount++
}

# Summary
Write-Host ""
Write-Host "=== Summary ===" -ForegroundColor Cyan
Write-Host "Files moved: $movedCount" -ForegroundColor $(if ($movedCount -gt 0) { "Green" } else { "Gray" })
Write-Host "Files updated: $updatedCount" -ForegroundColor $(if ($updatedCount -gt 0) { "Green" } else { "Gray" })

if ($WhatIf) {
    Write-Host ""
    Write-Host "This was a DRY RUN. Run without -WhatIf to perform actual moves." -ForegroundColor Yellow
} else {
    Write-Host ""
    Write-Host "Files moved and references updated!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Note: If watcher is currently running, restart it to use the new PID file location." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Move complete!" -ForegroundColor Cyan

```


Yes, these files can be moved. Created a script that will:

## Files to Move:

1. **Requirements files** → `06_config/requirements/`
   - `requirements.txt`
   - `requirements_api_gui.txt`
   - `requirements_rag.txt`

2. **Runtime file** → `05_logs/runtime/`
   - `watcher_pid.txt` (runtime PID tracking)

3. **Test output** → `05_logs/`
   - `watcher_test_output.txt`

## Script Updates:

The script will automatically update references in:
- `scripts\Start-Watcher.ps1`
- `scripts\Start-Watcher-Background.ps1`
- `scripts\Stop-Watcher.ps1`
- `scripts\KB-Health.ps1`

The dry run shows it will move 5 files and update 4 script files.

**Note:** If the watcher is currently running, restart it after moving `watcher_pid.txt` so it uses the new location.

Should I run the script now to perform the moves?

---

**User**

please stop watcher, run, re-enable watcher please

---

**Cursor**


Stopping the watcher, running the move script, then restarting it:



Fixing path issues in the script:



Fixing incorrect path replacements in the scripts:


```powershell
param(
  [string]$RepoRoot = "$PSScriptRoot\.."
)

Set-Location $RepoRoot
$env:PYTHONUNBUFFERED = "1"

Write-Host "Initializing Enterprise RAG Pipeline (Background Mode)..." -ForegroundColor Cyan

# Check for OneDrive path
$oneDriveRoot = Join-Path $env:OneDriveCommercial "KB_Shared"
if (-not (Test-Path $oneDriveRoot)) {
  Write-Host "OneDrive KB_Shared missing." -ForegroundColor Red
  exit 1
}

# Ensure logs directory exists
$logsDir = Join-Path $RepoRoot "05_logs"
if (-not (Test-Path $logsDir)) {
  New-Item -ItemType Directory -Path $logsDir -Force | Out-Null
}

# Check if watcher is already running
$pidFile = Join-Path $RepoRoot "05_logs\\runtime\\watcher_pid\.txt"
$skipWatcherStart = $false
if (Test-Path $pidFile) {
  $watcherPid = Get-Content $pidFile | Select-Object -First 1
  if ($watcherPid -and (Get-Process -Id $watcherPid -ErrorAction SilentlyContinue)) {
    Write-Host "Watcher already running. PID=$watcherPid" -ForegroundColor Yellow
    Write-Host "Starting Dashboard only..." -ForegroundColor Green
    $skipWatcherStart = $true
  }
}

# Check if dashboard is already running
$dashboard = Get-WmiObject Win32_Process -ErrorAction SilentlyContinue | Where-Object { $_.CommandLine -like "*streamlit run dashboard_kb_monitoring.py*" }
if ($dashboard) {
  Write-Host "Dashboard already running. PID=$($dashboard.ProcessId)" -ForegroundColor Yellow
}

# 1. Activate the Virtual Environment (if available)
$VenvPath = Join-Path $RepoRoot ".venv\Scripts\Activate.ps1"
$PythonExe = "python"
$PythonwExe = "pythonw"
$PipExe = "pip"
if (Test-Path $VenvPath) {
    . $VenvPath
    $PythonExe = Join-Path $RepoRoot ".venv\Scripts\python.exe"
    $PythonwExe = Join-Path $RepoRoot ".venv\Scripts\pythonw.exe"
    $PipExe = Join-Path $RepoRoot ".venv\Scripts\pip.exe"
    Write-Host "Virtual environment activated." -ForegroundColor Gray
} else {
    Write-Warning "Virtual environment not found at $VenvPath. Attempting to run with system Python..."
}

# Check and install missing dependencies (especially plotly for dashboard)
Write-Host "Checking dependencies..." -ForegroundColor Gray
$requirementsFile = Join-Path $RepoRoot "06_config\requirements\requirements.txt"
if (Test-Path $requirementsFile) {
    try {
        # Quick check if plotly is installed (required for dashboard)
        $plotlyCheck = & $PythonExe -c "import plotly" 2>&1
        if ($LASTEXITCODE -ne 0) {
            Write-Host "Installing missing dependencies (plotly required for dashboard)..." -ForegroundColor Yellow
            & $PipExe install -q -r $requirementsFile
            if ($LASTEXITCODE -eq 0) {
                Write-Host "Dependencies installed successfully." -ForegroundColor Green
            } else {
                Write-Warning "Some dependencies may have failed to install. Dashboard may not work correctly."
            }
        } else {
            Write-Host "Dependencies check passed." -ForegroundColor Gray
        }
    } catch {
        Write-Warning "Could not verify dependencies. Dashboard may fail if plotly is missing."
    }
} else {
    Write-Warning "06_config\\requirements\\requirements\.txt not found. Dashboard may fail if dependencies are missing."
}

# 2. Start the Watcher (The Core Processor) - Skip if already running
# This handles File Splitting AND Automatic KB Insertion
# Using pythonw.exe to run without console window
if (-not $skipWatcherStart) {
    Write-Host "Starting Watcher Service (Splitter + KB Auto-Insert) in background..." -ForegroundColor Green
    
    # Use pythonw.exe if available, otherwise fall back to python.exe with hidden window
    $watcherLogFile = Join-Path $logsDir "watcher_background.log"
    if (Test-Path $PythonwExe) {
        # pythonw.exe runs without console window
        $WatcherProcess = Start-Process -FilePath $PythonwExe `
            -ArgumentList "watcher_splitter.py" `
            -WorkingDirectory $RepoRoot `
            -WindowStyle Hidden `
            -PassThru
    } else {
        # Fallback: use python.exe but redirect output and hide window
        $WatcherProcess = Start-Process -FilePath $PythonExe `
            -ArgumentList "watcher_splitter.py" `
            -WorkingDirectory $RepoRoot `
            -WindowStyle Hidden `
            -RedirectStandardOutput $watcherLogFile `
            -RedirectStandardError $watcherLogFile `
            -PassThru
    }

    Start-Sleep -Seconds 2
    $watcherPid = $WatcherProcess.Id

    if ($null -ne $watcherPid -and (Get-Process -Id $watcherPid -ErrorAction SilentlyContinue)) {
      $watcherPid | Out-File -Encoding ascii -FilePath $pidFile -Force
      Write-Host "Watcher started in background. PID=$watcherPid" -ForegroundColor Green
      Write-Host "Logs: $watcherLogFile" -ForegroundColor Gray
    } else {
      Write-Host "Watcher process not found after start attempt." -ForegroundColor Red
      exit 1
    }

    # Optional: Health check (if KB-Health.ps1 exists)
    if (Test-Path "$RepoRoot\scripts\KB-Health.ps1") {
      $health = & "$RepoRoot\scripts\KB-Health.ps1" -RepoRoot $RepoRoot -OD $env:OneDriveCommercial
      if ($health -is [System.Array]) {
        $health = $health[0]
      }
      if ($health.Watcher -notlike "Running*") {
        Write-Host "Watcher health check failed: $($health.Watcher)" -ForegroundColor Red
        if ($null -ne $watcherPid -and (Get-Process -Id $watcherPid -ErrorAction SilentlyContinue)) {
          Stop-Process -Id $watcherPid -Force
        }
        if (Test-Path $pidFile) {
          Remove-Item $pidFile -ErrorAction SilentlyContinue
        }
        exit 1
      }
    }
}

# 3. Start the Monitoring Dashboard
# This allows you to view the Database and Real-time stats
# Running in hidden mode - access via browser at http://localhost:8501
if (-not $dashboard) {
  Write-Host "Starting KB Monitoring Dashboard in background..." -ForegroundColor Green
  $StreamlitExe = Join-Path $RepoRoot ".venv\Scripts\streamlit.exe"
  if (-not (Test-Path $StreamlitExe)) {
      $StreamlitExe = "streamlit"
  }
  
  $dashboardLogFile = Join-Path $logsDir "dashboard_background.log"
  Start-Process -FilePath $StreamlitExe `
      -ArgumentList "run dashboard_kb_monitoring.py" `
      -WorkingDirectory $RepoRoot `
      -WindowStyle Hidden `
      -RedirectStandardOutput $dashboardLogFile `
      -RedirectStandardError $dashboardLogFile `
      -PassThru | Out-Null
  
  Write-Host "Dashboard starting in background..." -ForegroundColor Gray
  Write-Host "Access dashboard at: http://localhost:8501" -ForegroundColor Cyan
  Write-Host "Logs: $dashboardLogFile" -ForegroundColor Gray
} else {
  Write-Host "Dashboard already running." -ForegroundColor Gray
}

Write-Host ""
Write-Host "All systems operational (running in background)." -ForegroundColor Cyan
Write-Host "1. Drop files into '02_data' to process." -ForegroundColor White
Write-Host "2. Access dashboard at: http://localhost:8501" -ForegroundColor White
Write-Host "3. Check logs in: $logsDir" -ForegroundColor White
Write-Host ""
Write-Host "To stop services, run: scripts\Stop-Watcher.ps1" -ForegroundColor Yellow


```

```powershell
param(
  [string]$RepoRoot = "$PSScriptRoot\.."
)

Set-Location $RepoRoot
$env:PYTHONUNBUFFERED = "1"

Write-Host "Initializing Enterprise RAG Pipeline (Background Mode)..." -ForegroundColor Cyan

# Check for OneDrive path
$oneDriveRoot = Join-Path $env:OneDriveCommercial "KB_Shared"
if (-not (Test-Path $oneDriveRoot)) {
  Write-Host "OneDrive KB_Shared missing." -ForegroundColor Red
  exit 1
}

# Ensure logs directory exists
$logsDir = Join-Path $RepoRoot "05_logs"
if (-not (Test-Path $logsDir)) {
  New-Item -ItemType Directory -Path $logsDir -Force | Out-Null
}

# Check if watcher is already running
$pidFile = Join-Path $RepoRoot "05_logs\\runtime\\watcher_pid\.txt"
$skipWatcherStart = $false
if (Test-Path $pidFile) {
  $watcherPid = Get-Content $pidFile | Select-Object -First 1
  if ($watcherPid -and (Get-Process -Id $watcherPid -ErrorAction SilentlyContinue)) {
    Write-Host "Watcher already running. PID=$watcherPid" -ForegroundColor Yellow
    Write-Host "Starting Dashboard only..." -ForegroundColor Green
    $skipWatcherStart = $true
  }
}

# Check if dashboard is already running
$dashboard = Get-WmiObject Win32_Process -ErrorAction SilentlyContinue | Where-Object { $_.CommandLine -like "*streamlit run dashboard_kb_monitoring.py*" }
if ($dashboard) {
  Write-Host "Dashboard already running. PID=$($dashboard.ProcessId)" -ForegroundColor Yellow
}

# 1. Activate the Virtual Environment (if available)
$VenvPath = Join-Path $RepoRoot ".venv\Scripts\Activate.ps1"
$PythonExe = "python"
$PythonwExe = "pythonw"
$PipExe = "pip"
if (Test-Path $VenvPath) {
    . $VenvPath
    $PythonExe = Join-Path $RepoRoot ".venv\Scripts\python.exe"
    $PythonwExe = Join-Path $RepoRoot ".venv\Scripts\pythonw.exe"
    $PipExe = Join-Path $RepoRoot ".venv\Scripts\pip.exe"
    Write-Host "Virtual environment activated." -ForegroundColor Gray
} else {
    Write-Warning "Virtual environment not found at $VenvPath. Attempting to run with system Python..."
}

# Check and install missing dependencies (especially plotly for dashboard)
Write-Host "Checking dependencies..." -ForegroundColor Gray
$requirementsFile = Join-Path $RepoRoot "06_config\requirements\requirements.txt"
if (Test-Path $requirementsFile) {
    try {
        # Quick check if plotly is installed (required for dashboard)
        $plotlyCheck = & $PythonExe -c "import plotly" 2>&1
        if ($LASTEXITCODE -ne 0) {
            Write-Host "Installing missing dependencies (plotly required for dashboard)..." -ForegroundColor Yellow
            & $PipExe install -q -r $requirementsFile
            if ($LASTEXITCODE -eq 0) {
                Write-Host "Dependencies installed successfully." -ForegroundColor Green
            } else {
                Write-Warning "Some dependencies may have failed to install. Dashboard may not work correctly."
            }
        } else {
            Write-Host "Dependencies check passed." -ForegroundColor Gray
        }
    } catch {
        Write-Warning "Could not verify dependencies. Dashboard may fail if plotly is missing."
    }
} else {
    Write-Warning "06_config\requirements\requirements.txt not found. Dashboard may fail if dependencies are missing."
}

# 2. Start the Watcher (The Core Processor) - Skip if already running
# This handles File Splitting AND Automatic KB Insertion
# Using pythonw.exe to run without console window
if (-not $skipWatcherStart) {
    Write-Host "Starting Watcher Service (Splitter + KB Auto-Insert) in background..." -ForegroundColor Green
    
    # Use pythonw.exe if available, otherwise fall back to python.exe with hidden window
    $watcherLogFile = Join-Path $logsDir "watcher_background.log"
    if (Test-Path $PythonwExe) {
        # pythonw.exe runs without console window
        $WatcherProcess = Start-Process -FilePath $PythonwExe `
            -ArgumentList "watcher_splitter.py" `
            -WorkingDirectory $RepoRoot `
            -WindowStyle Hidden `
            -PassThru
    } else {
        # Fallback: use python.exe but redirect output and hide window
        $WatcherProcess = Start-Process -FilePath $PythonExe `
            -ArgumentList "watcher_splitter.py" `
            -WorkingDirectory $RepoRoot `
            -WindowStyle Hidden `
            -RedirectStandardOutput $watcherLogFile `
            -RedirectStandardError $watcherLogFile `
            -PassThru
    }

    Start-Sleep -Seconds 2
    $watcherPid = $WatcherProcess.Id

    if ($null -ne $watcherPid -and (Get-Process -Id $watcherPid -ErrorAction SilentlyContinue)) {
      $watcherPid | Out-File -Encoding ascii -FilePath $pidFile -Force
      Write-Host "Watcher started in background. PID=$watcherPid" -ForegroundColor Green
      Write-Host "Logs: $watcherLogFile" -ForegroundColor Gray
    } else {
      Write-Host "Watcher process not found after start attempt." -ForegroundColor Red
      exit 1
    }

    # Optional: Health check (if KB-Health.ps1 exists)
    if (Test-Path "$RepoRoot\scripts\KB-Health.ps1") {
      $health = & "$RepoRoot\scripts\KB-Health.ps1" -RepoRoot $RepoRoot -OD $env:OneDriveCommercial
      if ($health -is [System.Array]) {
        $health = $health[0]
      }
      if ($health.Watcher -notlike "Running*") {
        Write-Host "Watcher health check failed: $($health.Watcher)" -ForegroundColor Red
        if ($null -ne $watcherPid -and (Get-Process -Id $watcherPid -ErrorAction SilentlyContinue)) {
          Stop-Process -Id $watcherPid -Force
        }
        if (Test-Path $pidFile) {
          Remove-Item $pidFile -ErrorAction SilentlyContinue
        }
        exit 1
      }
    }
}

# 3. Start the Monitoring Dashboard
# This allows you to view the Database and Real-time stats
# Running in hidden mode - access via browser at http://localhost:8501
if (-not $dashboard) {
  Write-Host "Starting KB Monitoring Dashboard in background..." -ForegroundColor Green
  $StreamlitExe = Join-Path $RepoRoot ".venv\Scripts\streamlit.exe"
  if (-not (Test-Path $StreamlitExe)) {
      $StreamlitExe = "streamlit"
  }
  
  $dashboardLogFile = Join-Path $logsDir "dashboard_background.log"
  Start-Process -FilePath $StreamlitExe `
      -ArgumentList "run dashboard_kb_monitoring.py" `
      -WorkingDirectory $RepoRoot `
      -WindowStyle Hidden `
      -RedirectStandardOutput $dashboardLogFile `
      -RedirectStandardError $dashboardLogFile `
      -PassThru | Out-Null
  
  Write-Host "Dashboard starting in background..." -ForegroundColor Gray
  Write-Host "Access dashboard at: http://localhost:8501" -ForegroundColor Cyan
  Write-Host "Logs: $dashboardLogFile" -ForegroundColor Gray
} else {
  Write-Host "Dashboard already running." -ForegroundColor Gray
}

Write-Host ""
Write-Host "All systems operational (running in background)." -ForegroundColor Cyan
Write-Host "1. Drop files into '02_data' to process." -ForegroundColor White
Write-Host "2. Access dashboard at: http://localhost:8501" -ForegroundColor White
Write-Host "3. Check logs in: $logsDir" -ForegroundColor White
Write-Host ""
Write-Host "To stop services, run: scripts\Stop-Watcher.ps1" -ForegroundColor Yellow


```


Fixing path issues in both scripts:


```powershell
param(
  [string]$RepoRoot = "$PSScriptRoot\.."
)

Set-Location $RepoRoot
$env:PYTHONUNBUFFERED = "1"

Write-Host "Initializing Enterprise RAG Pipeline (Background Mode)..." -ForegroundColor Cyan

# Check for OneDrive path
$oneDriveRoot = Join-Path $env:OneDriveCommercial "KB_Shared"
if (-not (Test-Path $oneDriveRoot)) {
  Write-Host "OneDrive KB_Shared missing." -ForegroundColor Red
  exit 1
}

# Ensure logs directory exists
$logsDir = Join-Path $RepoRoot "05_logs"
if (-not (Test-Path $logsDir)) {
  New-Item -ItemType Directory -Path $logsDir -Force | Out-Null
}

# Check if watcher is already running
$pidFile = Join-Path $RepoRoot "05_logs\runtime\watcher_pid.txt"
$skipWatcherStart = $false
if (Test-Path $pidFile) {
  $watcherPid = Get-Content $pidFile | Select-Object -First 1
  if ($watcherPid -and (Get-Process -Id $watcherPid -ErrorAction SilentlyContinue)) {
    Write-Host "Watcher already running. PID=$watcherPid" -ForegroundColor Yellow
    Write-Host "Starting Dashboard only..." -ForegroundColor Green
    $skipWatcherStart = $true
  }
}

# Check if dashboard is already running
$dashboard = Get-WmiObject Win32_Process -ErrorAction SilentlyContinue | Where-Object { $_.CommandLine -like "*streamlit run dashboard_kb_monitoring.py*" }
if ($dashboard) {
  Write-Host "Dashboard already running. PID=$($dashboard.ProcessId)" -ForegroundColor Yellow
}

# 1. Activate the Virtual Environment (if available)
$VenvPath = Join-Path $RepoRoot ".venv\Scripts\Activate.ps1"
$PythonExe = "python"
$PythonwExe = "pythonw"
$PipExe = "pip"
if (Test-Path $VenvPath) {
    . $VenvPath
    $PythonExe = Join-Path $RepoRoot ".venv\Scripts\python.exe"
    $PythonwExe = Join-Path $RepoRoot ".venv\Scripts\pythonw.exe"
    $PipExe = Join-Path $RepoRoot ".venv\Scripts\pip.exe"
    Write-Host "Virtual environment activated." -ForegroundColor Gray
} else {
    Write-Warning "Virtual environment not found at $VenvPath. Attempting to run with system Python..."
}

# Check and install missing dependencies (especially plotly for dashboard)
Write-Host "Checking dependencies..." -ForegroundColor Gray
$requirementsFile = Join-Path $RepoRoot "06_config\requirements\requirements.txt"
if (Test-Path $requirementsFile) {
    try {
        # Quick check if plotly is installed (required for dashboard)
        $plotlyCheck = & $PythonExe -c "import plotly" 2>&1
        if ($LASTEXITCODE -ne 0) {
            Write-Host "Installing missing dependencies (plotly required for dashboard)..." -ForegroundColor Yellow
            & $PipExe install -q -r $requirementsFile
            if ($LASTEXITCODE -eq 0) {
                Write-Host "Dependencies installed successfully." -ForegroundColor Green
            } else {
                Write-Warning "Some dependencies may have failed to install. Dashboard may not work correctly."
            }
        } else {
            Write-Host "Dependencies check passed." -ForegroundColor Gray
        }
    } catch {
        Write-Warning "Could not verify dependencies. Dashboard may fail if plotly is missing."
    }
} else {
    Write-Warning "06_config\requirements\requirements.txt not found. Dashboard may fail if dependencies are missing."
}

# 2. Start the Watcher (The Core Processor) - Skip if already running
# This handles File Splitting AND Automatic KB Insertion
# Using pythonw.exe to run without console window
if (-not $skipWatcherStart) {
    Write-Host "Starting Watcher Service (Splitter + KB Auto-Insert) in background..." -ForegroundColor Green
    
    # Use pythonw.exe if available, otherwise fall back to python.exe with hidden window
    $watcherLogFile = Join-Path $logsDir "watcher_background.log"
    if (Test-Path $PythonwExe) {
        # pythonw.exe runs without console window
        $WatcherProcess = Start-Process -FilePath $PythonwExe `
            -ArgumentList "watcher_splitter.py" `
            -WorkingDirectory $RepoRoot `
            -WindowStyle Hidden `
            -PassThru
    } else {
        # Fallback: use python.exe but redirect output and hide window
        $WatcherProcess = Start-Process -FilePath $PythonExe `
            -ArgumentList "watcher_splitter.py" `
            -WorkingDirectory $RepoRoot `
            -WindowStyle Hidden `
            -RedirectStandardOutput $watcherLogFile `
            -RedirectStandardError $watcherLogFile `
            -PassThru
    }

    Start-Sleep -Seconds 2
    $watcherPid = $WatcherProcess.Id

    if ($null -ne $watcherPid -and (Get-Process -Id $watcherPid -ErrorAction SilentlyContinue)) {
      $watcherPid | Out-File -Encoding ascii -FilePath $pidFile -Force
      Write-Host "Watcher started in background. PID=$watcherPid" -ForegroundColor Green
      Write-Host "Logs: $watcherLogFile" -ForegroundColor Gray
    } else {
      Write-Host "Watcher process not found after start attempt." -ForegroundColor Red
      exit 1
    }

    # Optional: Health check (if KB-Health.ps1 exists)
    if (Test-Path "$RepoRoot\scripts\KB-Health.ps1") {
      $health = & "$RepoRoot\scripts\KB-Health.ps1" -RepoRoot $RepoRoot -OD $env:OneDriveCommercial
      if ($health -is [System.Array]) {
        $health = $health[0]
      }
      if ($health.Watcher -notlike "Running*") {
        Write-Host "Watcher health check failed: $($health.Watcher)" -ForegroundColor Red
        if ($null -ne $watcherPid -and (Get-Process -Id $watcherPid -ErrorAction SilentlyContinue)) {
          Stop-Process -Id $watcherPid -Force
        }
        if (Test-Path $pidFile) {
          Remove-Item $pidFile -ErrorAction SilentlyContinue
        }
        exit 1
      }
    }
}

# 3. Start the Monitoring Dashboard
# This allows you to view the Database and Real-time stats
# Running in hidden mode - access via browser at http://localhost:8501
if (-not $dashboard) {
  Write-Host "Starting KB Monitoring Dashboard in background..." -ForegroundColor Green
  $StreamlitExe = Join-Path $RepoRoot ".venv\Scripts\streamlit.exe"
  if (-not (Test-Path $StreamlitExe)) {
      $StreamlitExe = "streamlit"
  }
  
  $dashboardLogFile = Join-Path $logsDir "dashboard_background.log"
  Start-Process -FilePath $StreamlitExe `
      -ArgumentList "run dashboard_kb_monitoring.py" `
      -WorkingDirectory $RepoRoot `
      -WindowStyle Hidden `
      -RedirectStandardOutput $dashboardLogFile `
      -RedirectStandardError $dashboardLogFile `
      -PassThru | Out-Null
  
  Write-Host "Dashboard starting in background..." -ForegroundColor Gray
  Write-Host "Access dashboard at: http://localhost:8501" -ForegroundColor Cyan
  Write-Host "Logs: $dashboardLogFile" -ForegroundColor Gray
} else {
  Write-Host "Dashboard already running." -ForegroundColor Gray
}

Write-Host ""
Write-Host "All systems operational (running in background)." -ForegroundColor Cyan
Write-Host "1. Drop files into '02_data' to process." -ForegroundColor White
Write-Host "2. Access dashboard at: http://localhost:8501" -ForegroundColor White
Write-Host "3. Check logs in: $logsDir" -ForegroundColor White
Write-Host ""
Write-Host "To stop services, run: scripts\Stop-Watcher.ps1" -ForegroundColor Yellow


```

```powershell
param(
  [string]$RepoRoot = "$PSScriptRoot\.."
)

Set-Location $RepoRoot
$env:PYTHONUNBUFFERED = "1"

Write-Host "Initializing Enterprise RAG Pipeline..." -ForegroundColor Cyan

# Check for OneDrive path
$oneDriveRoot = Join-Path $env:OneDriveCommercial "KB_Shared"
if (-not (Test-Path $oneDriveRoot)) {
  Write-Host "OneDrive KB_Shared missing." -ForegroundColor Red
  exit 1
}

# Check if watcher is already running
$pidFile = Join-Path $RepoRoot "05_logs\\runtime\\watcher_pid\.txt"
$skipWatcherStart = $false
if (Test-Path $pidFile) {
  $watcherPid = Get-Content $pidFile | Select-Object -First 1
  if ($watcherPid -and (Get-Process -Id $watcherPid -ErrorAction SilentlyContinue)) {
    Write-Host "Watcher already running. PID=$watcherPid" -ForegroundColor Yellow
    Write-Host "Starting Dashboard only..." -ForegroundColor Green
    $skipWatcherStart = $true
  }
}

# Check if dashboard is already running
$dashboard = Get-WmiObject Win32_Process -ErrorAction SilentlyContinue | Where-Object { $_.CommandLine -like "*streamlit run dashboard_kb_monitoring.py*" }
if ($dashboard) {
  Write-Host "Dashboard already running. PID=$($dashboard.ProcessId)" -ForegroundColor Yellow
}

# 1. Activate the Virtual Environment (if available)
$VenvPath = Join-Path $RepoRoot ".venv\Scripts\Activate.ps1"
$PythonExe = "python"
$PipExe = "pip"
if (Test-Path $VenvPath) {
    . $VenvPath
    $PythonExe = Join-Path $RepoRoot ".venv\Scripts\python.exe"
    $PipExe = Join-Path $RepoRoot ".venv\Scripts\pip.exe"
    Write-Host "Virtual environment activated." -ForegroundColor Gray
} else {
    Write-Warning "Virtual environment not found at $VenvPath. Attempting to run with system Python..."
}

# Check and install missing dependencies (especially plotly for dashboard)
Write-Host "Checking dependencies..." -ForegroundColor Gray
$requirementsFile = Join-Path $RepoRoot "06_config\requirements\requirements.txt"
if (Test-Path $requirementsFile) {
    try {
        # Quick check if plotly is installed (required for dashboard)
        $plotlyCheck = & $PythonExe -c "import plotly" 2>&1
        if ($LASTEXITCODE -ne 0) {
            Write-Host "Installing missing dependencies (plotly required for dashboard)..." -ForegroundColor Yellow
            & $PipExe install -q -r $requirementsFile
            if ($LASTEXITCODE -eq 0) {
                Write-Host "Dependencies installed successfully." -ForegroundColor Green
            } else {
                Write-Warning "Some dependencies may have failed to install. Dashboard may not work correctly."
            }
        } else {
            Write-Host "Dependencies check passed." -ForegroundColor Gray
        }
    } catch {
        Write-Warning "Could not verify dependencies. Dashboard may fail if plotly is missing."
    }
} else {
    Write-Warning "06_config\\requirements\\requirements\.txt not found. Dashboard may fail if dependencies are missing."
}

# 2. Start the Watcher (The Core Processor) - Skip if already running
# This handles File Splitting AND Automatic KB Insertion
if (-not $skipWatcherStart) {
    Write-Host "Starting Watcher Service (Splitter + KB Auto-Insert)..." -ForegroundColor Green
    $WatcherProcess = Start-Process -FilePath $PythonExe `
        -ArgumentList "watcher_splitter.py" `
        -WorkingDirectory $RepoRoot `
        -WindowStyle Minimized `
        -PassThru

    Start-Sleep -Seconds 2
    $watcherPid = $WatcherProcess.Id

    if ($null -ne $watcherPid -and (Get-Process -Id $watcherPid -ErrorAction SilentlyContinue)) {
      $watcherPid | Out-File -Encoding ascii -FilePath $pidFile -Force
      Write-Host "Watcher started. PID=$watcherPid" -ForegroundColor Green
    } else {
      Write-Host "Watcher process not found after start attempt." -ForegroundColor Red
      exit 1
    }

    # Optional: Health check (if KB-Health.ps1 exists)
    if (Test-Path "$RepoRoot\scripts\KB-Health.ps1") {
      $health = & "$RepoRoot\scripts\KB-Health.ps1" -RepoRoot $RepoRoot -OD $env:OneDriveCommercial
      if ($health -is [System.Array]) {
        $health = $health[0]
      }
      if ($health.Watcher -notlike "Running*") {
        Write-Host "Watcher health check failed: $($health.Watcher)" -ForegroundColor Red
        if ($null -ne $watcherPid -and (Get-Process -Id $watcherPid -ErrorAction SilentlyContinue)) {
          Stop-Process -Id $watcherPid -Force
        }
        if (Test-Path $pidFile) {
          Remove-Item $pidFile -ErrorAction SilentlyContinue
        }
        exit 1
      }
    }
}

# 3. Start the Monitoring Dashboard
# This allows you to view the Database and Real-time stats
# Dependencies already checked above, so proceed directly to starting dashboard
if (-not $dashboard) {
  Write-Host "Starting KB Monitoring Dashboard..." -ForegroundColor Green
  $StreamlitExe = Join-Path $RepoRoot ".venv\Scripts\streamlit.exe"
  if (-not (Test-Path $StreamlitExe)) {
      $StreamlitExe = "streamlit"
  }
  Start-Process -FilePath $StreamlitExe `
      -ArgumentList "run dashboard_kb_monitoring.py" `
      -WorkingDirectory $RepoRoot `
      -WindowStyle Normal
  Write-Host "Dashboard starting in browser..." -ForegroundColor Gray
} else {
  Write-Host "Dashboard already running." -ForegroundColor Gray
}

Write-Host ""
Write-Host "All systems operational." -ForegroundColor Cyan
Write-Host "1. Drop files into '02_data' to process." -ForegroundColor White
Write-Host "2. Check the Streamlit window to see them enter the Database." -ForegroundColor White


```


Fixing all incorrect path references:


```powershell
param(
  [string]$RepoRoot = "$PSScriptRoot\.."
)

Set-Location $RepoRoot
$env:PYTHONUNBUFFERED = "1"

Write-Host "Initializing Enterprise RAG Pipeline..." -ForegroundColor Cyan

# Check for OneDrive path
$oneDriveRoot = Join-Path $env:OneDriveCommercial "KB_Shared"
if (-not (Test-Path $oneDriveRoot)) {
  Write-Host "OneDrive KB_Shared missing." -ForegroundColor Red
  exit 1
}

# Check if watcher is already running
$pidFile = Join-Path $RepoRoot "05_logs\runtime\watcher_pid.txt"
$skipWatcherStart = $false
if (Test-Path $pidFile) {
  $watcherPid = Get-Content $pidFile | Select-Object -First 1
  if ($watcherPid -and (Get-Process -Id $watcherPid -ErrorAction SilentlyContinue)) {
    Write-Host "Watcher already running. PID=$watcherPid" -ForegroundColor Yellow
    Write-Host "Starting Dashboard only..." -ForegroundColor Green
    $skipWatcherStart = $true
  }
}

# Check if dashboard is already running
$dashboard = Get-WmiObject Win32_Process -ErrorAction SilentlyContinue | Where-Object { $_.CommandLine -like "*streamlit run dashboard_kb_monitoring.py*" }
if ($dashboard) {
  Write-Host "Dashboard already running. PID=$($dashboard.ProcessId)" -ForegroundColor Yellow
}

# 1. Activate the Virtual Environment (if available)
$VenvPath = Join-Path $RepoRoot ".venv\Scripts\Activate.ps1"
$PythonExe = "python"
$PipExe = "pip"
if (Test-Path $VenvPath) {
    . $VenvPath
    $PythonExe = Join-Path $RepoRoot ".venv\Scripts\python.exe"
    $PipExe = Join-Path $RepoRoot ".venv\Scripts\pip.exe"
    Write-Host "Virtual environment activated." -ForegroundColor Gray
} else {
    Write-Warning "Virtual environment not found at $VenvPath. Attempting to run with system Python..."
}

# Check and install missing dependencies (especially plotly for dashboard)
Write-Host "Checking dependencies..." -ForegroundColor Gray
$requirementsFile = Join-Path $RepoRoot "06_config\requirements\requirements.txt"
if (Test-Path $requirementsFile) {
    try {
        # Quick check if plotly is installed (required for dashboard)
        $plotlyCheck = & $PythonExe -c "import plotly" 2>&1
        if ($LASTEXITCODE -ne 0) {
            Write-Host "Installing missing dependencies (plotly required for dashboard)..." -ForegroundColor Yellow
            & $PipExe install -q -r $requirementsFile
            if ($LASTEXITCODE -eq 0) {
                Write-Host "Dependencies installed successfully." -ForegroundColor Green
            } else {
                Write-Warning "Some dependencies may have failed to install. Dashboard may not work correctly."
            }
        } else {
            Write-Host "Dependencies check passed." -ForegroundColor Gray
        }
    } catch {
        Write-Warning "Could not verify dependencies. Dashboard may fail if plotly is missing."
    }
} else {
    Write-Warning "06_config\\requirements\\requirements\.txt not found. Dashboard may fail if dependencies are missing."
}

# 2. Start the Watcher (The Core Processor) - Skip if already running
# This handles File Splitting AND Automatic KB Insertion
if (-not $skipWatcherStart) {
    Write-Host "Starting Watcher Service (Splitter + KB Auto-Insert)..." -ForegroundColor Green
    $WatcherProcess = Start-Process -FilePath $PythonExe `
        -ArgumentList "watcher_splitter.py" `
        -WorkingDirectory $RepoRoot `
        -WindowStyle Minimized `
        -PassThru

    Start-Sleep -Seconds 2
    $watcherPid = $WatcherProcess.Id

    if ($null -ne $watcherPid -and (Get-Process -Id $watcherPid -ErrorAction SilentlyContinue)) {
      $watcherPid | Out-File -Encoding ascii -FilePath $pidFile -Force
      Write-Host "Watcher started. PID=$watcherPid" -ForegroundColor Green
    } else {
      Write-Host "Watcher process not found after start attempt." -ForegroundColor Red
      exit 1
    }

    # Optional: Health check (if KB-Health.ps1 exists)
    if (Test-Path "$RepoRoot\scripts\KB-Health.ps1") {
      $health = & "$RepoRoot\scripts\KB-Health.ps1" -RepoRoot $RepoRoot -OD $env:OneDriveCommercial
      if ($health -is [System.Array]) {
        $health = $health[0]
      }
      if ($health.Watcher -notlike "Running*") {
        Write-Host "Watcher health check failed: $($health.Watcher)" -ForegroundColor Red
        if ($null -ne $watcherPid -and (Get-Process -Id $watcherPid -ErrorAction SilentlyContinue)) {
          Stop-Process -Id $watcherPid -Force
        }
        if (Test-Path $pidFile) {
          Remove-Item $pidFile -ErrorAction SilentlyContinue
        }
        exit 1
      }
    }
}

# 3. Start the Monitoring Dashboard
# This allows you to view the Database and Real-time stats
# Dependencies already checked above, so proceed directly to starting dashboard
if (-not $dashboard) {
  Write-Host "Starting KB Monitoring Dashboard..." -ForegroundColor Green
  $StreamlitExe = Join-Path $RepoRoot ".venv\Scripts\streamlit.exe"
  if (-not (Test-Path $StreamlitExe)) {
      $StreamlitExe = "streamlit"
  }
  Start-Process -FilePath $StreamlitExe `
      -ArgumentList "run dashboard_kb_monitoring.py" `
      -WorkingDirectory $RepoRoot `
      -WindowStyle Normal
  Write-Host "Dashboard starting in browser..." -ForegroundColor Gray
} else {
  Write-Host "Dashboard already running." -ForegroundColor Gray
}

Write-Host ""
Write-Host "All systems operational." -ForegroundColor Cyan
Write-Host "1. Drop files into '02_data' to process." -ForegroundColor White
Write-Host "2. Check the Streamlit window to see them enter the Database." -ForegroundColor White


```

```powershell
param(
  [string]$RepoRoot = "$PSScriptRoot\.."
)

Set-Location $RepoRoot
$env:PYTHONUNBUFFERED = "1"

Write-Host "Initializing Enterprise RAG Pipeline..." -ForegroundColor Cyan

# Check for OneDrive path
$oneDriveRoot = Join-Path $env:OneDriveCommercial "KB_Shared"
if (-not (Test-Path $oneDriveRoot)) {
  Write-Host "OneDrive KB_Shared missing." -ForegroundColor Red
  exit 1
}

# Check if watcher is already running
$pidFile = Join-Path $RepoRoot "05_logs\runtime\watcher_pid.txt"
$skipWatcherStart = $false
if (Test-Path $pidFile) {
  $watcherPid = Get-Content $pidFile | Select-Object -First 1
  if ($watcherPid -and (Get-Process -Id $watcherPid -ErrorAction SilentlyContinue)) {
    Write-Host "Watcher already running. PID=$watcherPid" -ForegroundColor Yellow
    Write-Host "Starting Dashboard only..." -ForegroundColor Green
    $skipWatcherStart = $true
  }
}

# Check if dashboard is already running
$dashboard = Get-WmiObject Win32_Process -ErrorAction SilentlyContinue | Where-Object { $_.CommandLine -like "*streamlit run dashboard_kb_monitoring.py*" }
if ($dashboard) {
  Write-Host "Dashboard already running. PID=$($dashboard.ProcessId)" -ForegroundColor Yellow
}

# 1. Activate the Virtual Environment (if available)
$VenvPath = Join-Path $RepoRoot ".venv\Scripts\Activate.ps1"
$PythonExe = "python"
$PipExe = "pip"
if (Test-Path $VenvPath) {
    . $VenvPath
    $PythonExe = Join-Path $RepoRoot ".venv\Scripts\python.exe"
    $PipExe = Join-Path $RepoRoot ".venv\Scripts\pip.exe"
    Write-Host "Virtual environment activated." -ForegroundColor Gray
} else {
    Write-Warning "Virtual environment not found at $VenvPath. Attempting to run with system Python..."
}

# Check and install missing dependencies (especially plotly for dashboard)
Write-Host "Checking dependencies..." -ForegroundColor Gray
$requirementsFile = Join-Path $RepoRoot "06_config\requirements\requirements.txt"
if (Test-Path $requirementsFile) {
    try {
        # Quick check if plotly is installed (required for dashboard)
        $plotlyCheck = & $PythonExe -c "import plotly" 2>&1
        if ($LASTEXITCODE -ne 0) {
            Write-Host "Installing missing dependencies (plotly required for dashboard)..." -ForegroundColor Yellow
            & $PipExe install -q -r $requirementsFile
            if ($LASTEXITCODE -eq 0) {
                Write-Host "Dependencies installed successfully." -ForegroundColor Green
            } else {
                Write-Warning "Some dependencies may have failed to install. Dashboard may not work correctly."
            }
        } else {
            Write-Host "Dependencies check passed." -ForegroundColor Gray
        }
    } catch {
        Write-Warning "Could not verify dependencies. Dashboard may fail if plotly is missing."
    }
} else {
    Write-Warning "06_config\requirements\requirements.txt not found. Dashboard may fail if dependencies are missing."
}

# 2. Start the Watcher (The Core Processor) - Skip if already running
# This handles File Splitting AND Automatic KB Insertion
if (-not $skipWatcherStart) {
    Write-Host "Starting Watcher Service (Splitter + KB Auto-Insert)..." -ForegroundColor Green
    $WatcherProcess = Start-Process -FilePath $PythonExe `
        -ArgumentList "watcher_splitter.py" `
        -WorkingDirectory $RepoRoot `
        -WindowStyle Minimized `
        -PassThru

    Start-Sleep -Seconds 2
    $watcherPid = $WatcherProcess.Id

    if ($null -ne $watcherPid -and (Get-Process -Id $watcherPid -ErrorAction SilentlyContinue)) {
      $watcherPid | Out-File -Encoding ascii -FilePath $pidFile -Force
      Write-Host "Watcher started. PID=$watcherPid" -ForegroundColor Green
    } else {
      Write-Host "Watcher process not found after start attempt." -ForegroundColor Red
      exit 1
    }

    # Optional: Health check (if KB-Health.ps1 exists)
    if (Test-Path "$RepoRoot\scripts\KB-Health.ps1") {
      $health = & "$RepoRoot\scripts\KB-Health.ps1" -RepoRoot $RepoRoot -OD $env:OneDriveCommercial
      if ($health -is [System.Array]) {
        $health = $health[0]
      }
      if ($health.Watcher -notlike "Running*") {
        Write-Host "Watcher health check failed: $($health.Watcher)" -ForegroundColor Red
        if ($null -ne $watcherPid -and (Get-Process -Id $watcherPid -ErrorAction SilentlyContinue)) {
          Stop-Process -Id $watcherPid -Force
        }
        if (Test-Path $pidFile) {
          Remove-Item $pidFile -ErrorAction SilentlyContinue
        }
        exit 1
      }
    }
}

# 3. Start the Monitoring Dashboard
# This allows you to view the Database and Real-time stats
# Dependencies already checked above, so proceed directly to starting dashboard
if (-not $dashboard) {
  Write-Host "Starting KB Monitoring Dashboard..." -ForegroundColor Green
  $StreamlitExe = Join-Path $RepoRoot ".venv\Scripts\streamlit.exe"
  if (-not (Test-Path $StreamlitExe)) {
      $StreamlitExe = "streamlit"
  }
  Start-Process -FilePath $StreamlitExe `
      -ArgumentList "run dashboard_kb_monitoring.py" `
      -WorkingDirectory $RepoRoot `
      -WindowStyle Normal
  Write-Host "Dashboard starting in browser..." -ForegroundColor Gray
} else {
  Write-Host "Dashboard already running." -ForegroundColor Gray
}

Write-Host ""
Write-Host "All systems operational." -ForegroundColor Cyan
Write-Host "1. Drop files into '02_data' to process." -ForegroundColor White
Write-Host "2. Check the Streamlit window to see them enter the Database." -ForegroundColor White


```

```powershell
param(
  [string]$RepoRoot = "$PSScriptRoot\.."
)

Write-Host "Stopping Enterprise RAG Pipeline..." -ForegroundColor Yellow

# 1. Stop the Watcher (Python)
# First try using PID file
$pidFile = Join-Path $RepoRoot "05_logs\runtime\watcher_pid.txt"
$watcherStopped = $false

if (Test-Path $pidFile) {
  $watcherPid = Get-Content $pidFile | Select-Object -First 1
  if ($watcherPid -and (Get-Process -Id $watcherPid -ErrorAction SilentlyContinue)) {
    try {
      Stop-Process -Id $watcherPid -Force -ErrorAction Stop
      Start-Sleep -Milliseconds 500
      if (-not (Get-Process -Id $watcherPid -ErrorAction SilentlyContinue)) {
        Write-Host "Watcher Service Stopped (PID=$watcherPid)." -ForegroundColor Red
        $watcherStopped = $true
        Remove-Item $pidFile -ErrorAction SilentlyContinue
      }
    } catch {
      Write-Warning "Failed to stop watcher via PID file: $_"
    }
  } else {
    # PID file exists but process is gone - clean up stale file
    Remove-Item $pidFile -ErrorAction SilentlyContinue
  }
}

# Also check for any python processes running watcher_splitter.py (fallback)
if (-not $watcherStopped) {
  $watcher = Get-WmiObject Win32_Process -ErrorAction SilentlyContinue | Where-Object { $_.CommandLine -like "*watcher_splitter.py*" }
  
  if ($watcher) {
    foreach ($proc in $watcher) {
      try {
        Stop-Process -Id $proc.ProcessId -Force -ErrorAction Stop
        Start-Sleep -Milliseconds 500
        if (-not (Get-Process -Id $proc.ProcessId -ErrorAction SilentlyContinue)) {
          Write-Host "Watcher Service Stopped (PID=$($proc.ProcessId))." -ForegroundColor Red
          $watcherStopped = $true
        }
      } catch {
        Write-Warning "Failed to stop watcher process $($proc.ProcessId): $_"
      }
    }
  }
  
  if (-not $watcherStopped) {
    Write-Host "Watcher Service was not running." -ForegroundColor Gray
  }
}

# 2. Stop the Dashboard (Streamlit)
# Streamlit runs as a python process, usually visible in command line
# Note: Streamlit may spawn child processes, but the main process should handle cleanup
$dashboard = Get-WmiObject Win32_Process -ErrorAction SilentlyContinue | Where-Object { $_.CommandLine -like "*streamlit run dashboard_kb_monitoring.py*" }
$dashboardStopped = $false

if ($dashboard) {
  foreach ($proc in $dashboard) {
    try {
      Stop-Process -Id $proc.ProcessId -Force -ErrorAction Stop
      Start-Sleep -Milliseconds 500
      if (-not (Get-Process -Id $proc.ProcessId -ErrorAction SilentlyContinue)) {
        Write-Host "Monitoring Dashboard Stopped (PID=$($proc.ProcessId))." -ForegroundColor Red
        $dashboardStopped = $true
      }
    } catch {
      Write-Warning "Failed to stop dashboard process $($proc.ProcessId): $_"
    }
  }
  
  if (-not $dashboardStopped) {
    Write-Host "Dashboard was not running or could not be stopped." -ForegroundColor Gray
  }
} else {
  Write-Host "Dashboard was not running." -ForegroundColor Gray
}

Write-Host ""
Write-Host "Pipeline Shutdown Complete." -ForegroundColor Cyan


```

```powershell
param(
  [string]$RepoRoot = "$PSScriptRoot\..",
  [string]$OD = $env:OneDriveCommercial
)

$watch = Join-Path $OD "KB_Shared\02_data"
$arc   = Join-Path $OD "KB_Shared\03_archive"
$out   = Join-Path $OD "KB_Shared\04_output"
$pidFile = Join-Path $RepoRoot "05_logs\runtime\watcher_pid.txt"

$watcher = if (Test-Path $pidFile) {
  $watcherPid = Get-Content $pidFile | Select-Object -First 1
  if ($watcherPid -and (Get-Process -Id $watcherPid -ErrorAction SilentlyContinue)) {
    "Running (PID=$watcherPid)"
  } else {
    "Not running"
  }
} else {
  "Not running"
}

$chromadb = Test-Path (Join-Path $RepoRoot "chroma_db")
$offline  = (Test-Path $watch) -and (Test-Path $arc) -and (Test-Path $out)

[pscustomobject]@{
  Watcher     = $watcher
  OneDriveOK  = $offline
  ChromaDB    = $chromadb
  WatchFolder = $watch
  Archive     = $arc
  Output      = $out
}


```


Restarting the watcher with the corrected paths:



Watcher is running. Fixing the dashboard startup issue:


```powershell
param(
  [string]$RepoRoot = "$PSScriptRoot\.."
)

Set-Location $RepoRoot
$env:PYTHONUNBUFFERED = "1"

Write-Host "Initializing Enterprise RAG Pipeline (Background Mode)..." -ForegroundColor Cyan

# Check for OneDrive path
$oneDriveRoot = Join-Path $env:OneDriveCommercial "KB_Shared"
if (-not (Test-Path $oneDriveRoot)) {
  Write-Host "OneDrive KB_Shared missing." -ForegroundColor Red
  exit 1
}

# Ensure logs directory exists
$logsDir = Join-Path $RepoRoot "05_logs"
if (-not (Test-Path $logsDir)) {
  New-Item -ItemType Directory -Path $logsDir -Force | Out-Null
}

# Check if watcher is already running
$pidFile = Join-Path $RepoRoot "05_logs\runtime\watcher_pid.txt"
$skipWatcherStart = $false
if (Test-Path $pidFile) {
  $watcherPid = Get-Content $pidFile | Select-Object -First 1
  if ($watcherPid -and (Get-Process -Id $watcherPid -ErrorAction SilentlyContinue)) {
    Write-Host "Watcher already running. PID=$watcherPid" -ForegroundColor Yellow
    Write-Host "Starting Dashboard only..." -ForegroundColor Green
    $skipWatcherStart = $true
  }
}

# Check if dashboard is already running
$dashboard = Get-WmiObject Win32_Process -ErrorAction SilentlyContinue | Where-Object { $_.CommandLine -like "*streamlit run dashboard_kb_monitoring.py*" }
if ($dashboard) {
  Write-Host "Dashboard already running. PID=$($dashboard.ProcessId)" -ForegroundColor Yellow
}

# 1. Activate the Virtual Environment (if available)
$VenvPath = Join-Path $RepoRoot ".venv\Scripts\Activate.ps1"
$PythonExe = "python"
$PythonwExe = "pythonw"
$PipExe = "pip"
if (Test-Path $VenvPath) {
    . $VenvPath
    $PythonExe = Join-Path $RepoRoot ".venv\Scripts\python.exe"
    $PythonwExe = Join-Path $RepoRoot ".venv\Scripts\pythonw.exe"
    $PipExe = Join-Path $RepoRoot ".venv\Scripts\pip.exe"
    Write-Host "Virtual environment activated." -ForegroundColor Gray
} else {
    Write-Warning "Virtual environment not found at $VenvPath. Attempting to run with system Python..."
}

# Check and install missing dependencies (especially plotly for dashboard)
Write-Host "Checking dependencies..." -ForegroundColor Gray
$requirementsFile = Join-Path $RepoRoot "06_config\requirements\requirements.txt"
if (Test-Path $requirementsFile) {
    try {
        # Quick check if plotly is installed (required for dashboard)
        $plotlyCheck = & $PythonExe -c "import plotly" 2>&1
        if ($LASTEXITCODE -ne 0) {
            Write-Host "Installing missing dependencies (plotly required for dashboard)..." -ForegroundColor Yellow
            & $PipExe install -q -r $requirementsFile
            if ($LASTEXITCODE -eq 0) {
                Write-Host "Dependencies installed successfully." -ForegroundColor Green
            } else {
                Write-Warning "Some dependencies may have failed to install. Dashboard may not work correctly."
            }
        } else {
            Write-Host "Dependencies check passed." -ForegroundColor Gray
        }
    } catch {
        Write-Warning "Could not verify dependencies. Dashboard may fail if plotly is missing."
    }
} else {
    Write-Warning "06_config\requirements\requirements.txt not found. Dashboard may fail if dependencies are missing."
}

# 2. Start the Watcher (The Core Processor) - Skip if already running
# This handles File Splitting AND Automatic KB Insertion
# Using pythonw.exe to run without console window
if (-not $skipWatcherStart) {
    Write-Host "Starting Watcher Service (Splitter + KB Auto-Insert) in background..." -ForegroundColor Green
    
    # Use pythonw.exe if available, otherwise fall back to python.exe with hidden window
    $watcherLogFile = Join-Path $logsDir "watcher_background.log"
    if (Test-Path $PythonwExe) {
        # pythonw.exe runs without console window
        $WatcherProcess = Start-Process -FilePath $PythonwExe `
            -ArgumentList "watcher_splitter.py" `
            -WorkingDirectory $RepoRoot `
            -WindowStyle Hidden `
            -PassThru
    } else {
        # Fallback: use python.exe but redirect output and hide window
        $WatcherProcess = Start-Process -FilePath $PythonExe `
            -ArgumentList "watcher_splitter.py" `
            -WorkingDirectory $RepoRoot `
            -WindowStyle Hidden `
            -RedirectStandardOutput $watcherLogFile `
            -RedirectStandardError $watcherLogFile `
            -PassThru
    }

    Start-Sleep -Seconds 2
    $watcherPid = $WatcherProcess.Id

    if ($null -ne $watcherPid -and (Get-Process -Id $watcherPid -ErrorAction SilentlyContinue)) {
      $watcherPid | Out-File -Encoding ascii -FilePath $pidFile -Force
      Write-Host "Watcher started in background. PID=$watcherPid" -ForegroundColor Green
      Write-Host "Logs: $watcherLogFile" -ForegroundColor Gray
    } else {
      Write-Host "Watcher process not found after start attempt." -ForegroundColor Red
      exit 1
    }

    # Optional: Health check (if KB-Health.ps1 exists)
    if (Test-Path "$RepoRoot\scripts\KB-Health.ps1") {
      $health = & "$RepoRoot\scripts\KB-Health.ps1" -RepoRoot $RepoRoot -OD $env:OneDriveCommercial
      if ($health -is [System.Array]) {
        $health = $health[0]
      }
      if ($health.Watcher -notlike "Running*") {
        Write-Host "Watcher health check failed: $($health.Watcher)" -ForegroundColor Red
        if ($null -ne $watcherPid -and (Get-Process -Id $watcherPid -ErrorAction SilentlyContinue)) {
          Stop-Process -Id $watcherPid -Force
        }
        if (Test-Path $pidFile) {
          Remove-Item $pidFile -ErrorAction SilentlyContinue
        }
        exit 1
      }
    }
}

# 3. Start the Monitoring Dashboard
# This allows you to view the Database and Real-time stats
# Running in hidden mode - access via browser at http://localhost:8501
if (-not $dashboard) {
  Write-Host "Starting KB Monitoring Dashboard in background..." -ForegroundColor Green
  $StreamlitExe = Join-Path $RepoRoot ".venv\Scripts\streamlit.exe"
  if (-not (Test-Path $StreamlitExe)) {
      $StreamlitExe = "streamlit"
  }
  
  $dashboardLogFile = Join-Path $logsDir "dashboard_background.log"
  $dashboardErrorLogFile = Join-Path $logsDir "dashboard_background_error.log"
  Start-Process -FilePath $StreamlitExe `
      -ArgumentList "run dashboard_kb_monitoring.py" `
      -WorkingDirectory $RepoRoot `
      -WindowStyle Hidden `
      -RedirectStandardOutput $dashboardLogFile `
      -RedirectStandardError $dashboardErrorLogFile `
      -PassThru | Out-Null
  
  Write-Host "Dashboard starting in background..." -ForegroundColor Gray
  Write-Host "Access dashboard at: http://localhost:8501" -ForegroundColor Cyan
  Write-Host "Logs: $dashboardLogFile" -ForegroundColor Gray
} else {
  Write-Host "Dashboard already running." -ForegroundColor Gray
}

Write-Host ""
Write-Host "All systems operational (running in background)." -ForegroundColor Cyan
Write-Host "1. Drop files into '02_data' to process." -ForegroundColor White
Write-Host "2. Access dashboard at: http://localhost:8501" -ForegroundColor White
Write-Host "3. Check logs in: $logsDir" -ForegroundColor White
Write-Host ""
Write-Host "To stop services, run: scripts\Stop-Watcher.ps1" -ForegroundColor Yellow


```


Checking watcher status:



The watcher process isn't running. Checking logs and restarting:



Verifying the watcher is running:



## Summary

1. Stopped the watcher — stopped successfully
2. Moved files:
   - `requirements.txt`, `requirements_api_gui.txt`, `requirements_rag.txt` → `06_config/requirements/`
   - `watcher_pid.txt` → `05_logs/runtime/` (will be created when watcher runs)
   - `watcher_test_output.txt` → `05_logs/`
3. Updated script references — fixed path issues in:
   - `Start-Watcher.ps1`
   - `Start-Watcher-Background.ps1`
   - `Stop-Watcher.ps1`
   - `KB-Health.ps1`
4. Restarted watcher — watcher started with PID 20092

The watcher is running in the background using the new file locations. The PID file is at `05_logs/runtime/watcher_pid.txt`, and all requirements files are in `06_config/requirements/`.

The dashboard also started (fixed the log redirection issue). You can access it at http://localhost:8501.

All files have been moved and the watcher is operational.

---

**User**

I'm preparing to export this chat. Please generate a descriptive filename that summarizes the main topic or task of this conversation.

Requirements:
• 4-8 words
• Title Case (capitalize major words)
• Replace spaces with underscores
• Include .md extension
• No dates or special characters

Output only the filename, nothing else.

After export, I'll process it using: scripts\quick_process_chatlog.bat

---

**Cursor**


Directory_Cleanup_And_File_Organization.md

