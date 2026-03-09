# Clery Act Request Checklist

**Version**: 1.0  
**Date**: 2026-03-09  
**Purpose**: Standard requirements for completing a Clery Act crime statistics request from an institution of higher education

---

## Overview

When a college or university (e.g., Fairleigh Dickinson University, Rutgers, Bergen Community College) requests crime data from Hackensack PD for their Clery Act annual security report, the following elements are typically required.

> **Note**: Institution-specific requirements may vary. For FDU requests, refer to `10_Projects\Clery\2024\2024_Clery_Request_FDU.pdf` for any additional or institution-specific requirements.

---

## 1. Data Scope

| Requirement | Description | Reference |
|-------------|-------------|-----------|
| **Date range** | Three most recent calendar years | DOE Handbook |
| **Geography** | Incidents within institution's Clery geography | `clery_geography_definitions.json` |
| **Location types** | On-Campus, Noncampus, Public Property | Per institution's defined geography |

### Geography Definitions (Quick Reference)

- **On-Campus**: Core campus, residence halls, institution-owned/controlled property
- **Noncampus**: Remote instructional sites, student org property, clinical placements (not contiguous)
- **Public Property**: Public streets/sidewalks immediately adjacent to campus

---

## 2. Crime Categories to Report

### Primary Crimes (Report All)

- [ ] Murder/Non-Negligent Manslaughter (09A)
- [ ] Manslaughter by Negligence (09B)
- [ ] Rape (11A)
- [ ] Fondling (11D)
- [ ] Incest (36A)
- [ ] Statutory Rape (36B)
- [ ] Robbery (120)
- [ ] Aggravated Assault (13A)
- [ ] Burglary (220)
- [ ] Motor Vehicle Theft (240)
- [ ] Arson (200)

### Hate Crimes (When Bias-Motivated)

- [ ] Any primary crime above + bias category
- [ ] Simple Assault (13B) — hate crime only
- [ ] Larceny-Theft (23A–23H) — hate crime only
- [ ] Intimidation (13C) — hate crime only
- [ ] Destruction/Damage/Vandalism (290) — hate crime only

**Bias categories**: Race, Religion, Sexual Orientation, Gender, Gender Identity, Disability, Ethnicity, National Origin

### Arrests and Referrals

- [ ] Liquor Law Violations
- [ ] Drug Law Violations (35A, 35B)
- [ ] Weapons Law Violations (520, 521)

### VAWA Crimes

- [ ] Dating Violence
- [ ] Domestic Violence
- [ ] Stalking

---

## 3. Required Data Fields (Typical Export)

| Field | Required | Notes |
|-------|----------|-------|
| Case Number | Yes | Format YY-NNNNNN |
| Incident Date | Yes | |
| Incident Time | Yes | |
| Full Address | Yes | For geography determination |
| NIBRS Classification | Yes | For Clery category mapping |
| Incident Type(s) | Yes | All_Incidents or similar |
| Narrative | Recommended | For VAWA/DV context, hate crime bias |
| Disposition | Optional | For arrest vs. referral |

---

## 4. Geography Filtering

1. **Obtain institution's Clery geography** (addresses, boundaries, or shapefile)
2. **Filter RMS/CAD data** to incidents within:
   - On-campus property
   - Noncampus property (if applicable)
   - Public property adjacent to campus
3. **Exclude** incidents outside Clery geography (e.g., general Hackensack incidents not near campus)

---

## 5. Classification Steps

1. **Map NIBRS codes** using `nibrs_to_clery_map.json`
2. **Flag hate crimes** — incidents with documented bias motivation
3. **Flag VAWA crimes** — check narrative/incident type for:
   - Domestic violence (relationship context)
   - Dating violence (romantic relationship)
   - Stalking (course of conduct)
4. **Separate arrests vs. referrals** for liquor/drug/weapons

---

## 6. Output Format

Institutions may request:

- **CSV** — e.g., `RUTGERS_CLERY_RMS.csv` format (Case Number, Incident Date, Incident Time, FullAddress, Narrative, NIBRS Classification, All_Incidents)
- **Excel** — Same fields, possibly with multiple sheets by year or geography
- **Import package** — Some institutions use Campus Safety Connect / similar (ImportLog, GpMessages)

---

## 7. Quality Checks

- [ ] All incidents have valid NIBRS codes
- [ ] Geography filter correctly applied
- [ ] No incidents outside date range
- [ ] VAWA crimes correctly identified from narrative
- [ ] Hate crimes include bias category when applicable
- [ ] Arrests vs. referrals correctly categorized

---

## 8. Related Standards

| Standard | Location | Use |
|----------|----------|-----|
| NIBRS offense definitions | `Standards/NIBRS/DataDictionary/current/schema/` | Offense classification |
| RMS to NIBRS mapping | `Standards/NIBRS/DataDictionary/current/mappings/` | RMS → NIBRS → Clery |
| Clery crime definitions | `Standards/Clery/DataDictionary/current/schema/` | Clery categories |
| Clery geography | `clery_geography_definitions.json` | Geography categories |

---

## 9. References

- **Clery Center**: [Understanding Clery Statistics](https://clerycenter.org/resources/understanding-clery-statistics/)
- **DOE Handbook**: [Handbook for Campus Safety and Security Reporting](https://www2.ed.gov/admins/lead/safety/handbook.pdf)
- **FBI UCR**: SRS User Manual, NIBRS User Manual, Hate Crime Data Collection Guidelines

---

**Maintained by**: R. A. Carucci  
**Last updated**: 2026-03-09
