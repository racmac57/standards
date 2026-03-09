# Clery Act Reference Data

**Location**: `Standards/Clery`  
**Version**: 1.1.0  
**Last Updated**: 2026-03-09  
**Status**: ✅ Active

---

## Overview

This directory contains reference data and mappings for completing **Clery Act** crime statistics requests from institutions of higher education. The Jeanne Clery Disclosure of Campus Security Policy and Campus Crime Statistics Act requires colleges and universities to report crime occurring within defined Clery geography.

**Purpose**: Provide authoritative Clery crime definitions, geography categories, and NIBRS-to-Clery mappings for Hackensack PD data used in institution requests (e.g., FDU, Rutgers, Bergen Community College, Eastwick College, Parisian Beauty Academy).

---

## Directory Structure

```
Clery/
├── DataDictionary/
│   └── current/
│       ├── schema/
│       │   ├── clery_crime_definitions.json    ⭐ Crime categories & definitions
│       │   └── clery_geography_definitions.json ⭐ On-Campus, Noncampus, Public Property
│       ├── mappings/
│       │   └── nibrs_to_clery_map.json         ⭐ NIBRS → Clery mapping
│       ├── institutions/                         # Institution geography (from ArcGIS export)
│       │   └── institution_clery_geography_index.json
│       └── REQUEST_CHECKLIST.md                 ⭐ Step-by-step request requirements
├── scripts/
│   ├── extract_clery_geography_from_arcgis.py  ⭐ ArcPy script to extract geography from projects
│   └── README.md
└── README.md                                    # This file
```

---

## Key Files

### 1. **clery_crime_definitions.json**

Clery Act crime categories with NIBRS code mappings.

**Contains**:
- **Primary crimes**: Murder, Manslaughter, Rape, Fondling, Incest, Statutory Rape, Robbery, Aggravated Assault, Burglary, Motor Vehicle Theft, Arson
- **Hate crime additions**: Simple Assault, Larceny-Theft, Intimidation, Destruction/Vandalism (when bias-motivated)
- **Arrests/Referrals**: Liquor Law, Drug Law, Weapons Law
- **VAWA crimes**: Dating Violence, Domestic Violence, Stalking
- **Bias categories**: Race, Religion, Sexual Orientation, Gender, etc.

---

### 2. **clery_geography_definitions.json**

Clery geographic categories per DOE Handbook.

**Categories**:
- **On-Campus**: Core campus, residence halls, institution-owned property
- **Noncampus**: Remote sites, student org property, clinical placements
- **Public Property**: Streets/sidewalks immediately adjacent to campus

---

### 3. **nibrs_to_clery_map.json**

Maps NIBRS offense codes to Clery categories.

**Use for**:
- Filtering RMS data for Clery-reportable incidents
- Classifying incidents for institution export
- Identifying hate-crime-only and arrest-referral-only categories

**Confidence levels**:
- `1.0` = Direct match (primary crimes)
- `0.5` = Context-dependent (hate crimes, VAWA)

---

### 4. **REQUEST_CHECKLIST.md**

Step-by-step checklist for completing a Clery request.

**Covers**:
- Data scope (date range, geography)
- Crime categories to report
- Required export fields
- Geography filtering
- Classification steps
- Quality checks

> **Institution-specific**: For FDU requests, see `10_Projects\Clery\2024\2024_Clery_Request_FDU.pdf` for any additional requirements.

---

## Extracting Geography from ArcGIS Pro

Use the ArcPy script to pull Clery geography from existing ArcGIS Pro projects. Requires ArcGIS Pro (arcpy). See [scripts/README.md](scripts/README.md) for full commands and ArcGIS Pro Python path.

---

## Quick Start

### Load Clery Definitions (Python)

```python
import json

# Load crime definitions
with open('DataDictionary/current/schema/clery_crime_definitions.json') as f:
    clery = json.load(f)

# Load NIBRS → Clery mapping
with open('DataDictionary/current/mappings/nibrs_to_clery_map.json') as f:
    mapping = json.load(f)

# Map NIBRS code to Clery category
def nibrs_to_clery(nibrs_code):
    if nibrs_code in mapping['nibrs_to_clery']:
        m = mapping['nibrs_to_clery'][nibrs_code]
        return m['clery_name'], m.get('hate_crime_only', False)
    return None, None

# Example: 13A → Aggravated Assault
name, hate_only = nibrs_to_clery('13A')
print(name, hate_only)  # ('Aggravated Assault', False)

# Unmapped code returns None — log these for QA
name, hate_only = nibrs_to_clery('99Z')
if name is None:
    print("WARNING: NIBRS code '99Z' has no Clery mapping")
```

### Filter RMS Data for Clery

1. Filter by **date range** (3 most recent calendar years)
2. Filter by **geography** (institution's Clery geography)
3. Map **NIBRS Classification** to Clery categories
4. Flag **VAWA** crimes:
   - **Dating Violence**: Look for relationship context (boyfriend/girlfriend/dating partner) in narrative
   - **Domestic Violence**: Check for household/family relationship per NJ DV statute (2C:25-19)
   - **Stalking**: Pattern of conduct causing fear; may span multiple incidents
   - *Note*: NIBRS codes alone are insufficient for VAWA classification
5. Flag **hate crimes** when bias documented

---

## Integration with Other Standards

| Standard | Relationship |
|----------|--------------|
| **NIBRS** | Clery uses FBI UCR/NIBRS definitions. Use `rms_to_nibrs_offense_map.json` then `nibrs_to_clery_map.json` |
| **RMS** | Source data (incidents, narratives) for Clery export |
| **CAD** | May supplement for calls-for-service context; primary source is RMS |
| **Power BI** | Clery counts may feed annual compliance dashboards |

---

## References

- **Clery Center**: [Understanding Clery Statistics](https://clerycenter.org/resources/understanding-clery-statistics/)
- **DOE**: [Handbook for Campus Safety and Security Reporting](https://www2.ed.gov/admins/lead/safety/handbook.pdf)
- **FBI**: SRS User Manual, NIBRS User Manual, Hate Crime Data Collection Guidelines
- **NJ Domestic Violence Act**: N.J.S.A. 2C:25-17 et seq.

---

## Maintenance

**Update frequency**: Annually (when DOE/FBI guidance changes) or when institution requirements change.

**Update protocol**:
1. Update relevant JSON/GeoJSON files
2. Update CHANGELOG.md with version bump
3. Update "Last Updated" in README.md, SUMMARY.md, CLAUDE.md
4. Verify institution geography index matches exports

**Contact**: R. A. Carucci

---

## See Also

- [SUMMARY.md](SUMMARY.md) — Executive summary
- [CLAUDE.md](CLAUDE.md) — AI agent protocol
- [CHANGELOG.md](CHANGELOG.md) — Version history
