# Changelog

All notable changes to this Standards folder (structure and key artifacts) will be documented here.

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
