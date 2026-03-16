# Clery Act ArcGIS Pro Workflow

**Version**: 1.0  
**Date**: 2026-03-09  
**Purpose**: Document how `Clery_Crimes` and `c250_Moore_Street_Clery_2024_Geocoded` (and equivalents) are created in ArcGIS Pro so the workflow can be repeated for 2025 and future years.

---

## Overview

The Eastwick College 2024 Clery project (`10_Projects\Clery\2024\Eastwick College\2024_Eastwick_College`) uses two main geoprocessing workflows:

1. **Clery_Crimes** — Crimes from the Hackensack PD Crimes feature service that fall **within** the institution's Clery geography (CleryAOI polygon)
2. **c250_Moore_Street_Clery_2024_Geocoded** — Point features created by **geocoding** a table of crime addresses (e.g., 8 incidents at 250 Moore Street)

Both layers are stored in the project geodatabase (`2024_Eastwick_College.gdb`).

---

## Data Sources

| Layer | Source | Type |
|-------|--------|------|
| **Crimes** | `https://services1.arcgis.com/JYl0Hy0wQdiiV0qh/arcgis/rest/services/Crimes_2153d1ef33a0414291a8eb54b938507b/FeatureServer/0` | Feature service (Hackensack PD) |
| **CleryAOI** | `2024_Eastwick_College.gdb\CleryAOI` | Polygon (institution Clery geography) |
| **Address table** | CSV or Excel with Full Address, Case Number, Incident Date, etc. | Tabular (RMS export filtered for Clery) |

---

## Workflow 1: Clery_Crimes (Crimes Within Clery Geography)

**Purpose**: Extract crimes that fall within the institution's Clery area of interest for mapping and reporting.

### Tools Used

1. **Select Layer By Location** (Data Management)
2. **Export Features** (Conversion) or **Copy Features** (Data Management)

### Steps

1. **Add layers to the map**
   - Add the **Crimes** feature service (or a local copy)
   - Add **CleryAOI** (polygon defining Clery geography)

2. **Select Layer By Location**
   - **Input Feature Layer**: Crimes
   - **Selecting Features**: CleryAOI
   - **Spatial Relationship**: `Within` (or `Intersect` if you want crimes that touch the boundary)
   - **Run** — This selects all crime points that fall inside the CleryAOI polygon

3. **Export Features**
   - **Input Features**: Crimes (with selection active)
   - **Output Feature Class**: `2024_Eastwick_College.gdb\Clery_Crimes` (or `2025_Eastwick_College.gdb\Clery_Crimes` for 2025)
   - **Run** — Creates a new point feature class with only the selected crimes

### Alternative: ModelBuilder / Python

```python
# arcpy example (run in ArcGIS Pro Python window)
arcpy.management.SelectLayerByLocation(
    "Crimes", "WITHIN", "CleryAOI", None, "NEW_SELECTION"
)
arcpy.conversion.ExportFeatures(
    "Crimes", r"C:\...\2025_Eastwick_College.gdb\Clery_Crimes"
)
```

---

## Workflow 2: c250_Moore_Street_Clery_2024_Geocoded (Geocode Addresses)

**Purpose**: Convert a table of crime addresses (from RMS export) into point features for mapping. The name pattern is `c{address}_Clery_{year}_Geocoded` (e.g., `c250_Moore_Street_Clery_2024_Geocoded`).

### Tool Used

**Geocode Addresses** (Geocoding)

### Evidence from GpMessages

- **Date**: Friday, June 6, 2025 12:31:49 PM
- **Tool**: Geocode Addresses
- **Result**: 8 Matched (100.00%), 0 Unmatched, 0 Tied
- **Output**: 8 point features (matches the 8 records in the address table)

### Steps

1. **Prepare the address table**
   - Export from RMS: Case Number, Incident Date, Full Address, NIBRS Classification, etc.
   - Filter to Clery-reportable incidents within the institution's geography and date range
   - Save as CSV or Excel with a **single address column** (e.g., `FullAddress` or `Address`)
   - For Eastwick 2024: 8 incidents at 250 Moore Street

