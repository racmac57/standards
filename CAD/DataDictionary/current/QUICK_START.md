# QUICK START - Fix Dashboard Now

**Problem:** Dashboard showing bad data  
**Solution:** 3 commands, ~1 hour

---

## Step 1: Clean the Data (5-10 min)

Open PowerShell and run:

```powershell
cd "C:\Users\carucci_r\OneDrive - City of Hackensack\09_Reference\Standards\CAD\DataDictionary\current\scripts"

python clean_howreported_data.py
```

**What it does:**
- Backs up original file
- Fixes ALL invalid values (`y789` → `Other`, `911` → `9-1-1`, etc.)
- Saves cleaned file
- Creates report

**Output Files:**
- `CAD_ESRI_Polished_Baseline.xlsx` (cleaned)
- `CAD_ESRI_Polished_Baseline_backup_TIMESTAMP.xlsx` (backup)
- `CAD_ESRI_Polished_Baseline_cleaning_report.txt` (report)

---

## Step 2: Update ArcGIS (20-30 min)

### 2a. Import Cleaned Data
1. Open ArcGIS Pro
2. Import cleaned Excel file to geodatabase
3. Overwrite existing feature class

### 2b. Update Domain
Run this (edit paths for your setup):

```powershell
python update_howreported_domain.py "C:\path\to\your.gdb" "CAD_Calls" "HowReported"
```

Or do it manually in ArcGIS Pro:
- Right-click feature class → Design → Fields
- Create domain with only 6 valid values:
  - `9-1-1`
  - `Phone`
  - `Walk-in`
  - `Self-Initiated`
  - `Radio`
  - `Other`

### 2c. Republish
- Right-click service → Overwrite Web Layer

---

## Step 3: Verify (5 min)

1. Clear browser cache (Ctrl + Shift + Delete)
2. Refresh dashboard (Ctrl + F5)
3. Click "Call Source" dropdown
4. **Should show ONLY 6 values** (no `y789`, `eMail`, etc.)

---

## That's It!

If dropdown still shows bad values:
- Check you uploaded the CLEANED file
- Verify domain was updated
- Try incognito window
- Check service was republished

---

## Files You Need

All in: `C:\Users\carucci_r\OneDrive - City of Hackensack\09_Reference\Standards\CAD\DataDictionary\current\`

**Run These:**
- `scripts/clean_howreported_data.py` ← RUN THIS FIRST!
- `scripts/update_howreported_domain.py` ← RUN THIS SECOND

**Read These:**
- `EXECUTIVE_SUMMARY.md` ← Full context
- `FIX_CHECKLIST.md` ← Detailed steps
- `HOW_REPORTED_REFERENCE.md` ← Valid values

---

## Why This Happened

The "polished" Excel file wasn't actually cleaned. It has values like:
- `u`, `y789`, `0` (errors)
- `911` instead of `9-1-1` (wrong format)
- `eMail`, `Teletype` (legacy)
- `pLito`, `hackensack` (corruption)

The cleaning script fixes all of these.

---

## Valid Values

Only these 6 values should exist:

1. **9-1-1** - Emergency 911
2. **Phone** - Non-emergency phone
3. **Walk-in** - Walk into station
4. **Self-Initiated** - Officer initiated
5. **Radio** - Radio dispatch
6. **Other** - Everything else

**NO OTHER VALUES ARE ALLOWED!**

---

**Priority:** 🔴 CRITICAL  
**Time Required:** ~1 hour  
**Difficulty:** Easy (scripts do the work)

---

**START NOW:** Run `clean_howreported_data.py`
