# Standards Repository

Central repository for CAD/RMS data standards, schemas, and field mappings.

## Repository Layout

```
Standards/
├── archive/                    # Archived files (packages, legacy, duplicates)
│   ├── packages/               # Packaging artifacts (Standards.7z)
│   ├── legacy_copies/          # Legacy file versions
│   └── removed_duplicates/     # Removed duplicate files
├── CAD/                        # CAD system standards
│   └── DataDictionary/
│       └── current/schema/     # CAD field definitions
├── Clery/                      # Clery Act crime statistics (institution requests)
│   └── DataDictionary/
│       └── current/            # clery_crime_definitions, geography, nibrs_to_clery_map
├── CAD_RMS/                    # Cross-system mapping (CANONICAL)
│   └── DataDictionary/
│       └── current/schema/     # cad_to_rms_field_map.json, rms_to_cad_field_map.json
├── config/                     # ETL configuration files
├── docs/                       # Documentation
├── mappings/                   # Call type mappings and lookups
├── RMS/                        # RMS system standards
│   └── DataDictionary/
│       └── current/schema/     # RMS field definitions (CANONICAL)
└── unified_data_dictionary/    # Unified data dictionary project
    ├── docs/chatlogs/          # Development chatlogs
    ├── mappings/               # Additional mappings (pointer files to canonical)
    ├── schemas/                # Schema definitions
    └── src/                    # Python utilities
```

## Canonical File Locations

| File | Canonical Location |
|------|-------------------|
| `cad_to_rms_field_map.json` | `CAD_RMS/DataDictionary/current/schema/` |
| `rms_to_cad_field_map.json` | `CAD_RMS/DataDictionary/current/schema/` |
| `multi_column_matching_strategy.md` | `CAD_RMS/DataDictionary/current/schema/` |
| `rms_export_field_definitions.md` | `RMS/DataDictionary/current/schema/` |
| `cad_export_field_definitions.md` | `CAD/DataDictionary/current/schema/` |
| `clery_crime_definitions.json` | `Clery/DataDictionary/current/schema/` |
| `nibrs_to_clery_map.json` | `Clery/DataDictionary/current/mappings/` |

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
