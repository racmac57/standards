# Clery Reference Data — Changelog

All notable changes to the Clery reference data and scripts.

For AI agent working guidelines, see [CLAUDE.md](CLAUDE.md).

---

## [1.0.0] - 2026-03-09

### Added

**Initial release**

- **Schema**
  - `clery_crime_definitions.json` — Clery crime categories (primary, hate crime, arrest/referral, VAWA)
  - `clery_geography_definitions.json` — On-Campus, Noncampus, Public Property per DOE Handbook

- **Mappings**
  - `nibrs_to_clery_map.json` — NIBRS → Clery mapping with confidence levels

- **Documentation**
  - `REQUEST_CHECKLIST.md` — Step-by-step requirements for completing Clery requests
  - `README.md` — Overview and quick start

- **Scripts**
  - `extract_clery_geography_from_arcgis.py` — ArcPy script to extract geography from ArcGIS Pro projects
  - Uses `arcpy.da.Walk` to discover geodatabases and feature classes
  - Exports GeoJSON to `DataDictionary/current/institutions/`
  - Generates `institution_clery_geography_index.json`

- **Institution geography** (exported from ArcGIS Pro projects)
  - Eastwick College: CleryAOI, Clery_Crimes, c250_Moore_Street_Clery_2024_Geocoded
  - FDU Clery Act: FDU_Property, Surronding_Area, Polygon, Point, Annotation1k, +3
  - Parisian: Parisian_Beauty
  - Rutgers: RUTGERS_CLERY_RMS_Geocoded

### Fixed

- **extract_clery_geography_from_arcgis.py** — Fixed `AttributeError` caused by local `datetime` module shadowing stdlib; changed to `import datetime` and `datetime.datetime.now()` to avoid conflict

### Known Issues

- **Bergen Community College**: GDB structure differs (feature datasets or hosted services); geography not yet exported
- **Bergen Academies**: No GDB or APRX found; geography source TBD
- **Bergen Community College Clery Act**: APRX references FDU geodatabase (possible misconfiguration)

---

## [1.1.0] - 2026-03-09

### Documentation updates (AI review)

- **CLAUDE.md**: Added Audience, date range constraint (#5), zero-reporting and PII DO/DON'T, RMS path placeholder, Bergen CC Clery Act row, Surronding_Area [sic], Parisian Beauty Academy, See Also
- **CHANGELOG.md**: Added CLAUDE.md link, Known Issues, clarified datetime fix
- **SUMMARY.md**: Added VAWA step to data flow, turnaround estimates, REQUEST_CHECKLIST path, Surronding_Area [sic], Parisian Beauty Academy, See Also
- **README.md**: Added error handling for unmapped codes, expanded VAWA step 4, NJ statute reference, update protocol, Power BI integration, See Also

---

## Format

Version format: [MAJOR.MINOR.PATCH]  
Date format: YYYY-MM-DD
