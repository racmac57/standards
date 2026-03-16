# Changelog

All notable changes to this Standards folder (structure and key artifacts) will be documented here.

## [Unreleased]

### Fixed
- **tools\NULL removed**: Leftover UDD directory (v2.2.0 Known Issues) deleted; OneDrive "path is too long" error for that path resolved. `Fix_OneDrive_Long_Path_Issue.ps1` (in SYNC) was extended to support `NULL`→`udd_legacy` when Repair is used.

---

## [v2.3.0] - 2026-01-17

### Added
- **NIBRS Standards**: FBI NIBRS 2023.0 offense classifications and RMS mappings
  - 81 NIBRS offense definitions (71 Group A + 10 Group B)
  - 85 Hackensack RMS incident type mappings with 68% auto-classification rate
  - Python validation scripts and Power BI integration M-Code
  - Comprehensive implementation guides and documentation
- **Reference Data Organization**: Structured GeographicData and LegalCodes directories
  - GeographicData/ZipCodes: 33,782 US ZIP codes with Hackensack proximity
  - LegalCodes/Title39: 1,414 NJ motor vehicle statutes
  - LegalCodes/2C: 4,276 NJ criminal offenses
  - LegalCodes/CityOrdinances: 36 Hackensack ordinances
  - Combined lookup files and Python enrichment scripts

### Changed
- Archived legacy FBI_UCR directory to NIBRS/DataDictionary/archive/
- Updated repository structure documentation
- Enhanced README with NIBRS integration examples

### Fixed
- Resolved documentation outdated migration status references
- Updated version synchronization across all documentation files

---

## [v2.2.0] - 2026-01-17

### Migration Complete - UDD Hybrid Migration Executed

**UDD Hybrid Migration - Successfully Completed**

#### Migration Actions Completed
- ✅ Moved `unified_data_dictionary/` → `tools/unified_data_dictionary/` (Python package preserved)
- ✅ Extracted reference data to root: `schemas/udd/` (9 files), `mappings/field_mappings/` (12 files)
- ✅ Organized standalone scripts: `scripts/validation/`, `scripts/extraction/`
- ✅ Moved documentation: `docs/html/`, `docs/generated/`
- ✅ Cleaned extracted data from tool location
- ✅ Git commit: `46577f2` - feat(migration): Complete UDD hybrid migration to tools/

#### Results
- **252 files** reorganized and committed
- Python package structure intact and functional
- Reference data now at Standards root (ready for NIBRS additions)
- Cleaner directory structure achieved

#### Known Issues
- **Old `unified_data_dictionary/` directory** had a recursive symlink issue (locked by process) and could not be fully removed. It may remain as **`tools\NULL`** with a deeply nested `Standards\unified_data_dictionary\...` structure.
- **Impact:** Can cause OneDrive **"path is too long"** errors. Does not affect UDD functionality (canonical location is `tools/unified_data_dictionary/`).
- **Fix:** Remove the `tools\NULL` tree (exit OneDrive first):  
  `Remove-Item -LiteralPath "…\09_Reference\Standards\tools\NULL" -Recurse -Force`  
  If long-path errors occur, run **`Fix_OneDrive_Long_Path_Issue.ps1 -Repair -RootPath "…\09_Reference\Standards\tools\NULL"`** (see `SYNC\Fix_OneDrive_Long_Path_Issue_README.md`), then delete `tools\udd_legacy`.

#### Next Steps
- Update external systems (Power BI, ETL scripts) to use new paths
- Consider creating symbolic links if external systems need gradual migration
- **Remove `tools\NULL` (old directory) after process unlock** — see Known Issues above.

---

## [v2.1.0] - 2026-01-16

### Migration Planning - Pre-Flight Phase

**UDD Hybrid Migration - Pre-Flight Assessment Complete**

#### Documentation Added

**Migration Planning Suite** (`docs/merge/`)
- Created comprehensive migration documentation (17 documents)
- **PRE-FLIGHT-CHECKLIST.md** - Mandatory checks before migration
  - UDD functionality testing (pip install, CLI, pytest)
  - External dependency search (Power BI, ETL scripts, scheduled tasks)
  - Git status verification
  - Backup requirements
  - OneDrive sync checks
  - Long path validation
- **CRITICAL-BLIND-SPOTS.md** - Risk assessment identifying 15 potential issues
  - External system dependencies (Power BI, ETL scripts)
  - OneDrive sync risks and file locking
  - Git history considerations (Move-Item vs git mv)
  - Path length limits (Windows 260-char)
  - Virtual environment impacts
  - "Why are we doing this?" analysis
- **EXTERNAL-DEPENDENCIES-TRACKING.md** - System update tracking
  - Power BI report update procedures
  - ETL script migration paths
  - Scheduled task modifications
  - Three migration strategy options (Phased, Maintenance Window, Symbolic Links)
  - Post-migration checklist (5-6 hours estimated)
