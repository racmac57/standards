# Prompt for Claude Code - Pre-Flight Checklist & Migration Review

**Copy and paste this entire prompt to Claude Code**

---

## 🚨 YOUR FIRST TASK: Execute Pre-Flight Checklist

**Before reviewing ANY migration plans, you MUST complete the pre-flight checklist.**

### Step 1: Read Critical Documents
1. **`docs/merge/PRE-FLIGHT-CHECKLIST.md`** - Complete ALL checklist items
2. **`docs/merge/CRITICAL-BLIND-SPOTS.md`** - Understand risks and assumptions

### Step 2: Execute Automated Checks

You can and should execute these PowerShell checks automatically:

```powershell
# 1. Test if UDD currently works
cd "C:\Users\carucci_r\OneDrive - City of Hackensack\09_Reference\Standards\unified_data_dictionary"
pip install -e .
python -c "import src.cli; print('✓ Import works')"
udd --help
pytest

# 2. Check for external dependencies
Get-ChildItem "C:\Users\carucci_r\OneDrive - City of Hackensack" -Recurse -Filter "*.pbix" -ErrorAction SilentlyContinue |
    Select-String "unified_data_dictionary|Standards\\schemas|Standards\\mappings"

Get-ChildItem "C:\Users\carucci_r\OneDrive - City of Hackensack\02_ETL_Scripts" -Recurse -Filter "*.py" -ErrorAction SilentlyContinue |
    Select-String "unified_data_dictionary" -List

Get-ScheduledTask | Where-Object {$_.Actions.Execute -like "*unified_data_dictionary*"}

# 3. Check git status
cd "C:\Users\carucci_r\OneDrive - City of Hackensack\09_Reference\Standards"
git status
git log --oneline -5
git branch

# 4. Check OneDrive sync status
Get-ChildItem "C:\Users\carucci_r\OneDrive - City of Hackensack\09_Reference\Standards\unified_data_dictionary" -Recurse -File |
    Where-Object {$_.Attributes -match "ReparsePoint"} |
    Select-Object FullName

# 5. Check for long paths
Get-ChildItem "unified_data_dictionary" -Recurse -File |
    Where-Object { $_.FullName.Length -gt 200 } |
    Select-Object FullName, @{N='Length';E={$_.FullName.Length}}

# 6. Document current state
$fileCount = (Get-ChildItem "unified_data_dictionary" -Recurse -File).Count
Write-Host "Files in UDD: $fileCount"

Get-ChildItem "unified_data_dictionary" -Directory -Recurse -Name | 
    Out-File "docs\merge\pre_migration_structure.txt"
```

### Step 3: Create Backup

**You MUST create a backup before proceeding:**

```powershell
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$backupPath = "C:\Temp\Standards_Backup_$timestamp"

Copy-Item "C:\Users\carucci_r\OneDrive - City of Hackensack\09_Reference\Standards" `
          $backupPath -Recurse -Force

