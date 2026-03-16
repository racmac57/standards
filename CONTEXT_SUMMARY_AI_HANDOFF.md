# Context Summary - Standards Repository & Dashboard Fix
## For AI Agent Handoff (2026-02-04)

**Created:** 2026-02-04  
**Purpose:** Quick reference for AI agents starting work on this project  
**Priority:** EMERGENCY - Production dashboard showing bad data

---

## 🚨 CURRENT CRISIS

### What's Wrong
- **Dashboard Problem:** ArcGIS Pro "Calls for Service" dashboard showing 18+ invalid "Call Source" values
  - Examples: `hackensack`, `ppp`, `u`, `mv`, `Phone/911`, `0`, `911 `, `r`, `phone`, etc.
  - Should only show 12 canonical values (9-1-1, Phone, Walk-In, Self-Initiated, Radio, etc.)

- **Root Cause:** Normalization step was skipped during baseline generation
  - Step 1: ✅ `consolidate_cad_2019_2026.py` merged 7 years of data → Raw CSV
  - Step 2: ❌ `enhanced_esri_output_generator.py` NOT run → Normalization skipped
  - Step 3: ❌ Dashboard consumed raw unnormalized data

### What's Been Done
✅ **Identified the issue** (dashboard screenshots showed invalid values)  
✅ **Located normalization engine** (`enhanced_esri_output_generator.py`)  
✅ **Added missing mappings** (HACKENSACK, PHONE/911)  
✅ **Created execution plan** (CURSOR_AI_CONSOLIDATION_GUIDE.md)  
✅ **Made 4 critical decisions** (see below)

### What Needs to Happen Next
1. **Phase 1 (URGENT - 2 hours):** Re-run ESRI polishing with updated mappings
2. **Phase 2 (Tomorrow - 3-4 hours):** Complete repository consolidation

---

## 📚 KEY DOCUMENTS (Read These First)

### Primary Instruction Manual
📄 **`CURSOR_AI_CONSOLIDATION_GUIDE.md`** (This directory)
- Complete Phase 1 & 2 instructions
- All PowerShell/Python scripts included
- Validation procedures at each step
- Rollback instructions if something breaks
- ~7,000 lines, comprehensive

### Normalizer Documentation  
📄 **`ENHANCED_ESRI_GENERATOR_README.md`** (This directory)
- How the normalizer works
- What it does to the data
- How to run it
- Troubleshooting guide

### AI Agent Context
📄 **`Claude.md`** (This directory)
- Operational guidelines
- Repository architecture
- Critical files table
- Common pitfalls
- Version history

### Reference Files
📄 **`2026_02_03_Standards_directory_tree.json`** (This directory)
- Current directory structure (60% migrated)

📄 **`enhanced_esri_output_generator_REFERENCE.py`** (This directory)
- Copy of normalizer with mappings added
- For reference only - do NOT execute this copy

---

## 🎯 THE 4 CRITICAL DECISIONS

### 1. Which mapping format is authoritative?
**ANSWER: A (with additions) - CAD_RMS v2.0 (2025-12-30) + dashboard validation fixes**

**Rationale:**
- Most recent version (2025-12-30)
- Includes multi-column matching strategy
- 280+ comprehensive mappings
- Located in PRODUCTION normalizer: `enhanced_esri_output_generator.py`

**DO NOT USE:**
- ❌ `unified_data_dictionary/mappings/` (different format, being archived)
- ❌ `CAD/DataDictionary/current/schema/` v1.0 mappings (basic, outdated)

---

### 2. How to handle -PD_BCI_01 suffixed files?
**ANSWER: A - Archive all (scripts reference non-suffixed versions)**

**Rationale:**
- Non-suffixed versions are actively maintained (v1.3.2)
- `-PD_BCI_01` versions are frozen snapshots from initial AI setup (v0.2.1)
- No scripts reference the suffixed versions
- Archive location: `archive/PD_BCI_01_versions/`

**Files to archive:**
- `CHANGELOG-PD_BCI_LTP.md`
- `README-PD_BCI_LTP.md`
- `SUMMARY-PD_BCI_LTP.md`
- Plus any in `unified_data_dictionary/` subdirectories

---

### 3. When to do comprehensive validation?
**ANSWER: B - Consolidate first, THEN comprehensive validation**

**Rationale:**
- Need single consolidated dataset to validate against
- Validation discovers gaps in normalization (e.g., "hackensack" value found in dashboard)
- Iterative process: Consolidate → Validate → Fix mappings → Re-polish → Validate again
- Fragmented validation across 7 yearly files would miss patterns

