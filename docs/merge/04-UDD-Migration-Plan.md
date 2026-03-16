# UDD to Standards Root - Migration Plan

**Date**: 2026-01-16  
**Goal**: Flatten unified_data_dictionary structure by moving/merging files to Standards root  
**Status**: READY FOR EXECUTION

---

## Overview

The `unified_data_dictionary/` subdirectory contains a Python project (v0.2.3) with schema extraction, dictionary building, and documentation generation tools. You want to integrate this functionality at the Standards root level while preserving the organizational structure.

---

## Current UDD Structure

```
unified_data_dictionary/
├── src/               # Python source (8 files)
├── schemas/           # JSON schemas (9 files)
├── mappings/          # Field mappings (12 files, including pointers)
├── scripts/           # Utility scripts
├── docs/              # Documentation (167+ files with chatlogs)
├── tests/             # Python tests (5 files)
├── templates/         # Reusable templates
├── data/              # Sample & test data
├── examples/          # Usage examples
├── validators/        # Validation scripts
└── [config files]     # README, CHANGELOG, etc.
```

---

## Migration Strategy

### Phase 1: Merge Overlapping Directories ⚡ HIGH PRIORITY

#### 1.1 Merge `docs/` → `Standards/docs/`

**Current State:**
- `Standards/docs/` has: call_type_category_mapping.md, merge/
- `UDD/docs/` has: 167+ files (chatlogs, setup, planning, workflows, maintenance)

**Action:**
```powershell
# Keep both but organize
# UDD docs are project-specific, Standards docs are general
mv unified_data_dictionary/docs/ docs/unified_data_dictionary/
```

**Result:** 
- `Standards/docs/call_type_category_mapping.md` (keep)
- `Standards/docs/merge/` (keep)
- `Standards/docs/unified_data_dictionary/` (UDD project docs)

---

#### 1.2 Merge `mappings/` → `Standards/mappings/`

**Current State:**
- `Standards/mappings/` has: 11 call_types_*.csv files, call_type_category_mapping.json
- `UDD/mappings/` has: 12 files (field maps, pointers, mapping_rules.md)

**Action:**
```powershell
# Move UDD mappings to Standards/mappings/field_mappings/
mkdir Standards/mappings/field_mappings
mv unified_data_dictionary/mappings/* Standards/mappings/field_mappings/
```

**Result:**
- `Standards/mappings/call_types_*.csv` (call type classifications)
- `Standards/mappings/call_type_category_mapping.json` (call type lookup)
- `Standards/mappings/field_mappings/` (UDD field mappings)

---

#### 1.3 Merge `scripts/` → `Standards/scripts/`

**Current State:**
- `Standards/` root has: validate_rms_export.py, extract_narrative_fields.py (loose)
- `UDD/scripts/` has: cleanup/, processing/, tests/, utilities/, Process_UDD_Chatlog.bat, README.md

**Action:**
```powershell
# Create organized scripts structure
mkdir Standards/scripts/validation
mkdir Standards/scripts/extraction
mkdir Standards/scripts/processing
mkdir Standards/scripts/utilities

# Move root-level scripts
mv Standards/validate_rms_export.py Standards/scripts/validation/
mv Standards/extract_narrative_fields.py Standards/scripts/extraction/

# Move UDD scripts
mv unified_data_dictionary/scripts/* Standards/scripts/
```

**Result:**
- `Standards/scripts/validation/` - Validation scripts
- `Standards/scripts/extraction/` - Extraction scripts
- `Standards/scripts/processing/` - Processing scripts (from UDD)
- `Standards/scripts/utilities/` - Utility scripts (from UDD)
- `Standards/scripts/cleanup/` - Cleanup scripts (from UDD)
- `Standards/scripts/tests/` - Test scripts (from UDD)

---

### Phase 2: Move Python Project Components 🔵 MEDIUM PRIORITY

#### 2.1 Move `src/` → `Standards/src/`

**Action:**
```powershell
# Move Python source code to root
mv unified_data_dictionary/src/ Standards/src/
```

**Files (8 total):**
- cli.py - Command-line interface
- extract_from_repos.py - Schema extraction
- build_dictionary.py - Dictionary building
- generate_excel_output.py - Excel generation
- standardize_cads.py - CAD standardization
- extract_rules_from_repo.py - Rule extraction
- (2 more Python files)

---

#### 2.2 Move `tests/` → `Standards/tests/`

**Action:**
```powershell
mv unified_data_dictionary/tests/ Standards/tests/
```

**Files (5 total):**
- test_join_keys.py
- test_datetime_parsing.py
- test_coordinate_validation.py
- test_allowed_values.py
- (1 more test file)

---

#### 2.3 Move `validators/` → `Standards/validators/`

**Action:**
```powershell
mv unified_data_dictionary/validators/ Standards/validators/
```

**Files:**
- run_validation_benchmarks.py

---

#### 2.4 Move `schemas/` → `Standards/schemas/`

**Current State:**
- `Standards/schemas/` might not exist or has different content
- `UDD/schemas/` has: 8 JSON files, 1 YAML file

