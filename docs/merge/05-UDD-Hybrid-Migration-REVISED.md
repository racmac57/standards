# UDD Hybrid Migration Plan (REVISED)

**Date**: 2026-01-16  
**Approach**: Hybrid - Keep UDD as tool, extract reference data  
**Status**: READY FOR EXECUTION

---

## 🎯 Strategy Overview

**Goal**: Separate the UDD Python tool from its reference data outputs.

**Key Principle**: 
- **Tools** = Development code (stays cohesive in `tools/`)
- **Reference Data** = Schemas, mappings, generated docs (moves to Standards root)

---

## 📋 What Goes Where

### Keep in `tools/unified_data_dictionary/` (Functional Python Package)
✅ All Python development files:
- `src/` - Python source code
- `tests/` - Unit tests  
- `pyproject.toml` - Package config
- `Makefile` - Build automation
- `requirements.txt` - Dependencies (UDD-specific)
- `config.yaml` - Tool configuration
- `setup.py` / `.egg-info` - Package metadata
- `.gitignore` - Tool-specific ignores
- `examples/` - Tool usage examples
- `README.md` - Tool documentation
- `CHANGELOG.md` - Tool version history

### Move to Standards Root (Reference Data)
📤 Reference/output data:
- `schemas/` → `Standards/schemas/udd/`
- `mappings/` → `Standards/mappings/field_mappings/`
- `templates/` → `Standards/templates/udd/`
- `data/sample/` → `Standards/data/samples/`
- `data/test/` → `Standards/data/test/`
- Generated docs → `Standards/docs/generated/`
- Tool docs → `Standards/docs/tools/udd/`
- Chatlogs → `Standards/docs/tools/udd/chatlogs/`

### Organize Root-Level Scripts
📁 Create organized script structure:
- `validate_rms_export.py` → `Standards/scripts/validation/`
- `extract_narrative_fields.py` → `Standards/scripts/extraction/`
- `rms_field_dictionary.html` → `Standards/docs/html/`
- `sample_rms_export.csv` → `Standards/data/samples/rms/`

---

## 🔧 Migration Steps

### Phase 1: Create New Directory Structure ⚡

```powershell
# Create tools directory
New-Item -ItemType Directory -Path "tools" -Force

# Create organized directories at root
New-Item -ItemType Directory -Path "schemas\udd" -Force
New-Item -ItemType Directory -Path "mappings\field_mappings" -Force
New-Item -ItemType Directory -Path "templates\udd" -Force
New-Item -ItemType Directory -Path "data\samples\rms" -Force
New-Item -ItemType Directory -Path "data\test" -Force
New-Item -ItemType Directory -Path "docs\generated" -Force
New-Item -ItemType Directory -Path "docs\tools\udd" -Force
New-Item -ItemType Directory -Path "docs\html" -Force
New-Item -ItemType Directory -Path "scripts\validation" -Force
New-Item -ItemType Directory -Path "scripts\extraction" -Force
New-Item -ItemType Directory -Path "scripts\processing" -Force
New-Item -ItemType Directory -Path "scripts\utilities" -Force
```

---

### Phase 2: Extract Reference Data 🔵

```powershell
# Move schemas (reference data)
Copy-Item "unified_data_dictionary\schemas\*" "schemas\udd\" -Recurse -Force

# Move mappings (except pointers - those stay with tool)
Copy-Item "unified_data_dictionary\mappings\*" "mappings\field_mappings\" -Recurse -Force

# Move templates
Copy-Item "unified_data_dictionary\templates\*" "templates\udd\" -Recurse -Force

# Move sample/test data
Copy-Item "unified_data_dictionary\data\sample\*" "data\samples\" -Recurse -Force -ErrorAction SilentlyContinue
Copy-Item "unified_data_dictionary\data\test\*" "data\test\" -Recurse -Force -ErrorAction SilentlyContinue
```

---

### Phase 3: Organize Documentation 📚

```powershell
# Move generated/output documentation
$genDocs = @(
    "2025_12_30_unified_data_dictionary_directory_tree.json",
    "2025_12_30_unified_data_dictionary_directory_tree.md",
    "release_notes.md",
    "SUMMARY.md"
)

foreach ($doc in $genDocs) {
    if (Test-Path "unified_data_dictionary\$doc") {
        Move-Item "unified_data_dictionary\$doc" "docs\generated\" -Force
    }
}

# Move tool documentation
Copy-Item "unified_data_dictionary\docs\*" "docs\tools\udd\" -Recurse -Force

# Move chatlogs to tool docs
Move-Item "docs\tools\udd\chatlogs" "docs\tools\udd\chatlogs" -Force
```

