# 🕒 2026-01-16-18-15-00
# docs/merge/EXTERNAL-DEPENDENCIES-TRACKING.md
# Author: R. A. Carucci
# Purpose: Track all external systems referencing UDD paths that must be updated post-migration.

# External System Dependencies - Migration Impact Assessment

**Date**: 2026-01-16  
**Status**: 🔴 MUST UPDATE AFTER MIGRATION  
**Risk Level**: HIGH

---

## 🚨 Critical Warning

The pre-flight checklist confirmed that **external systems reference unified_data_dictionary paths**. After migration, these systems MUST be updated or they will break.

---

## 📋 Systems Requiring Path Updates

### 1. Power BI Reports

**Status**: ⚠️ NEEDS DOCUMENTATION

**Action Required**: Document all Power BI reports that load data from:
- `unified_data_dictionary/schemas/`
- `unified_data_dictionary/mappings/`
- `unified_data_dictionary/data/`
- Any other UDD paths

**Where to Check**:
```
Power BI files likely in:
- C:\Users\carucci_r\OneDrive - City of Hackensack\04_PowerBI\
- C:\Users\carucci_r\OneDrive - City of Hackensack\06_Reports\
```

**Post-Migration Updates Required**:

| Report Name | Current Path | New Path | Update Method |
|-------------|--------------|----------|---------------|
| _(To be documented)_ | `unified_data_dictionary/schemas/...` | `schemas/udd/...` | Update M code in Power Query |
| _(To be documented)_ | `unified_data_dictionary/mappings/...` | `mappings/field_mappings/...` | Update M code in Power Query |

**Update Instructions**:
1. Open each Power BI file in Power BI Desktop
2. Go to Transform Data → Advanced Editor
3. Find all references to `unified_data_dictionary`
4. Update paths according to new structure:
   - `unified_data_dictionary/schemas/` → `schemas/udd/`
   - `unified_data_dictionary/mappings/` → `mappings/field_mappings/`
   - `unified_data_dictionary/templates/` → `templates/udd/`
   - `unified_data_dictionary/data/` → `data/samples/`

---

### 2. ETL Scripts (02_ETL_Scripts)

**Status**: ⚠️ NEEDS DOCUMENTATION

**Action Required**: Document all Python/PowerShell scripts in ETL that reference:
- `unified_data_dictionary` paths
- UDD CLI commands
- UDD Python imports

**Where to Check**:
```
C:\Users\carucci_r\OneDrive - City of Hackensack\02_ETL_Scripts\
```

**Post-Migration Updates Required**:

| Script Name | Current References | New References | Update Method |
|-------------|-------------------|----------------|---------------|
| _(To be documented)_ | `sys.path.append('../unified_data_dictionary')` | `sys.path.append('../tools/unified_data_dictionary')` | Update Python imports |
| _(To be documented)_ | `from unified_data_dictionary.src import ...` | No change (relative imports work) | Test imports |
| _(To be documented)_ | File paths to schemas/mappings | Update to new structure | Update path strings |

**Update Instructions**:
1. Search all .py files for `unified_data_dictionary`
2. Update sys.path references
3. Update file path strings
4. Test each script after updates

---

### 3. Scheduled Tasks

**Status**: ⚠️ NEEDS DOCUMENTATION

**Action Required**: Document any Windows scheduled tasks that:
- Run UDD CLI commands
- Reference UDD paths in working directory
- Call scripts that use UDD

**Where to Check**:
```powershell
Get-ScheduledTask | Where-Object {$_.Actions.Execute -like "*unified_data_dictionary*"}
Get-ScheduledTask | Where-Object {$_.Actions.Execute -like "*Standards*"}
```

**Post-Migration Updates Required**:

| Task Name | Current Working Directory | New Working Directory | Update Method |
|-----------|--------------------------|----------------------|---------------|
| _(To be documented)_ | `Standards\unified_data_dictionary` | `Standards\tools\unified_data_dictionary` | Update task properties |

**Update Instructions**:
1. Open Task Scheduler
2. Find each task referencing UDD
3. Update working directory paths
4. Update any command-line arguments with paths
5. Test task execution

---

### 4. Custom Scripts (User-Created)

**Status**: ⚠️ NEEDS DOCUMENTATION

**Action Required**: Document any custom analysis scripts that:
- Import from UDD
- Load schemas/mappings
- Reference UDD paths

