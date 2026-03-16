# Cursor AI Agent: Standards Repository Consolidation & Dashboard Fix

**Version:** 1.1  
**Created:** 2026-02-04  
**Updated:** 2026-02-04 (Added 4 critical decisions, updated normalizer status)  
**Priority:** EMERGENCY - Production Dashboard Data Quality Issue  
**Estimated Time:** 5-6 hours (structure 60% complete)

---

## ✅ LATEST UPDATE - 2026-02-04

### Mappings Updated - Ready to Execute Phase 1

**File Modified:** `enhanced_esri_output_generator.py`
- ✅ Added `'HACKENSACK': 'Phone'` mapping (line 298)
- ✅ Added `'PHONE/911': 'Phone'` mapping (line 299)
- ✅ File location verified: `CAD_Data_Cleaning_Engine/scripts/`
- ✅ Reference copy created: `Standards/enhanced_esri_output_generator_REFERENCE.py`
- ✅ Documentation created: `Standards/ENHANCED_ESRI_GENERATOR_README.md`

**Status:** Ready to proceed with Phase 1 Task 1.4 (Re-run ESRI polishing)

### 4 Critical Decisions (Authority for Execution)

1. **Schema/Mapping Authority:** CAD_RMS v2.0 (2025-12-30) with additions
   - `enhanced_esri_output_generator.py` HOW_REPORTED_MAPPING is canonical
   - 280+ mappings cover comprehensive edge cases
   
2. **PD_BCI Files:** Archive all `-PD_BCI_01` suffixed files
   - Non-suffixed versions are canonical (actively maintained)
   - Archive to: `archive/PD_BCI_01_versions/`

3. **Validation Timing:** Consolidate first, THEN comprehensive validation
   - Need single dataset to validate against
   - Validation reveals gaps that inform normalization rules

4. **Validation Depth:** Quick review of critical fields only (HowReported, Disposition, Incident)
   - Dashboard is live with bad data - fix critical fields immediately
   - Defer comprehensive vendor documentation review

**Related Files:**
- 📄 `ENHANCED_ESRI_GENERATOR_README.md` - Complete normalizer documentation
- 📄 `Claude.md` - Updated with same 4 decisions for consistency
- 📄 `2026_02_03_Standards_directory_tree.json` - Current directory state

---

## 🚨 CRITICAL CONTEXT

### Mission
Fix production ArcGIS Pro dashboard showing invalid "Call Source" values, then complete the partially-finished Standards repository consolidation.

### Current Crisis
- **Dashboard Issue:** Showing invalid HowReported values (`hackensack`, `ppp`, `u`, `mv`, `Phone/911`, `0`, `911`, `r`, `phone`, `eMail`, etc.)
- **Root Cause:** CAD baseline (724,794 records) was consolidated but NOT normalized - ESRI polishing step skipped
- **Production Impact:** Live dashboard feeding police resource allocation decisions
- **Timeline:** Dashboard fix needed TODAY, structure cleanup can follow

### Repository State
- Directory structure `CAD/`, `RMS/`, `CAD_RMS/` already exists (60% migrated)
- `unified_data_dictionary/` still present (needs consolidation)
- Multiple duplicate mapping files across 3+ locations
- Misnamed files in `schemas/udd/` (contain quality reports, not schemas)
- Legacy normalization script `standardize_cads.py` (superseded by `enhanced_esri_output_generator.py`)
- See attached `2026_02_03_Standards_directory_tree.json` for exact current state

**Repository Locations:**
- **Standards Repository:** `C:\Users\carucci_r\OneDrive - City of Hackensack\09_Reference\Standards`
- **CAD Quality Project:** `C:\Users\carucci_r\OneDrive - City of Hackensack\02_ETL_Scripts\cad_rms_data_quality`
- **Normalization Engine:** `C:\Users\carucci_r\OneDrive - City of Hackensack\02_ETL_Scripts\CAD_Data_Cleaning_Engine`

---

## 📋 TWO-PHASE EXECUTION PLAN

### ⚠️ CRITICAL: Execute Phase 1 FIRST
**DO NOT touch repository structure until dashboard is fixed and validated.**

---

## PHASE 1: EMERGENCY DATA FIX (Execute NOW - 2 hours)

### Why This Comes First
The CAD baseline at `13_PROCESSED_DATA/ESRI_Polished/base/CAD_ESRI_Polished_Baseline.xlsx` contains raw, unnormalized HowReported values because:
1. `consolidate_cad_2019_2026.py` merged files → Created raw CSV
2. `enhanced_esri_output_generator.py` was NOT run → Normalization skipped
3. Dashboard consumes unnormalized data → Shows typos/variants

**Pipeline should be:**
```
Raw CAD Exports → consolidate_cad_2019_2026.py → Raw CSV 
→ enhanced_esri_output_generator.py → Normalized Excel → Dashboard
     ☝️ THIS STEP WAS SKIPPED
```

---

### Task 1.1: Locate & Validate Current Files (15 minutes)

#### Find the Authoritative Normalization Logic

⚠️ **IMPORTANT:** Use `enhanced_esri_output_generator.py` (PRODUCTION), NOT `standardize_cads.py` (LEGACY)

```powershell
# Primary normalizer location (PRODUCTION)
$normalizerPath = "C:\Users\carucci_r\OneDrive - City of Hackensack\02_ETL_Scripts\CAD_Data_Cleaning_Engine\scripts\enhanced_esri_output_generator.py"

# LEGACY normalizer (DO NOT USE - being archived)
$legacyPath = "C:\Users\carucci_r\OneDrive - City of Hackensack\09_Reference\Standards\unified_data_dictionary\src\standardize_cads.py"

if (Test-Path $normalizerPath) {
    Write-Host "✅ PRODUCTION normalizer found" -ForegroundColor Green
    
    # Check HOW_REPORTED_MAPPING exists (should be ~280 entries)
    $mappingLine = Select-String -Path $normalizerPath -Pattern "HOW_REPORTED_MAPPING = {" -Context 0,5
    if ($mappingLine) {
        Write-Host "✅ HOW_REPORTED_MAPPING found at line $($mappingLine.LineNumber)" -ForegroundColor Green
    }
    
    # Verify case-insensitive matching exists (critical for lowercase variants)
    $upperCheck = Select-String -Path $normalizerPath -Pattern "\.str\.upper\(\)|\.upper\(\)" 
    if ($upperCheck) {
        Write-Host "✅ Case-insensitive matching enabled" -ForegroundColor Green
    } else {
        Write-Host "⚠️ Case-insensitive matching not found - may need to add" -ForegroundColor Yellow
    }
} else {
    Write-Host "❌ CRITICAL: Normalizer not found at expected location" -ForegroundColor Red
    Write-Host "   Search for enhanced_esri_output_generator.py in CAD_Data_Cleaning_Engine/" -ForegroundColor Yellow
    exit 1
}
```

#### Find the Baseline That Needs Re-Polishing

```powershell
$baselinePath = "C:\Users\carucci_r\OneDrive - City of Hackensack\13_PROCESSED_DATA\ESRI_Polished\base\CAD_ESRI_Polished_Baseline.xlsx"

if (Test-Path $baselinePath) {
    $baseline = Get-Item $baselinePath
    $sizeGB = [math]::Round($baseline.Length / 1GB, 2)
    Write-Host "✅ Baseline found" -ForegroundColor Green
    Write-Host "   Path: $baselinePath" -ForegroundColor Gray
    Write-Host "   Size: $sizeGB GB" -ForegroundColor Gray
    Write-Host "   Modified: $($baseline.LastWriteTime)" -ForegroundColor Gray
} else {
    Write-Host "⚠️ Baseline not at expected location" -ForegroundColor Yellow
    Write-Host "   Searching for CAD_ESRI_Polished*.xlsx..." -ForegroundColor Yellow
    Get-ChildItem "C:\Users\carucci_r\OneDrive - City of Hackensack\13_PROCESSED_DATA" -Recurse -Filter "CAD_ESRI_Polished*.xlsx" | 
        Select-Object FullName, Length, LastWriteTime
}
```

#### Find the Raw Consolidated CSV to Re-Process

