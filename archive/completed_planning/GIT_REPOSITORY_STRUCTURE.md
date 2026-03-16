# Git Repository Structure for CAD-RMS Schema Integration

**Version**: 1.0
**Date**: 2025-12-30
**Purpose**: Recommended folder layout for version control and future Git repository organization

---

## 📁 Proposed Folder Structure

```
cad-rms-schema-integration/
│
├── schemas/                          # Export field definitions and data dictionaries
│   ├── rms_export_field_definitions.md
│   ├── cad_export_field_definitions.md
│   └── README.md
│
├── mappings/                         # Field mapping schemas and strategies
│   ├── cad_to_rms_field_map.json
│   ├── rms_to_cad_field_map.json
│   ├── multi_column_matching_strategy.md
│   └── README.md
│
├── docs/                             # Documentation and release notes
│   ├── README.md
│   ├── CHANGELOG.md
│   ├── SUMMARY.md
│   ├── RELEASE_NOTES.md
│   ├── SCHEMA_FILES_SUMMARY.md
│   └── html/
│       └── rms_field_dictionary.html
│
├── samples/                          # Sample data for testing and validation
│   ├── sample_rms_export.csv
│   ├── sample_cad_export.csv
│   └── README.md
│
├── scripts/                          # Validation and utility scripts
│   ├── validate_rms_export.py
│   ├── validate_cad_export.py
│   ├── extract_narrative_fields.py
│   ├── requirements.txt
│   └── README.md
│
├── tests/                            # Test cases and validation tests
│   ├── test_rms_validation.py
│   ├── test_field_mappings.py
│   ├── test_narrative_extraction.py
│   └── README.md
│
├── .gitignore                        # Git ignore file
├── .gitattributes                    # Git attributes for line endings
├── LICENSE                           # License file (if applicable)
└── README.md                         # Root repository README

```

---

## 📋 File Migration Plan

### Current → Proposed Structure

| Current Location | New Location | Notes |
|-----------------|--------------|-------|
| `rms_export_field_definitions.md` | `schemas/rms_export_field_definitions.md` | Move |
| `CAD/DataDictionary/current/schema/cad_export_field_definitions.md` | `schemas/cad_export_field_definitions.md` | Copy |
| `cad_to_rms_field_map.json` | `mappings/cad_to_rms_field_map.json` | Move |
| `rms_to_cad_field_map.json` | `mappings/rms_to_cad_field_map.json` | Move |
| `multi_column_matching_strategy.md` | `mappings/multi_column_matching_strategy.md` | Move |
| `README.md` | `docs/README.md` | Move |
| `CHANGELOG.md` | `docs/CHANGELOG.md` | Move |
| `SUMMARY.md` | `docs/SUMMARY.md` | Move |
| `RELEASE_NOTES.md` | `docs/RELEASE_NOTES.md` | Move |
| `SCHEMA_FILES_SUMMARY.md` | `docs/SCHEMA_FILES_SUMMARY.md` | Move |
| `rms_field_dictionary.html` | `docs/html/rms_field_dictionary.html` | Move |
| `sample_rms_export.csv` | `samples/sample_rms_export.csv` | Move |
| `validate_rms_export.py` | `scripts/validate_rms_export.py` | Move |
| `extract_narrative_fields.py` | `scripts/extract_narrative_fields.py` | New file |

---

## 🚀 PowerShell Migration Script

```powershell
# Git Repository Structure Setup Script
# Run from the Standards directory

# Create directories
$dirs = @(
    "schemas",
    "mappings",
    "docs",
    "docs/html",
    "samples",
    "scripts",
    "tests"
)

foreach ($dir in $dirs) {
    New-Item -ItemType Directory -Force -Path $dir
    Write-Host "Created directory: $dir"
}

# Move schema files
Move-Item -Path "rms_export_field_definitions.md" -Destination "schemas/" -Force
Copy-Item -Path "CAD/DataDictionary/current/schema/cad_export_field_definitions.md" -Destination "schemas/" -Force

# Move mapping files
Move-Item -Path "cad_to_rms_field_map.json" -Destination "mappings/" -Force
Move-Item -Path "rms_to_cad_field_map.json" -Destination "mappings/" -Force
Move-Item -Path "multi_column_matching_strategy.md" -Destination "mappings/" -Force

# Move documentation
Move-Item -Path "README.md" -Destination "docs/" -Force
Move-Item -Path "CHANGELOG.md" -Destination "docs/" -Force
Move-Item -Path "SUMMARY.md" -Destination "docs/" -Force
Move-Item -Path "RELEASE_NOTES.md" -Destination "docs/" -Force
Move-Item -Path "SCHEMA_FILES_SUMMARY.md" -Destination "docs/" -Force
Move-Item -Path "rms_field_dictionary.html" -Destination "docs/html/" -Force

# Move samples
Move-Item -Path "sample_rms_export.csv" -Destination "samples/" -Force

# Move scripts
Move-Item -Path "validate_rms_export.py" -Destination "scripts/" -Force
Move-Item -Path "extract_narrative_fields.py" -Destination "scripts/" -Force

Write-Host "Repository structure created successfully!"
```