Write-Host "Backup created at: $backupPath"
```

### Step 4: Report Pre-Flight Results

**Create a report file documenting all findings:**

```
docs/merge/PRE-FLIGHT-RESULTS.md
```

Include:
- ✅/❌ for each checklist item
- Results of all automated checks
- Any external dependencies found
- Git status summary
- Backup location
- GO/NO-GO recommendation

**DO NOT proceed to migration planning until pre-flight is complete and approved.**

---

## Context

I need you to review a directory migration plan for the Hackensack Police Department's Standards repository. This involves moving the `unified_data_dictionary` (UDD) Python project into a cleaner structure while maintaining functionality.

## Background

The Standards repository currently has a nested structure where the UDD tool (a Python package for schema extraction and data dictionary generation) is a subdirectory. We want to reorganize this for clarity and to prepare for adding NIBRS content.

A Hybrid Migration Plan has been created that:
1. Moves UDD Python package to `tools/unified_data_dictionary/` (keeps it functional)
2. Extracts reference data (schemas, mappings, docs) to Standards root
3. Organizes loose scripts into proper directories

## Your Task

Please review the migration plan and provide:
1. **Risk Assessment** - What could go wrong?
2. **Path Dependency Analysis** - Will anything break?
3. **Recommendations** - How to improve the plan?
4. **Missing Considerations** - What did we overlook?
5. **Alternative Approaches** - Are there better ways?

---

## Files to Review

### Priority 1: The Migration Plan
Please read these files first:

1. **`docs/merge/05-UDD-Hybrid-Migration-REVISED.md`** 
   - The actual migration plan with PowerShell script
   - **THIS IS THE CORE DOCUMENT TO REVIEW**

2. **`docs/merge/APPROACH-COMPARISON.md`**
   - Why we chose hybrid over full flattening

3. **`docs/merge/00-QuickStart.md`**
   - Current merge status

### Priority 2: Current Structure
Please review these to understand current state:

4. **`README.md`** (Standards root)
   - Overview of Standards repository

5. **`unified_data_dictionary/README.md`**
   - Overview of UDD tool

6. **`unified_data_dictionary/SUMMARY.md`**
   - UDD project status

7. **`unified_data_dictionary/pyproject.toml`**
   - Python package configuration
   - **CRITICAL**: Will package still install after move?

8. **`GIT_REPOSITORY_STRUCTURE.md`**
   - Current repository layout documentation

### Priority 3: Python Package Analysis
Please analyze these for path dependencies:

9. **`unified_data_dictionary/src/cli.py`**
   - Entry point, likely has path references

10. **`unified_data_dictionary/src/extract_from_repos.py`**
    - Main functionality

11. **`unified_data_dictionary/src/build_dictionary.py`**
    - Core logic

12. **`unified_data_dictionary/config.yaml`**
    - Configuration that might reference paths

### Priority 4: Additional Context

13. **`.claude/settings.local.json`**
    - Project-specific Claude settings
    - Shows how previous Claude sessions worked with this project

14. **`unified_data_dictionary/Makefile`**
    - Build automation that might break

15. **Directory structure of `unified_data_dictionary/`**
    - List all subdirectories to verify migration plan covers everything

---

## Specific Questions to Answer

### 1. Python Package Integrity
- After moving to `tools/unified_data_dictionary/`, will `pip install -e .` still work?
- Does `pyproject.toml` have any path assumptions?
- Will the package structure remain valid?
- Do we need to update any package configuration?

### 2. Path Dependencies
- Search all Python files in `unified_data_dictionary/src/` for:
  - Hardcoded paths
  - References to `unified_data_dictionary/` directory
  - Relative path assumptions (../, ./, etc.)
  - `os.path`, `Path()`, `__file__` usage
- Will the proposed `standards_paths.ini` configuration file solve these?

### 3. Import Statements
- Search for import statements in all Python files
- Are there any imports that assume current directory structure?
- Will `from src import ...` still work?
- Do we need to update `__init__.py` files?

### 4. Test Suite
- Will tests still run from `tools/unified_data_dictionary/tests/`?
- Do tests reference fixtures or test data?
- Where is test data located and will paths still work?

### 5. Configuration Files
- Review `config.yaml` for path references
- Review `pyproject.toml` for directory assumptions
- Review `Makefile` for hardcoded paths
- Will these still work after migration?

### 6. Documentation References
- Are there README files that reference file locations?
- Do examples have paths that need updating?
- Are there setup guides with old paths?

### 7. Missing Files
- Compare the migration plan against actual UDD directory contents
- Are all directories accounted for in the migration?
- Any files that should move but aren't listed?

### 8. Git Considerations
- Is this a safe git operation?
- Should we create a migration branch first?
- Any concerns about git history?

### 9. Cross-Platform Compatibility
- Will paths work on both Windows and Unix?
- Are there any OS-specific path issues?
- Should we use pathlib instead of os.path?

### 10. Future Maintenance
- How do we sync updates from UDD GitHub repo?
- What happens when we pull new UDD versions?
- Is the structure maintainable long-term?

---

## Analysis Steps

### Step 1: Verify Migration Plan Coverage
```
1. List all subdirectories in unified_data_dictionary/
2. Check each directory is mentioned in migration plan
3. Identify any missing directories
```

### Step 2: Analyze Path Dependencies
```
1. Search all .py files for path-related code:
   - grep -r "os.path" unified_data_dictionary/src/
   - grep -r "Path(" unified_data_dictionary/src/
   - grep -r "__file__" unified_data_dictionary/src/
   - grep -r "../" unified_data_dictionary/src/

2. Check config files for path references:
   - unified_data_dictionary/config.yaml
   - unified_data_dictionary/pyproject.toml
```

### Step 3: Review Python Package Structure
```
1. Check pyproject.toml for:
   - package name
   - package directory references
   - entry points
   - data files

2. Verify package will install from new location
```

### Step 4: Assess Import Dependencies
```
1. Find all import statements:
   - grep -r "^import " unified_data_dictionary/src/
   - grep -r "^from " unified_data_dictionary/src/