---

### Phase 4: Organize Root-Level Files 🗂️

```powershell
# Move standalone scripts to organized structure
Move-Item "validate_rms_export.py" "scripts\validation\" -Force
Move-Item "extract_narrative_fields.py" "scripts\extraction\" -Force

# Move HTML documentation
Move-Item "rms_field_dictionary.html" "docs\html\" -Force

# Move sample data
Move-Item "sample_rms_export.csv" "data\samples\rms\" -Force
```

---

### Phase 5: Relocate UDD Tool 🔨

```powershell
# Move entire UDD directory to tools/
Move-Item "unified_data_dictionary" "tools\unified_data_dictionary" -Force

# Clean up extracted reference data from tool directory
Remove-Item "tools\unified_data_dictionary\schemas" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item "tools\unified_data_dictionary\templates" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item "tools\unified_data_dictionary\data\sample" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item "tools\unified_data_dictionary\data\test" -Recurse -Force -ErrorAction SilentlyContinue

# Remove docs that were moved
Remove-Item "tools\unified_data_dictionary\docs" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item "tools\unified_data_dictionary\2025_12_30*" -Force -ErrorAction SilentlyContinue
Remove-Item "tools\unified_data_dictionary\release_notes.md" -Force -ErrorAction SilentlyContinue
Remove-Item "tools\unified_data_dictionary\SUMMARY.md" -Force -ErrorAction SilentlyContinue
```

---

### Phase 6: Update UDD Configuration 📝

```powershell
# Create config file that points to Standards data locations
$configContent = @"
# UDD Tool Configuration
# Updated: 2026-01-16
# Paths relative to Standards root

[paths]
schemas_dir = "../schemas/udd"
mappings_dir = "../mappings/field_mappings"
templates_dir = "../templates/udd"
output_dir = "../docs/generated"
sample_data_dir = "../data/samples"
test_data_dir = "../data/test"

[tool]
name = "Unified Data Dictionary"
version = "0.2.3"
location = "tools/unified_data_dictionary"
"@

$configContent | Out-File "tools\unified_data_dictionary\standards_paths.ini" -Encoding UTF8
```

---

## 📜 Complete Migration Script

```powershell
# ============================================
# UDD HYBRID MIGRATION SCRIPT
# Date: 2026-01-16
# Approach: Keep tool cohesive, extract data
# ============================================

$ErrorActionPreference = "Continue"
$baseDir = "C:\Users\carucci_r\OneDrive - City of Hackensack\09_Reference\Standards"
cd $baseDir

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "UDD HYBRID MIGRATION" -ForegroundColor Cyan
Write-Host "Tool stays cohesive, data extracted" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# ============================================
# PHASE 1: Create Directory Structure
# ============================================

Write-Host "PHASE 1: Creating directory structure..." -ForegroundColor Yellow

$directories = @(
    "tools",
    "schemas\udd",
    "mappings\field_mappings",
    "templates\udd",
    "data\samples\rms",
    "data\test",
    "docs\generated",
    "docs\tools\udd",
    "docs\html",
    "scripts\validation",
    "scripts\extraction",
    "scripts\processing",
    "scripts\utilities"
)

foreach ($dir in $directories) {
    New-Item -ItemType Directory -Path $dir -Force | Out-Null
    Write-Host "  ✓ Created: $dir" -ForegroundColor Green
}

# ============================================
# PHASE 2: Extract Reference Data
# ============================================

Write-Host "`nPHASE 2: Extracting reference data..." -ForegroundColor Yellow

# Schemas
if (Test-Path "unified_data_dictionary\schemas") {
    Copy-Item "unified_data_dictionary\schemas\*" "schemas\udd\" -Recurse -Force
    Write-Host "  ✓ Schemas extracted" -ForegroundColor Green
}

# Mappings
if (Test-Path "unified_data_dictionary\mappings") {
    Copy-Item "unified_data_dictionary\mappings\*" "mappings\field_mappings\" -Recurse -Force
    Write-Host "  ✓ Mappings extracted" -ForegroundColor Green
}

# Templates
if (Test-Path "unified_data_dictionary\templates") {
    Copy-Item "unified_data_dictionary\templates\*" "templates\udd\" -Recurse -Force
    Write-Host "  ✓ Templates extracted" -ForegroundColor Green
}

