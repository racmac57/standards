# Fix ArcGIS Dashboard - How Reported Invalid Values

**Issue:** Call Source dropdown showing MANY invalid values  
**Date:** 2026-02-03  
**Status:** Schema Fixed ✅ | **CRITICAL: Source Data Needs Cleaning** 🔴

---

## 🔴 CRITICAL FINDING

**The source Excel file has NOT been properly cleaned!**

File: `C:\Users\carucci_r\OneDrive - City of Hackensack\13_PROCESSED_DATA\ESRI_Polished\base\CAD_ESRI_Polished_Baseline.xlsx`

### Invalid Values Found (from screenshots):
- `u`, `y789`, `0` - Data entry errors
- `911` (should be `9-1-1`)
- `9155` - Typo/error
- `phone` (lowercase), `Phone/911` - Not normalized
- `pLito`, `ppp`, `r`, `mv` - Data corruption
- `hackensack` - Incorrect value
- `eMail`, `Mail`, `Virtual Patrol`, `Teletype` - Legacy values

**Impact:** The dashboard is showing the raw, uncleaned data values directly.

---

## ✅ Completed Steps

- [x] Identified invalid values in dashboard (MANY MORE than initially thought)
- [x] Located root cause: **Source Excel file needs data cleaning**
- [x] Updated field definitions to canonical values
- [x] Updated schema registry (`cad_rms_schema_registry.yaml`)
- [x] Created fix documentation and reference guide
- [x] Created Python scripts for domain update AND data cleaning

---

## ⏳ Pending Steps (Action Required)

### 🔴 STEP 0: CLEAN THE SOURCE DATA FILE (DO THIS FIRST!)

**THIS IS THE MOST IMPORTANT STEP - Do this before updating ArcGIS!**

Run the data cleaning script:

```bash
cd "C:\Users\carucci_r\OneDrive - City of Hackensack\09_Reference\Standards\CAD\DataDictionary\current\scripts"

python clean_howreported_data.py
```

This script will:
1. ✅ Create a backup of your original file
2. ✅ Analyze all How Reported values
3. ✅ Map ALL invalid values to canonical values
4. ✅ Generate a cleaning report
5. ✅ Save the cleaned file (overwrites original, but backup is created)

**The script handles these mappings:**
- `911`, `9155`, `Phone/911` → `9-1-1`
- `phone`, `ppp`, `Fax`, `Teletype` → `Phone`
- `u`, `y789`, `0`, `pLito`, `hackensack`, `mv` → `Other`
- `eMail`, `Mail`, `Virtual patrol` → `Other`
- And many more variations...

**After cleaning, verify:**
- Review the cleaning report: `CAD_ESRI_Polished_Baseline_cleaning_report.txt`
- Check that backup was created: `CAD_ESRI_Polished_Baseline_backup_YYYYMMDD_HHMMSS.xlsx`

---

### Step 1: Upload Cleaned Data to ArcGIS

After cleaning the Excel file:
1. Open ArcGIS Pro
2. Import the cleaned Excel file to your geodatabase (overwrite existing)
3. Or: Update the existing feature class with cleaned data

### Step 2: Update ArcGIS Field Domain

You need to update the ArcGIS feature class field domain to enforce valid values.

#### Option A: Use the Python Script (Recommended)

```bash
cd "C:\Users\carucci_r\OneDrive - City of Hackensack\09_Reference\Standards\CAD\DataDictionary\current\scripts"

python update_howreported_domain.py "C:\path\to\your.gdb" "CAD_Calls" "HowReported"
```

The script will:
1. ✅ Create/update the domain with correct values
2. ✅ Assign domain to the field
3. ✅ Clean any legacy values in existing data
4. ✅ Verify all values are valid

#### Option B: Manual Update in ArcGIS Pro