2. Check if imports assume directory structure
```

### Step 5: Review Test Structure
```
1. Check test discovery patterns in pyproject.toml
2. Verify test data locations
3. Check if tests import from parent directories
```

---

## Additional Context Questions

**Before starting the review, please ask me:**

1. Do you actively use the UDD CLI commands?
2. Do you update UDD from its GitHub repository?
3. Are there any custom scripts that reference UDD?
4. Are there any scheduled tasks or automation using UDD?
5. Do other projects depend on UDD?

**And check:**
- Can you successfully run `cd unified_data_dictionary && pip install -e .` currently?
- Can you run `udd --help` currently?
- Have you run UDD tests recently?

---

## Expected Output Format

Please provide your review in this structure:

### Executive Summary
- Overall assessment (Safe/Risky/Needs Changes)
- Key concerns (3-5 bullets)
- Recommendation (Proceed/Modify/Reconsider)

### Detailed Analysis

#### 1. Python Package Integrity [PASS/FAIL/WARNING]
- Findings
- Concerns
- Recommendations

#### 2. Path Dependencies [PASS/FAIL/WARNING]
- Files with path issues
- Specific problems found
- Suggested fixes

#### 3. Import Structure [PASS/FAIL/WARNING]
- Import issues found
- Will break/won't break
- Required changes

#### 4. Configuration Files [PASS/FAIL/WARNING]
- Config files reviewed
- Issues found
- Updates needed

#### 5. Test Suite [PASS/FAIL/WARNING]
- Test discoverability
- Fixture access
- Required changes

#### 6. Missing Coverage [Items found/None]
- Directories not in plan
- Files not accounted for
- Additional considerations

### Risk Assessment

**High Risk:**
- [List high-risk issues]

**Medium Risk:**
- [List medium-risk issues]

**Low Risk:**
- [List low-risk issues]

### Recommendations

**Before Migration:**
1. [Actions to take before running script]

**Migration Script Changes:**
1. [Suggested modifications to script]

**After Migration:**
1. [Post-migration actions needed]

**Alternative Approaches:**
1. [If you see better ways]

---

## 📝 Code Header Standards

**IMPORTANT**: When providing updated code or script artifacts, you MUST include a standardized header.

### Header Format Requirements

All code files must include this header at the top, adapted to the language's comment syntax:

**Required Components:**
1. Timestamp (EST): YYYY-MM-DD-HH-MM-SS
2. Project Path and File Name
3. Author: R. A. Carucci
4. Purpose: One-line description (AI-generated)

### Comment Syntax by Language

| Language | Comment Symbol | Example File |
|----------|---------------|--------------|
| M Code | `//` | ArrestAnalysis/lookup_zip.m |
| Python | `#` | ArrestAnalysis/arrest_processor.py |
| VBA | `'` | ArrestAnalysis/ExportQueries.bas |
| SQL | `--` | ArrestAnalysis/daily_extract.sql |
| JavaScript | `//` | CrimeMap/init.js |
| PowerShell | `#` | Scripts/migration.ps1 |
| Bash | `#` | scripts/deploy.sh |

### Header Examples

#### Python
```python
# 🕒 2026-01-16-14-30-45
# unified_data_dictionary/src/cli.py
# Author: R. A. Carucci
# Purpose: Command-line interface for UDD schema extraction and dictionary generation.
```

#### PowerShell
```powershell
# 🕒 2026-01-16-14-30-45
# Scripts/udd_migration.ps1
# Author: R. A. Carucci
# Purpose: Automated migration script for UDD hybrid integration into Standards repository.
```

#### M Code / JavaScript
```javascript
// 🕒 2026-01-16-14-30-45
// CrimeMap/init.js
// Author: R. A. Carucci
// Purpose: Initialize crime mapping dashboard with spatial data layers and filters.
```

#### VBA
```vba
' 🕒 2026-01-16-14-30-45
' ArrestAnalysis/ExportQueries.bas
' Author: R. A. Carucci
' Purpose: Export M code from all queries in workbook to individual files for audit and backup.
```

#### SQL
```sql
-- 🕒 2026-01-16-14-30-45
-- ArrestAnalysis/daily_extract.sql
-- Author: R. A. Carucci
-- Purpose: Daily extraction of arrest records with geographic and demographic enrichment.
```

### Implementation Rules

✅ **DO:**
- Insert header at the very top of every code file
- Use correct comment symbol for the language
- Use current timestamp in Eastern Standard Time (EST)
- Write "R. A. Carucci" exactly as shown
- Generate a clear, professional, one-line purpose
- Include the clock emoji 🕒 before timestamp

❌ **DON'T:**
- Skip the header
- Use wrong comment syntax
- Write long multi-line purposes
- Misspell the author name
- Forget the timestamp

### When to Apply Headers

Apply standardized headers when:
- Creating new code files
- Providing updated/revised versions of existing code
- Generating migration scripts
- Creating utility scripts
- Writing any executable code artifact

---

## Success Criteria

The review is complete when you've:
- [ ] ✅ **COMPLETED PRE-FLIGHT CHECKLIST** (MANDATORY FIRST STEP)
- [ ] Created backup of Standards directory
- [ ] Verified UDD currently works
- [ ] Searched for external dependencies
- [ ] Checked git status
- [ ] Generated PRE-FLIGHT-RESULTS.md report
- [ ] Received GO/NO-GO approval
- [ ] Read all Priority 1 files
- [ ] Analyzed Python package structure
- [ ] Searched for path dependencies
- [ ] Reviewed import statements
- [ ] Checked configuration files
- [ ] Assessed test suite impact
- [ ] Verified migration plan coverage
- [ ] Provided risk assessment
- [ ] Given clear recommendation
- [ ] Suggested improvements

---

## Note on .claude Directory

The `.claude/settings.local.json` file shows:
- Previous Claude sessions had specific permissions
- Git operations were pre-approved
- File operations were pre-approved
- This suggests an established workflow

Use this to inform your understanding of how this project has been managed.

---

**START YOUR REVIEW HERE**

Please begin by:
1. Reading the migration plan (docs/merge/05-UDD-Hybrid-Migration-REVISED.md)
2. Understanding the current UDD structure
3. Then proceed with detailed analysis

Thank you!
