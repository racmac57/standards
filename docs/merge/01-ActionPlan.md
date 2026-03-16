# Merge Action Plan

**Date**: 2026-01-16  
**Priority**: HIGH  
**Effort**: 6-7 hours total

---

## Executive Summary

The `unified_data_dictionary/mappings/` contains **outdated v1.0 files** (2025-12-16) while canonical locations have **v2.0 files** (2025-12-30).

**Key Decision**: Archive v1.0 cross-system mappings and create pointers to v2.0 canonical locations.

---

## Critical Finding - Version Mismatch

| File | UDD Version | Canonical Version | Status |
|------|-------------|-------------------|--------|
| cad_to_rms_field_map | v1.0 (2025-12-16) | v2.0 (2025-12-30) | ⚠️ OUTDATED |
| rms_to_cad_field_map | v1.0 (need check) | v2.0 (2025-12-30) | ⚠️ LIKELY OUTDATED |

**v2.0 Enhancements:**
- Multi-column matching strategies
- Confidence scoring (0.0-1.0)
- Enhanced audit fields
- Alternative matching when primary key fails

---

## Phase 1: File Consolidation (2.5-3.5 hours)

### Task 1: Archive Outdated Cross-System Mappings (1 hour) ⚡

**Steps:**

1. **Compare rms_to_cad versions** (similar check as cad_to_rms):
```powershell
cd "C:\Users\carucci_r\OneDrive - City of Hackensack\09_Reference\Standards"
(Get-FileHash "CAD_RMS\DataDictionary\current\schema\rms_to_cad_field_map.json").Hash
(Get-FileHash "unified_data_dictionary\mappings\rms_to_cad_field_map_latest.json").Hash
```

2. **Create archive directory** for v1.0 files:
```powershell
New-Item -ItemType Directory -Path "archive\legacy_copies\v1.0_mappings" -Force
```

3. **Move outdated v1.0 files**:
```powershell
Move-Item "unified_data_dictionary\mappings\cad_to_rms_field_map_latest.json" `
          "archive\legacy_copies\v1.0_mappings\" -Force

Move-Item "unified_data_dictionary\mappings\rms_to_cad_field_map_latest.json" `
          "archive\legacy_copies\v1.0_mappings\" -Force
```

4. **Create pointer files** (see templates below)

---

### Task 2: Verify Other Mapping Files (1-2 hours) ⚡

**Files to Check:**
1. `cad_field_map_v2.json` - Compare with `cad_field_map_latest.json`
2. `cad_to_rms_mapping.csv` - CSV export of JSON?
3. `rms_to_cad_mapping.csv` - CSV export of JSON?
4. `cad_rms_merge_policy_latest.json` - Purpose?
5. `cad_to_rms_field_map_v2_enhanced.md` - Which version documented?
6. `rms_to_cad_field_map_v2_enhanced.md` - Which version documented?

**Comparison Script:**
```powershell
cd "C:\Users\carucci_r\OneDrive - City of Hackensack\09_Reference\Standards"

$files = @(
    "unified_data_dictionary\mappings\cad_field_map_latest.json",
    "unified_data_dictionary\mappings\cad_field_map_v2.json"
)

foreach ($file in $files) {
    if (Test-Path $file) {
        $hash = (Get-FileHash $file).Hash
        $size = (Get-Item $file).Length
        Write-Host "$file"
        Write-Host "  Hash: $hash"
        Write-Host "  Size: $size bytes`n"
    }
}
```

---

### Task 3: Create mappings/README.md (30 min) ⚡

Create `unified_data_dictionary\mappings\README.md` explaining:
- Which files are pointers to canonical v2.0
- Which files are system-specific (keep)
- Version history and rationale

(See detailed template in full action plan document)

---

## Phase 2: Documentation Updates (1 hour)

### Task 4: Update Standards/README.md (30 min) 🔵
- Add v2.0 canonical mappings note
- Update UDD integration section
- Add version history

### Task 5: Consolidate CHANGELOGs (30 min) 🔵
- Keep both files but add cross-references
- Standards/CHANGELOG.md = repository-wide
- UDD/CHANGELOG.md = project-specific

---

## Phase 3: Root Directory Cleanup (2.5 hours)

### Task 6: Organize Root-Level Files (1 hour) 🔵

**Move from root:**
- `validate_rms_export.py` → `scripts/validation/`
- `extract_narrative_fields.py` → `scripts/extraction/`
- `rms_field_dictionary.html` → `docs/html/`
- `sample_rms_export.csv` → `data/samples/rms/`

### Task 7: Check Script References (30 min) 🔵

**Before archiving, search for references:**
```powershell
cd "C:\Users\carucci_r\OneDrive - City of Hackensack\09_Reference\Standards"
Get-ChildItem -Recurse -Filter "*.py" | Select-String "cad_to_rms_field_map_latest" -List
Get-ChildItem -Recurse -Filter "*.bat" | Select-String "cad_to_rms_field_map_latest" -List
Get-ChildItem -Recurse -Filter "*.ps1" | Select-String "cad_to_rms_field_map_latest" -List
```

### Task 8: Update GIT_REPOSITORY_STRUCTURE.md (1 hour) 🟢
- Reflect actual structure (not proposed)

---

## Pointer File Template

**File**: `unified_data_dictionary\mappings\cad_to_rms_field_map_latest_POINTER.md`

```markdown
# File Archived - Use Canonical Location

This file (v1.0, 2025-12-16) has been archived. Use canonical v2.0:

## Canonical Location
- **Path**: `../../CAD_RMS/DataDictionary/current/schema/cad_to_rms_field_map.json`
- **Version**: 2.0 (2025-12-30)
- **Enhancements**: Multi-column matching, confidence scoring

## What Changed in v2.0
- Alternative matching strategies (temporal+address, officer+temporal)
- Confidence thresholds (0.75-0.85)
- Enhanced audit fields
- Backward compatible with v1.0 primary key matching

## Archived Location
- **v1.0**: `../../archive/legacy_copies/v1.0_mappings/cad_to_rms_field_map_latest.json`
- **Retention**: 30 days (see archive/README.md)

See [README.md](../../README.md) for repository layout.
```

---

## Time Estimates

| Phase | Tasks | Time |
|-------|-------|------|
| Phase 1 | File Consolidation | 2.5-3.5 hours |
| Phase 2 | Documentation | 1 hour |
| Phase 3 | Cleanup | 2.5 hours |
| **Total** | | **6-7 hours** |

---

## Success Criteria

- [ ] All v1.0 cross-system mappings archived
- [ ] Pointer files created
- [ ] mappings/README.md complete
- [ ] No duplicate files outside archive/
- [ ] Documentation cross-references work
- [ ] Root directory clean
- [ ] Git committed with clear messages
- [ ] v2.0.1 tagged

---

## Risk Assessment

**Low Risk:**
- Creating pointers (reversible)
- Documentation updates (non-breaking)

**Medium Risk:**
- Archiving v1.0 (check references first)
- Moving root files (may break paths)

**Mitigation:**
1. Search references before archiving
2. Create pointers before archiving
3. Test canonical locations work
4. Commit incrementally

---

## Recommended Session Plan

- **Session 1** (3 hours): Phase 1 (Tasks 1-3)
- **Session 2** (1 hour): Phase 2 (Tasks 4-5)
- **Session 3** (2.5 hours): Phase 3 (Tasks 6-8)

---

**Created**: 2026-01-16  
**Status**: Ready for execution  
**Location**: `docs/merge/`