---

## 📝 README Files for Each Directory

### `schemas/README.md`

```markdown
# Field Schemas and Data Dictionaries

This directory contains comprehensive field definitions for RMS and CAD exports.

## Files

- `rms_export_field_definitions.md` - RMS field definitions (29 fields, 8 groups)
- `cad_export_field_definitions.md` - CAD field definitions

## Usage

Reference these schemas when:
- Building ETL pipelines
- Validating export data
- Implementing data quality checks
- Documenting system interfaces
```

### `mappings/README.md`

```markdown
# Field Mappings and Matching Strategies

This directory contains field mapping schemas and multi-column matching strategies.

## Files

- `cad_to_rms_field_map.json` - CAD-to-RMS mapping schema (v2.0)
- `rms_to_cad_field_map.json` - RMS-to-CAD mapping schema (v2.0)
- `multi_column_matching_strategy.md` - Matching strategy guide

## Usage

Use these mappings to:
- Configure data integration workflows
- Implement multi-column matching
- Backfill missing CAD data from RMS
```

### `samples/README.md`

```markdown
# Sample Data Files

This directory contains sample export data for testing and validation.

## Files

- `sample_rms_export.csv` - Sample RMS export with 3 cases
- `sample_cad_export.csv` - Sample CAD export (to be added)

## Usage

Use sample data to:
- Test validation scripts
- Develop ETL pipelines
- Demo matching strategies
- Verify field formats

**Note**: Sample data is anonymized and for testing only.
```

### `scripts/README.md`

```markdown
# Validation and Utility Scripts

This directory contains Python scripts for validation and data extraction.

## Files

- `validate_rms_export.py` - Validates RMS exports against schema
- `extract_narrative_fields.py` - Extracts structured data from narratives
- `requirements.txt` - Python dependencies

## Setup

```bash
pip install -r requirements.txt
```

## Usage

```bash
# Validate RMS export
python validate_rms_export.py sample_rms_export.csv

# Extract narrative fields
python extract_narrative_fields.py sample_rms_export.csv
```
```

---

## 🔧 `.gitignore` Template

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Data files (exclude real data, keep samples)
*.csv
!sample_*.csv

# Reports
validation_report*.html
narrative_extraction_report*.html

# Logs
*.log

# Temporary files
tmp/
temp/
*.tmp
```

---

## 🎯 Git Initialization Steps

### 1. Initialize Repository

```bash
cd cad-rms-schema-integration
git init
git add .
git commit -m "Initial commit: CAD-RMS schema integration v0.3.0"
```

### 2. Create Remote Repository

On GitHub/GitLab/Bitbucket:
- Create new repository: `cad-rms-schema-integration`
- Do not initialize with README (already exists)

### 3. Link and Push

```bash
git remote add origin https://github.com/your-org/cad-rms-schema-integration.git
git branch -M main
git push -u origin main
```

### 4. Create Version Tag

```bash
git tag -a v0.3.0 -m "Release v0.3.0: Comprehensive RMS field definitions"
git push origin v0.3.0
```

---

## 📦 Branch Strategy

### Main Branches

- `main` - Production-ready code and documentation
- `develop` - Integration branch for ongoing work

### Feature Branches

- `feature/rms-schema-v2` - RMS schema enhancements
- `feature/cad-schema-v2` - CAD schema enhancements
- `feature/validation-scripts` - Script development
- `bugfix/*` - Bug fixes

### Release Workflow

1. Develop on feature branches
2. Merge to `develop` for integration testing
3. Create release branch: `release/v0.4.0`
4. Final testing and documentation updates
5. Merge to `main` and tag version
6. Merge back to `develop`

---

## 🔄 CI/CD Recommendations

### GitHub Actions Workflow

```yaml
name: Validate Schemas

on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: pip install -r scripts/requirements.txt
      - name: Validate JSON schemas
        run: |
          python -m json.tool mappings/cad_to_rms_field_map.json
          python -m json.tool mappings/rms_to_cad_field_map.json
      - name: Run validation tests
        run: python scripts/validate_rms_export.py samples/sample_rms_export.csv
```

---

## 📚 Next Steps

1. **Execute migration script** to reorganize files
2. **Initialize Git repository** with new structure
3. **Create remote repository** and push
4. **Set up branch protection** rules for main branch
5. **Configure CI/CD** for automated validation
6. **Document contribution guidelines** in CONTRIBUTING.md

---

**End of Git Repository Structure Guide**
