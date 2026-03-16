# PRE-FLIGHT CHECKLIST - DO NOT SKIP

**Date**: 2026-01-16  
**Status**: 🔴 MANDATORY BEFORE MIGRATION

---

## ⚠️ STOP - Read This First

**DO NOT run the migration script until you complete this checklist.**

Many assumptions were made during planning. These must be verified.

---

## 🔴 CRITICAL - Answer These First

### 1. Does UDD Currently Work?

```powershell
# Run these commands RIGHT NOW:
cd "C:\Users\carucci_r\OneDrive - City of Hackensack\09_Reference\Standards\unified_data_dictionary"

# Test 1: Can it install?
pip install -e .

# Test 2: Can you import it?
python -c "import src.cli; print('✓ Import works')"

# Test 3: Does CLI work?
udd --help

# Test 4: Do tests pass?
pytest
```

**Results:**
- [ ] pip install worked
- [ ] Import worked
- [ ] CLI worked
- [ ] Tests passed

**If ANY fail:** UDD is already broken. Fix it first or abandon migration.

---

### 2. Who Uses This Repository?

Ask yourself:
- [ ] Am I the only person using this?
- [ ] Do other analysts access these files?
- [ ] Is this shared documentation?
- [ ] Do other departments reference this?

**If anyone else uses this:** Communicate before migrating.

---

### 3. External Dependencies?

```powershell
# Search for Power BI files
Get-ChildItem "C:\Users\carucci_r\OneDrive - City of Hackensack" -Recurse -Filter "*.pbix" -ErrorAction SilentlyContinue |
    Select-String "unified_data_dictionary|Standards\\schemas|Standards\\mappings"

# Search ETL scripts
Get-ChildItem "C:\Users\carucci_r\OneDrive - City of Hackensack\02_ETL_Scripts" -Recurse -Filter "*.py" -ErrorAction SilentlyContinue |
    Select-String "unified_data_dictionary" -List

# Check scheduled tasks
Get-ScheduledTask | Where-Object {$_.Actions.Execute -like "*unified_data_dictionary*"}
```

**Results:**
- [ ] No Power BI dependencies found
- [ ] No ETL script dependencies found
- [ ] No scheduled tasks found

**If dependencies found:** Document them and update after migration.

---

### 4. Why Are You Doing This?

**Answer these questions:**

Q: What specific problem does this migration solve?  
A: _____________________________________

Q: What happens if you do nothing?  
A: _____________________________________

Q: Is there a simpler solution?  
A: _____________________________________

Q: Is 2-3 hours effort worth the benefit?  
A: _____________________________________

**If answers are unclear:** Reconsider if migration is needed.

---

### 5. What Does NIBRS Content Look Like?

- [ ] I have reviewed NIBRS content structure
- [ ] I know how much content there is
- [ ] I verified new structure will work for NIBRS
- [ ] NIBRS doesn't need special organization

**If unchecked:** Review NIBRS content before reorganizing for it.

---

## 🟡 IMPORTANT - Verify Environment

### Git Status

```powershell
cd "C:\Users\carucci_r\OneDrive - City of Hackensack\09_Reference\Standards"

git status
git log --oneline -5
git branch
```

**Requirements:**
- [ ] Git status is clean (no uncommitted changes)
- [ ] Latest commit is pushed
- [ ] On correct branch (main or feature branch)
- [ ] No untracked important files

**If dirty:** Commit or stash changes first.

---

### OneDrive Status

```powershell
# Check for cloud-only files
Get-ChildItem "C:\Users\carucci_r\OneDrive - City of Hackensack\09_Reference\Standards\unified_data_dictionary" -Recurse -File |
    Where-Object {$_.Attributes -match "ReparsePoint"} |
    Select-Object FullName
```

**Requirements:**
- [ ] All files are downloaded (not cloud-only)
- [ ] OneDrive is not currently syncing
- [ ] No sync errors in OneDrive

**Action:** Pause OneDrive before migration.

---

### Long Paths Check

```powershell
Get-ChildItem "unified_data_dictionary" -Recurse -File |
    Where-Object { $_.FullName.Length -gt 200 } |
    Select-Object FullName, @{N='Length';E={$_.FullName.Length}}
```