```powershell
$rawCsvDir = "C:\Users\carucci_r\OneDrive - City of Hackensack\02_ETL_Scripts\CAD_Data_Cleaning_Engine\data\01_raw"

if (Test-Path $rawCsvDir) {
    Write-Host "✅ Raw data directory found" -ForegroundColor Green
    $csvFiles = Get-ChildItem $rawCsvDir -Filter "*.csv" | Sort-Object LastWriteTime -Descending
    
    if ($csvFiles) {
        Write-Host "`nAvailable CSV files:" -ForegroundColor Cyan
        $csvFiles | ForEach-Object {
            $sizeMB = [math]::Round($_.Length / 1MB, 1)
            Write-Host "   $($_.Name) - $sizeMB MB - $($_.LastWriteTime)" -ForegroundColor Gray
        }
        
        # Most likely candidate
        $expected = "2019_to_2026_01_30_CAD.csv"
        if (Test-Path (Join-Path $rawCsvDir $expected)) {
            Write-Host "`n✅ Expected file found: $expected" -ForegroundColor Green
        }
    } else {
        Write-Host "❌ No CSV files found in $rawCsvDir" -ForegroundColor Red
        Write-Host "   Run consolidate_cad_2019_2026.py first" -ForegroundColor Yellow
    }
} else {
    Write-Host "❌ Raw data directory not found: $rawCsvDir" -ForegroundColor Red
}
```

---

### Task 1.2: Add Missing HowReported Mappings (15 minutes)

#### Validate Current Mappings

```powershell
$mappingFile = "C:\Users\carucci_r\OneDrive - City of Hackensack\02_ETL_Scripts\CAD_Data_Cleaning_Engine\scripts\enhanced_esri_output_generator.py"

# Check if specific invalid values are already mapped
$checkValues = @('HACKENSACK', 'PHONE/911', 'MAIL')
foreach ($val in $checkValues) {
    $found = Select-String -Path $mappingFile -Pattern "'$val':" -CaseSensitive
    if ($found) {
        Write-Host "✅ '$val' already mapped at line $($found.LineNumber)" -ForegroundColor Green
    } else {
        Write-Host "❌ '$val' NOT mapped - needs to be added" -ForegroundColor Red
    }
}

# Count total mappings
$mappingStart = (Select-String -Path $mappingFile -Pattern "HOW_REPORTED_MAPPING = {").LineNumber
$mappingEnd = (Select-String -Path $mappingFile -Pattern "^}" -Context 0,0 | Where-Object {$_.LineNumber -gt $mappingStart} | Select-Object -First 1).LineNumber
$totalMappings = $mappingEnd - $mappingStart
Write-Host "`nTotal mapping lines: $totalMappings (should be ~280)" -ForegroundColor Cyan
```

#### Add Missing Mappings (if needed)

**File to edit:** `enhanced_esri_output_generator.py`

**Invalid values found in dashboard screenshots:**
- `hackensack` → Should map to `Phone`
- `Phone/911` → Should map to `Phone`
- `Mail` → Should map to `Mail` (case variant)
- `ppp`, `u`, `mv` → Already mapped to `Phone` (lines 226, 294, 282)
- `y789`, `9155` → Already mapped to `9-1-1` (lines 255, 251)
- `pLito` → Already mapped to `Phone` (line 236)
- `0`, `911`, `r`, `phone`, `eMail` → Should work with case-insensitive matching

**If missing, add at line ~296 (before closing brace `}`):**

```python
    # Additional mappings from dashboard validation (2026-02-04)
    'HACKENSACK': 'Phone',      # Location reference/typo
    'PHONE/911': 'Phone',       # Mixed value - default to Phone
    'MAIL': 'Mail',             # Uppercase variant (lowercase already exists at line 169)
}
```

**Verify the closing brace is on a line by itself after your additions.**

---

### Task 1.3: Validate Mappings Against Actual Data (30 minutes)

#### Create Validation Script

**Save as:** `validate_howreported_mappings.py` in CAD_Data_Cleaning_Engine directory

```python
"""
Validate HowReported mappings against actual baseline data.
Identifies unmapped values that need normalization rules.
"""
import pandas as pd
import sys
from pathlib import Path

# Paths
BASELINE_PATH = Path(r"C:\Users\carucci_r\OneDrive - City of Hackensack\13_PROCESSED_DATA\ESRI_Polished\base\CAD_ESRI_Polished_Baseline.xlsx")

# Valid output values after normalization
VALID_OUTPUT_VALUES = [
    '9-1-1', 'Phone', 'Walk-In', 'Self-Initiated', 'Radio', 
    'eMail', 'Mail', 'Other - See Notes', 'Fax', 'Teletype',
    'Virtual Patrol', 'Canceled Call'
]

def main():
    print("=" * 80)
    print("HowReported Mapping Validation")
    print("=" * 80)
    
    # Load baseline
    print(f"\nLoading baseline: {BASELINE_PATH}")
    if not BASELINE_PATH.exists():
        print(f"❌ ERROR: Baseline not found at {BASELINE_PATH}")
        print("   Check if path is correct or file was moved")
        sys.exit(1)
    
    try:
        df = pd.read_excel(BASELINE_PATH, sheet_name='Sheet1')
        print(f"✅ Loaded {len(df):,} records")
    except Exception as e:
        print(f"❌ ERROR loading baseline: {e}")
        sys.exit(1)
    
    # Check if HowReported field exists
    if 'How Reported' not in df.columns:
        print(f"❌ ERROR: 'How Reported' column not found")
        print(f"   Available columns: {', '.join(df.columns[:10])}...")
        sys.exit(1)
    
    # Get unique values (case-insensitive for comparison)
    actual_values = df['How Reported'].dropna().astype(str).str.strip()
    unique_upper = actual_values.str.upper().unique()
    
    print(f"\nTotal unique HowReported values: {len(unique_upper)}")
    print(f"Total records with HowReported: {len(actual_values):,}")
    
    # Separate normalized vs unmapped
    valid_upper = [v.upper() for v in VALID_OUTPUT_VALUES]
    normalized = [v for v in unique_upper if v in valid_upper]
    unmapped = [v for v in unique_upper if v not in valid_upper]
    
    print(f"\n{'='*80}")
    print(f"VALIDATION RESULTS")
    print(f"{'='*80}")
    print(f"✅ Already normalized: {len(normalized)} values")
    print(f"❌ Need mapping rules: {len(unmapped)} values")
    
    if len(unmapped) > 0:
        print(f"\n{'='*80}")
        print(f"UNMAPPED VALUES (need normalization rules):")
        print(f"{'='*80}")
        
        # Get counts for unmapped values
        unmapped_df = df[df['How Reported'].str.upper().isin(unmapped)]
        value_counts = unmapped_df['How Reported'].value_counts()
        
        print(f"\nTop 20 unmapped values by frequency:")
        for i, (val, count) in enumerate(value_counts.head(20).items(), 1):
            pct = (count / len(df)) * 100
            print(f"  {i:2d}. '{val}' - {count:,} occurrences ({pct:.3f}%)")
        
        if len(value_counts) > 20:
            print(f"\n  ... and {len(value_counts) - 20} more unmapped values")
        
        print(f"\n{'='*80}")
        print(f"RECOMMENDATION:")
        print(f"{'='*80}")
        print(f"Add these values to HOW_REPORTED_MAPPING in enhanced_esri_output_generator.py")
        print(f"before running the ESRI polishing step.")
        
        return 1  # Exit code 1 = unmapped values found
    else:
        print(f"\n✅ ALL VALUES ALREADY MAPPED")
        print(f"   Safe to proceed with ESRI polishing")
        return 0  # Exit code 0 = success

if __name__ == "__main__":
    sys.exit(main())
```

#### Run Validation

```powershell
cd "C:\Users\carucci_r\OneDrive - City of Hackensack\02_ETL_Scripts\CAD_Data_Cleaning_Engine"
python validate_howreported_mappings.py
```

**Expected Output:**
- If mappings complete: "✅ ALL VALUES ALREADY MAPPED"
- If mappings missing: List of unmapped values with frequencies

**Action:** Add any unmapped values to `HOW_REPORTED_MAPPING` before proceeding to Task 1.4

---

### Task 1.4: Re-run ESRI Polishing (45-60 minutes runtime)

#### Pre-Flight Checks

```powershell
cd "C:\Users\carucci_r\OneDrive - City of Hackensack\02_ETL_Scripts\CAD_Data_Cleaning_Engine"

# 1. Verify input CSV exists
$inputCsv = "data/01_raw/2019_to_2026_01_30_CAD.csv"
if (Test-Path $inputCsv) {
    $csvSize = [math]::Round((Get-Item $inputCsv).Length / 1MB, 1)
    Write-Host "✅ Input CSV found: $csvSize MB" -ForegroundColor Green
} else {
    Write-Host "❌ Input CSV not found: $inputCsv" -ForegroundColor Red
    Write-Host "Available files in data/01_raw/:" -ForegroundColor Yellow
    Get-ChildItem "data/01_raw" -Filter "*.csv" | Select-Object Name, Length, LastWriteTime
    exit 1
}

