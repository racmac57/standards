# NIBRS - National Incident-Based Reporting System

**Location**: `Standards/NIBRS`  
**Last Updated**: 2026-01-17  
**Status**: ✅ Active  
**FBI Manual Version**: 2023.0

---

## Overview

This directory contains FBI NIBRS (National Incident-Based Reporting System) offense classifications, definitions, and mappings for RMS (Records Management System) integration. NIBRS is the modernized replacement for the legacy UCR (Uniform Crime Reporting) system.

**Purpose**: Provide authoritative definitions and automated classification tools for crime reporting and data quality validation.

---

## Directory Structure

```
NIBRS/
├── DataDictionary/
│   ├── current/
│   │   ├── schema/
│   │   │   ├── nibrs_offense_definitions.md ⭐
│   │   │   └── ucr_offense_classification.json ⭐
│   │   └── mappings/
│   │       └── rms_to_nibrs_offense_map.json ⭐
│   └── archive/
│       └── FBI_UCR_Legacy/              # Old UCR files (archived)
├── README.md                             # This file
├── PROJECT_SUMMARY.md                    # Executive overview
├── DELIVERABLES_CATALOG.md               # File descriptions
├── RMS_NIBRS_Implementation_Guide.md     # Complete guide (890 lines)
├── RMS_NIBRS_Mapping_Guide.md            # Quick lookup tables
├── validate_rms_nibrs_mapping.py         # Python validator
├── rms_nibrs_validator.py                # Alternative validator
├── PowerBI_RMS_NIBRS_Integration.m       # Power BI M-Code
└── RMS_NIBRS_Validation_Report.xlsx      # Sample report
```

---

## Key Files

### 📚 **Core Reference Data**

#### 1. **`nibrs_offense_definitions.md`** ⭐
**Human-readable offense reference**

**Contains**:
- All 81 NIBRS offense definitions (71 Group A + 10 Group B)
- Full FBI definitions from 2023.0 manual
- NIBRS codes and NCIC cross-references
- Crime type classifications (Person/Property/Society)
- Reporting notes and examples
- Classification decision trees

**Use For**:
- Authoritative offense definitions
- Training and reference
- Manual classification guidance

---

#### 2. **`ucr_offense_classification.json`** ⭐
**Machine-readable offense lookup**

**Structure**:
```json
{
  "group_a_offenses": {
    "13A": {
      "code": "13A",
      "offense_name": "Aggravated Assault",
      "category": "Assault Offenses",
      "crime_type": "Crime Against Person",
      "ncic_codes": ["1301", "1302", ...],
      "definition": "...",
      "key_elements": [...],
      "includes": [...],
      "excludes": [...]
    }
  },
  "group_b_offenses": {...},
  "crime_type_index": {...},
  "ncic_to_nibrs_lookup": {...}
}
```

**Use For**:
- Python/API integration
- Automated validation
- Quick programmatic lookups

---

#### 3. **`rms_to_nibrs_offense_map.json`** ⭐
**Hackensack RMS → NIBRS mapping**

**Contains**:
- 85 RMS incident type mappings
- Confidence scoring (0.0-1.0)
- Validation requirements for ambiguous mappings
- Classification logic for edge cases

**Statistics**:
- 68% auto-mappable (confidence ≥ 0.9)
- 18% need minor validation
- 14% need manual review or exclusion

**Use For**:
- Automated RMS classification
- Data quality validation
- NIBRS submission preparation

---

## Quick Start

### Python Validation

```python
import json

# Load definitions and mappings
with open('DataDictionary/current/schema/ucr_offense_classification.json') as f:
    nibrs = json.load(f)

with open('DataDictionary/current/mappings/rms_to_nibrs_offense_map.json') as f:
    rms_mapping = json.load(f)

# Validate UCR code
def validate_ucr_code(code):
    if code in nibrs['group_a_offenses']:
        return nibrs['group_a_offenses'][code]['offense_name']
    return 'Invalid code'

# Map RMS to NIBRS
def map_rms_incident(rms_type):
    if rms_type in rms_mapping['rms_to_nibrs']:
        mapping = rms_mapping['rms_to_nibrs'][rms_type]
        return {
            'nibrs_code': mapping['nibrs_code'],
            'confidence': mapping['confidence'],
            'status': 'mapped' if mapping['confidence'] >= 0.9 else 'review_required'
        }
    return {'status': 'unmapped'}

# Example
print(validate_ucr_code('13A'))  # "Aggravated Assault"
print(map_rms_incident('AGGRAVATED ASSAULT'))  # {'nibrs_code': '13A', ...}
```