**Workflow:**
1. ✅ Consolidate data (724,794 records) - DONE
2. ⏳ Validate (found invalid HowReported values) - IN PROGRESS
3. ✅ Update mappings (added HACKENSACK, PHONE/911) - DONE
4. ⏳ Re-run normalization - NEXT STEP
5. ⏳ Validate normalized output - AFTER STEP 4
6. ⏳ Deploy to dashboard - AFTER STEP 5

---

### 4. How thorough should schema validation be?
**ANSWER: A - Quick review of critical fields only**

**Rationale:**
- Dashboard is LIVE with BAD DATA - need fast fix
- Critical fields: HowReported, Disposition, Incident (drive dashboard analytics)
- Other fields (Officer, Unit, TimeDispatched) are "nice to have" but not blocking
- Can do comprehensive vendor documentation review later

**Priority:**
1. **NOW:** HowReported (Call Source) - BROKEN, visible to users
2. **NOW:** Disposition, Incident - Core analytics fields
3. **LATER:** Address quality, response time calculations
4. **MUCH LATER:** Stakeholder workshop, vendor documentation review

---

## 🔑 CRITICAL FILE LOCATIONS

### Production Normalizer (USE THIS)
```
C:\Users\carucci_r\OneDrive - City of Hackensack\02_ETL_Scripts\CAD_Data_Cleaning_Engine\scripts\enhanced_esri_output_generator.py
```
- **Status:** ✅ Updated with dashboard fixes (2026-02-04)
- **Lines 137-299:** HOW_REPORTED_MAPPING (280+ entries)
- **Purpose:** Normalizes HowReported, Disposition, Incident fields

### Legacy Normalizer (DO NOT USE)
```
C:\Users\carucci_r\OneDrive - City of Hackensack\09_Reference\Standards\unified_data_dictionary\src\standardize_cads.py
```
- **Status:** ❌ DEPRECATED - Being archived
- **Replaced by:** enhanced_esri_output_generator.py

### Dashboard Data Source
```
C:\Users\carucci_r\OneDrive - City of Hackensack\13_PROCESSED_DATA\ESRI_Polished\base\CAD_ESRI_Polished_Baseline.xlsx
```
- **Records:** 724,794 (2019-01-01 to 2026-01-30)
- **Unique cases:** 559,202
- **Status:** ❌ Contains unnormalized data - needs replacement

### Input for Re-Processing
```
C:\Users\carucci_r\OneDrive - City of Hackensack\02_ETL_Scripts\CAD_Data_Cleaning_Engine\data\01_raw\2019_to_2026_01_30_CAD.csv
```
- **Purpose:** Raw consolidated CSV to be normalized

---

## ⚡ QUICK START FOR NEW AI AGENT

