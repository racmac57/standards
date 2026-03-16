# Detailed Merge Assessment

**Date**: 2026-01-16  
**Status**: Merge 70% complete
**Last Updated**: After file comparison analysis

---

## Overview

Merge between `Standards/` and `unified_data_dictionary/` initiated 2026-01-15 (v2.0.0). File consolidation incomplete.

---

## Key Finding

**File comparison shows UDD contains OLD versions (v1.0, 2025-12-16) while canonical locations have NEW versions (v2.0, 2025-12-30).**

These are NOT duplicates but outdated versions to update or archive.

---

## What Was Completed ✅

### Repository Structure (2026-01-15)
- [x] Removed nested `.git/` from unified_data_dictionary/
- [x] Single `.git/` at root level
- [x] Backup saved to archive/legacy_copies/udd_git_backup/

### Canonical Locations Established
- [x] cad_to_rms_field_map.json → CAD_RMS/DataDictionary/current/schema/
- [x] rms_to_cad_field_map.json → CAD_RMS/DataDictionary/current/schema/
- [x] multi_column_matching_strategy.md → CAD_RMS/DataDictionary/current/schema/
- [x] rms_export_field_definitions.md → RMS/DataDictionary/current/schema/
- [x] cad_export_field_definitions.md → CAD/DataDictionary/current/schema/

### Pointer Files Created
- [x] unified_data_dictionary/mappings/multi_column_matching_strategy_POINTER.md
- [x] unified_data_dictionary/docs/rms_export_field_definitions_POINTER.md

### Archive Structure
- [x] Archive directory created with subdirectories
- [x] Legacy files moved to archive/legacy_copies/

---

## Remaining Tasks 🔴

### 1. Version Reconciliation ⚠️ CRITICAL

**Cross-System Mappings - Version Mismatch:**

`cad_to_rms_field_map_latest.json`:
- **UDD**: v1.0 (2025-12-16), simple join
- **Canonical**: v2.0 (2025-12-30), multi-column matching
- **Hash**: Different (2A277BE... vs 12CBA96...)
- **Action**: Archive v1.0, create pointer to v2.0

`rms_to_cad_field_map_latest.json`:
- **Status**: Needs version comparison
- **Action**: Compare with canonical, archive if outdated

**System-Specific Field Maps - UNIQUE (Keep):**

`cad_field_map_latest.json`:
- **Purpose**: CAD raw → internal → ESRI names
- **Unique to**: CAD_Data_Cleaning_Engine
- **Action**: Keep (not duplicate)

`rms_field_map_latest.json`:
- **Purpose**: RMS field definitions
- **Unique to**: Unified data dictionary
- **Action**: Keep (system-specific)

**Supporting Files - Need Review:**
- ⚠️ cad_field_map_v2.json - Check if duplicate
- ⚠️ cad_rms_merge_policy_latest.json - Unknown purpose
- ⚠️ cad_to_rms_mapping.csv - CSV version?
- ⚠️ rms_to_cad_mapping.csv - CSV version?

**Action Required:**
1. Archive outdated v1.0 cross-system mappings
2. Create pointer files to canonical v2.0
3. Document retained files in README.md
4. Version audit for all `*_v2.json` and `*_latest.json`

---

### 2. Enhanced Documentation Files

Check these files:
- `cad_to_rms_field_map_v2_enhanced.md`
- `rms_to_cad_field_map_v2_enhanced.md`

**Action:**
1. Check if documentation for v1.0 or v2.0
2. If v2.0, move to canonical location
3. If v1.0, archive with v1.0 files

---

### 3. Create mappings/README.md

**Action:**
Create `unified_data_dictionary/mappings/README.md` explaining:
- Pointer files to canonical v2.0
- System-specific files (unique, retained)
- General documentation
- Version history

---

### 4. Documentation Updates

**Action:**
1. Update CHANGELOG.md with completion status
2. Verify SUMMARY.md reflects current structure
3. Update README.md if needed

---

## File Comparison Results

### Cross-System Mappings (Canonical in CAD_RMS/)

| Canonical (v2.0) | UDD (v1.0) | Relationship | Action |
|------------------|------------|--------------|--------|
| cad_to_rms_field_map.json | mappings/cad_to_rms_field_map_latest.json | Different versions | Archive v1.0, create pointer |
| rms_to_cad_field_map.json | mappings/rms_to_cad_field_map_latest.json | Needs comparison | Compare, archive if outdated |
| multi_column_matching_strategy.md | mappings/multi_column_matching_strategy_POINTER.md | ✅ Pointer exists | Done |

### System-Specific Maps (UNIQUE - Keep)

| File | Version | Purpose | Action |
|------|---------|---------|--------|
| cad_field_map_latest.json | v1.0 (2025-12-16) | CAD internal structure | ✅ Keep |
| rms_field_map_latest.json | v1.0 (2025-12-16) | RMS internal structure | ✅ Keep |
| mapping_rules.md | v1.0.0 (2025-12-17) | Strategy documentation | ✅ Keep |

### Documentation Pointers

| Canonical | UDD Pointer | Status |
|-----------|-------------|--------|
| RMS/.../rms_export_field_definitions.md | docs/rms_export_field_definitions_POINTER.md | ✅ Done |
| CAD/.../cad_export_field_definitions.md | Not needed | N/A |

---

## Priority Tasks

### Priority 1 (Critical)
1. Create pointer files for confirmed duplicates
2. Remove/archive duplicate JSON files

### Priority 2 (Important)
1. Compare and verify other mapping files
2. Create mappings README
3. Update CHANGELOG.md

### Priority 3 (Documentation)
1. Verify canonical locations correct
2. Update cross-references
3. Create migration guide if needed

---

## Questions RESOLVED ✅

1. ✅ **Are `*_latest.json` identical to canonical?**
   - NO - v1.0 vs v2.0
   - Hash: 2A277BE... ≠ 12CBA96...
   - v2.0 adds multi-column matching

2. ⚠️ **Should `*_v2_enhanced.md` be merged or kept?**
   - Need content review

3. ⚠️ **Are CSV mapping files duplicates or unique?**
   - Need to check

4. ⚠️ **Do scripts reference old paths?**
   - Need to grep before archiving

## NEW Questions

5. Should v1.0 be preserved for backward compatibility?
6. Are ETL scripts using v1.0 structure?
7. Should we create migration guide for v1.0→v2.0?

---

## Pointer File Template

```markdown
# File Archived - Use Canonical Location

This file (v1.0, 2025-12-16) archived. Use canonical v2.0:

## Canonical Location
- Path: ../../CAD_RMS/DataDictionary/current/schema/cad_to_rms_field_map.json
- Version: 2.0 (2025-12-30)
- Enhancements: Multi-column matching, confidence scoring

## Archived Location
- v1.0: ../../archive/legacy_copies/v1.0_mappings/cad_to_rms_field_map_latest.json
- Retention: 30 days
```

---

**Created**: 2026-01-16  
**Next Review**: After Priority 1 tasks complete  
**Location**: `docs/merge/`
