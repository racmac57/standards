# Clery Act Reference Data — Summary

**Version:** 1.1.0  
**Last Updated:** 2026-03-09  
**Status:** ✅ Active

---

## Overview

This directory provides reference data and tools for completing **Clery Act** crime statistics requests from institutions of higher education. Hackensack PD receives requests from colleges and universities (FDU, Rutgers, Bergen Community College, Eastwick College, Parisian, etc.) for crime data occurring within their Clery-defined geography.

---

## Key Deliverables

| Deliverable | Location | Purpose |
|-------------|----------|---------|
| **Crime definitions** | `DataDictionary/current/schema/clery_crime_definitions.json` | Clery crime categories with NIBRS mappings |
| **Geography definitions** | `DataDictionary/current/schema/clery_geography_definitions.json` | On-Campus, Noncampus, Public Property (DOE Handbook) |
| **NIBRS → Clery mapping** | `DataDictionary/current/mappings/nibrs_to_clery_map.json` | Map RMS/NIBRS codes to Clery categories |
| **Request checklist** | `DataDictionary/current/REQUEST_CHECKLIST.md` | Step-by-step requirements for completing requests |
| **Institution geography** | `DataDictionary/current/institutions/*.geojson` | Exported Clery boundaries from ArcGIS Pro projects |
| **Geography index** | `DataDictionary/current/institutions/institution_clery_geography_index.json` | Inventory of exported feature classes per institution |
| **Extraction script** | `scripts/extract_clery_geography_from_arcgis.py` | ArcPy script to extract geography from Clery ArcGIS projects |

---

## Institution Coverage (as of 2026-03-09)

| Institution | Geography exported | Feature classes |
|-------------|---------------------|-----------------|
| Eastwick College | ✅ | CleryAOI (polygon), Clery_Crimes, geocoded points |
| FDU Clery Act | ✅ | FDU_Property, Surronding_Area [sic], Polygon, Point, Annotation1k, +3 |
| Parisian (Parisian Beauty Academy) | ✅ | Parisian_Beauty (polygon) |
| Rutgers | ✅ | RUTGERS_CLERY_RMS_Geocoded (points) |
| Bergen Community College | ⚠️ | GDB exists; feature classes in feature datasets or hosted services |
| Bergen Community College Clery Act | — | APRX references FDU geodatabase |
| Bergen Academies | — | No geodatabase or APRX found |

---

## Data Flow

```
RMS incidents (Hackensack PD)
    ↓
NIBRS classification (rms_to_nibrs_offense_map.json)
    ↓
Clery mapping (nibrs_to_clery_map.json)
    ↓
Geography filter (institution *.geojson)
    ↓
VAWA/Hate Crime narrative review (manual or AI-assisted)
    ↓
Clery export for institution
```

---

## Typical Request Turnaround

- **Standard request** (geography already exported): ~2–4 hours
- **New institution** (geography extraction needed): ~1 day

---

## Quick Reference

- **Source projects:** `10_Projects\Clery\2024\{institution}\`
- **Clery request PDF (FDU):** `10_Projects\Clery\2024\2024_Clery_Request_FDU.pdf`
- **Request checklist:** `DataDictionary/current/REQUEST_CHECKLIST.md`
- **Run extraction:** See [scripts/README.md](scripts/README.md) (requires ArcGIS Pro Python)

---

## Related Standards

- **NIBRS:** `Standards/NIBRS` — offense definitions, RMS to NIBRS mapping
- **RMS:** `Standards/RMS` — RMS field definitions
- **CAD_RMS:** `Standards/CAD_RMS` — cross-system mappings

---

## See Also

- [README.md](README.md) — Overview and quick start
- [CLAUDE.md](CLAUDE.md) — AI agent protocol
- [CHANGELOG.md](CHANGELOG.md) — Version history

---

**Maintained by:** R. A. Carucci
