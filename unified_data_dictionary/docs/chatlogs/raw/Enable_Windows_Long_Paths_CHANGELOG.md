# Enable Windows Long Path Support - Changelog

## 2026-01-XX - Fix_OneDrive_Long_Path_Issue.ps1 -Repair and Docs

### Added
- **`Fix_OneDrive_Long_Path_Issue_README.md`**: Full documentation for the path-too-long repair script
  - When to use, parameters (`-Repair`, `-RootPath`, `-WhatIf`), run examples, troubleshooting

- **`Fix_OneDrive_Long_Path_Issue.ps1 -Repair`**: Automatic path shortening for OneDrive "path is too long" errors
  - Root: `Standards_Backup_20260116_181122` → `SB_160116`
  - `unified_data_dictionary` → `udd`; `Standards` → `Std`
  - Long chunk folders (e.g. `2025_12_17_22_24_14_...`) → `c_YYYYMMDD_HHMM`; matching files shortened
  - Continues from `SB_160116` if root already renamed; `-RootPath` for custom root
  - Move-Item fallback and Access denied guidance (exit OneDrive, close Cursor/Explorer)

### Updated
- **Enable_Windows_Long_Paths_README.md**: Files list; OneDrive troubleshooting step 3 now describes `-Repair` and points to `Fix_OneDrive_Long_Path_Issue_README.md`; removed `Check_Path_Length.ps1` from Files; Related Files updated.
- **Enable_Windows_Long_Paths_Instructions.md**: OneDrive troubleshooting steps 3–5 replaced with `-Repair` workflow and pointer to the new README.
- **Fix_OneDrive_Long_Path_Sync_Issues.md**: Quick reference block at top for "path is too long" and `-Repair`.
- **OneDrive_Sync_Error_Troubleshooting_Fix.md**: "Path too long" subsection with `-Repair` and README pointer.

## 2026-01-17 - OneDrive Troubleshooting Scripts Added

### Added
- **`Fix_OneDrive_Long_Path_Issue.ps1`**: New troubleshooting script for OneDrive-specific long path issues
  - Checks Windows long path registry setting
  - Verifies OneDrive process status
  - Tests actual file path lengths
  - Provides specific recommendations based on the situation
  - Includes multiple solution options (restart OneDrive, restart computer, move files, etc.)

- **`Check_Path_Length.ps1`**: Utility script to check file path lengths
  - Analyzes specific file paths
  - Shows path length in characters
  - Compares against common limits (260, 400 characters)
  - Provides path breakdown (base path vs. relative path)

### Improved
- **Documentation**: Updated README and Instructions to include OneDrive troubleshooting guidance
  - Added information about OneDrive needing restart after enabling long paths
  - Documented that even paths under 260 characters may cause OneDrive errors
  - Added references to new troubleshooting scripts

### Verified
- OneDrive may show errors even for paths under 260 characters if not restarted
- Restarting OneDrive is often necessary after enabling Windows long path support
- Windows long paths can be working correctly while OneDrive still has issues

## 2026-01-17 - Functionality Testing and Enhanced Verification

### Added
- **`Test-LongPathSupport` Function**: New function that actually tests if long paths are working
  - Creates a test path over 280 characters
  - Attempts to create and access the path
  - Returns true if successful, false if path too long error, null for other errors
  - Provides real-world verification beyond just registry checking

- **Enhanced Status Reporting**: Script now provides detailed feedback showing:
  - Registry setting status (Enabled/Disabled)
  - Functionality test results (Passed/Failed/Inconclusive)
  - Clear distinction between registry enabled vs. actually working

- **OneDrive-Specific Troubleshooting**: Added guidance for OneDrive issues:
  - Instructions to restart OneDrive after enabling
  - Notes about OneDrive's own path length limitations
  - Alternative solutions (shorter paths, junctions, etc.)