# 2. Check output directory exists
if (!(Test-Path "data/03_final")) {
    New-Item -ItemType Directory -Path "data/03_final" | Out-Null
    Write-Host "✅ Created output directory: data/03_final" -ForegroundColor Green
}

# 3. Verify Python script exists
if (!(Test-Path "scripts/enhanced_esri_output_generator.py")) {
    Write-Host "❌ ESRI generator not found" -ForegroundColor Red
    exit 1
}
```

#### Execute ESRI Polishing

**⚠️ IMPORTANT:** This will take 45-60 minutes. Do NOT interrupt.

```powershell
# Record start time
$startTime = Get-Date
Write-Host "Starting ESRI polishing at $($startTime.ToString('HH:mm:ss'))" -ForegroundColor Cyan

# Run polishing with parallel processing
python scripts/enhanced_esri_output_generator.py `
  --input "data/01_raw/2019_to_2026_01_30_CAD.csv" `
  --output-dir "data/03_final" `
  --format excel `
  --enable-parallel true `
  --n-workers 4

# Check result
$endTime = Get-Date
$duration = ($endTime - $startTime).TotalMinutes
Write-Host "`nPolishing completed in $([math]::Round($duration, 1)) minutes" -ForegroundColor Cyan

# Verify output file was created
$latestOutput = Get-ChildItem "data/03_final" -Filter "CAD_ESRI_POLISHED*.xlsx" | 
                Sort-Object LastWriteTime -Descending | 
                Select-Object -First 1

if ($latestOutput) {
    $sizeMB = [math]::Round($latestOutput.Length / 1MB, 1)
    Write-Host "`n✅ SUCCESS: Polished file created" -ForegroundColor Green
    Write-Host "   Name: $($latestOutput.Name)" -ForegroundColor Gray
    Write-Host "   Size: $sizeMB MB" -ForegroundColor Gray
    Write-Host "   Path: $($latestOutput.FullName)" -ForegroundColor Gray
    
    # Save path for next step
    $global:polishedFilePath = $latestOutput.FullName
} else {
    Write-Host "`n❌ ERROR: No output file generated" -ForegroundColor Red
    Write-Host "Check console output above for errors" -ForegroundColor Yellow
    exit 1
}
```

**Expected Console Output:**
- Loading source data...
- Applying field normalization (HowReported, Disposition, etc.)
- Processing records in parallel...
- Writing to Excel...
- Complete!

**If errors occur:**
- Check Python traceback for specific error
- Verify input CSV is readable
- Ensure sufficient disk space (~100 MB needed)
- Check that pandas/openpyxl libraries are installed

---

### Task 1.5: Validate Polished Output (30 minutes)

#### Create Validation Script

**Save as:** `validate_polished_output.py` in CAD_Data_Cleaning_Engine directory

```python
"""
Comprehensive validation of polished ESRI output.
Ensures data quality before deploying to production dashboard.
"""
import pandas as pd
import sys
from pathlib import Path
from datetime import datetime

# Expected values for critical fields
VALID_HOW_REPORTED = [
    '9-1-1', 'Phone', 'Walk-In', 'Self-Initiated', 'Radio', 
    'eMail', 'Mail', 'Other - See Notes', 'Fax', 'Teletype',
    'Virtual Patrol', 'Canceled Call'
]

EXPECTED_RECORD_COUNT = 724794  # Known baseline count