**Likely Locations**:
- Desktop
- Documents
- Project-specific folders
- Jupyter notebooks

**Post-Migration Updates Required**:

| Script Location | Current References | New References | Notes |
|----------------|-------------------|----------------|-------|
| _(To be documented)_ | _(Path references)_ | _(Updated paths)_ | _(Special notes)_ |

---

### 5. Documentation & README Files

**Status**: ⚠️ NEEDS DOCUMENTATION

**Action Required**: Document which documentation files reference old UDD structure

**Search Command**:
```powershell
Get-ChildItem -Recurse -Include *.md,*.txt,*.docx |
    Select-String "unified_data_dictionary[/\\]" |
    Group-Object Path
```

**Post-Migration Updates Required**:

| Document | Old Path References | Update Required | Priority |
|----------|-------------------|-----------------|----------|
| _(To be documented)_ | _(Old paths)_ | YES/NO | HIGH/MEDIUM/LOW |

---

### 6. VS Code / IDE Workspace Files

**Status**: ⚠️ CHECK

**Files to Check**:
- `.code-workspace` files
- `.vscode/settings.json`
- Cursor IDE settings
- Any IDE project files

**Post-Migration Updates**:
- Update folder paths in workspace files
- Update Python interpreter paths if pointing to UDD venv
- Update search exclusions
- Update file associations

---

## 📝 Pre-Migration Checklist

**Complete BEFORE running migration script:**

- [ ] **Document all Power BI reports** with UDD dependencies
- [ ] **Document all ETL scripts** with UDD imports/paths
- [ ] **Document all scheduled tasks** that reference UDD
- [ ] **Search for custom scripts** in common locations
- [ ] **List all documentation** with UDD path references
- [ ] **Check workspace files** for path dependencies
- [ ] **Create update plan** for each system
- [ ] **Estimate downtime** if systems must be offline during updates
- [ ] **Notify users** if shared reports will be temporarily broken

---

## 📋 Post-Migration Update Checklist

**Complete IMMEDIATELY after migration:**

### Phase 1: Verify Migration Success (30 min)
- [ ] Verify UDD tool works: `cd tools/unified_data_dictionary && pip install -e . && udd --help`
- [ ] Verify schemas in new location: `ls schemas/udd/`
- [ ] Verify mappings in new location: `ls mappings/field_mappings/`
- [ ] Run post-migration tests

### Phase 2: Update Power BI (1-2 hours)
- [ ] Open each documented Power BI report
- [ ] Update M code paths in Power Query
- [ ] Refresh data to test
- [ ] Save and publish updated reports
- [ ] Notify users of updates

### Phase 3: Update ETL Scripts (1-2 hours)
- [ ] Update each documented ETL script
- [ ] Test imports and path references
- [ ] Run each script to verify functionality
- [ ] Commit updated scripts to git
- [ ] Document changes in CHANGELOG

### Phase 4: Update Scheduled Tasks (30 min)
- [ ] Update each documented task
- [ ] Test task execution manually
- [ ] Verify task runs on schedule
- [ ] Monitor logs for failures

### Phase 5: Update Custom Scripts (30 min)
- [ ] Update each documented custom script
- [ ] Test script execution
- [ ] Notify script owners of changes

### Phase 6: Update Documentation (30 min)
- [ ] Update all markdown files with old paths
- [ ] Update README files
- [ ] Update setup/installation guides
- [ ] Update examples and tutorials

### Phase 7: Final Verification (30 min)
- [ ] Run all systems end-to-end
- [ ] Verify no broken references remain
- [ ] Check logs for path-related errors
- [ ] Confirm all users can access updated resources

**Total Estimated Time**: 5-6 hours for all updates

---

## 🚨 Rollback Plan

**If external systems break and cannot be quickly fixed:**

1. **Immediate**: Restore from backup
   ```powershell
   # Stop OneDrive sync first
   Remove-Item "C:\Users\carucci_r\OneDrive - City of Hackensack\09_Reference\Standards" -Recurse -Force
   Copy-Item "C:\Temp\Standards_Backup_20260116_181122" `
             "C:\Users\carucci_r\OneDrive - City of Hackensack\09_Reference\Standards" `
             -Recurse -Force
   ```

2. **Git rollback**:
   ```bash
   git checkout main
   git branch -D feature/udd-hybrid-migration
   ```

3. **Resume OneDrive sync**

