# How Reported - Quick Reference Card

## Valid Values (Canonical Schema)

Use these values **ONLY** for all CAD "How Reported" field configurations:

| Value | Description | Use For |
|-------|-------------|---------|
| `9-1-1` | Emergency 911 call | All 911 emergency calls |
| `Phone` | Non-emergency phone call | Business line, non-emergency calls |
| `Walk-in` | Person walked into station | Walk-in reports, station lobby |
| `Self-Initiated` | Officer-initiated | Officer self-initiated activity |
| `Radio` | Radio dispatch/call | Radio communications |
| `Other` | Other methods | Any method not covered above |

## ⚠️ DO NOT USE These Values

The following values are **INVALID** and should NOT appear in:
- ArcGIS field domains
- Dashboard dropdowns
- Data entry forms
- Import templates

❌ Invalid values:
- ~~eMail~~
- ~~Mail~~
- ~~Virtual patrol~~ / ~~Virtual Patrol~~
- ~~Cancelled~~ / ~~Canceled Call~~
- ~~Fax~~
- ~~Teletype~~

## Legacy Value Mapping

If you encounter legacy values in old data, map them as follows:

| Old Value | Map To |
|-----------|--------|
| eMail | Other |
| Mail | Other |
| Virtual Patrol | Other |
| Canceled Call | Other |
| Fax | Phone |
| Teletype | Phone |

## Data Sources

**Authoritative Schema:** `unified_data_dictionary/schemas/canonical_schema.json` (line 292)

**Current Data Status:** ✅ All existing CAD data contains only valid values  
**Source:** `CAD/SCRPA/cad_data_quality_report.md` shows:
- Phone: 55 records
- 9-1-1: 29 records  
- Walk-In: 20 records
- Other - See Notes: 5 records
- Radio: 5 records

## ArcGIS Configuration

When configuring ArcGIS field domains for the `HowReported` field:

1. Create a **Coded Value Domain** named `HowReported_Domain`
2. Add exactly 6 coded values (listed above)
3. Apply domain to the `HowReported` field
4. Republish the feature service

## Excel Import Note

⚠️ **IMPORTANT:** The value `9-1-1` must be stored as **TEXT**, not a date!  
- Excel may try to convert it to `1901-09-01` or similar
- Always format the column as Text before importing
- Use leading apostrophe if needed: `'9-1-1`

---

**Last Updated:** 2026-02-03  
**Related Document:** `HOW_REPORTED_FIX_SUMMARY.md`