def validate_polished_file(file_path: Path):
    """Validate polished ESRI output file."""
    
    print("=" * 80)
    print("POLISHED OUTPUT VALIDATION")
    print("=" * 80)
    print(f"File: {file_path.name}")
    print(f"Path: {file_path}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    # Load file
    print("\n[1/6] Loading Excel file...")
    try:
        df = pd.read_excel(file_path, sheet_name='Sheet1')
        print(f"   ✅ Loaded {len(df):,} records")
    except Exception as e:
        print(f"   ❌ ERROR loading file: {e}")
        return False
    
    # Validation 1: Record count
    print("\n[2/6] Validating record count...")
    if len(df) == EXPECTED_RECORD_COUNT:
        print(f"   ✅ Record count correct: {len(df):,}")
    else:
        diff = len(df) - EXPECTED_RECORD_COUNT
        sign = "+" if diff > 0 else ""
        print(f"   ⚠️  Record count changed: {len(df):,} ({sign}{diff})")
        print(f"      Expected: {EXPECTED_RECORD_COUNT:,}")
    
    # Validation 2: Unique case numbers
    print("\n[3/6] Validating case numbers...")
    if 'ReportNumberNew' in df.columns:
        unique_cases = df['ReportNumberNew'].nunique()
        null_cases = df['ReportNumberNew'].isna().sum()
        print(f"   ✅ Unique cases: {unique_cases:,}")
        print(f"   ✅ NULL cases: {null_cases:,} ({(null_cases/len(df)*100):.3f}%)")
    else:
        print(f"   ❌ ReportNumberNew column not found")
        return False
    
    # Validation 3: HowReported domain compliance (CRITICAL)
    print("\n[4/6] Validating HowReported domain compliance...")
    if 'How Reported' not in df.columns:
        print(f"   ❌ 'How Reported' column not found")
        return False
    
    invalid_how_reported = df[~df['How Reported'].isin(VALID_HOW_REPORTED)]
    
    if len(invalid_how_reported) == 0:
        null_count = df['How Reported'].isna().sum()
        print(f"   ✅ 100% domain compliance ({len(df):,} records)")
        print(f"   ✅ NULL values: {null_count} ({(null_count/len(df)*100):.3f}%)")
        print(f"   ✅ Ready for dashboard deployment")
    else:
        print(f"   ❌ VALIDATION FAILED: {len(invalid_how_reported):,} invalid values")
        print(f"\n   Invalid values found:")
        invalid_counts = invalid_how_reported['How Reported'].value_counts().head(20)
        for val, count in invalid_counts.items():
            print(f"      '{val}': {count:,} occurrences")
        print(f"\n   ❌ DO NOT DEPLOY - Fix mappings and re-run polishing")
        return False
    
    # Validation 4: Critical field completeness
    print("\n[5/6] Validating critical field completeness...")
    critical_fields = {
        'ReportNumberNew': 99.99,
        'Incident': 99.95,
        'Time of Call': 100.0,
        'FullAddress2': 99.90,
        'How Reported': 99.90,
        'Disposition': 99.00
    }
    
    all_passed = True
    for field, threshold in critical_fields.items():
        if field in df.columns:
            completeness = (df[field].notna().sum() / len(df)) * 100
            status = "✅" if completeness >= threshold else "❌"
            print(f"   {status} {field}: {completeness:.2f}% (threshold: {threshold}%)")
            if completeness < threshold:
                all_passed = False
        else:
            print(f"   ⚠️  {field}: Column not found")
    
    # Validation 5: Date range integrity
    print("\n[6/6] Validating date range...")
    if 'Time of Call' in df.columns:
        df['Time of Call'] = pd.to_datetime(df['Time of Call'], errors='coerce')
        min_date = df['Time of Call'].min()
        max_date = df['Time of Call'].max()
        null_dates = df['Time of Call'].isna().sum()
        
        print(f"   ✅ Date range: {min_date.date()} to {max_date.date()}")
        print(f"   ✅ NULL dates: {null_dates:,} ({(null_dates/len(df)*100):.3f}%)")
    
    # Final verdict
    print("\n" + "=" * 80)
    if len(invalid_how_reported) == 0 and all_passed:
        print("✅ ALL VALIDATIONS PASSED")
        print("=" * 80)
        print("\n🎯 SAFE TO DEPLOY TO PRODUCTION DASHBOARD")
        return True
    else:
        print("❌ VALIDATION FAILED")
        print("=" * 80)
        print("\n🛑 DO NOT DEPLOY - Fix issues and re-validate")
        return False

def main():
    # Get most recent polished file
    output_dir = Path("data/03_final")
    polished_files = sorted(output_dir.glob("CAD_ESRI_POLISHED*.xlsx"), 
                           key=lambda p: p.stat().st_mtime, 
                           reverse=True)
    
    if not polished_files:
        print("❌ ERROR: No polished files found in data/03_final/")
        return 1
    
    latest_file = polished_files[0]
    success = validate_polished_file(latest_file)
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
```

#### Run Validation

```powershell
cd "C:\Users\carucci_r\OneDrive - City of Hackensack\02_ETL_Scripts\CAD_Data_Cleaning_Engine"
python validate_polished_output.py
```

**Expected Output:**
```
================================================================================
POLISHED OUTPUT VALIDATION
================================================================================
[1/6] Loading Excel file...
   ✅ Loaded 724,794 records
[2/6] Validating record count...
   ✅ Record count correct: 724,794
[3/6] Validating case numbers...
   ✅ Unique cases: 559,202
[4/6] Validating HowReported domain compliance...
   ✅ 100% domain compliance (724,794 records)
   ✅ NULL values: 0 (0.000%)
   ✅ Ready for dashboard deployment
[5/6] Validating critical field completeness...
   ✅ ReportNumberNew: 99.997%
   ✅ Incident: 99.96%
   ✅ Time of Call: 100.00%
   ...
[6/6] Validating date range...
   ✅ Date range: 2019-01-01 to 2026-01-30
================================================================================
✅ ALL VALIDATIONS PASSED
================================================================================

🎯 SAFE TO DEPLOY TO PRODUCTION DASHBOARD
```

**If validation fails:**
1. Review error messages
2. Check which validation step failed
3. Fix issues (likely missing mappings)
4. Re-run Task 1.4 (ESRI polishing)
5. Re-validate

**DO NOT proceed to Task 1.6 unless validation passes 100%**

---

### Task 1.6: Deploy to Production (15 minutes)

#### Pre-Deployment Checklist

```powershell
# 1. Confirm validation passed
Write-Host "Did validation pass 100%? (Y/N)" -ForegroundColor Yellow
$confirm = Read-Host
if ($confirm -ne "Y") {
    Write-Host "❌ Deployment aborted - Fix validation issues first" -ForegroundColor Red
    exit 1
}

# 2. Verify deployment script exists
$deployScript = "C:\Users\carucci_r\OneDrive - City of Hackensack\02_ETL_Scripts\cad_rms_data_quality\scripts\copy_polished_to_processed_and_update_manifest.py"
if (!(Test-Path $deployScript)) {
    Write-Host "❌ Deployment script not found: $deployScript" -ForegroundColor Red
    exit 1
}

# 3. Check destination directory
$destDir = "C:\Users\carucci_r\OneDrive - City of Hackensack\13_PROCESSED_DATA\ESRI_Polished\base"
if (!(Test-Path $destDir)) {
    Write-Host "⚠️ Destination directory not found: $destDir" -ForegroundColor Yellow
    Write-Host "Creating directory..." -ForegroundColor Yellow
    New-Item -ItemType Directory -Path $destDir -Force | Out-Null
}

Write-Host "✅ Pre-deployment checks passed" -ForegroundColor Green
```

#### Execute Deployment

```powershell
cd "C:\Users\carucci_r\OneDrive - City of Hackensack\02_ETL_Scripts\cad_rms_data_quality"

# Get the validated polished file
$polishedDir = "..\CAD_Data_Cleaning_Engine\data\03_final"
$polishedFile = Get-ChildItem $polishedDir -Filter "CAD_ESRI_POLISHED*.xlsx" | 
                Sort-Object LastWriteTime -Descending | 
                Select-Object -First 1

if ($polishedFile) {
    Write-Host "Deploying: $($polishedFile.Name)" -ForegroundColor Cyan
    Write-Host "Size: $([math]::Round($polishedFile.Length / 1MB, 1)) MB" -ForegroundColor Gray
    
    # Run deployment script
    python scripts/copy_polished_to_processed_and_update_manifest.py `
      --source "$($polishedFile.FullName)" `
      --mode baseline `
      --update-manifest
    
    # Verify deployment
    $deployed = "C:\Users\carucci_r\OneDrive - City of Hackensack\13_PROCESSED_DATA\ESRI_Polished\base\CAD_ESRI_Polished_Baseline.xlsx"
    if (Test-Path $deployed) {
        $deployedFile = Get-Item $deployed
        $deployedTime = $deployedFile.LastWriteTime
        
        if ($deployedTime -gt (Get-Date).AddMinutes(-5)) {
            Write-Host "`n✅ DEPLOYMENT SUCCESSFUL" -ForegroundColor Green
            Write-Host "   File: $deployed" -ForegroundColor Gray
            Write-Host "   Size: $([math]::Round($deployedFile.Length / 1MB, 1)) MB" -ForegroundColor Gray
            Write-Host "   Modified: $deployedTime" -ForegroundColor Gray
            Write-Host "`n🎯 Dashboard will update on next refresh" -ForegroundColor Cyan
        } else {
            Write-Host "`n⚠️ File exists but timestamp unchanged" -ForegroundColor Yellow
            Write-Host "   Check deployment script output for errors" -ForegroundColor Yellow
        }
    } else {
        Write-Host "`n❌ Deployment failed - file not found at destination" -ForegroundColor Red
    }
} else {
    Write-Host "❌ No polished file found to deploy" -ForegroundColor Red
    exit 1
}
```

#### Post-Deployment Verification

```powershell
# Quick verification - open file and check HowReported values
Write-Host "`nPost-deployment verification..." -ForegroundColor Cyan

# Use Python to quickly check deployed file
python -c @"
import pandas as pd
df = pd.read_excel(r'C:\Users\carucci_r\OneDrive - City of Hackensack\13_PROCESSED_DATA\ESRI_Polished\base\CAD_ESRI_Polished_Baseline.xlsx')
valid = ['9-1-1', 'Phone', 'Walk-In', 'Self-Initiated', 'Radio', 'eMail', 'Mail', 'Other - See Notes', 'Fax', 'Teletype', 'Virtual Patrol', 'Canceled Call']
invalid = df[~df['How Reported'].isin(valid)]['How Reported'].unique()
if len(invalid) == 0:
    print('✅ Deployed file validated - No invalid HowReported values')
else:
    print(f'❌ WARNING: {len(invalid)} invalid values in deployed file')
"@
```

---

## 🎯 PHASE 1 COMPLETE - CHECKPOINT

### Success Criteria (All Must Pass)

- ✅ Validation script shows 100% HowReported domain compliance
- ✅ Record count unchanged: 724,794 records
- ✅ Unique cases: 559,202
- ✅ Deployed file timestamp within last 5 minutes
- ✅ Quick post-deployment check passes

### Deliverables for Review

1. **Validation output** - Save console output showing "✅ ALL VALIDATIONS PASSED"
2. **Deployment confirmation** - Screenshot or log showing successful deployment
3. **Dashboard screenshot** (optional) - If you can access the ArcGIS dashboard, screenshot showing clean dropdown values

### ⚠️ STOP HERE

**DO NOT PROCEED TO PHASE 2 UNTIL:**
1. Phase 1 validations all pass
2. Dashboard is confirmed working with clean data
3. You've reviewed deliverables with project owner

**If Phase 1 fails:**
1. Document the exact error
2. Save all console output
3. DO NOT touch repository structure
4. Request assistance

---

## PHASE 2: REPOSITORY CONSOLIDATION (Execute Tomorrow - 3-4 hours)

**Prerequisites:**
- ✅ Phase 1 completed successfully
- ✅ Dashboard validated with clean data
- ✅ Git repository clean (no uncommitted changes)
- ✅ Full backup created

---

### Pre-Flight Safety Checks

#### 1. Git Checkpoint

```powershell
cd "C:\Users\carucci_r\OneDrive - City of Hackensack\09_Reference\Standards"

# Check current status
git status

# If there are uncommitted changes, commit them first
git add .
git commit -m "Checkpoint before Standards repository consolidation - Phase 1 dashboard fix complete"

# Verify clean state
$status = git status --porcelain
if ($status) {
    Write-Host "⚠️ Warning: Repository has uncommitted changes" -ForegroundColor Yellow
    Write-Host $status
} else {
    Write-Host "✅ Git repository clean" -ForegroundColor Green
}
```

#### 2. Create Full Backup

```powershell
# Create backup on Desktop (not in OneDrive to avoid sync conflicts)
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$backupPath = "C:\Users\carucci_r\Desktop\Standards_Backup_$timestamp.zip"

Write-Host "Creating full backup..." -ForegroundColor Cyan
Write-Host "This may take 5-10 minutes..." -ForegroundColor Gray

Compress-Archive -Path "." -DestinationPath $backupPath -CompressionLevel Optimal

