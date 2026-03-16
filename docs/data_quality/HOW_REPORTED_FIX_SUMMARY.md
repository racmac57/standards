# How Reported Field - Invalid Values Fix

**Date:** 2026-02-03  
**Issue:** ArcGIS Dashboard showing invalid values in Call Source (How Reported) dropdown  
**Status:** ✅ FIXED - Schema Updated

---

## Problem Statement

The ArcGIS daily call dashboard dropdown menu for "Call Source" (mapped to CAD field `HowReported`) was displaying values that are not in the canonical schema, causing data quality and reporting issues.

### Invalid Values Found in Dashboard

The following values were appearing in the dropdown but are **NOT** valid according to the canonical schema:

- ❌ `eMail`
- ❌ `Mail`
- ❌ `Virtual patrol`
- ❌ `Cancelled`
- ❌ `Fax`
- ❌ `Teletype`

### Valid Values (Canonical Schema)

According to the authoritative schemas in `unified_data_dictionary/schemas/`:

✅ **Correct values:**
- `9-1-1`
- `Phone`
- `Walk-in`
- `Self-Initiated`
- `Radio`
- `Other`

---

## Root Cause

The invalid values were documented in:

**File:** `CAD/DataDictionary/current/schema/cad_export_field_definitions.md`  
**Lines:** 59-71

This file is used as a reference for field definitions and may have been used to configure the ArcGIS feature class field domains.

---

## Resolution

### 1. Updated Schema Documentation

✅ **File Updated:** `CAD/DataDictionary/current/schema/cad_export_field_definitions.md`

**Changes Made:**
- Removed invalid values: `Teletype`, `Fax`, `eMail`, `Mail`, `Virtual Patrol`, `Canceled Call`
- Standardized to canonical values: `9-1-1`, `Phone`, `Walk-in`, `Self-Initiated`, `Radio`, `Other`
- Added mapping guidance for legacy values

### 2. Next Steps for ArcGIS Dashboard

To complete the fix, you need to update the ArcGIS feature class field domain:

#### Option A: Update Domain in ArcGIS Pro

1. Open the feature class in ArcGIS Pro
2. Navigate to the feature class properties → Fields
3. Find the `HowReported` or `How Reported` field
4. Update the field domain to match the canonical values above
5. Remove the invalid values from the domain
6. Save and republish the layer/service

#### Option B: Update via Python (ArcPy)

```python
import arcpy

# Set workspace
arcpy.env.workspace = "path/to/your.gdb"

# Define the feature class
fc = "CAD_Calls"  # Replace with your feature class name

# Delete old domain if it exists
try:
    arcpy.management.DeleteDomain(arcpy.env.workspace, "HowReported_Domain")
except:
    pass

# Create new domain with correct values
arcpy.management.CreateDomain(
    in_workspace=arcpy.env.workspace,
    domain_name="HowReported_Domain",
    domain_description="Method by which call was reported",
    field_type="TEXT",
    domain_type="CODED"
)

# Add correct coded values
valid_values = {
    "9-1-1": "9-1-1",
    "Phone": "Phone",
    "Walk-in": "Walk-in",
    "Self-Initiated": "Self-Initiated",
    "Radio": "Radio",
    "Other": "Other"
}

for code, description in valid_values.items():
    arcpy.management.AddCodedValueToDomain(
        in_workspace=arcpy.env.workspace,
        domain_name="HowReported_Domain",
        code=code,
        code_description=description
    )

# Assign domain to field
arcpy.management.AssignDomainToField(
    in_table=fc,
    field_name="HowReported",  # or "How_Reported" - check your field name
    domain_name="HowReported_Domain"
)

print("Domain updated successfully!")
```

### 3. Data Cleanup (If Needed)

If existing records in your feature class contain the invalid values, you'll need to clean them:

```python
import arcpy

fc = "path/to/CAD_Calls"

# Map old values to new values
value_mapping = {
    "eMail": "Other",
    "Mail": "Other",
    "Virtual patrol": "Other",
    "Virtual Patrol": "Other",
    "Cancelled": "Other",
    "Canceled Call": "Other",
    "Fax": "Phone",
    "Teletype": "Phone"
}

# Update records
with arcpy.da.UpdateCursor(fc, ["HowReported"]) as cursor:
    for row in cursor:
        old_value = row[0]
        if old_value in value_mapping:
            row[0] = value_mapping[old_value]
            cursor.updateRow(row)
            print(f"Updated: {old_value} → {row[0]}")
```

---

## Verification

After updating the ArcGIS domain and cleaning the data:

1. Refresh the dashboard in your browser (hard refresh: Ctrl+F5)
2. Check the Call Source dropdown - should only show the 6 valid values
3. Run a query to ensure no records contain the old invalid values:

```sql
SELECT DISTINCT HowReported 
FROM CAD_Calls 
WHERE HowReported NOT IN ('9-1-1', 'Phone', 'Walk-in', 'Self-Initiated', 'Radio', 'Other')
```

---

## Related Files

### Schema Files (Authoritative)
- `unified_data_dictionary/schemas/canonical_schema.json` (line 292)
- `unified_data_dictionary/schemas/transformation_spec.json` (line 459)
- `unified_data_dictionary/schemas/cad_rms_schema_registry.yaml` (lines 204-209)

### Field Mapping Files
- `unified_data_dictionary/mappings/cad_field_map_latest.json`
- `CAD/DataDictionary/current/schema/cad_to_rms_field_map.json`

### Quality Reports
- `CAD/SCRPA/cad_data_quality_report.md` (shows only valid values in actual data)

---

## Notes

- The canonical schema is the authoritative source for all valid values
- Any data export/ETL processes should normalize values to match the canonical schema
- ArcGIS field domains should always reference the canonical schema values
- The invalid values may have been legacy values from an older CAD system

---

**Updated By:** AI Assistant  
**Review Status:** Pending human review  
**Next Review Date:** After ArcGIS domain update