### If Starting Fresh
1. **Read this file first** (you're doing it!)
2. **Open:** `CURSOR_AI_CONSOLIDATION_GUIDE.md`
3. **Start at:** Phase 1, Task 1.4 (mappings already added, skip to re-running)
4. **Execute:** Follow tasks sequentially
5. **Validate:** Run validation scripts at each checkpoint

### If Resuming Work
1. **Check status:** Look for "✅ LATEST UPDATE" section at top of CURSOR_AI_CONSOLIDATION_GUIDE.md
2. **Find checkpoint:** Look for last completed task
3. **Resume:** Continue from next task

### If Something Breaks
1. **STOP immediately**
2. **Check log files:** Look for error messages
3. **Run rollback:** See CURSOR_AI_CONSOLIDATION_GUIDE.md rollback procedures
4. **Git reset:** `git reset --hard HEAD` if needed
5. **Restore backup:** Desktop has full backup ZIP

---

## 🎬 EXECUTION TIMELINE

### Phase 1: Dashboard Fix (URGENT - Start Now)
- **Duration:** 2 hours
- **Priority:** EMERGENCY
- **Goal:** Get dashboard showing clean data

**Tasks:**
1. ~~Locate files~~ ✅ DONE
2. ~~Add mappings~~ ✅ DONE  
3. ~~Validate mappings~~ ✅ DONE
4. ⏳ Re-run ESRI polishing (45-60 min runtime)
5. ⏳ Validate polished output (30 min)
6. ⏳ Deploy to production (15 min)

### Phase 2: Repository Consolidation (Execute Tomorrow)
- **Duration:** 3-4 hours
- **Priority:** Secondary (after dashboard fixed)
- **Goal:** Clean up repository structure

**Tasks:**
1. ⏳ Create backups (git + ZIP)
2. ⏳ Run consolidation script (5-10 min)
3. ⏳ Validate structure (1 hour)
4. ⏳ Test critical scripts (1 hour)
5. ⏳ Git commit changes

---

## 🚫 COMMON MISTAKES TO AVOID

### ❌ Don't skip Phase 1 validation
**Problem:** Deploy unnormalized data → Dashboard still broken  
**Solution:** Run validation script, check for 100% domain compliance

### ❌ Don't use legacy normalizer
**Problem:** `standardize_cads.py` has outdated mappings → Still shows invalid values  
**Solution:** Use `enhanced_esri_output_generator.py` (280+ mappings)

### ❌ Don't start Phase 2 before Phase 1 complete
**Problem:** Touch repository structure while debugging data issue → Confusion  
**Solution:** Complete dashboard fix, validate, THEN do consolidation

### ❌ Don't modify production baseline directly
**Problem:** Corruption, no rollback → Production data lost  
**Solution:** Always generate NEW file, validate, then deploy

### ❌ Don't skip backups
**Problem:** Consolidation breaks something, no way to restore  
**Solution:** Git checkpoint + full ZIP backup before Phase 2

---

## 📞 EMERGENCY CONTACTS

### If You Get Stuck

**Check these first:**
1. Log files (consolidation_log_*.txt)
2. Git status (`git status`)
3. Error messages in PowerShell/Python output

**Rollback procedures:**
- See CURSOR_AI_CONSOLIDATION_GUIDE.md "Rollback Procedure" sections
- Desktop has full backup: `Standards_Backup_[timestamp].zip`
- Git can revert: `git reset --hard HEAD`

**Ask for help if:**
- Validation fails and you don't know why
- Consolidation script errors and rollback doesn't work
- Dashboard still shows bad data after Phase 1
- You need clarification on any decision

---

## ✅ SUCCESS CRITERIA

### Phase 1 Success (Dashboard Fix)
- ✅ Polished file generated: `CAD_ESRI_POLISHED_[timestamp].xlsx`
- ✅ Record count unchanged: 724,794
- ✅ HowReported validation: 100% domain compliance (only 12 valid values)
- ✅ No new NULL values introduced
- ✅ Deployed to: `13_PROCESSED_DATA/ESRI_Polished/base/`
- ✅ Dashboard dropdown shows only canonical values

### Phase 2 Success (Repository Consolidation)
- ✅ `unified_data_dictionary/` archived
- ✅ All `-PD_BCI_01` files archived
- ✅ Zero broken path references in scripts
- ✅ v2.0 mappings confirmed in `CAD_RMS/DataDictionary/current/mappings/`
- ✅ 3+ critical scripts still run without errors
- ✅ Git commit with detailed message
- ✅ Consolidation log shows no errors

---

## 📊 PROJECT METRICS

**Data Scale:**
- Records: 724,794 (2019-2026)
- Unique cases: 559,202
- Years: 7 (2019-2025) + 2 months (2026)
- Files: 7 yearly + 2 monthly

**Repository Scale:**
- Total files: ~1,000+ (from directory tree)
- Archive candidates: ~200 (unified_data_dictionary + PD_BCI)
- Scripts to update: ~50-100 (path replacements)

**Time Investment:**
- Phase 1: 2 hours (critical)
- Phase 2: 3-4 hours (cleanup)
- Total: 5-6 hours

---

## 🏆 WHAT GOOD LOOKS LIKE

### After Phase 1
```powershell
# Dashboard Call Source dropdown
9-1-1             ← Only these
Phone             ← 12 values
Walk-In           ← should show
Self-Initiated    
Radio             
eMail             
Mail              
Other - See Notes 
Fax               
Teletype          
Virtual Patrol    
Canceled Call     

# No more:
hackensack        ← All these
ppp               ← gone
u
mv
Phone/911
etc.
```

### After Phase 2
```
Standards/
├── CAD/                              ← Clean, organized
├── RMS/                              ← Clean, organized
├── CAD_RMS/                          ← Canonical authority (v2.0)
├── archive/                          ← Old stuff here
│   ├── unified_data_dictionary_backup/
│   └── PD_BCI_01_versions/
└── (No more unified_data_dictionary/ clutter)
```

---

**Last Updated:** 2026-02-04  
**Status:** Ready for Phase 1 execution  
**Next Step:** Open CURSOR_AI_CONSOLIDATION_GUIDE.md, start Phase 1, Task 1.4

**Good luck! 🚀**