if (Test-Path $backupPath) {
    $sizeMB = [math]::Round((Get-Item $backupPath).Length / 1MB, 1)
    Write-Host "✅ Backup created: $backupPath" -ForegroundColor Green
    Write-Host "   Size: $sizeMB MB" -ForegroundColor Gray
    Write-Host "   Keep this file until consolidation is validated!" -ForegroundColor Yellow
} else {
    Write-Host "❌ Backup failed" -ForegroundColor Red
    exit 1
}
```

#### 3. Verify Directory Structure

```powershell
# Verify expected directories exist
$expectedDirs = @("CAD", "RMS", "CAD_RMS", "archive", "unified_data_dictionary")
foreach ($dir in $expectedDirs) {
    if (Test-Path $dir) {
        $itemCount = (Get-ChildItem $dir -Recurse -File | Measure-Object).Count
        Write-Host "✅ $dir exists ($itemCount files)" -ForegroundColor Green
    } else {
        Write-Host "❌ $dir not found" -ForegroundColor Red
    }
}

# Check for key files that will be moved
$keyFiles = @(
    "CAD_RMS/DataDictionary/current/schema/cad_to_rms_field_map.json",
    "unified_data_dictionary/schemas/canonical_schema.json"
)

foreach ($file in $keyFiles) {
    if (Test-Path $file) {
        Write-Host "✅ Found: $file" -ForegroundColor Green
    } else {
        Write-Host "⚠️ Not found: $file" -ForegroundColor Yellow
    }
}
```

---

### Task 2.1: Execute Master Consolidation Script

#### Create Consolidation Script

**Save as:** `consolidate_standards_repository.ps1` in Standards root directory

```powershell
#Requires -RunAsAdministrator
<#
.SYNOPSIS
    Standards Repository Consolidation Script
.DESCRIPTION
    Completes the partial migration to CAD/RMS/CAD_RMS structure.
    - Archives unified_data_dictionary and PD_BCI_01 files
    - Establishes CAD_RMS v2.0 as canonical authority
    - Updates paths in all automation scripts
    - Creates detailed log for review
.NOTES
    Version: 1.0
    Date: 2026-02-04
    Prerequisites: Git checkpoint and backup completed
#>

$ErrorActionPreference = "Stop"
$root = Get-Location
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$logFile = "consolidation_log_$timestamp.txt"
$errorLog = "consolidation_errors_$timestamp.txt"

function Write-Log {
    param(
        [string]$Message,
        [string]$Color = "White",
        [switch]$IsError
    )
    $logMessage = "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') - $Message"
    Write-Host $logMessage -ForegroundColor $Color
    Add-Content $logFile $logMessage
    if ($IsError) {
        Add-Content $errorLog $logMessage
    }
}

function Test-PathSafe {
    param([string]$Path)
    try {
        return Test-Path $Path
    } catch {
        Write-Log "Error checking path: $Path - $($_.Exception.Message)" "Red" -IsError
        return $false
    }
}

function Move-ItemSafe {
    param(
        [string]$Source,
        [string]$Destination,
        [switch]$Force
    )
    try {
        if (Test-PathSafe $Source) {
            $destDir = Split-Path $Destination -Parent
            if ($destDir -and !(Test-PathSafe $destDir)) {
                New-Item -ItemType Directory -Path $destDir -Force | Out-Null
            }
            Move-Item $Source $Destination -Force:$Force -ErrorAction Stop
            return $true
        } else {
            Write-Log "Source not found: $Source" "Yellow"
            return $false
        }
    } catch {
        Write-Log "Error moving $Source to $Destination : $($_.Exception.Message)" "Red" -IsError
        return $false
    }
}

# ============================================================================
# START CONSOLIDATION
# ============================================================================

Write-Log "╔═══════════════════════════════════════════════════════════════╗" "Cyan"
Write-Log "║   STANDARDS REPOSITORY CONSOLIDATION                          ║" "Cyan"
Write-Log "║   Version 1.0 - Emergency Dashboard Fix (Phase 2)            ║" "Cyan"
Write-Log "╚═══════════════════════════════════════════════════════════════╝" "Cyan"
Write-Log ""
Write-Log "Timestamp: $timestamp"
Write-Log "Root Directory: $root"
Write-Log "Log File: $logFile"
Write-Log ""

# ============================================================================
# STEP 1: STRUCTURE VALIDATION
# ============================================================================

Write-Log "═══════════════════════════════════════════════════════════════" "Yellow"
Write-Log "STEP 1: Validating Directory Structure" "Yellow"
Write-Log "═══════════════════════════════════════════════════════════════" "Yellow"

$requiredDirs = @("CAD", "RMS", "CAD_RMS", "archive")
$missingDirs = @()

foreach ($dir in $requiredDirs) {
    if (Test-PathSafe $dir) {
        Write-Log "  ✅ $dir exists" "Green"
    } else {
        Write-Log "  ⚠️ $dir missing - creating" "Yellow"
        New-Item -ItemType Directory -Path $dir | Out-Null
        $missingDirs += $dir
    }
}

if ($missingDirs.Count -gt 0) {
    Write-Log "Created $($missingDirs.Count) missing directories" "Yellow"
}

# ============================================================================
# STEP 1.5: ARCHIVE MISNAMED FILES (CRITICAL)
# ============================================================================

Write-Log ""
Write-Log "═══════════════════════════════════════════════════════════════" "Yellow"
Write-Log "STEP 1.5: Archiving Misnamed Files (Contain Wrong Content)" "Yellow"
Write-Log "═══════════════════════════════════════════════════════════════" "Yellow"

# These files have quality reports instead of schemas/specs
$misnamedFiles = @(
    @{Src="schemas/udd/cad_rms_schema_registry.yaml"; Name="cad_quality_report_misnamed.yaml"},
    @{Src="schemas/udd/transformation_spec.json"; Name="rms_quality_report_misnamed.json"}
)

foreach ($file in $misnamedFiles) {
    if (Test-PathSafe $file.Src) {
        $dest = "archive/merge_artifacts/$($file.Name)"
        Write-Log "  Misnamed file found: $($file.Src)" "Yellow"
        Write-Log "  Contains: Wrong content (quality report, not schema)" "Yellow"
        if (Move-ItemSafe $file.Src $dest -Force) {
            Write-Log "  ✅ Archived as: $($file.Name)" "Green"
        }
    }
}

# ============================================================================
# STEP 2: CREATE SUBDIRECTORIES
# ============================================================================

Write-Log ""
Write-Log "═══════════════════════════════════════════════════════════════" "Yellow"
Write-Log "STEP 2: Creating Subdirectory Structure" "Yellow"
Write-Log "═══════════════════════════════════════════════════════════════" "Yellow"

$subdirs = @(
    "CAD/DataDictionary/current/schemas",
    "CAD/DataDictionary/current/mappings",
    "CAD/DataDictionary/current/scripts",
    "CAD/DataDictionary/current/docs",
    "RMS/DataDictionary/current/schemas",
    "RMS/DataDictionary/current/mappings",
    "RMS/DataDictionary/current/scripts",
    "RMS/DataDictionary/current/docs",
    "CAD_RMS/DataDictionary/current/schemas",
    "CAD_RMS/DataDictionary/current/mappings",
    "CAD_RMS/DataDictionary/current/merge_policies",
    "CAD_RMS/DataDictionary/current/scripts",
    "archive/unified_data_dictionary_backup_$timestamp",
    "archive/PD_BCI_01_versions",
    "archive/merge_artifacts"
)

