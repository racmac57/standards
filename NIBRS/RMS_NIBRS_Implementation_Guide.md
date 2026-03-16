# RMS-to-NIBRS Offense Mapping Implementation Guide

**Version:** 1.0  
**Date:** 2026-01-16  
**Author:** R. A. Carucci  
**Department:** Hackensack Police Department

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [System Components](#system-components)
3. [Quick Start Guide](#quick-start-guide)
4. [Python Integration](#python-integration)
5. [Power BI Integration](#power-bi-integration)
6. [Data Quality Workflow](#data-quality-workflow)
7. [Maintenance & Updates](#maintenance--updates)
8. [Troubleshooting](#troubleshooting)
9. [Best Practices](#best-practices)

---

## 🎯 Overview

### Purpose
This system automates the classification of RMS incident types to NIBRS offense codes, enabling:
- **Automated classification** for 68% of incidents (high confidence mappings)
- **Guided validation** for ambiguous cases
- **Quality control** through confidence scoring
- **NIBRS submission** readiness validation

### Key Benefits
- ✅ **Time Savings**: Auto-map majority of incidents
- ✅ **Accuracy**: Standardized FBI definitions
- ✅ **Consistency**: Eliminate subjective classification
- ✅ **Compliance**: NIBRS submission requirements met
- ✅ **Visibility**: Data quality metrics and reporting

### Mapping Statistics
| Confidence Level | Count | Percentage | Action Required |
|------------------|-------|------------|----------------|
| **High (≥0.9)** | 58 | 68% | Auto-map ✅ |
| **Medium (0.7-0.8)** | 15 | 18% | Minor validation ⚠️ |
| **Low (0.5-0.6)** | 6 | 7% | Manual review 🔴 |
| **Non-Crime (0.0)** | 6 | 7% | Exclude 🚫 |

---

## 🧩 System Components

### Core Files

#### 1. **ucr_offense_classification.json**
- **Purpose**: Master NIBRS offense definitions
- **Contains**: All 81 NIBRS offenses with full specifications
- **Use**: Reference lookup for validation and reporting

#### 2. **rms_to_nibrs_offense_map.json**
- **Purpose**: Maps Hackensack RMS types to NIBRS codes
- **Contains**: 85 mappings with confidence levels
- **Use**: Primary classification engine

#### 3. **validate_rms_nibrs_mapping.py**
- **Purpose**: Python validation script
- **Contains**: Validator class and quality reporting
- **Use**: Data quality analysis and bulk validation

#### 4. **PowerBI_RMS_NIBRS_Integration.m**
- **Purpose**: Power BI M-code queries and DAX measures
- **Contains**: Complete Power BI integration
- **Use**: Visual dashboards and reporting

#### 5. **RMS_NIBRS_Mapping_Guide.md** (Generated)
- **Purpose**: User-friendly reference guide
- **Contains**: Quick lookup tables by confidence level
- **Use**: Manual classification decisions

---

## 🚀 Quick Start Guide

### Step 1: File Setup (5 minutes)

```bash
# Create project structure
UCR_NIBRS_Standards/
├── ucr_offense_classification.json
├── rms_to_nibrs_offense_map.json
├── validate_rms_nibrs_mapping.py
├── PowerBI_RMS_NIBRS_Integration.m
└── README.md (this file)
```

### Step 2: Generate Mapping Guide (1 minute)

```python
from validate_rms_nibrs_mapping import RMSNIBRSValidator

validator = RMSNIBRSValidator(
    'rms_to_nibrs_offense_map.json',
    'ucr_offense_classification.json'
)

# This creates RMS_NIBRS_Mapping_Guide.md
validator.create_mapping_guide('RMS_NIBRS_Mapping_Guide.md')
```

### Step 3: Validate Sample Data (5 minutes)

```python
import pandas as pd

# Load your RMS data
df = pd.read_excel('rms_export.xlsx')

# Validate
validated_df = validator.validate_dataframe(df)

# Generate report
report = validator.generate_quality_report(validated_df)

# Print summary
validator.print_report(report)

# Export results
validator.export_results(validated_df, report, 'output/')
```

---

## 🐍 Python Integration

### Installation Requirements

```bash
# Required packages
pip install pandas openpyxl

# Optional for enhanced reporting
pip install matplotlib seaborn
```

### Basic Usage

```python
from validate_rms_nibrs_mapping import RMSNIBRSValidator
import pandas as pd

# Initialize
validator = RMSNIBRSValidator(
    rms_mapping_path='rms_to_nibrs_offense_map.json',
    nibrs_classification_path='ucr_offense_classification.json'
)

# Load RMS data
df = pd.read_csv('rms_export.csv')

# Validate
validated_df = validator.validate_dataframe(
    df, 
    incident_type_columns=['Incident Type_1', 'Incident Type_2', 'Incident Type_3']
)

# Generate quality report
report = validator.generate_quality_report(validated_df)

# Review results
print(f"Auto-mappable: {report['summary']['mapped_pct']}%")
print(f"Requires review: {report['summary']['review_required_pct']}%")

# Export
files = validator.export_results(validated_df, report, 'output_folder/')
```

### Advanced Usage: Single Incident Mapping

```python
# Map a single incident type
result = validator.map_rms_to_nibrs("AGGRAVATED ASSAULT")

if result['status'] == 'mapped':
    print(f"NIBRS Code: {result['nibrs_code']}")
    print(f"NIBRS Name: {result['nibrs_name']}")
    print(f"Confidence: {result['confidence']}")
    
elif result['status'] == 'review_required':
    print(f"Possible codes: {result['possible_codes']}")
    print(f"Validation needed: {result['validation_required']}")
    print(f"Logic: {result['classification_logic']}")
    
elif result['status'] == 'unmapped':
    print("No mapping found - add to mapping file")
    
elif result['status'] == 'non_crime':
    print("Administrative code - exclude from NIBRS")
```

### Integration into Existing ETL Pipeline

```python
# Add to your RMS processing script

def process_rms_export(rms_file):
    """Process RMS export with NIBRS classification."""
    
    # Load data
    df = pd.read_excel(rms_file)
    
    # Initialize validator
    validator = RMSNIBRSValidator(
        'rms_to_nibrs_offense_map.json',
        'ucr_offense_classification.json'
    )
    
    # Validate
    validated_df = validator.validate_dataframe(df)
    
    # Filter to auto-mappable records
    auto_mapped = validated_df[
        validated_df['Incident Type_1_Status'] == 'mapped'
    ].copy()
    
    # Extract review cases
    needs_review = validated_df[
        validated_df['Incident Type_1_Status'].isin(['review_required', 'unmapped'])
    ].copy()
    
    # Export
    auto_mapped.to_excel('auto_classified_incidents.xlsx', index=False)
    needs_review.to_excel('incidents_for_review.xlsx', index=False)
    
    return {
        'total': len(df),
        'auto_mapped': len(auto_mapped),
        'needs_review': len(needs_review)
    }
```

---

## 📊 Power BI Integration

### Setup Instructions

#### 1. Import JSON Files (5 minutes)

```m
// Query: RMS_NIBRS_Mapping
let
    Source = Json.Document(File.Contents("C:\path\to\rms_to_nibrs_offense_map.json")),
    RMSMappings = Source[rms_to_nibrs],
    MappingsTable = Record.ToTable(RMSMappings),
    // ... (see PowerBI_RMS_NIBRS_Integration.m for complete code)
in
    TypedTable

// Query: NIBRS_Definitions
let
    Source = Json.Document(File.Contents("C:\path\to\ucr_offense_classification.json")),
    // ... (see PowerBI_RMS_NIBRS_Integration.m for complete code)
in
    TypedTable
```

#### 2. Create Clean Function (2 minutes)

Copy the `CleanIncidentType` function from `PowerBI_RMS_NIBRS_Integration.m`:

```m
// Function: CleanIncidentType
let
    CleanIncidentType = (incidentType as nullable text) as nullable text =>
        let
            Result = if incidentType = null then null
            else
                let
                    Trimmed = Text.Trim(incidentType),
                    WithoutStatute = 
                        if Text.Contains(Trimmed, " - 2C:") then
                            Text.BeforeDelimiter(Trimmed, " - 2C:", 0)
                        else
                            Trimmed,
                    Cleaned = Text.Trim(WithoutStatute)
                in
                    if Cleaned = "" then null else Cleaned
        in
            Result
in
    CleanIncidentType
```

#### 3. Apply Mapping to Data (10 minutes)

```m
// Query: RMS_Data_with_NIBRS
let
    Source = Excel.Workbook(File.Contents("RMS_Export.xlsx"), null, true),
    Data = Source{[Item="Sheet1",Kind="Sheet"]}[Data],
    
    // Clean incident types
    CleanType1 = Table.AddColumn(Data, "Type1_Clean", 
        each CleanIncidentType([#"Incident Type_1"])),
    
    // Merge with mapping
    MergeMapping = Table.NestedJoin(
        CleanType1,
        {"Type1_Clean"},
        RMS_NIBRS_Mapping,
        {"RMS_Incident_Type"},
        "Mapping",
        JoinKind.LeftOuter
    ),
    
    // Expand mapping fields
    ExpandMapping = Table.ExpandTableColumn(
        MergeMapping,
        "Mapping",
        {"NIBRS_Code", "NIBRS_Name", "Confidence", "Mapping_Status"},
        {"NIBRS_Code", "NIBRS_Name", "Confidence", "Status"}
    )
in
    ExpandMapping
```

#### 4. Add DAX Measures (5 minutes)

```dax
// Total Incidents
Total Incidents = COUNTROWS('RMS_Data_with_NIBRS')

// Auto-Mapped Count
Auto Mapped = 
CALCULATE(
    [Total Incidents],
    'RMS_Data_with_NIBRS'[Status] = "Auto-Map"
)

// Mapping Success Rate
Success Rate = 
DIVIDE([Auto Mapped], [Total Incidents], 0)

// Requires Validation
Needs Review = 
CALCULATE(
    [Total Incidents],
    'RMS_Data_with_NIBRS'[Status] IN {"Review Required", "Manual Review"}
)

// Status Color (for conditional formatting)
Status Color = 
SWITCH(
    SELECTEDVALUE('RMS_Data_with_NIBRS'[Status]),
    "Auto-Map", "#00B050",
    "Review Required", "#FFC000",
    "Manual Review", "#FF0000",
    "Non-Crime", "#808080",
    "#C0C0C0"
)
```

#### 5. Create Dashboard (15 minutes)

**Recommended Visuals:**

1. **KPI Cards**
   - Total Incidents
   - Auto-Mapped Count
   - Success Rate %
   - Needs Review Count

2. **Donut Chart: Mapping Status Distribution**
   - Values: Count of incidents
   - Legend: Mapping Status
   - Conditional formatting: Use Status Color measure

3. **Table: Unmapped Incidents**
   - Filter: Status = null
   - Columns: Case Number, Incident Date, Incident Type, Notes

4. **Bar Chart: Top Incident Types**
   - Axis: RMS Incident Type
   - Values: Count
   - Sort: Descending

5. **Matrix: NIBRS Distribution**
   - Rows: NIBRS Category
   - Columns: Crime Type
   - Values: Count

6. **Table: Review Queue**
   - Filter: Status IN ("Review Required", "Manual Review")
   - Columns: Case, Date, Type, Possible Codes, Validation Needed

---

## 🔍 Data Quality Workflow

### Daily Workflow

```
1. IMPORT RMS DATA
   └─→ Load new RMS exports

2. AUTO-CLASSIFY
   └─→ Apply mapping (68% auto-mapped)

3. REVIEW QUEUE
   └─→ Manual review for ambiguous cases
   
4. VALIDATE
   └─→ Run quality checks
   
5. EXPORT
   └─→ Generate NIBRS submission file
```

### Weekly Validation

```python
# Weekly validation script
def weekly_validation():
    """Run weekly data quality validation."""
    
    # Load last week's data
    df = load_rms_data(days=7)
    
    # Validate
    validator = RMSNIBRSValidator('...', '...')
    validated_df = validator.validate_dataframe(df)
    report = validator.generate_quality_report(validated_df)
    
    # Check for new unmapped types
    new_unmapped = report['unmapped_types']['types']
    if new_unmapped:
        send_alert(f"Found {len(new_unmapped)} new unmapped types")
    
    # Check success rate
    if report['summary']['mapped_pct'] < 60:
        send_alert(f"Mapping success rate low: {report['summary']['mapped_pct']}%")
    
    # Export report
    validator.export_results(validated_df, report, f'weekly_report_{date}/')
```

### Monthly Review

1. **Review Mapping Coverage**
   - Check for new incident types in RMS
   - Add mappings for unmapped types
   - Update ambiguous mappings based on patterns

2. **Validate Confidence Levels**
   - Review manual classifications
   - Adjust confidence scores if needed
   - Update validation requirements

3. **Update Documentation**
   - Document new mappings
   - Update classification logic
   - Share findings with records staff

---

## 🔧 Maintenance & Updates

### Adding New RMS Incident Types

When you encounter an unmapped RMS incident type:

1. **Identify the NIBRS Code**
   - Review nibrs_offense_definitions.md
   - Check key elements and classification rules
   - Determine appropriate NIBRS code

2. **Add to Mapping File**
   ```json
   "NEW RMS TYPE": {
     "nibrs_code": "13A",
     "nibrs_name": "Aggravated Assault",
     "confidence": 1.0,
     "crime_type": "Crime Against Person",
     "notes": "Direct match - description",
     "validation_required": []
   }
   ```

3. **Test the Mapping**
   ```python
   result = validator.map_rms_to_nibrs("NEW RMS TYPE")
   print(result)
   ```

4. **Update Documentation**
   - Regenerate mapping guide
   - Document decision rationale
   - Share with team

### Adjusting Confidence Levels

If manual reviews consistently show a mapping is accurate:

```json
// Before
"THEFT": {
  "confidence": 0.5,  // Ambiguous
  ...
}

// After pattern analysis shows it's always shoplifting
"THEFT": {
  "confidence": 0.9,  // High confidence
  "nibrs_code": "23C",
  "notes": "Analysis shows 95% are shoplifting incidents",
  ...
}
```

### Version Control

Maintain versions of mapping file:

```
rms_to_nibrs_offense_map_v1.0.json  (2026-01-16)
rms_to_nibrs_offense_map_v1.1.json  (2026-02-01 - Added 5 new types)
rms_to_nibrs_offense_map_v1.2.json  (2026-03-01 - Updated confidence)
```

---

## 🔎 Troubleshooting

### Issue: Mapping not found

**Symptom:** `status: 'unmapped'`

**Solutions:**
1. Check if incident type has statute code → Clean it
2. Verify exact spelling in mapping file
3. Add new mapping if legitimately unmapped

### Issue: Multiple incident types, unclear which to use

**Symptom:** `possible_codes: ['23A', '23B', ...]`

**Solutions:**
1. Review `classification_logic` in mapping
2. Check `validation_required` fields
3. Examine incident narrative for context
4. Consult NIBRS definitions for key elements

### Issue: Low mapping success rate

**Symptom:** `mapped_pct < 60%`

**Solutions:**
1. Review unmapped types list
2. Add missing mappings
3. Check for data quality issues (typos, new codes)
4. Verify RMS export format hasn't changed

### Issue: Power BI merge not working

**Symptom:** All NIBRS codes showing as null

**Solutions:**
1. Verify JSON file paths are correct
2. Check CleanIncidentType function is applied
3. Confirm column names match exactly
4. Test merge with small sample first

---

## ✅ Best Practices

### Classification Guidelines

1. **Trust High Confidence Mappings**
   - Confidence ≥ 0.9 = Auto-classify
   - Only review if outcome seems wrong

2. **Always Validate Ambiguous Cases**
   - Confidence < 0.7 = Manual review required
   - Check narrative and details
   - Document classification rationale

3. **Multiple Incident Types**
   - Report ALL offenses that occurred
   - Follow NIBRS "Acting in Concert" rules
   - Watch for lesser included offenses

4. **Special Cases**
   - Carjacking = 120 (Robbery) ONLY
   - Auto Burglary = 23F (NOT 220)
   - DV = Relationship indicator, classify underlying offense

### Data Quality

1. **Regular Validation**
   - Run weekly quality reports
   - Monitor unmapped type trends
   - Track success rate metrics

2. **Clean Data at Source**
   - Standardize RMS incident type entry
   - Use dropdown lists where possible
   - Train records staff on NIBRS principles

3. **Document Decisions**
   - Keep log of manual classifications
   - Note rationale for ambiguous cases
   - Share knowledge with team

### NIBRS Submission

1. **Pre-Submission Checklist**
   - [ ] All incidents mapped or reviewed
   - [ ] No unmapped types in export
   - [ ] Non-crimes excluded
   - [ ] Duplicate checking complete
   - [ ] Data quality report generated

2. **Monthly Submission Workflow**
   ```
   Week 1: Process all incidents
   Week 2: Review ambiguous cases
   Week 3: Quality validation
   Week 4: Generate submission file
   ```

---

## 📚 Additional Resources

### FBI NIBRS Resources
- NIBRS User Manual 2023.0
- NIBRS Technical Specification
- NIBRS Data Element Definitions

### Internal Documents
- nibrs_offense_definitions.md
- RMS_NIBRS_Mapping_Guide.md
- Police_Analytics_Implementation_TODO.md

### Support
- **Technical Issues:** Contact IT/Analytics team
- **Classification Questions:** Review NIBRS manual or consult supervisor
- **Mapping Updates:** Submit request to Principal Analyst

---

## 📝 Change Log

### Version 1.0 (2026-01-16)
- Initial implementation
- 85 RMS incident types mapped
- Python validator created
- Power BI integration complete
- Comprehensive documentation

---

**Document Status:** Final  
**Next Review:** 2026-02-16  
**Maintained By:** Principal Analyst, Hackensack PD
