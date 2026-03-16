# Summary (current state)

## What exists now

- **CAD**
  - `CAD/DataDictionary/current/schema/` contains:
    - `cad_to_rms_field_map.json`
    - `rms_to_cad_field_map.json`
    - `cad_export_field_definitions.md`
- **RMS**
  - `RMS/DataDictionary/` scaffolding exists (schema/domains/defaults + archive/templates/scripts)
- **Cross-system**
  - `CAD_RMS/DataDictionary/current/schema/` contains:
    - `cad_to_rms_field_map.json`
    - `rms_to_cad_field_map.json`

## Notes

- The two cross-system field maps are intentionally kept in **both** locations:
  - Original location under `CAD/DataDictionary/current/schema/` (existing)
  - Canonical cross-system location under `CAD_RMS/DataDictionary/current/schema/` (new)

- A bootstrap script is available at:
  - `CAD_RMS/DataDictionary/scripts/init_cad_rms_standards.ps1`

- Root + per-DataDictionary documentation exists:
  - Root: `README.md`, `SUMMARY.md`, `CHANGELOG.md`
  - Per DataDictionary: `*/DataDictionary/{README.md,SUMMARY.md,CHANGELOG.md}`

- This folder is a local Git repo:
  - `.git/` and `.gitignore` are present
