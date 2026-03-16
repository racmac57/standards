# Standards Repository

**Version**: v2.3.0  
**Last Updated**: 2026-01-17  
**Status**: ✅ Operational

Central repository for CAD/RMS data standards, schemas, and field mappings. Includes NIBRS offense classifications and reference data organization.

---

## 🎯 What Changed in v2.3.0

**Major additions**: [View full changelog](CHANGELOG.md#v230---2026-01-17)

- **NIBRS Standards Added**: FBI NIBRS 2023.0 offense classifications with 81 offense definitions and 85 RMS mappings
- **Reference Data Organized**: Geographic data (ZIP codes) and Legal codes (Title 39, 2C, Ordinances) structured into dedicated directories
- **Enhanced Integration**: Python validation scripts, Power BI M-Code, and comprehensive implementation guides

---

## 🟢 Migration Status

**Current Status**: ✅ Migration Complete and Operational  
**Branch**: `main`  
**Latest Version**: v2.3.0

The unified_data_dictionary has been successfully migrated to a hybrid structure:
- **UDD Python tool** → `tools/unified_data_dictionary/` (functional)
- **Reference data** → Root-level `schemas/udd/`, `mappings/field_mappings/`, `templates/udd/`
- **NIBRS Standards** → `NIBRS/` (FBI offense classifications and RMS mappings)

**Migration Results**: ✅ 252 files reorganized | ✅ Python tool functional | ✅ Reference data at root

### ✅ Leftover `tools\NULL` (directory removal) — resolved

**Resolved:** The `tools\NULL` folder has been removed; the OneDrive "path is too long" error for this path has been addressed.

The old `unified_data_dictionary` directory could not be fully removed after the merge (recursive symlink / locked-by-process; see **CHANGELOG** v2.2.0 **Known Issues**). It had appeared as **`tools\NULL`** with a deeply nested `Standards\unified_data_dictionary\...` structure. It did not affect UDD functionality.

**Fix (if it reappears):** Delete the `tools\NULL` tree (exit OneDrive first):
```powershell
Remove-Item -LiteralPath "C:\Users\carucci_r\OneDrive - City of Hackensack\09_Reference\Standards\tools\NULL" -Recurse -Force -ErrorAction SilentlyContinue
```
If that hits long-path errors, run **`Fix_OneDrive_Long_Path_Issue.ps1 -Repair -RootPath "…\09_Reference\Standards\tools\NULL"`** (see `SYNC\Fix_OneDrive_Long_Path_Issue_README.md`), then delete the resulting `tools\udd_legacy` folder.

---

## Repository Layout

```
Standards/
├── archive/                    # Archived files
├── CAD/                        # CAD system standards
│   └── DataDictionary/
│       └── current/schema/     # CAD field definitions
├── CAD_RMS/                    # Cross-system mapping (CANONICAL)
│   └── DataDictionary/
│       └── current/schema/     # cad_to_rms_field_map.json, rms_to_cad_field_map.json
├── config/                     # ETL configuration files
├── docs/                       # Documentation
├── mappings/                   # Call type mappings and lookups
│   └── field_mappings/         # Extracted UDD field mappings
├── NIBRS/                      # FBI NIBRS Standards (NEW in v2.3.0)
│   ├── DataDictionary/
│   │   ├── current/
│   │   │   ├── schema/         # nibrs_offense_definitions.md, ucr_offense_classification.json
│   │   │   └── mappings/       # rms_to_nibrs_offense_map.json
│   │   └── archive/            # FBI_UCR_Legacy
│   ├── README.md
│   ├── validate_rms_nibrs_mapping.py
│   └── PowerBI_RMS_NIBRS_Integration.m
├── RMS/                        # RMS system standards
│   └── DataDictionary/
│       └── current/schema/     # RMS field definitions (CANONICAL)
├── schemas/
│   └── udd/                    # Extracted UDD schemas (9 files)
├── scripts/
│   ├── validation/             # validate_rms_export.py
│   └── extraction/             # extract_narrative_fields.py
├── templates/
│   └── udd/                    # Extracted UDD templates
├── tools/
│   └── unified_data_dictionary/  # UDD Python package (functional)
└── README.md                   # This file
```

## Canonical File Locations

| File | Canonical Location |
|------|-------------------|
| `cad_to_rms_field_map.json` | `CAD_RMS/DataDictionary/current/schema/` |
| `rms_to_cad_field_map.json` | `CAD_RMS/DataDictionary/current/schema/` |
| `multi_column_matching_strategy.md` | `CAD_RMS/DataDictionary/current/schema/` |
| `rms_export_field_definitions.md` | `RMS/DataDictionary/current/schema/` |
| `cad_export_field_definitions.md` | `CAD/DataDictionary/current/schema/` |

## Archive Policy

Files in `archive/` are retained for 30 days after merge to main. See `archive/README.md` for details.

---

## CAD-RMS Cross-System Mapping Schema

This repository contains enhanced mapping schemas and strategies for integrating CAD (Computer-Aided Dispatch) and RMS (Records Management System) data.

## Files

### Core Mapping Schemas

- **`cad_to_rms_field_map.json`** (v2.0) - Enhanced CAD-to-RMS field mapping with multi-column matching strategies
- **`rms_to_cad_field_map.json`** (v2.0) - Enhanced RMS-to-CAD field mapping with multi-column matching strategies

### Documentation

- **`multi_column_matching_strategy.md`** - Comprehensive guide to multi-column matching strategies for confident record linking
- **`rms_export_field_definitions.md`** - Comprehensive RMS field definitions with validation rules, formats, and mapping notes (29 fields across 8 functional groups)
- **`docs/call_type_category_mapping.md`** - Complete Call Type to Category Type mapping documentation (649 call types across 11 categories, ESRI standard)

## Version 2.0 Enhancements

The enhanced mapping schemas (v2.0) include:

1. **Multi-Column Matching Strategies**: Three alternative matching strategies beyond primary key matching:
   - Temporal + Address Match (confidence threshold: 0.85)
   - Officer + Temporal Match (confidence threshold: 0.80)
   - Address + Zone + Approximate Date Match (confidence threshold: 0.75)

2. **Confidence Scoring**: Each match includes a confidence score (0.0 to 1.0) indicating match quality

3. **Match Strategy Tracking**: Audit fields track which matching strategy was used for each record

4. **Enhanced Audit Fields**: Additional metadata fields for match quality analysis and troubleshooting

## Usage

### Primary Key Matching

The primary join key (`ReportNumberNew` ↔ `Case Number`) should be used first for exact matching. The enhanced schemas maintain backward compatibility with primary key matching.

### Alternative Matching Strategies

When primary key matching fails or confidence is low, the alternative matching strategies can be applied according to the workflow defined in `multi_column_matching_strategy.md`.

### Backward Compatibility

The enhanced schemas are backward compatible with v1.0 schemas. Existing code that uses primary key matching will continue to work. Alternative matching strategies are additive enhancements.

## Related Documentation

- **CAD Field Definitions**: `CAD/DataDictionary/current/schema/cad_export_field_definitions.md`
- **RMS Field Definitions**: `rms_export_field_definitions.md` (comprehensive v1.0 with 29 fields organized into 8 functional groups)
- **Call Type Classification**: `docs/call_type_category_mapping.md` (527 call types mapped to 11 ESRI categories with response types)
- **Mapping Rules**: `unified_data_dictionary/mappings/mapping_rules.md`

## Call Type Classification System

The Standards folder now includes a comprehensive Call Type to Category Type mapping system for RMS Incident Type classification:

- **Primary Reference**: `09_Reference/Classifications/CallTypes/CallType_Categories.csv` (649 entries, with Incident_Norm column, 11 ESRI standard categories only)
- **Documentation**: `docs/call_type_category_mapping.md` - Human-readable breakdown by category
- **Category Files**: `mappings/call_types_*.csv` - 11 category-specific CSV files for targeted loading
- **JSON Mapping**: `mappings/call_type_category_mapping.json` - Programmatic lookup dictionaries

**Usage Example:**
```python
import pandas as pd
from pathlib import Path

# Load standard reference
calltype_file = Path(r"C:\Users\carucci_r\OneDrive - City of Hackensack\09_Reference\Classifications\CallTypes\CallType_Categories.csv")
df = pd.read_csv(calltype_file)

# Or load specific category
criminal_file = Path(r"C:\Users\carucci_r\OneDrive - City of Hackensack\09_Reference\Standards\mappings\call_types_criminal_incidents.csv")
criminal_incidents = pd.read_csv(criminal_file)

# Or use JSON for quick lookups
import json
json_file = Path(r"C:\Users\carucci_r\OneDrive - City of Hackensack\09_Reference\Standards\mappings\call_type_category_mapping.json")
with open(json_file, 'r') as f:
    mapping = json.load(f)
category = mapping['call_type_to_category']['Domestic Dispute']  # Returns: 'Criminal Incidents'
```

**Categories (11 total):**
1. Administrative and Support (122 call types)
2. Assistance and Mutual Aid (21 call types)
3. Community Engagement (20 call types)
4. Criminal Incidents (201 call types)
5. Emergency Response (33 call types)
6. Investigations and Follow-Ups (44 call types)
7. Juvenile-Related Incidents (16 call types)
8. Public Safety and Welfare (85 call types)
9. Regulatory and Ordinance (31 call types)
10. Special Operations and Tactical (19 call types)
11. Traffic and Motor Vehicle (57 call types)

**Note:** The reference file includes an `Incident_Norm` column for normalized incident type matching, with E.D.P. variations (E.D.P., EDP, edp, etc.) all mapping to "Mental Health Incident".

## Schema Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-12-15 | Initial mapping schema with primary key matching |
| 2.0 | 2025-12-30 | Added multi-column matching strategies, confidence scoring, enhanced audit fields |