# Sample/Test Data
if (Test-Path "unified_data_dictionary\data\sample") {
    Copy-Item "unified_data_dictionary\data\sample\*" "data\samples\" -Recurse -Force
    Write-Host "  ✓ Sample data extracted" -ForegroundColor Green
}

if (Test-Path "unified_data_dictionary\data\test") {
    Copy-Item "unified_data_dictionary\data\test\*" "data\test\" -Recurse -Force
    Write-Host "  ✓ Test data extracted" -ForegroundColor Green
}

# ============================================
# PHASE 3: Organize Documentation
# ============================================

Write-Host "`nPHASE 3: Organizing documentation..." -ForegroundColor Yellow

# Generated/output docs
$genDocs = @(
    "2025_12_30_unified_data_dictionary_directory_tree.json",
    "2025_12_30_unified_data_dictionary_directory_tree.md",
    "release_notes.md",
    "SUMMARY.md"
)

foreach ($doc in $genDocs) {
    if (Test-Path "unified_data_dictionary\$doc") {
        Copy-Item "unified_data_dictionary\$doc" "docs\generated\" -Force
        Write-Host "  ✓ Moved: $doc" -ForegroundColor Green
    }
}

# Tool documentation
if (Test-Path "unified_data_dictionary\docs") {
    Copy-Item "unified_data_dictionary\docs\*" "docs\tools\udd\" -Recurse -Force
    Write-Host "  ✓ Tool docs moved" -ForegroundColor Green
}

# ============================================
# PHASE 4: Organize Root-Level Files
# ============================================

Write-Host "`nPHASE 4: Organizing root-level files..." -ForegroundColor Yellow

# Scripts
if (Test-Path "validate_rms_export.py") {
    Move-Item "validate_rms_export.py" "scripts\validation\" -Force
    Write-Host "  ✓ Moved: validate_rms_export.py" -ForegroundColor Green
}

if (Test-Path "extract_narrative_fields.py") {
    Move-Item "extract_narrative_fields.py" "scripts\extraction\" -Force
    Write-Host "  ✓ Moved: extract_narrative_fields.py" -ForegroundColor Green
}

# HTML docs
if (Test-Path "rms_field_dictionary.html") {
    Move-Item "rms_field_dictionary.html" "docs\html\" -Force
    Write-Host "  ✓ Moved: rms_field_dictionary.html" -ForegroundColor Green
}

# Sample data
if (Test-Path "sample_rms_export.csv") {
    Move-Item "sample_rms_export.csv" "data\samples\rms\" -Force
    Write-Host "  ✓ Moved: sample_rms_export.csv" -ForegroundColor Green
}

# ============================================
# PHASE 5: Relocate UDD Tool
# ============================================

Write-Host "`nPHASE 5: Relocating UDD tool..." -ForegroundColor Yellow

# Move entire UDD to tools/
Move-Item "unified_data_dictionary" "tools\unified_data_dictionary" -Force
Write-Host "  ✓ UDD moved to tools/" -ForegroundColor Green

# Clean up extracted data from tool directory
Write-Host "  - Cleaning extracted data from tool..." -ForegroundColor Gray

$cleanupPaths = @(
    "tools\unified_data_dictionary\schemas",
    "tools\unified_data_dictionary\templates",
    "tools\unified_data_dictionary\data\sample",
    "tools\unified_data_dictionary\data\test",
    "tools\unified_data_dictionary\docs",
    "tools\unified_data_dictionary\2025_12_30_unified_data_dictionary_directory_tree.json",
    "tools\unified_data_dictionary\2025_12_30_unified_data_dictionary_directory_tree.md",
    "tools\unified_data_dictionary\release_notes.md",
    "tools\unified_data_dictionary\SUMMARY.md"
)

foreach ($path in $cleanupPaths) {
    if (Test-Path $path) {
        Remove-Item $path -Recurse -Force -ErrorAction SilentlyContinue
        $fileName = Split-Path $path -Leaf
        Write-Host "    ✓ Removed: $fileName (now at Standards root)" -ForegroundColor Gray
    }
}

# ============================================
# PHASE 6: Create Tool Configuration
# ============================================

Write-Host "`nPHASE 6: Creating tool configuration..." -ForegroundColor Yellow

$configContent = @"
# UDD Tool Configuration
# Updated: 2026-01-16
# Paths relative to Standards root