**Action:**
```powershell
# Check if Standards/schemas exists
# If not, move directly
# If yes, create subfolder
mv unified_data_dictionary/schemas/ Standards/schemas/
# OR
mv unified_data_dictionary/schemas/ Standards/schemas/udd_schemas/
```

---

### Phase 3: Move Supporting Directories 🟢 LOW PRIORITY

#### 3.1 Move `templates/` → `Standards/templates/`

**Action:**
```powershell
mv unified_data_dictionary/templates/ Standards/templates/
```

**Contents:**
- configs/, mappings/, schemas/, README.md

---

#### 3.2 Move `data/` → `Standards/data/`

**Action:**
```powershell
mv unified_data_dictionary/data/ Standards/data/
```

**Contents:**
- sample/, test/, README.md

---

#### 3.3 Move `examples/` → `Standards/examples/`

**Action:**
```powershell
mv unified_data_dictionary/examples/ Standards/examples/
```

**Contents:**
- api/, cli/, README.md

---

### Phase 4: Merge Configuration Files ⚡ HIGH PRIORITY

#### 4.1 Python Package Files

**Move to root:**
```powershell
mv unified_data_dictionary/pyproject.toml Standards/
mv unified_data_dictionary/requirements.txt Standards/requirements_udd.txt
mv unified_data_dictionary/config.yaml Standards/
mv unified_data_dictionary/Makefile Standards/
mv unified_data_dictionary/LICENSE Standards/LICENSE_UDD
```

**Note:** Standards/ already has requirements.txt, so rename UDD version or merge them.

---

#### 4.2 Workspace Files

**Decision needed:**
- `unified_data_dictionary.code-workspace` - Keep or delete?
- `unified_data_dictionary.egg-info/` - Can delete (Python build artifact)
- `tree_report_error.log` - Can delete

---

#### 4.3 Documentation Files

**Merge or keep separate:**
- `unified_data_dictionary/README.md` → Merge with `Standards/README.md`
- `unified_data_dictionary/CHANGELOG.md` → Keep as `Standards/CHANGELOG_UDD.md`
- `unified_data_dictionary/SUMMARY.md` → Keep as `Standards/docs/unified_data_dictionary/SUMMARY.md`
- `unified_data_dictionary/release_notes.md` → Keep as `Standards/docs/unified_data_dictionary/release_notes.md`
- Directory tree files → Move to `Standards/docs/unified_data_dictionary/`

---

## Migration Script

```powershell
# UDD to Standards Root Migration Script
# Date: 2026-01-16
# Run from Standards directory

$baseDir = "C:\Users\carucci_r\OneDrive - City of Hackensack\09_Reference\Standards"
cd $baseDir

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "UDD to Standards Root Migration" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# PHASE 1: Merge Overlapping Directories

Write-Host "Phase 1: Merging overlapping directories..." -ForegroundColor Yellow

# 1.1 Merge docs
Write-Host "  - Moving UDD docs..." -ForegroundColor Green
New-Item -ItemType Directory -Path "docs\unified_data_dictionary" -Force | Out-Null
Move-Item "unified_data_dictionary\docs\*" "docs\unified_data_dictionary\" -Force

# 1.2 Merge mappings
Write-Host "  - Moving UDD mappings..." -ForegroundColor Green
New-Item -ItemType Directory -Path "mappings\field_mappings" -Force | Out-Null
Move-Item "unified_data_dictionary\mappings\*" "mappings\field_mappings\" -Force

# 1.3 Merge scripts
Write-Host "  - Organizing scripts..." -ForegroundColor Green
New-Item -ItemType Directory -Path "scripts\validation" -Force | Out-Null
New-Item -ItemType Directory -Path "scripts\extraction" -Force | Out-Null

# Move root-level scripts
Move-Item "validate_rms_export.py" "scripts\validation\" -Force
Move-Item "extract_narrative_fields.py" "scripts\extraction\" -Force

# Move UDD scripts
Move-Item "unified_data_dictionary\scripts\*" "scripts\" -Force

# PHASE 2: Move Python Components

Write-Host "`nPhase 2: Moving Python components..." -ForegroundColor Yellow

Write-Host "  - Moving src..." -ForegroundColor Green
Move-Item "unified_data_dictionary\src" "src" -Force

Write-Host "  - Moving tests..." -ForegroundColor Green
Move-Item "unified_data_dictionary\tests" "tests" -Force

Write-Host "  - Moving validators..." -ForegroundColor Green
Move-Item "unified_data_dictionary\validators" "validators" -Force

Write-Host "  - Moving schemas..." -ForegroundColor Green
Move-Item "unified_data_dictionary\schemas" "schemas" -Force

# PHASE 3: Move Supporting Directories

Write-Host "`nPhase 3: Moving supporting directories..." -ForegroundColor Yellow

Write-Host "  - Moving templates..." -ForegroundColor Green
Move-Item "unified_data_dictionary\templates" "templates" -Force

Write-Host "  - Moving data..." -ForegroundColor Green
Move-Item "unified_data_dictionary\data" "data" -Force

Write-Host "  - Moving examples..." -ForegroundColor Green
Move-Item "unified_data_dictionary\examples" "examples" -Force