2. **Geocode Addresses**
   - **Input Table**: Your CSV/Excel with addresses
   - **Input Address Locator**: Use default (e.g., `ArcGIS World Geocoding Service`) or a local locator (e.g., NJ address locator for better accuracy)
   - **Address Fields**: Map `Address` or `FullAddress` to the locator's address field
   - **Output Feature Class**: `2024_Eastwick_College.gdb\c250_Moore_Street_Clery_2024_Geocoded` (or `2025_Eastwick_College.gdb\c250_Moore_Street_Clery_2025_Geocoded` for 2025)
   - **Run**

3. **Verify**
   - Check match rate (aim for 100%)
   - For unmatched records, use **Rematch Addresses** or fix addresses in the source table

### Naming Convention

- `c` prefix — Common for geocoded output
- `250_Moore_Street` — Address or location identifier (no spaces in FC name)
- `Clery_2024` — Clery report year
- `Geocoded` — Indicates source was address table, not spatial selection

---

## 2025 Version: Exact Steps to Repeat

### Prerequisites

1. Create or copy the 2025 project folder:  
   `10_Projects\Clery\2025\Eastwick College\2025_Eastwick_College\`
2. Create a new geodatabase: `2025_Eastwick_College.gdb`
3. Define **CleryAOI** for 2025 (draw/import polygon for Eastwick's Clery geography)

### Step-by-Step

| Step | Action | Output |
|------|--------|--------|
| 1 | Create `2025_Eastwick_College.gdb` and `CleryAOI` polygon | CleryAOI |
| 2 | Add Crimes feature service + CleryAOI to map | — |
| 3 | **Select Layer By Location**: Crimes within CleryAOI | Selection |
| 4 | **Export Features**: Crimes → `Clery_Crimes` | Clery_Crimes |
| 5 | Export RMS data for Clery-reportable incidents (addresses) to CSV | Address table |
| 6 | **Geocode Addresses**: CSV → `c250_Moore_Street_Clery_2025_Geocoded` | Geocoded points |
| 7 | Add both layers to map, symbolize, and save project | 2025_Eastwick_College.aprx |

### Output Feature Classes (2025)

| Feature Class | Geometry | Source |
|---------------|----------|--------|
| `CleryAOI` | Polygon | Manual / imported |
| `Clery_Crimes` | Point | Select by Location + Export Features |
| `c250_Moore_Street_Clery_2025_Geocoded` | Point | Geocode Addresses |

---

## Related Projects

| Institution | Geocoded Layer | Notes |
|-------------|----------------|------|
| Eastwick College | `c250_Moore_Street_Clery_2024_Geocoded` | 8 points, 250 Moore Street |
| Rutgers | `RUTGERS_CLERY_RMS_Geocoded` | 9 points (GpMessages: April 3, 2025) |
| FDU | `Crimes_OnCampus` | Spatial selection within FDU_Property |
| Parisian | `Parisian_Beauty` | Campus polygon only |

---

## References

- **Geocode Addresses**: [ArcGIS Pro Tool Reference](https://pro.arcgis.com/en/pro-app/latest/tool-reference/geocoding/geocode-addresses.htm)
- **Select Layer By Location**: [ArcGIS Pro Tool Reference](https://pro.arcgis.com/en/pro-app/latest/tool-reference/data-management/select-layer-by-location.htm)
- **Export Features**: [ArcGIS Pro Tool Reference](https://pro.arcgis.com/en/pro-app/latest/tool-reference/conversion/export-features.htm)
- **REQUEST_CHECKLIST.md** — Data scope, crime categories, export fields
- **institution_clery_geography_index.json** — Current inventory of Clery feature classes

---

**Maintained by**: R. A. Carucci  
**Last updated**: 2026-03-09