[paths]
# Reference data locations (now at Standards root)
schemas_dir = "../../schemas/udd"
mappings_dir = "../../mappings/field_mappings"
templates_dir = "../../templates/udd"
output_dir = "../../docs/generated"
sample_data_dir = "../../data/samples"
test_data_dir = "../../data/test"

# Tool paths
tool_docs = "../../docs/tools/udd"
chatlogs = "../../docs/tools/udd/chatlogs"

[tool]
name = "Unified Data Dictionary"
version = "0.2.3"
location = "tools/unified_data_dictionary"
install_cmd = "pip install -e ."

[notes]
# This tool is maintained as a cohesive Python package
# Reference data has been extracted to Standards root
# Tool can be updated independently from Standards content
"@

$configContent | Out-File "tools\unified_data_dictionary\standards_paths.ini" -Encoding UTF8
Write-Host "  ✓ Created: standards_paths.ini" -ForegroundColor Green

# ============================================
# PHASE 7: Create Tool README
# ============================================

Write-Host "`nPHASE 7: Creating tool README..." -ForegroundColor Yellow

$toolReadme = @"
# UDD Tool Location

The Unified Data Dictionary Python tool has been moved to:
``````
tools/unified_data_dictionary/
``````

## About This Structure

**Standards/** = Reference data, schemas, documentation (the "what")
**tools/** = Development tools, code, packages (the "how")

The UDD tool generates and processes Standards reference data.

## Using the Tool

``````powershell
# Install the tool
cd tools/unified_data_dictionary
pip install -e .

# Use CLI
udd --help
udd status
``````

## Reference Data Locations

The UDD tool now references data at Standards root:
- **Schemas**: ``schemas/udd/``
- **Mappings**: ``mappings/field_mappings/``
- **Templates**: ``templates/udd/``
- **Generated Docs**: ``docs/generated/``
- **Tool Docs**: ``docs/tools/udd/``

See ``standards_paths.ini`` for complete path configuration.

## Updating the Tool

The tool can be updated independently:
1. Pull updates from UDD GitHub repo
2. Tool stays in ``tools/unified_data_dictionary/``
3. Reference data stays at Standards root

---

**Last Updated**: 2026-01-16
"@

$toolReadme | Out-File "tools\README.md" -Encoding UTF8
Write-Host "  ✓ Created: tools/README.md" -ForegroundColor Green

# ============================================
# COMPLETION
# ============================================

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "MIGRATION COMPLETE!" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

Write-Host "Summary:" -ForegroundColor Yellow
Write-Host "  ✓ UDD tool: tools/unified_data_dictionary/" -ForegroundColor Green
Write-Host "  ✓ Schemas: schemas/udd/" -ForegroundColor Green
Write-Host "  ✓ Mappings: mappings/field_mappings/" -ForegroundColor Green
Write-Host "  ✓ Scripts: scripts/[organized]/" -ForegroundColor Green
Write-Host "  ✓ Docs: docs/[organized]/" -ForegroundColor Green

Write-Host "`nNext Steps:" -ForegroundColor Yellow
Write-Host "  1. Test UDD tool installation" -ForegroundColor White
Write-Host "     cd tools/unified_data_dictionary" -ForegroundColor Gray
Write-Host "     pip install -e ." -ForegroundColor Gray
Write-Host "`n  2. Update any hardcoded paths in Python scripts" -ForegroundColor White
Write-Host "`n  3. Merge requirements files if needed" -ForegroundColor White
Write-Host "     - Standards/requirements.txt" -ForegroundColor Gray
Write-Host "     - tools/unified_data_dictionary/requirements.txt" -ForegroundColor Gray
Write-Host "`n  4. Add NIBRS content to Standards/NIBRS/" -ForegroundColor White
Write-Host "`n  5. Commit changes to git" -ForegroundColor White

Write-Host "`n========================================`n" -ForegroundColor Cyan
```

---

## 📁 Final Structure

```
Standards/
├── CAD/
│   ├── DataDictionary/
│   └── SCRPA/
├── RMS/
│   ├── DataDictionary/
│   └── SCRPA/
├── CAD_RMS/
│   └── DataDictionary/
├── NIBRS/                           ← Ready for your content
│   └── [your NIBRS files]
├── FBI_UCR/
├── StateReporting/
├── CALEA/
│
├── tools/                           ← Development tools
│   ├── unified_data_dictionary/     ← UDD Python package
│   │   ├── src/                     (Python source)
│   │   ├── tests/                   (Unit tests)
│   │   ├── pyproject.toml          (Package config)
│   │   ├── Makefile                (Build automation)
│   │   ├── requirements.txt        (Dependencies)
│   │   ├── config.yaml             (Tool config)
│   │   ├── standards_paths.ini     (NEW: Points to Standards data)
│   │   ├── README.md               (Tool docs)
│   │   └── CHANGELOG.md            (Tool version history)
│   └── README.md                    (Tools directory guide)
│
├── schemas/                         ← All schema definitions
│   ├── udd/                         (UDD schemas - from tool)
│   └── [future schema types]
│
├── mappings/                        ← All mapping files
│   ├── call_types_*.csv            (Call type classifications)
│   ├── call_type_category_mapping.json
│   └── field_mappings/              (UDD mappings - from tool)
│       ├── cad_field_map_latest.json
│       ├── rms_field_map_latest.json
│       ├── mapping_rules.md
│       └── [pointer files]
│
├── templates/                       ← Reusable templates
│   └── udd/                         (UDD templates - from tool)
│
├── data/                            ← Sample and test data
│   ├── samples/
│   │   └── rms/
│   │       └── sample_rms_export.csv
│   └── test/
│
├── scripts/                         ← Organized scripts
│   ├── validation/
│   │   └── validate_rms_export.py
│   ├── extraction/
│   │   └── extract_narrative_fields.py
│   ├── processing/                  (From UDD)
│   └── utilities/                   (From UDD)
│
├── docs/                            ← All documentation
│   ├── merge/                       (Merge documentation)
│   ├── generated/                   (UDD-generated docs)
│   ├── tools/
│   │   └── udd/                     (UDD tool documentation & chatlogs)
│   ├── html/
│   │   └── rms_field_dictionary.html
│   └── call_type_category_mapping.md
│
├── archive/                         (Legacy files)
├── config/                          (ETL configs)
│
├── README.md                        (Standards overview)
├── CHANGELOG.md                     (Standards changelog)
├── CHANGELOG_UDD.md                 (UDD tool changelog - reference)
├── SUMMARY.md                       (Standards summary)
└── [other root files]
```

---

## ✅ Advantages of This Approach

1. **UDD Tool Stays Functional**
   - Python package structure intact
   - `pip install -e .` still works
   - CLI commands still work
   - Tests still run

2. **Clear Separation of Concerns**
   - `tools/` = Development code
   - Root = Reference data
   - Easy to understand structure

3. **Easy to Update**
   - Pull UDD updates from GitHub
   - Tool updates don't affect Standards data
   - Standards data updates don't affect tool

4. **Future-Proof**
   - Can add more tools to `tools/` directory
   - NIBRS content goes cleanly to root
   - Scalable structure

5. **Maintains Functionality**
   - No broken paths (with config file)
   - Tests still work
   - Package still installs

---

## 📋 Post-Migration Checklist

### Immediate Tasks
- [ ] Run migration script
- [ ] Test UDD tool installation (`cd tools/unified_data_dictionary && pip install -e .`)
- [ ] Test UDD CLI (`udd --help`, `udd status`)
- [ ] Verify reference data accessible at new locations

### Configuration Updates
- [ ] Review `tools/unified_data_dictionary/standards_paths.ini`
- [ ] Update any hardcoded paths in Python scripts
- [ ] Update any hardcoded paths in documentation

### Documentation
- [ ] Update Standards/README.md to mention tools directory
- [ ] Add tools section to documentation
- [ ] Document new structure in CHANGELOG

### Git
- [ ] Review all changes
- [ ] Commit migration with descriptive message
- [ ] Consider tagging as v2.1.0 (post-restructure)

### Future
- [ ] Add NIBRS content to Standards/NIBRS/
- [ ] Consider adding other development tools to tools/

---

## ⏱️ Time Estimate

| Phase | Duration |
|-------|----------|
| Script execution | 15-20 minutes |
| Testing UDD tool | 15 minutes |
| Path updates | 30 minutes |
| Documentation | 30 minutes |
| Git commit | 15 minutes |
| **Total** | **1.5-2 hours** |

---

## 🚀 Ready to Execute

The script is ready to run! This approach is much cleaner than full flattening.

**To execute:**
1. Copy the complete script
2. Run in PowerShell from Standards directory
3. Follow post-migration checklist

**Status**: ✅ RECOMMENDED APPROACH  
**Created**: 2026-01-16  
**Confidence**: High - This preserves functionality while organizing structure