**Results:**
- [ ] No paths over 200 characters
- [ ] OR long paths are enabled in Windows

**If long paths found:** Enable long paths in Windows first.

---

## 🟢 PREPARATION - Create Safety Net

### 1. Create Backup

```powershell
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$backupPath = "C:\Temp\Standards_Backup_$timestamp"

# Full backup
Copy-Item "C:\Users\carucci_r\OneDrive - City of Hackensack\09_Reference\Standards" `
          $backupPath -Recurse -Force

Write-Host "Backup created at: $backupPath"
```

**Verification:**
- [ ] Backup created successfully
- [ ] Backup size looks correct
- [ ] Can access backup files

**Time:** 5-10 minutes  
**Space needed:** ~2-3 GB

---

### 2. Create Migration Branch

```powershell
cd "C:\Users\carucci_r\OneDrive - City of Hackensack\09_Reference\Standards"

git checkout -b feature/udd-hybrid-migration
git status
```

**Verification:**
- [ ] New branch created
- [ ] On feature branch (not main)
- [ ] Status is clean

---

### 3. Document Current State

```powershell
# File count before migration
$fileCount = (Get-ChildItem "unified_data_dictionary" -Recurse -File).Count
Write-Host "Files in UDD: $fileCount"

# Directory structure
Get-ChildItem "unified_data_dictionary" -Directory -Recurse -Name | 
    Out-File "docs\merge\pre_migration_structure.txt"

# Take screenshots of key directories
```

**Documentation:**
- [ ] File count recorded: _______
- [ ] Directory structure saved
- [ ] Screenshots taken

---

### 4. Prepare Rollback Plan

**If migration fails, I will:**
1. `git reset --hard` to undo changes
2. Restore from backup at C:\Temp\Standards_Backup_[timestamp]
3. Resume OneDrive sync
4. Verify restore worked

**Verification:**
- [ ] I understand rollback process
- [ ] I have backup location saved
- [ ] I can restore if needed

---

## 📋 FINAL GO/NO-GO DECISION

### All Critical Items Complete? (Must be YES)
- [ ] UDD currently works (tested)
- [ ] No unexpected external dependencies
- [ ] Clear reason for migration
- [ ] NIBRS content reviewed (or not relevant)
- [ ] Git status clean
- [ ] Backup created
- [ ] OneDrive paused
- [ ] Migration branch created
- [ ] Rollback plan understood

### Risk Assessment
- [ ] I accept the risks documented in CRITICAL-BLIND-SPOTS.md
- [ ] I have time to complete migration (2-3 hours)
- [ ] I have time to test after migration (1 hour)
- [ ] I can rollback if needed

### Final Decision

**GO**: Proceed with migration ✅  
**NO-GO**: Stop, address concerns first ⛔

**If NO-GO:** Review CRITICAL-BLIND-SPOTS.md for alternatives.

---

## ⏱️ TIME BUDGET

Plan for:
- Pre-flight checks: 30-60 minutes
- Migration execution: 15-20 minutes
- Post-migration testing: 30-60 minutes
- Documentation updates: 30 minutes
- Buffer for issues: 30 minutes

**Total: 2.5-3.5 hours**

**Do you have this time available?**
- [ ] Yes, I can dedicate 3-4 hours uninterrupted
- [ ] No, I should schedule this for later

---

## 🚀 READY TO PROCEED?

**If all checkboxes are marked:**

1. **Pause OneDrive**
2. **Close any programs accessing these files**
3. **Open PowerShell as Administrator**
4. **Open the migration script**
5. **Read script one more time**
6. **Take a deep breath**
7. **Execute**

**If any checkboxes remain unchecked:**

❌ **DO NOT PROCEED**

Address the unchecked items first.

---

## 📞 NEED HELP?

**If you're unsure:**
- Re-read CRITICAL-BLIND-SPOTS.md
- Ask Claude Code to review
- Consider the "do nothing" option
- Schedule migration for when you have more time

**Remember:**
- Doing nothing is often the safest choice
- You can always migrate later
- Current structure works
- Don't fix what isn't broken

---

**Checklist Status:** ⬜ INCOMPLETE  
**Ready to Migrate:** ❌ NO (complete checklist first)  
**Created**: 2026-01-16