$createdCount = 0
foreach ($dir in $subdirs) {
    if (!(Test-PathSafe $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        Write-Log "  Created: $dir" "Green"
        $createdCount++
    }
}

Write-Log "Created $createdCount new subdirectories" "Cyan"

# ============================================================================
# STEP 3: ARCHIVE PD_BCI_01 FILES
# ============================================================================

Write-Log ""
Write-Log "═══════════════════════════════════════════════════════════════" "Yellow"
Write-Log "STEP 3: Archiving PD_BCI_01 Files" "Yellow"
Write-Log "═══════════════════════════════════════════════════════════════" "Yellow"

$pdBciFiles = Get-ChildItem -Recurse -Filter "*-PD_BCI_01*" -File -ErrorAction SilentlyContinue
if ($pdBciFiles) {
    Write-Log "Found $($pdBciFiles.Count) PD_BCI_01 files to archive" "Cyan"
    foreach ($file in $pdBciFiles) {
        $dest = "archive/PD_BCI_01_versions/$($file.Name)"
        if (!(Test-PathSafe $dest)) {
            if (Move-ItemSafe $file.FullName $dest -Force) {
                Write-Log "  ✅ Archived: $($file.Name)" "Green"
            }
        } else {
            Write-Log "  ⚠️ Already exists: $($file.Name)" "Yellow"
        }
    }
} else {
    Write-Log "No PD_BCI_01 files found (already archived?)" "Gray"
}

# ============================================================================
# STEP 4: BACKUP unified_data_dictionary
# ============================================================================

Write-Log ""
Write-Log "═══════════════════════════════════════════════════════════════" "Yellow"
Write-Log "STEP 4: Backing Up unified_data_dictionary" "Yellow"
Write-Log "═══════════════════════════════════════════════════════════════" "Yellow"

if (Test-PathSafe "unified_data_dictionary") {
    $uddBackup = "archive/unified_data_dictionary_backup_$timestamp"
    
    Write-Log "Copying unified_data_dictionary to $uddBackup..." "Cyan"
    Write-Log "(This may take a few minutes...)" "Gray"
    
    try {
        Copy-Item -Recurse "unified_data_dictionary" $uddBackup -Force
        
        # Verify backup
        $originalCount = (Get-ChildItem "unified_data_dictionary" -Recurse -File | Measure-Object).Count
        $backupCount = (Get-ChildItem $uddBackup -Recurse -File | Measure-Object).Count
        $backupSize = (Get-ChildItem $uddBackup -Recurse -File | Measure-Object -Property Length -Sum).Sum / 1MB
        
        if ($backupCount -eq $originalCount) {
            Write-Log "  ✅ Backup complete: $uddBackup" "Green"
            Write-Log "     Files: $backupCount" "Gray"
            Write-Log "     Size: $([math]::Round($backupSize, 1)) MB" "Gray"
        } else {
            Write-Log "  ⚠️ Backup file count mismatch (original: $originalCount, backup: $backupCount)" "Yellow"
        }
    } catch {
        Write-Log "  ❌ Backup failed: $($_.Exception.Message)" "Red" -IsError
        Write-Log "  ABORTING consolidation - backup is critical" "Red"
        exit 1
    }
} else {
    Write-Log "unified_data_dictionary not found (already migrated?)" "Yellow"
}

# ============================================================================
# STEP 5: MOVE CANONICAL SCHEMAS TO CAD_RMS
# ============================================================================

Write-Log ""
Write-Log "═══════════════════════════════════════════════════════════════" "Yellow"
Write-Log "STEP 5: Moving Canonical Schemas" "Yellow"
Write-Log "═══════════════════════════════════════════════════════════════" "Yellow"

$schemaMoves = @(
    @{Src="unified_data_dictionary/schemas/canonical_schema.json"; Dst="CAD_RMS/DataDictionary/current/schemas/canonical_schema.json"},
    @{Src="unified_data_dictionary/schemas/cad_fields_schema_latest.json"; Dst="CAD/DataDictionary/current/schemas/cad_fields_schema_latest.json"},
    @{Src="unified_data_dictionary/schemas/rms_fields_schema_latest.json"; Dst="RMS/DataDictionary/current/schemas/rms_fields_schema_latest.json"}
)

foreach ($move in $schemaMoves) {
    $srcName = Split-Path $move.Src -Leaf
    if (Test-PathSafe $move.Src) {
        if (!(Test-PathSafe $move.Dst)) {
            if (Move-ItemSafe $move.Src $move.Dst) {
                Write-Log "  ✅ Moved: $srcName" "Green"
            }
        } else {
            Write-Log "  ⚠️ Destination exists: $srcName (keeping newer version)" "Yellow"
        }
    } else {
        Write-Log "  ⚠️ Source not found: $srcName" "Yellow"
    }
}

# ============================================================================
# STEP 6: ESTABLISH CAD_RMS v2.0 AS AUTHORITY
# ============================================================================

Write-Log ""
Write-Log "═══════════════════════════════════════════════════════════════" "Yellow"
Write-Log "STEP 6: Establishing CAD_RMS v2.0 as Canonical Authority" "Yellow"
Write-Log "═══════════════════════════════════════════════════════════════" "Yellow"

$v2Mappings = @(
    @{Src="CAD_RMS/DataDictionary/current/schema/cad_to_rms_field_map.json"; Dst="CAD_RMS/DataDictionary/current/mappings/cad_to_rms_field_map.json"},
    @{Src="CAD_RMS/DataDictionary/current/schema/rms_to_cad_field_map.json"; Dst="CAD_RMS/DataDictionary/current/mappings/rms_to_cad_field_map.json"}
)

foreach ($mapping in $v2Mappings) {
    $name = Split-Path $mapping.Src -Leaf
    if (Test-PathSafe $mapping.Src) {
        if (!(Test-PathSafe $mapping.Dst)) {
            if (Move-ItemSafe $mapping.Src $mapping.Dst) {
                Write-Log "  ✅ Promoted v2.0: $name" "Green"
            }
        } else {
            Write-Log "  ⚠️ v2.0 mapping already exists: $name" "Yellow"
        }
    }
}

# ============================================================================
# STEP 7: ARCHIVE v1.0 MAPPINGS
# ============================================================================

Write-Log ""
Write-Log "═══════════════════════════════════════════════════════════════" "Yellow"
Write-Log "STEP 7: Archiving Older v1.0 Mappings" "Yellow"
Write-Log "═══════════════════════════════════════════════════════════════" "Yellow"

$v1Mappings = @(
    "CAD/DataDictionary/current/schema/cad_to_rms_field_map.json",
    "CAD/DataDictionary/current/schema/rms_to_cad_field_map.json"
)

foreach ($mapping in $v1Mappings) {
    if (Test-PathSafe $mapping) {
        $name = Split-Path $mapping -Leaf
        $archiveName = $name -replace "\.json", "_v1.0.json"
        $dest = "archive/merge_artifacts/$archiveName"
        
        if (Move-ItemSafe $mapping $dest -Force) {
            Write-Log "  ✅ Archived v1.0: $name" "Green"
        }
    }
}

# ============================================================================
# STEP 8: CLEAN ROOT-LEVEL DUPLICATES
# ============================================================================

Write-Log ""
Write-Log "═══════════════════════════════════════════════════════════════" "Yellow"
Write-Log "STEP 8: Cleaning Root-Level Duplicate Directories" "Yellow"
Write-Log "═══════════════════════════════════════════════════════════════" "Yellow"

$rootCleanup = @("mappings", "schemas/udd")
foreach ($item in $rootCleanup) {
    if (Test-PathSafe $item) {
        Write-Log "  Moving contents of $item to archive..." "Cyan"
        $items = Get-ChildItem $item -Recurse -File -ErrorAction SilentlyContinue
        foreach ($file in $items) {
            $relativePath = $file.FullName.Substring((Get-Location).Path.Length + 1)
            $dest = "archive/merge_artifacts/$relativePath"
            $destDir = Split-Path $dest -Parent
            
            if (!(Test-PathSafe $destDir)) {
                New-Item -ItemType Directory -Path $destDir -Force | Out-Null
            }
            
            Move-ItemSafe $file.FullName $dest -Force | Out-Null
        }
        Write-Log "  ✅ Archived: $item" "Green"
    }
}

# ============================================================================
# STEP 9: GLOBAL PATH SURGERY
# ============================================================================

Write-Log ""
Write-Log "═══════════════════════════════════════════════════════════════" "Yellow"
Write-Log "STEP 9: Updating Paths in Automation Scripts" "Yellow"
Write-Log "═══════════════════════════════════════════════════════════════" "Yellow"

$scriptFiles = Get-ChildItem -Recurse -Include *.bat,*.ps1,*.py,*.yaml,*.md -File -ErrorAction SilentlyContinue | 
               Where-Object { $_.FullName -notmatch "archive" -and $_.FullName -notmatch "\.git" }

Write-Log "Scanning $($scriptFiles.Count) files for path updates..." "Cyan"

$pathUpdates = @{
    "unified_data_dictionary/schemas/" = "CAD_RMS/DataDictionary/current/schemas/"
    "unified_data_dictionary/mappings/" = "CAD_RMS/DataDictionary/current/mappings/"
    "unified_data_dictionary/" = "CAD_RMS/DataDictionary/current/"
}

$updatedCount = 0
$updatedFiles = @()

foreach ($file in $scriptFiles) {
    try {
        $content = Get-Content $file.FullName -Raw -ErrorAction Stop
        $originalContent = $content
        
        foreach ($update in $pathUpdates.GetEnumerator()) {
            $pattern = [regex]::Escape($update.Key)
            $content = $content -replace $pattern, $update.Value
        }
        
        if ($content -ne $originalContent) {
            Set-Content $file.FullName $content -ErrorAction Stop
            Write-Log "  ✅ Updated: $($file.Name)" "Green"
            $updatedCount++
            $updatedFiles += $file.Name
        }
    } catch {
        Write-Log "  ⚠️ Error updating $($file.Name): $($_.Exception.Message)" "Yellow"
    }
}

Write-Log ""
Write-Log "Updated paths in $updatedCount files" "Cyan"
if ($updatedFiles.Count -gt 0 -and $updatedFiles.Count -le 10) {
    Write-Log "Files modified: $($updatedFiles -join ', ')" "Gray"
} elseif ($updatedFiles.Count -gt 10) {
    Write-Log "Files modified: $($updatedFiles[0..9] -join ', ') ... and $($updatedFiles.Count - 10) more" "Gray"
}

# ============================================================================
# STEP 10: FINAL CLEANUP
# ============================================================================

Write-Log ""
Write-Log "═══════════════════════════════════════════════════════════════" "Yellow"
Write-Log "STEP 10: Final Cleanup" "Yellow"
Write-Log "═══════════════════════════════════════════════════════════════" "Yellow"

if (Test-PathSafe "unified_data_dictionary") {
    $remainingFiles = Get-ChildItem "unified_data_dictionary" -Recurse -File -ErrorAction SilentlyContinue
    if ($remainingFiles.Count -eq 0) {
        Write-Log "Removing empty unified_data_dictionary directory..." "Cyan"
        Remove-Item "unified_data_dictionary" -Recurse -Force
        Write-Log "  ✅ Removed empty unified_data_dictionary" "Green"
    } else {
        Write-Log "  ⚠️ unified_data_dictionary still has $($remainingFiles.Count) files" "Yellow"
        Write-Log "     Review before manual deletion" "Yellow"
    }
}

# ============================================================================
# CONSOLIDATION COMPLETE
# ============================================================================

Write-Log ""
Write-Log "╔═══════════════════════════════════════════════════════════════╗" "Cyan"
Write-Log "║   CONSOLIDATION COMPLETE                                      ║" "Cyan"
Write-Log "╚═══════════════════════════════════════════════════════════════╝" "Cyan"
Write-Log ""
Write-Log "Log file: $logFile" "Gray"
Write-Log "Error log: $errorLog" "Gray"
Write-Log ""
Write-Log "═══════════════════════════════════════════════════════════════" "Yellow"
Write-Log "NEXT STEPS" "Yellow"
Write-Log "═══════════════════════════════════════════════════════════════" "Yellow"
Write-Log "1. Review log files for any warnings" "White"
Write-Log "2. Run validation tests (see Task 2.3)" "White"
Write-Log "3. Test 3-5 critical scripts" "White"
Write-Log "4. Run 'git status' and commit changes" "White"
Write-Log "5. Keep backup until validated!" "Yellow"
Write-Log ""

# Display error summary if any
if (Test-Path $errorLog) {
    $errorCount = (Get-Content $errorLog | Measure-Object -Line).Lines
    if ($errorCount -gt 0) {
        Write-Log "⚠️ $errorCount errors logged - Review $errorLog" "Yellow"
    }
}
```

#### Run Consolidation Script

```powershell
cd "C:\Users\carucci_r\OneDrive - City of Hackensack\09_Reference\Standards"

# Run as Administrator (required for some file operations)
.\consolidate_standards_repository.ps1

# Script will take 5-10 minutes
# Do NOT interrupt
```

**Expected Output:**
- Step-by-step progress with colored status messages
- Green ✅ for successful operations
- Yellow ⚠️ for warnings (expected if files already moved)
- Red ❌ only for critical errors

**If script fails:**
1. Note the step number where it failed
2. Check error log file
3. Run rollback procedure (see below)
4. Request assistance

---

### Task 2.2: Validate Consolidation

#### Test 1: Schema Path Resolution

```powershell
cd "C:\Users\carucci_r\OneDrive - City of Hackensack\02_ETL_Scripts\cad_rms_data_quality"

# Test config file loads
python -c "import yaml; cfg = yaml.safe_load(open('config/schemas.yaml')); print('✅ Config loads successfully')"

# Test if schemas path is correct
python -c @"
import yaml
cfg = yaml.safe_load(open('config/schemas.yaml'))
canonical_path = cfg['schemas']['canonical'].replace('\${standards_root}', 'C:/Users/carucci_r/OneDrive - City of Hackensack/09_Reference/Standards')
print(f'Canonical schema path: {canonical_path}')
import os
if os.path.exists(canonical_path):
    print('✅ Canonical schema accessible')
else:
    print('❌ Canonical schema NOT found')
"@
```

#### Test 2: Check for Broken References

```powershell
cd "C:\Users\carucci_r\OneDrive - City of Hackensack\09_Reference\Standards"

Write-Host "Scanning for references to old paths..." -ForegroundColor Cyan

$brokenRefs = Get-ChildItem -Recurse -Include *.py,*.yaml,*.ps1,*.bat,*.md -File | 
  Select-String "unified_data_dictionary/schemas|unified_data_dictionary/mappings" | 
  Where-Object {
    $_.Line -notmatch "^#" -and           # Not a comment
    $_.Line -notmatch "archive" -and       # Not in archive path
    $_.Path -notmatch "archive" -and       # Not in archive directory
    $_.Path -notmatch "consolidation_log"  # Not in log file
  }

if ($brokenRefs) {
    Write-Host "❌ Found $($brokenRefs.Count) broken references:" -ForegroundColor Red
    $brokenRefs | ForEach-Object {
        Write-Host "   $($_.Filename):$($_.LineNumber) - $($_.Line.Trim())" -ForegroundColor Yellow
    }
    Write-Host "`n⚠️ These files need manual review" -ForegroundColor Yellow
} else {
    Write-Host "✅ No broken path references found" -ForegroundColor Green
}
```

#### Test 3: Verify v2.0 Mappings Location

```powershell
cd "C:\Users\carucci_r\OneDrive - City of Hackensack\09_Reference\Standards"

$v2Files = @(
    "CAD_RMS/DataDictionary/current/mappings/cad_to_rms_field_map.json",
    "CAD_RMS/DataDictionary/current/mappings/rms_to_cad_field_map.json",
    "CAD_RMS/DataDictionary/current/schemas/canonical_schema.json"
)

Write-Host "Verifying v2.0 canonical files..." -ForegroundColor Cyan
foreach ($file in $v2Files) {
    if (Test-Path $file) {
        $size = [math]::Round((Get-Item $file).Length / 1KB, 1)
        Write-Host "  ✅ $file ($size KB)" -ForegroundColor Green
    } else {
        Write-Host "  ❌ $file NOT FOUND" -ForegroundColor Red
    }
}
```

#### Test 4: Run Critical Scripts

**Test consolidation script:**
```powershell
cd "C:\Users\carucci_r\OneDrive - City of Hackensack\02_ETL_Scripts\cad_rms_data_quality"
python consolidate_cad_2019_2026.py --help
# Should show help without errors
```

**Test monthly validation:**
```powershell
python monthly_validation/scripts/validate_cad.py --help
# Should show help without errors
```

---

### Task 2.3: Git Commit Changes

```powershell
cd "C:\Users\carucci_r\OneDrive - City of Hackensack\09_Reference\Standards"

# Check what changed
git status

# Review changes
git diff --stat

# Stage changes
git add .

# Commit with detailed message
git commit -m "$(cat <<'EOF'
Complete Standards repository consolidation

Phase 2 of emergency dashboard fix:
- Archived unified_data_dictionary/ (backup in archive/)
- Archived all -PD_BCI_01 files
- Established CAD_RMS v2.0 as canonical authority
- Moved schemas to CAD/, RMS/, CAD_RMS/ structure
- Updated paths in automation scripts
- Cleaned up root-level duplicates

Files modified: See consolidation_log for details
Validation: All tests passed
Rollback: Full backup at Desktop/Standards_Backup_[timestamp].zip

Related to: Dashboard HowReported normalization fix (Phase 1)
EOF
)"

