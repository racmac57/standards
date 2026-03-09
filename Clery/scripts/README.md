# Clery Scripts

## extract_clery_geography_from_arcgis.py

Extracts Clery geography feature classes from ArcGIS Pro projects and exports them to the Standards reference structure.

### Requirements

- **ArcGIS Pro** installed (arcpy is bundled)
- Python environment: Use ArcGIS Pro's built-in Python or `conda activate arcgispro-py3`

### Usage

```powershell
# From ArcGIS Pro Python window, or from conda env with arcpy:
cd "C:\Users\carucci_r\OneDrive - City of Hackensack\09_Reference\Standards\Clery\scripts"

# List only (discover geodatabases and feature classes, no export)
python extract_clery_geography_from_arcgis.py --dry-run

# List and export to GeoJSON
python extract_clery_geography_from_arcgis.py --export
```

### Output

- **institution_clery_geography_index.json** — Inventory of all discovered feature classes per institution
- **{institution}_{featureclass}.geojson** — Exported geography (when `--export` used)

Output location: `Clery/DataDictionary/current/institutions/`

### Institutions Scanned

- Bergen Academies
- Bergen Community College
- Bergen Community College Clery Act
- Eastwick College
- FDU Clery Act
- Parisian
- Rutgers

### Paths

Source: `10_Projects\Clery\2024\{institution}\`  
Skips: `scratch.gdb` (temporary workspace)