# PHASE 4: Merge Configuration Files

Write-Host "`nPhase 4: Merging configuration files..." -ForegroundColor Yellow

Write-Host "  - Moving Python package files..." -ForegroundColor Green
Move-Item "unified_data_dictionary\pyproject.toml" "pyproject.toml" -Force
Move-Item "unified_data_dictionary\requirements.txt" "requirements_udd.txt" -Force
Move-Item "unified_data_dictionary\config.yaml" "config.yaml" -Force
Move-Item "unified_data_dictionary\Makefile" "Makefile" -Force
Move-Item "unified_data_dictionary\LICENSE" "LICENSE_UDD" -Force

Write-Host "  - Moving documentation files..." -ForegroundColor Green
Move-Item "unified_data_dictionary\CHANGELOG.md" "CHANGELOG_UDD.md" -Force
Move-Item "unified_data_dictionary\SUMMARY.md" "docs\unified_data_dictionary\SUMMARY.md" -Force
Move-Item "unified_data_dictionary\release_notes.md" "docs\unified_data_dictionary\release_notes.md" -Force
Move-Item "unified_data_dictionary\2025_12_30_unified_data_dictionary_directory_tree.*" "docs\unified_data_dictionary\" -Force

# PHASE 5: Cleanup

Write-Host "`nPhase 5: Cleanup..." -ForegroundColor Yellow

# Delete build artifacts
Write-Host "  - Removing build artifacts..." -ForegroundColor Green
Remove-Item "unified_data_dictionary\unified_data_dictionary.egg-info" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item "unified_data_dictionary\tree_report_error.log" -Force -ErrorAction SilentlyContinue
Remove-Item "unified_data_dictionary\unified_data_dictionary.code-workspace" -Force -ErrorAction SilentlyContinue
Remove-Item "unified_data_dictionary\.gitignore" -Force -ErrorAction SilentlyContinue

# Archive empty UDD directory
Write-Host "  - Archiving empty UDD directory..." -ForegroundColor Green
if ((Get-ChildItem "unified_data_dictionary" -Force).Count -eq 0) {
    Remove-Item "unified_data_dictionary" -Force
    Write-Host "    ✓ UDD directory removed (empty)" -ForegroundColor Green
} else {
    Write-Host "    ⚠ UDD directory not empty, check contents:" -ForegroundColor Yellow
    Get-ChildItem "unified_data_dictionary" -Force | Select-Object Name
}

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "Migration Complete!" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Review migrated files" -ForegroundColor White
Write-Host "2. Merge README files manually" -ForegroundColor White
Write-Host "3. Merge requirements.txt with requirements_udd.txt" -ForegroundColor White
Write-Host "4. Update path references in scripts" -ForegroundColor White
Write-Host "5. Test Python package installation" -ForegroundColor White
Write-Host "6. Commit changes to git`n" -ForegroundColor White
```

---

## Post-Migration Tasks

### 1. Merge README Files
Manually combine:
- `Standards/README.md` (current)
- `unified_data_dictionary/README.md` (UDD content)

Add UDD sections to Standards README.

### 2. Merge requirements.txt
Compare and merge:
- `Standards/requirements.txt`
- `Standards/requirements_udd.txt`

Remove duplicates, keep all unique dependencies.

### 3. Update Path References
Search and replace old paths in all Python scripts:
- `unified_data_dictionary/` → `./` or appropriate relative path

### 4. Test Python Package
```powershell
cd Standards
pip install -e .
# Test CLI if it was working
```

### 5. Update Documentation
- Update all internal links in docs
- Update CHANGELOG to reflect migration
- Create migration note in docs/merge/

---

##Conflicting Files Resolution

| File | Standards Version | UDD Version | Resolution |
|------|-------------------|-------------|------------|
| `requirements.txt` | Exists | Exists | Merge, rename UDD to requirements_udd.txt temporarily |
| `README.md` | Exists | Exists | Merge content, UDD sections into Standards README |
| `CHANGELOG.md` | Exists | Exists | Keep separate as CHANGELOG_UDD.md |
| `SUMMARY.md` | Exists | Exists | Move UDD to docs/unified_data_dictionary/ |

---

## NIBRS Files Planning

You mentioned adding NIBRS files. After migration, the structure will be:

```
Standards/
├── CAD/
├── RMS/
├── CAD_RMS/
├── NIBRS/           ← Add NIBRS content here
│   ├── DataDictionary/
│   ├── SCRPA/
│   └── ...
├── FBI_UCR/
├── StateReporting/
├── CALEA/
└── [UDD components now at root]
```

---

## Timeline Estimate

| Phase | Duration |
|-------|----------|
| Phase 1 (Merge directories) | 30 min |
| Phase 2 (Python components) | 15 min |
| Phase 3 (Supporting dirs) | 15 min |
| Phase 4 (Config files) | 30 min |
| Phase 5 (Cleanup) | 15 min |
| Post-migration tasks | 1-2 hours |
| **Total** | **2.5-3.5 hours** |

---

**Status**: Ready to execute
**Created**: 2026-01-16
**Recommendation**: Run script, then handle post-migration tasks manually