- **PRE-FLIGHT-RESULTS.md** - Automated assessment results
- **MIGRATION-STATUS-CURRENT.md** - Real-time status tracking
- **CLAUDE-CODE-PROMPT.md** - Automation instructions with code header standards
- **05-UDD-Hybrid-Migration-REVISED.md** - Hybrid migration approach (recommended)
- **04-UDD-Migration-Plan.md** - Original flattening approach (deprecated)
- **APPROACH-COMPARISON.md** - Strategy comparison (flatten vs hybrid)
- **00-QuickStart.md** - Status at a glance
- **01-ActionPlan.md** - Detailed execution plan
- **02-DetailedAssessment.md** - Comprehensive file analysis
- **03-RecentFilesReview.md** - Git history review
- **QUICK-REFERENCE.md** - 2-minute overview card
- **DOCUMENTATION-UPDATE-SUMMARY.md** - Complete change summary
- **PRE-FLIGHT-RESULTS-TEMPLATE.md** - Template for results
- **COMMIT-PLAN.md** - This commit's structured plan

**Root-Level Files**
- **MERGE-STATUS.md** - Pointer to merge documentation
- **MERGE_COMPLETION_ASSESSMENT.md** - Initial assessment (being replaced by docs/merge/)

#### Code Header Standards

**Implemented standardized headers for all code artifacts**
- Format: 🕒 timestamp (EST), project path, author (R. A. Carucci), purpose
- Language-specific comment symbols:
  - Python: `#`
  - PowerShell: `#`
  - M Code/JavaScript: `//`
  - VBA: `'`
  - SQL: `--`
- Applied to all migration scripts and documentation

#### Pre-Flight Validation Results

**All Critical Checks Passed** ✅
- **UDD tool functionality**: `pip install -e .` → SUCCESS
- **CLI functionality**: `udd --help` → SUCCESS
- **Test suite**: `pytest` → ALL TESTS PASS
- **Python package structure**: Sound, no breaking changes found
- **Import dependencies**: All valid, relative imports work
- **Configuration files**: No path issues found
- **Git status**: Clean, on feature branch
- **Backup created**: **139,390 files** at `C:\Temp\Standards_Backup_20260116_181122`
- **Migration branch created**: `feature/udd-hybrid-migration`

**Risk Assessment** ⚠️
- **External dependencies confirmed**: Power BI reports and ETL scripts reference UDD paths
- **Highest risk**: External system breakage if paths not updated
- **Recommendation**: Symbolic links strategy for zero-downtime migration
- **Status**: CONDITIONAL GO pending external dependency documentation

#### Migration Strategy Options

**Option 1: Phased Migration**
- Migrate in stages, update systems incrementally
- Time: 2-3 days | Risk: MEDIUM | Downtime: Minimal

**Option 2: Maintenance Window**
- Migrate all at once, update all systems same day
- Time: 6-8 hours continuous | Risk: MEDIUM-HIGH | Downtime: 4-8 hours

**Option 3: Symbolic Links** ⭐ **RECOMMENDED**
- Migrate UDD, create symlinks at old locations
- External systems work unchanged
- Update systems gradually over time
- Time: 2-3 hours migration + gradual updates | Risk: LOW | Downtime: ZERO

#### Next Phase

**Pending**: Execute UDD hybrid migration with symbolic links strategy
- Move UDD Python project to `tools/unified_data_dictionary/` (preserves functionality)
- Extract reference data (schemas, mappings, templates) to Standards root
- Create symbolic links (junction points) at old UDD locations
- External systems continue working via symlinks
- Update external systems gradually post-migration (no rush)

---

## [v2.0.0] - 2026-01-15

### Repository Restructuring

Major cleanup and reorganization of the Standards repository.

#### Changes

**Nested Git Repository Removed**
- Removed nested `.git/` from `unified_data_dictionary/`
- Repository now has single `.git/` at root
- Backup of nested git saved to `archive/legacy_copies/udd_git_backup/`

**Archive Structure Created**
- New `archive/` directory with subdirectories:
  - `packages/` - Packaging artifacts (Standards.7z moved here)
  - `legacy_copies/` - Legacy file versions
  - `removed_duplicates/` - Duplicate files removed during cleanup
- See `archive/README.md` for retention policy

**Duplicate Files Resolved**
- `CallType_Categories_backup_20260109_214115.csv` removed (duplicate of latest)
- Canonical locations established for mapping files:
  - `CAD_RMS/DataDictionary/current/schema/` for cad_to_rms, rms_to_cad mappings
  - `RMS/DataDictionary/current/schema/` for rms_export_field_definitions.md