---

### Power BI Integration

See `PowerBI_RMS_NIBRS_Integration.m` for complete M-Code.

**Quick Example**:
```m
// Load NIBRS lookup
let
    Source = Json.Document(File.Contents("ucr_offense_classification.json")),
    GroupA = Source[group_a_offenses],
    Expanded = Table.FromRecords(Record.FieldValues(GroupA))
in
    Expanded
```

---

### Command Line Validation

```bash
# Run validator on RMS data
python validate_rms_nibrs_mapping.py your_incidents.csv

# Output: Validation report with:
# - High confidence mappings (auto-processable)
# - Review required items
# - Invalid/unmapped codes
```

---

## Documentation

### Comprehensive Guides

1. **`RMS_NIBRS_Implementation_Guide.md`** (890 lines)
   - Complete system documentation
   - Integration patterns
   - Python and Power BI examples
   - Data quality checks
   - Troubleshooting

2. **`RMS_NIBRS_Mapping_Guide.md`**
   - Quick reference tables
   - High-confidence mappings
   - Ambiguous mapping logic
   - Common scenarios

3. **`PROJECT_SUMMARY.md`**
   - Executive overview
   - System statistics
   - Key files summary

4. **`DELIVERABLES_CATALOG.md`**
   - Detailed file descriptions
   - Usage recommendations

---

## Statistics

**NIBRS Coverage**:
- 71 Group A Offenses (full incident reporting)
- 10 Group B Offenses (arrest-only reporting)
- 370+ NCIC code mappings
- 3 crime classifications (Person, Property, Society)

**RMS Mapping Accuracy**:
- 85 Hackensack RMS incident types mapped
- 68% auto-classification rate (high confidence)
- 18% medium confidence (minor validation)
- 14% requires manual review

**Expected Time Savings**:
- 76% reduction in manual classification time
- Automated validation for 68% of incidents

---

## Use Cases

### 1. **Arrest Analytics Validation**
- Validate UCR code assignments against FBI standards
- Cross-check NCIC vs NIBRS codes
- Resolve disputed classifications

### 2. **Monthly Report Accuracy**
- Verify crime categorizations
- Ensure NIBRS compliance
- Provide authoritative definitions

### 3. **Data Quality Monitoring**
- Flag invalid NIBRS codes
- Identify mapping ambiguities
- Track classification confidence

### 4. **NIBRS Submission Preparation**
- Automated code assignment
- Validation before submission
- Error checking and reporting

---

## Scripts & Tools

### Python Scripts

1. **`validate_rms_nibrs_mapping.py`**
   - Validates RMS data against NIBRS standards
   - Generates detailed validation reports
   - Exports results to Excel

2. **`rms_nibrs_validator.py`**
   - Alternative validation tool
   - More detailed error messages
   - Custom validation rules

**Usage**:
```bash
python validate_rms_nibrs_mapping.py incidents.csv
# Output: validation_report.xlsx
```

### Power BI Integration

**`PowerBI_RMS_NIBRS_Integration.m`**
- Complete M-Code for NIBRS integration
- DAX measures for validation
- Pre-built queries

---

## Integration Workflow

### Recommended Implementation

**Phase 1: Setup** (15 min)
1. Load `ucr_offense_classification.json` into Python/Power BI
2. Load `rms_to_nibrs_offense_map.json`
3. Test with sample data

**Phase 2: Validation** (1 hour)
1. Run validator on historical RMS data
2. Review high-confidence mappings (auto-approve)
3. Manually review medium/low confidence items

**Phase 3: Production** (ongoing)
1. Integrate into monthly reporting pipeline
2. Monitor classification accuracy
3. Update mappings as needed

---

## Maintenance

**Update Frequency**: 
- Annually (when FBI releases new NIBRS manual)
- As needed (when RMS incident types change)

**Version Tracking**:
- Current: FBI NIBRS 2023.0
- Previous versions archived in `DataDictionary/archive/`

**Contact**: R. A. Carucci

---

## Related Resources

- **Standards/CAD**: CAD data schemas
- **Standards/RMS**: RMS data schemas
- **Standards/CAD_RMS**: Cross-system mappings
- **LegalCodes/2C**: NJ Criminal Law categorizations (complements NIBRS)

---

## Migration Notes

**2026-01-17**: Migrated from separate Claude AI project artifacts  
**Legacy**: Old FBI_UCR files archived at `DataDictionary/archive/FBI_UCR_Legacy/`  
**Rationale**: NIBRS is the modernized replacement for legacy UCR reporting