4. **Verify old structure restored**

5. **Notify affected users**

6. **Post-mortem**: Document what went wrong and how to prevent it

---

## 📊 Risk Mitigation Strategy

### Option 1: Phased Migration (RECOMMENDED)
1. **Phase 1**: Migrate UDD but create symbolic links at old locations
2. **Phase 2**: Update half of external systems
3. **Phase 3**: Test and verify
4. **Phase 4**: Update remaining systems
5. **Phase 5**: Remove symbolic links after all systems updated

**Advantage**: Systems continue working during update process

### Option 2: Maintenance Window (If downtime acceptable)
1. Schedule maintenance window (evening/weekend)
2. Notify all users
3. Execute migration
4. Update all external systems
5. Test everything
6. Resume operations

**Advantage**: Clean cutover, all systems updated at once

### Option 3: Create Symbolic Links Permanently (CONSERVATIVE)
1. Migrate UDD to new location
2. Create symbolic links from old locations to new
3. External systems continue working unchanged
4. Update systems gradually over time
5. Remove symbolic links after all updates complete (optional)

**Advantage**: Zero downtime, no rush to update systems

---

## 💡 Recommended Approach

Given **CONDITIONAL GO** status and confirmed external dependencies:

**I recommend Option 3: Symbolic Links**

**Why:**
- Zero risk of breaking production systems
- No time pressure to update all systems immediately
- Can update systems one at a time and test thoroughly
- Easy rollback (just remove symlinks if issues)
- Allows gradual migration of references

**Implementation**:
```powershell
# After migration, create symbolic links:
cd "C:\Users\carucci_r\OneDrive - City of Hackensack\09_Reference\Standards"

# Link schemas
New-Item -ItemType Junction -Path "unified_data_dictionary\schemas" `
         -Target "schemas\udd"

# Link mappings  
New-Item -ItemType Junction -Path "unified_data_dictionary\mappings" `
         -Target "mappings\field_mappings"

# Link templates
New-Item -ItemType Junction -Path "unified_data_dictionary\templates" `
         -Target "templates\udd"

# Link data
New-Item -ItemType Junction -Path "unified_data_dictionary\data" `
         -Target "data\samples"
```

**Result**: External systems work unchanged while you update them at your own pace.

---

## 📋 Action Items Before Proceeding

**YOU MUST complete this section:**

### 1. Power BI Dependencies
**Found**: ⬜ YES / ⬜ NO  
**Count**: _______  
**Critical Reports**: _______________________  
**Documented**: ⬜ YES / ⬜ NO

### 2. ETL Script Dependencies
**Found**: ⬜ YES / ⬜ NO  
**Count**: _______  
**Critical Scripts**: _______________________  
**Documented**: ⬜ YES / ⬜ NO

### 3. Scheduled Task Dependencies
**Found**: ⬜ YES / ⬜ NO  
**Count**: _______  
**Critical Tasks**: _______________________  
**Documented**: ⬜ YES / ⬜ NO

### 4. Migration Strategy Decision
**Selected Strategy**:
- ⬜ Option 1: Phased Migration
- ⬜ Option 2: Maintenance Window
- ⬜ Option 3: Symbolic Links (RECOMMENDED)

**Rationale**: _______________________

### 5. Downtime Acceptable?
**Answer**: ⬜ YES (use Option 2) / ⬜ NO (use Option 3)

### 6. Ready to Proceed?
- ⬜ All dependencies documented
- ⬜ Update plan created
- ⬜ Migration strategy selected
- ⬜ Backup verified (✅ C:\Temp\Standards_Backup_20260116_181122)
- ⬜ Migration branch created (✅ feature/udd-hybrid-migration)
- ⬜ OneDrive paused
- ⬜ Time allocated for updates (5-6 hours)

---

## 🎯 Final GO/NO-GO Decision

**Based on external dependency documentation:**

⬜ **GO** - All dependencies documented, strategy selected, ready to proceed  
⬜ **NO-GO** - More documentation needed before proceeding

**Sign-Off**:
- **Date**: _________________
- **Time**: _________________
- **Strategy**: _________________
- **Estimated Downtime**: _________________
- **Approved By**: R. A. Carucci

---

**Status**: 🟡 AWAITING DEPENDENCY DOCUMENTATION  
**Next Step**: Complete sections above before proceeding  
**Created**: 2026-01-16-18-15-00
