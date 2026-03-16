# Standards

This folder is the **standards repository** for exports and reference materials used by the City of Hackensack (e.g., CAD, RMS, state/federal reporting).

## Data dictionaries (CAD, RMS, and cross-system)

Data dictionary artifacts are organized under:

- `CAD/DataDictionary/`
- `RMS/DataDictionary/`
- `CAD_RMS/DataDictionary/` (cross-system mapping + merge rules)

Each DataDictionary uses the same layout:

- `current/schema/`: schemas + field maps (JSON)
- `current/domains/`: allowed value sets / enumerations (JSON)
- `current/defaults/`: defaults / standardization rules (JSON)
- `archive/`: dated snapshots (read-only historical copies)
- `templates/`: reusable templates for new dictionary items
- `scripts/`: helper scripts

## Recommended JSON placement

- **Cross-system**
  - `CAD_RMS/DataDictionary/current/schema/cad_to_rms_field_map.json`
  - `CAD_RMS/DataDictionary/current/schema/rms_to_cad_field_map.json`

## CAD export field definitions

Draft CAD export field definitions and validation rules live at:

- `CAD/DataDictionary/current/schema/cad_export_field_definitions.md`

## Bootstrap script

Use `CAD_RMS/DataDictionary/scripts/init_cad_rms_standards.ps1` to create/repair the folder scaffolding and optionally place incoming JSON files into the correct locations.

## Documentation

In addition to the root docs, each DataDictionary root includes its own:

- `README.md`
- `SUMMARY.md`
- `CHANGELOG.md`

## Local Git

This folder is initialized as a **local Git repository** (see `.git/`) and includes a `.gitignore` to keep common OS/temp/editor noise out of commits.