1. Open ArcGIS Pro
2. Connect to your geodatabase
3. Right-click the feature class → Design → Fields
4. Find the `HowReported` field
5. Click the domain dropdown
6. Create new domain: `HowReported_Domain`
7. Add these coded values:
   - `9-1-1` | Emergency 911 call
   - `Phone` | Non-emergency phone call
   - `Walk-in` | Walk-in to station
   - `Self-Initiated` | Officer self-initiated
   - `Radio` | Radio dispatch
   - `Other` | Other method
8. Remove old domain (if exists)
9. Assign new domain to field
10. Save changes

### Step 3: Clean Data in Feature Class (If Needed)

If the feature class contains records with invalid values, run this in Python window:

```python
import arcpy

fc = r"C:\path\to\your.gdb\CAD_Calls"

# Map old values to new
mapping = {
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
count = 0
with arcpy.da.UpdateCursor(fc, ["HowReported"]) as cursor:
    for row in cursor:
        if row[0] in mapping:
            row[0] = mapping[row[0]]
            cursor.updateRow(row)
            count += 1

print(f"Updated {count} records")
```

### Step 4: Republish Feature Service

1. In ArcGIS Pro, right-click the feature service
2. Select "Overwrite Web Layer"
3. Or: Share → Web Layer → Overwrite

### Step 5: Verify Dashboard

1. Clear browser cache (Ctrl + Shift + Delete)
2. Hard refresh dashboard (Ctrl + F5)
3. Click Call Source dropdown
4. **Verify only these 6 values appear:**
   - ✅ 9-1-1
   - ✅ Phone
   - ✅ Walk-in
   - ✅ Self-Initiated
   - ✅ Radio
   - ✅ Other

### Step 6: Run Verification Query

In ArcGIS Pro Python window or SQL:

```python
# Count records by HowReported value
import arcpy
fc = r"C:\path\to\your.gdb\CAD_Calls"

values = {}
with arcpy.da.SearchCursor(fc, ["HowReported"]) as cursor:
    for row in cursor:
        values[row[0]] = values.get(row[0], 0) + 1

for value, count in sorted(values.items()):
    print(f"{value}: {count}")
```

Expected output should only show the 6 valid values.

---

## 📋 Verification Checklist

After completing all steps, verify:

- [ ] Dashboard Call Source dropdown shows only 6 valid values
- [ ] No "eMail", "Mail", "Virtual patrol", etc. appear
- [ ] Existing dashboard filters/visualizations still work
- [ ] New records can only select from valid values
- [ ] Data export shows consistent values

---

## 📚 Reference Documents

Created during this fix:

1. **HOW_REPORTED_FIX_SUMMARY.md** - Complete technical summary
2. **HOW_REPORTED_REFERENCE.md** - Quick reference card  
3. **update_howreported_domain.py** - Python automation script

Updated files:

1. **cad_export_field_definitions.md** - Updated allowed values
2. **cad_rms_schema_registry.yaml** - Aligned with canonical schema

Authoritative sources:

1. **unified_data_dictionary/schemas/canonical_schema.json** (line 292)
2. **unified_data_dictionary/schemas/transformation_spec.json** (line 459)

---

## 🔍 Troubleshooting

### Issue: Invalid values still appear after update

**Solution:** 
1. Confirm feature service was republished
2. Clear all browser caches
3. Try in incognito/private window
4. Check if dashboard is using cached layer

### Issue: Script fails with permission error

**Solution:**
1. Ensure you have edit access to the geodatabase
2. Check if feature class is locked by another user
3. Close any ArcGIS Pro sessions accessing the database

### Issue: Domain update works but data not cleaned

**Solution:**
1. Run the verification query to identify problematic records
2. Manually run the data cleanup section of the script
3. Check for NULL values that need handling

---

## 📞 Need Help?

- Review: `HOW_REPORTED_FIX_SUMMARY.md` for detailed context
- Reference: `HOW_REPORTED_REFERENCE.md` for valid values
- Script: `update_howreported_domain.py` for automation

---

**Last Updated:** 2026-02-03  
**Next Review:** After ArcGIS domain update complete