# Verify commit
git log -1 --stat
```

---

### Rollback Procedure (If Needed)

**If consolidation created problems:**

```powershell
cd "C:\Users\carucci_r\OneDrive - City of Hackensack\09_Reference\Standards"

Write-Host "═══════════════════════════════════════════════════════════════" "Red"
Write-Host "ROLLBACK PROCEDURE" "Red"
Write-Host "═══════════════════════════════════════════════════════════════" "Red"

# Step 1: Revert git changes
Write-Host "`nStep 1: Reverting git changes..." -ForegroundColor Yellow
git reset --hard HEAD~1
git status

# Step 2: Restore from backup (if needed)
Write-Host "`nStep 2: Finding latest backup..." -ForegroundColor Yellow
$latestBackup = Get-ChildItem "archive" -Filter "unified_data_dictionary_backup_*" -Directory | 
                Sort-Object LastWriteTime -Descending | 
                Select-Object -First 1

if ($latestBackup) {
    Write-Host "Found backup: $($latestBackup.Name)" -ForegroundColor Cyan
    Write-Host "Restore unified_data_dictionary? (Y/N)" -ForegroundColor Yellow
    $confirm = Read-Host
    
    if ($confirm -eq "Y") {
        if (Test-Path "unified_data_dictionary") {
            Remove-Item "unified_data_dictionary" -Recurse -Force
        }
        Copy-Item -Recurse $latestBackup.FullName "unified_data_dictionary" -Force
        Write-Host "✅ Restored unified_data_dictionary from backup" -ForegroundColor Green
    }
}

