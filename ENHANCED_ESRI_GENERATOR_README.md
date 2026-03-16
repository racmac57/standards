# Enhanced ESRI Output Generator - Reference Copy

**Original Location:** `C:\Users\carucci_r\OneDrive - City of Hackensack\02_ETL_Scripts\CAD_Data_Cleaning_Engine\scripts\enhanced_esri_output_generator.py`

**Copy Created:** 2026-02-04 (for documentation/reference)

**Status:** ✅ Updated with dashboard validation fixes (HACKENSACK, PHONE/911 mappings added)

---

## Purpose

This is the **PRODUCTION** normalization engine for CAD data. It applies field-level normalizations including:

1. **HowReported normalization** (lines 137-299): 280+ mappings
2. **Disposition normalization**: 30+ mappings
3. **Incident normalization**: 637 mappings from reference file
4. **Parallel processing** for performance

---

## Critical Information

### This is the AUTHORITATIVE normalizer

**✅ USE THIS:** `enhanced_esri_output_generator.py`
- Location: `CAD_Data_Cleaning_Engine/scripts/`
- Status: Production, actively maintained
- Last updated: 2026-02-04 (dashboard fix)

**❌ DO NOT USE:** `standardize_cads.py`
- Location: `unified_data_dictionary/src/`
- Status: Legacy, being archived
- Replaced by: enhanced_esri_output_generator.py

---

## Recent Updates (2026-02-04)

### Dashboard Validation Fix

**Problem:** Dashboard showed invalid HowReported values from raw baseline data

**Root Cause:** Normalization step was skipped after consolidation
- `consolidate_cad_2019_2026.py` merged files → Created raw CSV
- `enhanced_esri_output_generator.py` was NOT run → Normalization skipped
- Dashboard consumed unnormalized data

**Solution:** Added 2 missing mappings (lines 297-299):
```python
'HACKENSACK': 'Phone',      # Location reference/typo found in dashboard
'PHONE/911': 'Phone',       # Mixed value found in dashboard
```

**Note:** Most dashboard invalid values were already covered by existing mappings:
- `ppp`, `u`, `mv` → Already mapped to `Phone`
- `y789`, `9155`, `911` → Already mapped to `9-1-1`
- `r` (lowercase) → Handled by case-insensitive matching (line 326: `.str.upper()`)
- `pLito` → Already mapped to `Phone` (line 236: `'PLITO'`)

---

## How It Works

### Input
- CSV file with raw CAD data
- Expected ~724K records (consolidated 2019-2026)

### Processing
1. **Load data** with optimized dtypes
2. **Apply field normalizations** (parallel processing)
   - HowReported: 280+ mappings
   - Disposition: 30+ mappings
   - Incident: 637 mappings
3. **Column ordering** to match ESRI requirements
4. **Export to Excel** with proper formatting

### Output
- Excel file: `CAD_ESRI_POLISHED_[timestamp].xlsx`
- Sheet name: `Sheet1` (required by ArcGIS)
- Columns: 20 ESRI-required fields in specific order

---

## Usage

### Basic Execution
```powershell
cd "C:\Users\carucci_r\OneDrive - City of Hackensack\02_ETL_Scripts\CAD_Data_Cleaning_Engine"

python scripts/enhanced_esri_output_generator.py \
  --input "data/01_raw/2019_to_2026_01_30_CAD.csv" \
  --output-dir "data/03_final" \
  --format excel
```

### With Parallel Processing (Recommended)
```powershell
python scripts/enhanced_esri_output_generator.py \
  --input "data/01_raw/2019_to_2026_01_30_CAD.csv" \
  --output-dir "data/03_final" \
  --format excel \
  --enable-parallel true \
  --n-workers 4
```

**Runtime:** ~45-60 minutes for 724K records on 4 cores

---

## Validation

### Expected Output Characteristics
- Record count: 724,794 (unchanged from input)
- Unique cases: 559,202
- HowReported: 100% domain compliance (only 12 valid values)
- Disposition: 100% domain compliance
- No new NULL values introduced

### Valid HowReported Values (after normalization)
1. `9-1-1`
2. `Phone`
3. `Walk-In`
4. `Self-Initiated`
5. `Radio`
6. `eMail`
7. `Mail`
8. `Other - See Notes`
9. `Fax`
10. `Teletype`
11. `Virtual Patrol`
12. `Canceled Call`

**Any other value in output = normalization failed**

---

## Troubleshooting

### Issue: "Invalid HowReported values in output"
**Cause:** Mapping missing for specific variant
**Solution:** 
1. Check HOW_REPORTED_MAPPING (lines 137-299)
2. Add missing variant in UPPERCASE
3. Re-run generator
4. Validate output

### Issue: "Record count changed"
**Cause:** Filtering or deduplication occurred
**Solution:** Check input CSV integrity, verify no date filtering

### Issue: "Takes too long"
**Cause:** Not using parallel processing
**Solution:** Add `--enable-parallel true --n-workers 4`

---

## Dependencies

Required Python packages:
- pandas
- numpy
- openpyxl (for Excel output)
- concurrent.futures (built-in)

Install:
```powershell
pip install pandas numpy openpyxl
```

---

## Integration with Dashboard

### Data Flow
```
Raw CAD Exports (Excel)
    ↓
consolidate_cad_2019_2026.py
    ↓
2019_to_2026_01_30_CAD.csv (raw)
    ↓
enhanced_esri_output_generator.py ← YOU ARE HERE
    ↓
CAD_ESRI_POLISHED_[timestamp].xlsx (normalized)
    ↓
copy_polished_to_processed_and_update_manifest.py
    ↓
13_PROCESSED_DATA/ESRI_Polished/base/CAD_ESRI_Polished_Baseline.xlsx
    ↓
ArcGIS Pro Dashboard
```

### Critical Path Rule
**NEVER skip this step** - Dashboard will show raw, unnormalized data if you deploy consolidated CSV directly

---

## Version History

| Date | Version | Changes |
|------|---------|---------|
| 2025-12-22 | 3.0 | Complete rewrite with parallel processing, 280+ HowReported mappings |
| 2026-02-04 | 3.1 | Added HACKENSACK, PHONE/911 mappings for dashboard validation |

---

## Contact

**Author:** R. A. Carucci  
**Department:** City of Hackensack Police Department  
**Purpose:** CAD/RMS data quality system for ArcGIS Pro dashboards

---

**Last Updated:** 2026-02-04  
**Status:** Production-ready with dashboard validation fixes