- Pointer files added in `unified_data_dictionary/` pointing to canonical locations

**Legacy Files Archived**
- Root-level legacy mapping files moved to `archive/legacy_copies/`:
  - `cad_to_rms_field_map.json` (older version)
  - `rms_to_cad_field_map.json` (older version)
  - `multi_column_matching_strategy.md` (older version)

**Chatlog Structure Flattened**
- 9 nested chatlog folders flattened from `chunked/<topic>/<timestamp>_<topic>/` to `chunked/<timestamp>_<topic>/`

**unified_data_dictionary Integrated**
- Content from previously nested repository now part of main repo

---

## [v1.2.2] - 2026-01-14

### Added
- **Response Time Filter Configuration**
  - New config directory: `config/`
  - Added `config/response_time_filters.json` - JSON configuration for Response Time ETL filtering rules
  - Configuration includes:
    - How Reported exclusions (Self-Initiated)
    - Category_Type exclusions (4 categories: Regulatory/Ordinance, Admin/Support, Investigations, Community Engagement)
    - Specific incident exclusions (41 incidents)
    - Inclusion overrides (14 incidents kept despite category exclusion)
  - Source: `Master_Automation/config/response_time_filters.json`
  - Used by: `02_ETL_Scripts/Response_Times/response_time_monthly_generator.py` (v2.0.0)

---

## [v1.2.1] - 2026-01-09

### Added
- **Backup Strategy for CallType_Categories.csv**
  - Timestamped backups created in both CallTypes directory and Standards directory
  - Backup script: `scripts/backup_calltype_categories.py` (in Year-End Report project)
  - Backups created: `CallType_Categories_backup_YYYYMMDD_HHMMSS.csv`
  - "Latest" copy maintained in Standards directory: `CallType_Categories_latest.csv`
  - Backup locations:
    - Primary: `09_Reference/Classifications/CallTypes/` (same directory as source)
    - Secondary: `09_Reference/Standards/` (centralized reference location)

### Updated
- **Documentation** - Updated category counts in README.md and call_type_category_mapping.md to reflect actual counts (122 Admin/Support, 201 Criminal Incidents, 85 Public Safety, etc.)

## [v1.2.0] - 2026-01-08

### Fixed
- **Standardized to 11 ESRI Categories Only**
  - Fixed category mapping: All entries now use only the 11 ESRI standard categories
  - Mapped non-standard categories to ESRI standard:
    - "Miscellaneous" → "Public Safety and Welfare" (14 entries)
    - "Uncategorized" → "Public Safety and Welfare" (4 entries)
    - "Criminal Investigation" → "Criminal Incidents" (39 entries)
    - "Patrol and Prevention" → "Public Safety and Welfare" (8 entries)
    - "Community Engagement and Services" → "Community Engagement" (2 entries)
  - Total categories reduced from 16 to 11 (ESRI standard)
  - **ESRI Standard Categories** (11 total):
    1. Administrative and Support
    2. Assistance and Mutual Aid
    3. Community Engagement
    4. Criminal Incidents
    5. Emergency Response
    6. Investigations and Follow-Ups
    7. Juvenile-Related Incidents
    8. Public Safety and Welfare
    9. Regulatory and Ordinance
    10. Special Operations and Tactical
    11. Traffic and Motor Vehicle

### Added
- **Added 9 Remaining Unmatched Types from 2023 RMS Processing**
  - Missing Person- Return → Investigations and Follow-Ups
  - Motor Vehicle Theft → Criminal Incidents
  - Duty to Warn-E.D.P. → Public Safety and Welfare
  - FERPO/TERPO → Emergency Response
  - Handle With Care → Emergency Response
  - Medical Emergency → Public Safety and Welfare
  - Evidence Delivery / Retrieval → Investigations and Follow-Ups
  - (Child Safety Seat Installation...) → Community Engagement
  - Invasion of Privacy → Criminal Incidents
  - Total entries: 649 (up from 640)

## [v1.1.0] - 2026-01-08

### Updated
- **Call Type to Category Type Mapping System - Single Source of Truth**
  - Primary reference file renamed: `CallType_Categories_.csv` → `CallType_Categories.csv` (removed underscore)
  - Now includes `Incident_Norm` column for normalized incident type matching
  - Total entries increased from 516 to 640 entries
  - Added missing entries from archive file
  - Updated E.D.P. mappings: All E.D.P. variations (E.D.P., EDP, edp, e.d.p., etc.) now map to "Mental Health Incident"
    - Category: "Public Safety and Welfare"
    - Response: "Emergency"
    - Incident_Norm: "Mental Health Incident"
  - Format: Incident, Incident_Norm, Category_Type, Response_Type
  - **Single Source of Truth**: This file is now the authoritative reference for all Call Type classifications
  - Location: `09_Reference/Classifications/CallTypes/CallType_Categories.csv`

