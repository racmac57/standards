# Scripts Directory

This directory contains utility scripts organized by function.

## 📁 Directory Structure

```
scripts/
├── Process_UDD_Chatlog.bat  # Main chatlog processor (must stay in root for Directory Opus)
├── tests/              # Test files and test runners
├── processing/         # Other chatlog processing scripts
├── cleanup/            # Cleanup and maintenance scripts
└── utilities/          # General utility scripts
```

**Note**: `Process_UDD_Chatlog.bat` must remain in the scripts root directory as it's referenced by the Directory Opus button configuration.

## 📂 Folder Descriptions

### `tests/`
Test framework and test results for `Process_UDD_Chatlog.bat`:
- `Process_UDD_Chatlog_TEST_PLAN.md` - Comprehensive test plan
- `run_all_tests.bat` - Automated test runner
- `setup_test_environment.ps1` - Test environment setup script
- `TEST_RESULTS.md` - Test execution results
- `TEST_EXECUTION_REPORT.md` - Detailed test report
- `TEST_FIXES_APPLIED.md` - Documentation of fixes applied during testing
- `FINAL_TEST_RESULTS.md` - Final test summary

### Root Directory
- `Process_UDD_Chatlog.bat` - **Main chatlog processor (v1.3.0)** - Must stay in root
  - Auto-detects workspace structure
  - Supports numbered folder structures
  - Debug mode with `-v` or `--verbose` flag
  - Activity logging to `chatlog_processor.log`
  - Referenced by Directory Opus button configuration

### `processing/`
Other chatlog processing scripts:
- `process_chatlog.bat` - Alternative processing script
- `quick_process_chatlog.bat` - Quick processing utility
- `Test_Chatlog_Processing.bat` - Processing test script

### `cleanup/`
Scripts for cleaning up duplicate files and organizing output:
- `cleanup_duplicates.ps1` - Remove duplicate/redundant files
- `cleanup_duplicate_outputs.ps1` - Clean up duplicate outputs
- `list_duplicate_outputs.ps1` - List duplicate outputs without removing
- `Reorganize_Chunked_Files.ps1` - Reorganize chunked file structure

### `utilities/`
General utility scripts and configurations:
- `CREATE_STRUCTURE.bat` - Create directory structure
- `Sync_UDD_Processors_local_run.ps1` - Sync processors for local runs
- `DOpus_Process_UDD_Chatlog_Button.dcf` - Directory Opus button configuration

## 🚀 Quick Start

### Processing a Chatlog
```batch
cd scripts
Process_UDD_Chatlog.bat "path\to\chatlog.txt"
```

Or use the Directory Opus button (configured to run from scripts root).

### Running Tests
```batch
cd tests
run_all_tests.bat
```

### Cleaning Up Duplicates
```powershell
cd cleanup
.\cleanup_duplicates.ps1
```

## 📝 Notes

- All scripts are designed to work from their respective directories
- Test scripts require the test environment to be set up first
- Processing scripts auto-detect workspace structure
- Cleanup scripts include safety checks before deletion

---

**Last Updated**: 2026-01-09  
**Organization**: Organized by function for better maintainability