### Changed
- **Verification Process**: Script now tests both registry setting AND actual functionality
  - When registry is already enabled, automatically runs functionality test
  - When enabling registry, runs test to verify it's working (may need restart)
  - Provides clear feedback about whether restart is needed

- **User Feedback**: Enhanced output messages to clearly show:
  - Whether registry is enabled
  - Whether functionality test passed/failed
  - Specific recommendations based on test results

### Improved
- **Troubleshooting Guidance**: Better guidance when OneDrive still has issues
  - Explains that OneDrive may need restart even if Windows long paths work
  - Notes that some OneDrive versions have their own limitations
  - Provides step-by-step troubleshooting approach

### Verified
- Script successfully tests long path functionality on Windows 10 Pro Build 26200
- Test path creation and access works correctly when long paths are enabled
- Script correctly identifies when restart is needed vs. when everything is working

## 2026-01-17 - Scheduling Support Added

### Added
- **`-NonInteractive` Parameter**: New parameter to `Enable_Windows_Long_Paths.ps1` to enable non-interactive execution
  - Skips the "Continue anyway?" prompt when Windows version check fails
  - Prevents scheduled tasks from hanging on user input prompts
  - Used in conjunction with `-SkipRestartPrompt` for scheduled execution

- **`Schedule_Enable_Long_Paths.ps1`**: New script to automate scheduled task creation
  - Creates Windows Task Scheduler task named "Enable_Windows_Long_Paths_Daily"
  - Configures task to run daily at 2:00 AM
  - Sets up task to run with Administrator privileges
  - Passes `-SkipRestartPrompt -NonInteractive` parameters automatically
  - Includes verification and status checking

### Changed
- **Windows Version Check**: Modified to respect `-NonInteractive` parameter
  - In non-interactive mode, automatically continues if Windows version check fails
  - Prevents hanging on user prompts during scheduled execution

## 2026-01-17 - Bug Fix

### Fixed
- **Registry Backup Function**: Fixed conflicting PowerShell parameters in `Start-Process` command
  - **Issue**: Script failed with error: "Parameters '-NoNewWindow' and '-WindowStyle' cannot be specified at the same time"
  - **Fix**: Removed `-NoNewWindow` parameter, kept only `-WindowStyle Hidden` on line 55
  - **Location**: `Backup-RegistryKey` function in `Enable_Windows_Long_Paths.ps1`
  - **Tested On**: ssocc_desk (Windows 10 Pro Build 26200)

### Changed
- **Registry Backup Method**: Updated to use `cmd.exe` with proper quoting to handle paths containing spaces
  - Converts PowerShell registry path format (`HKLM:\...`) to format expected by `reg export` (`HKEY_LOCAL_MACHINE\...`)
  - Uses `cmd.exe /c` to execute `reg export` with proper argument handling

### Removed
- Unused variable `$osVersion` from `Test-WindowsVersion` function (line 28)

### Verified
- Script successfully backs up registry key even when paths contain spaces
- Script correctly detects when long paths are already enabled
- Exit codes are properly handled

## 2026-01-16 - Initial Creation

### Added
- Initial PowerShell script to enable Windows Long Path support
- Administrator privilege checking
- Windows version compatibility verification
- Registry backup functionality
- Verification of registry changes
- Optional restart prompt

### Documentation
- Created `Enable_Windows_Long_Paths_Instructions.md` with detailed instructions
- Created `Enable_Windows_Long_Path_Support.md` (chat export)

## Notes

- **Development Machine**: ssocc_desk
- **Scheduled Execution**: Can be set up to run daily at 2:00 AM via Windows Task Scheduler using `Schedule_Enable_Long_Paths.ps1`
- **OneDrive Sync**: This OneDrive folder is shared between ssocc_laptop and ssocc_desk
- **Purpose**: Prevent OneDrive sync failures caused by long file/folder paths
- **Scheduling Setup**: Run `Schedule_Enable_Long_Paths.ps1` as Administrator on each machine where scheduled execution is desired