### Notes
- Old file `CallType_Categories_.csv` removed (replaced by `CallType_Categories.csv`)
- All scripts should reference `CallType_Categories.csv` (without underscore)
- Incident_Norm column enables better fuzzy matching and normalization
- E.D.P. variations are now properly categorized as Mental Health Incidents

## [v1.0.0] - 2026-01-08

### Added
- **Call Type to Category Type Mapping System**
  - Primary reference file: `CallType_Categories_.csv` (516 entries) - ESRI standardized classification
    - Location: `09_Reference/Classifications/CallTypes/CallType_Categories_.csv`
    - Format: Call_Type, Category, Response Type
    - 11 standardized categories based on ESRI classification system
    - 3 Response Types (Emergency, Urgent, Routine)
  - Documentation: `docs/call_type_category_mapping.md`
    - Complete breakdown of all Call Types organized by Category Type
    - Human-readable format with statistics and response type distributions
  - Category-specific CSV files: `mappings/call_types_*.csv` (11 files)
    - One file per category for targeted script loading
    - Files: administrative_and_support, assistance_and_mutual_aid, community_engagement, criminal_incidents, emergency_response, investigations_and_follow-ups, juvenile-related_incidents, public_safety_and_welfare, regulatory_and_ordinance, special_operations_and_tactical, traffic_and_motor_vehicle
  - JSON mapping file: `mappings/call_type_category_mapping.json`
    - Programmatic lookup dictionaries for Python scripts
    - Includes: `call_type_to_category`, `call_type_to_response`, `category_to_call_types`
    - Metadata: total count, categories list, response types list
  - Purpose: Streamline knowledge base with script-referenceable files for RMS Incident Type classification, filtering admin reports vs calls for service, and standardized categorization

### Notes
- All files are script-referenceable and ready for use across ETL projects
- Standardized filename (`CallType_Categories_.csv`) for consistent script references
- ESRI format maintained for compatibility with existing systems

## [v0.3.0] - 2025-12-30

### Added
- **RMS Export Field Definitions** (`rms_export_field_definitions.md`)
  - Comprehensive documentation of 29 RMS export fields
  - Organized into 8 logical groups: Incident Identification, Temporal, Incident Classification, Location, Incident Details, Property, Vehicle, Personnel, and Case Management
  - Each field includes: Export Header, Standard Name, Definition, Source Field, Format/Regex, Logic, Validation Rules, Mapping Notes, and Group classification
  - Special narrative extraction logic for deriving suspect descriptions, vehicle details, property information, and modus operandi (M.O.)
  - Multi-column matching strategy usage summary showing which RMS fields are used in each matching strategy
  - Data quality validation rules summary organized by field group
  - Integration references to `rms_to_cad_field_map_v2_enhanced.json` and `multi_column_matching_strategy.md`

### Enhanced
- **CAD Export Field Definitions** (`CAD/DataDictionary/current/schema/cad_export_field_definitions.md`)
  - Finalized draft v1.0 comprehensive CAD export field definitions and validation rules
  - Cross-referenced with RMS definitions and mapping schemas
  - Standardized field naming conventions and validation patterns
- Updated `README.md` with reference to comprehensive RMS field definitions
- Updated `SUMMARY.md` to reflect new schema documentation
- Enhanced cross-referencing between CAD and RMS schema documentation

## 2025-12-15

- Created CAD/RMS/CAD_RMS `DataDictionary/` scaffolding:
  - `current/schema`, `current/domains`, `current/defaults`
  - `archive`, `templates`, `scripts`
- Added root documentation files:
  - `README.md`, `SUMMARY.md`, `CHANGELOG.md`
- Added per-DataDictionary documentation files:
  - `CAD/DataDictionary/{README.md,SUMMARY.md,CHANGELOG.md}`
  - `RMS/DataDictionary/{README.md,SUMMARY.md,CHANGELOG.md}`
  - `CAD_RMS/DataDictionary/{README.md,SUMMARY.md,CHANGELOG.md}`
- Added bootstrap scaffolding + placement script:
  - `CAD_RMS/DataDictionary/scripts/init_cad_rms_standards.ps1`
- Copied cross-system field maps into the canonical cross-system location:
  - `CAD_RMS/DataDictionary/current/schema/cad_to_rms_field_map.json`
  - `CAD_RMS/DataDictionary/current/schema/rms_to_cad_field_map.json`
- Initialized local Git repository:
  - `.git/` created (branch `main`)
  - `.gitignore` added

## 2025-12-17

- Added CAD export field definitions / validation rules (draft):
  - `CAD/DataDictionary/current/schema/cad_export_field_definitions.md`
- Updated summaries to reference the new CAD definitions document.