# Step 3: Restore full backup from Desktop (nuclear option)
Write-Host "`nStep 3: Full restore from Desktop backup available if needed" -ForegroundColor Yellow
$desktopBackup = Get-ChildItem "C:\Users\carucci_r\Desktop" -Filter "Standards_Backup_*.zip" | 
                 Sort-Object LastWriteTime -Descending | 
                 Select-Object -First 1

if ($desktopBackup) {
    Write-Host "Full backup available: $($desktopBackup.Name)" -ForegroundColor Gray
    Write-Host "To restore: Extract $($desktopBackup.FullName) to Standards directory" -ForegroundColor Gray
}

Write-Host "`n✅ Rollback complete" -ForegroundColor Green
Write-Host "Review git status and test critical scripts" -ForegroundColor Yellow
```

---

## 🎯 PHASE 2 COMPLETE - FINAL CHECKPOINT

### Success Criteria (All Must Pass)

- ✅ Consolidation script completed without errors
- ✅ Zero broken path references in codebase
- ✅ v2.0 mappings confirmed in CAD_RMS/DataDictionary/current/mappings/
- ✅ unified_data_dictionary archived or removed
- ✅ All -PD_BCI_01 files archived
- ✅ Critical scripts run without "FileNotFoundError"
- ✅ Git commit successful with clean status

### Deliverables for Review

1. **Consolidation log** - `consolidation_log_[timestamp].txt`
2. **Git commit hash** - From `git log -1`
3. **Path validation output** - Results of Test 2 (should show zero broken refs)
4. **Critical script test results** - Output from Test 4

### What Should Work Now

```
✅ Dashboard shows clean HowReported values (Phase 1)
✅ Repository structure follows CAD/RMS/CAD_RMS organization
✅ v2.0 mappings are the sole authority
✅ No duplicate schemas across multiple locations
✅ All automation scripts use updated paths
✅ Clean git history with detailed commit messages
```

### Cleanup After Validation

**After 1 week of successful operation:**

```powershell
# Can safely delete backups
Remove-Item "C:\Users\carucci_r\Desktop\Standards_Backup_*.zip"
Remove-Item "C:\...\Standards\archive\unified_data_dictionary_backup_*" -Recurse
```

---

## 📊 SUMMARY & METRICS

### Time Investment

| Phase | Estimated | Actual | Tasks |
|-------|-----------|--------|-------|
| Phase 1 (Dashboard Fix) | 2 hours | ___ hours | 6 tasks |
| Phase 2 (Consolidation) | 3-4 hours | ___ hours | 3 tasks |
| **Total** | **5-6 hours** | **___ hours** | **9 tasks** |

### Impact Metrics

**Before Consolidation:**
- ❌ Dashboard showing 18+ invalid HowReported values
- ❌ Schemas duplicated in 3+ locations
- ❌ Unclear which mapping version is authoritative
- ❌ unified_data_dictionary residue cluttering structure

**After Consolidation:**
- ✅ Dashboard showing only 12 valid normalized values
- ✅ Single source of truth: CAD_RMS v2.0 mappings
- ✅ Clean CAD/, RMS/, CAD_RMS/ structure
- ✅ Comprehensive validation and rollback procedures
- ✅ Detailed logs for audit trail

### Files Processed

- **Schemas moved:** ~5 key files to proper locations
- **Mappings consolidated:** v2.0 promoted, v1.0 archived
- **Scripts updated:** ~50-100 files (actual count in log)
- **Archives created:** 2 full backups + incremental safety
- **Data validated:** 724,794 records, 100% domain compliance

---

## 🆘 EMERGENCY CONTACTS & SUPPORT

### If Something Goes Wrong

**Phase 1 Issues (Dashboard Data):**
1. Check validation output - which test failed?
2. Review HowReported mapping in enhanced_esri_output_generator.py
3. Verify input CSV has expected record count
4. DO NOT deploy if validation fails

**Phase 2 Issues (Repository Structure):**
1. Check consolidation log for error details
2. Run rollback procedure immediately
3. Review which step failed
4. Check if files exist in backup locations

### Common Issues & Solutions

**Issue:** "FileNotFoundError" in Python scripts
- **Cause:** Path not updated correctly
- **Fix:** Check schemas.yaml paths, verify Standards location

**Issue:** Git merge conflicts
- **Cause:** Multiple people editing same files
- **Fix:** Stash changes, pull latest, reapply carefully

**Issue:** OneDrive sync conflicts
- **Cause:** Moving files while OneDrive syncing
- **Fix:** Pause OneDrive during consolidation

**Issue:** PowerShell permission denied
- **Cause:** Not running as Administrator
- **Fix:** Right-click PowerShell → Run as Administrator

---

## 📚 APPENDIX: KEY FILE LOCATIONS

### Critical Files (Post-Consolidation)

```
Production Data:
📄 13_PROCESSED_DATA/ESRI_Polished/base/CAD_ESRI_Polished_Baseline.xlsx
   └─ 724,794 records | 559,202 unique cases | Dashboard data source

Normalization Logic (PRODUCTION - USE THIS):
📄 CAD_Data_Cleaning_Engine/scripts/enhanced_esri_output_generator.py
   └─ HOW_REPORTED_MAPPING (lines 137-297) | 280+ normalization rules
   ⚠️ NOT: unified_data_dictionary/src/standardize_cads.py (LEGACY - DO NOT USE)

Canonical Authority:
📁 09_Reference/Standards/CAD_RMS/DataDictionary/current/
   ├─ schemas/canonical_schema.json          | Master field definitions
   ├─ mappings/cad_to_rms_field_map.json    | v2.0 (280 lines)
   └─ mappings/rms_to_cad_field_map.json    | v2.0 (258 lines)

Configuration:
📄 cad_rms_data_quality/config/schemas.yaml  | Schema path registry
📄 cad_rms_data_quality/config/validation_rules.yaml | Domain rules

Consolidation Script:
📄 Standards/consolidate_standards_repository.ps1 | Master consolidation script (Task 2.1)

Backups:
📁 Standards/archive/unified_data_dictionary_backup_[timestamp]/
📦 C:\Users\carucci_r\Desktop\Standards_Backup_[timestamp].zip
```

### Quick Reference Commands

```powershell
# Check dashboard baseline
Get-Item "C:\...\13_PROCESSED_DATA\ESRI_Polished\base\CAD_ESRI_Polished_Baseline.xlsx" | 
  Select LastWriteTime, @{N='SizeMB';E={[math]::Round($_.Length/1MB,1)}}

# Verify v2.0 mappings exist
Test-Path "C:\...\Standards\CAD_RMS\DataDictionary\current\mappings\*.json"

# Check for broken references
cd "C:\...\Standards"
git grep "unified_data_dictionary/" -- ':!archive' ':!*.log'

# View consolidation log
Get-Content "consolidation_log_*.txt" | Select-Object -Last 50
```

---

**END OF GUIDE**

**Version:** 1.0  
**Last Updated:** 2026-02-04  
**Maintained By:** R. A. Carucci  
**For:** Cursor AI Agent (Standards Repository Consolidation)

---

**Remember:**
- ✅ Phase 1 MUST succeed before Phase 2
- ✅ Always create backups before major operations
- ✅ Validate thoroughly at each checkpoint
- ✅ Keep logs and commit messages detailed
- ✅ Don't deploy to production until validations pass 100%

**Good luck! 🚀**
