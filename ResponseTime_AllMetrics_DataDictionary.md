# Response Time All Metrics — Data Dictionary

**Version:** 1.0  
**Date:** 2026-03-09  
**ETL Script:** `response_time_batch_all_metrics.py` v1.17.21  
**Analyst:** R. A. Carucci  

---

## Overview

This document defines the schema, source lineage, and business rules for the per-month CSV files produced by the Response Time All Metrics ETL pipeline. Each CSV represents one calendar month of aggregated response time statistics, consumed by Power BI via `Folder.Files()`.

---

## Output Location

```
C:\Users\carucci_r\OneDrive - City of Hackensack\PowerBI_Date\response_time_all_metrics\
```

**Filename pattern:** `YYYY_MM_response_times.csv`  
**Example:** `2026_02_response_times.csv`

---

## Output Schema

| # | Column | Data Type | Nullable | Description | Example |
|---|--------|-----------|----------|-------------|---------|
| 1 | `Response_Type` | string | No | Priority classification of the call. One of: Emergency, Urgent, Routine. Resolved via three-step cascade (see Resolution Logic below). | `Emergency` |
| 2 | `MM-YY` | string | No | Month-Year label for the aggregation period, zero-padded month with two-digit year. | `02-26` |
| 3 | `Metric_Type` | string | No | Which time interval was measured. See Metric Definitions below. | `Time Out - Time Dispatched` |
| 4 | `First_Response_Time_MMSS` | string | No | Average response time for the group formatted as `M:SS` (minutes and seconds). | `4:32` |
| 5 | `Avg_Minutes` | float | No | Average response time in decimal minutes, rounded to 4 decimal places. | `4.5333` |
| 6 | `Record_Count` | int | No | Number of valid records contributing to this aggregation group. | `147` |
| 7 | `Median_Minutes` | float | No | Median response time in decimal minutes for the group. | `4.2000` |

**Aggregation grain:** One row per unique combination of (`Response_Type`, `MM-YY`, `Metric_Type`).

---

## Metric Definitions

| Metric_Type | Semantic Label | Calculation | Business Meaning |
|---|---|---|---|
| `Time Out - Time Dispatched` | Travel Time | `Time Out` minus `Time Dispatched` | Time from dispatch to officer departure/arrival on scene |
| `Time Out - Time of Call` | Total Response | `Time Out` minus `Time of Call` | Total elapsed time from citizen call to officer on scene |
| `Time Dispatched - Time of Call` | Dispatch Queue | `Time Dispatched` minus `Time of Call` | Time the call waited in queue before being dispatched |

**Relationship:** Total Response ≈ Dispatch Queue + Travel Time.

---

## Source Files

### Timereport Exports (Input)

| Directory | Pattern | Description |
|---|---|---|
| `05_EXPORTS/_CAD/timereport/yearly/` | `YYYY_full_timereport.xlsx` | Full-year CAD timereport export |
| `05_EXPORTS/_CAD/timereport/monthly/` | `YYYY_MM_timereport.xlsx` | Monthly CAD timereport export |

**Discovery:** Files are discovered dynamically via `pathlib.glob` at runtime. The `discover_sources()` function scans both directories and includes all files with year >= (current year - 1). No code changes are required when new monthly exports are added.

### Source Columns Used

| Source Column | Type | Purpose |
|---|---|---|
| `ReportNumberNew` | string | Primary key — used for first-arriving-unit deduplication |
| `Incident` | string | Call type descriptor — used for normalization and classification |
| `How Reported` | string | Method of call initiation — used in Layer 1 filter |
| `Time of Call` | datetime | Timestamp when citizen call was received |
| `Time Dispatched` | datetime | Timestamp when unit was dispatched |
| `Time Out` | datetime | Timestamp when unit went en route / arrived on scene |
| `Response Type` | string | CAD-assigned priority (may be missing or invalid) |

### Reference File

| File | Path | Purpose |
|---|---|---|
| `CallType_Categories.csv` | `09_Reference/Classifications/CallTypes/` | 449-row mapping of Incident to Response_Type and Category_Type |

**CallType_Categories.csv schema:**

| Column | Description |
|---|---|
| `Incident` | Raw incident type string from CAD |
| `Incident_Norm` | Normalized version (not used by ETL — normalization is done at runtime) |
| `Category_Type` | ESRI-style category (11 values) — used for Layer 3 filter |
| `Response_Type` | Priority classification: Emergency, Urgent, or Routine |

---

## Processing Pipeline

### Step 1: Source Discovery

`discover_sources(min_year)` scans `yearly/` and `monthly/` directories. Default `min_year` = current year - 1.

### Step 2: Data Loading and Year Filter

Each source file is loaded via `pd.read_excel()`. Records are filtered to the expected year derived from the filename.

### Step 3: NaT Coercion Monitoring

After each `pd.to_datetime(..., errors="coerce")` call, the script counts how many non-null raw values failed to parse. If the coercion rate exceeds 5%, a `ValueError` is raised to prevent silent data loss from upstream format changes.

### Step 4: Three-Layer Exclusion Filter

**Layer 1 — How Reported:** Excludes non-citizen-initiated calls. Retained values: 9-1-1, Phone, Walk-In. Excluded: Self-Initiated, Radio, Teletype, Fax, eMail, Mail, Other - See Notes, Virtual Patrol, Canceled Call.

**Layer 2 — Incident Exclusion:** Excludes ~234 administrative, self-initiated, and non-dispatched incident types (court assignments, records requests, patrol checks, training, etc.).

**Layer 3 — Category_Type:** Safety net exclusion of any incident mapped to "Community Engagement" or "Administrative and Support" in `CallType_Categories.csv`.

### Step 5: First-Arriving Unit Deduplication

Records are sorted by `[ReportNumberNew, Time Out]` and deduplicated on `ReportNumberNew` keeping the first row (earliest `Time Out` = first-arriving unit).

### Step 6: Response Type Resolution

Priority cascade for backfilling missing `Response_Type`:

1. **CAD original:** If the `Response Type` column already contains Emergency, Urgent, or Routine, use it
2. **Exact match:** Look up the raw `Incident` string in `CallType_Categories.csv`
3. **Normalized match:** Apply `_normalize()` and look up the result
4. **Unresolvable:** Record is excluded from output

### Step 7: Metric Calculation

For each of the three metrics, compute `(col_a - col_b).dt.total_seconds() / 60.0`. The timereport exports contain full `datetime64` timestamps (not time-only), so overnight crossings are handled correctly by datetime subtraction.

### Step 8: Bounds Filtering

| Condition | Action |
|---|---|
| Duration is `NaN` (missing timestamp) | Excluded |
| Duration <= 0 minutes | Excluded, logged at WARNING if negative |
| Duration > per-type cap | Excluded, logged at WARNING with breakdown |

**Per-Response_Type upper caps:**

| Response_Type | Max Minutes |
|---|---|
| Emergency | 15 |
| Urgent | 30 |
| Routine | 60 |

### Step 9: Aggregation and Output

Valid records are grouped by (`Response_Type`, `MM-YY`) and aggregated to produce mean, count, and median. One CSV file is written per month.

---

## Data Quality Safeguards

| Safeguard | Trigger | Action |
|---|---|---|
| NaT coercion monitoring | >5% of non-null timestamps fail to parse | `ValueError` raised — script stops |
| Negative duration logging | Any record with col_a < col_b | `WARNING` logged with count |
| Over-cap logging | Any record exceeding per-type max | `WARNING` logged with per-type breakdown |
| Unmapped Response Type | Incident not found in any lookup | Record excluded; count logged |
| Zero source files | `discover_sources()` returns empty list | Script exits with error message |

---

## Downstream Consumers

| Consumer | Query | How It Uses This Data |
|---|---|---|
| Power BI | `___ResponseTime_AllMetrics` (M/Power Query) | Loads CSVs via `Folder.Files()`, applies 13-month rolling window from `pReportMonth`, renames columns for visual layer |

**Power BI column mapping:**

| CSV Column | Power BI Column |
|---|---|
| `Avg_Minutes` | `Average_Response_Time` |
| `First_Response_Time_MMSS` | `Response_Time_MMSS` |
| `Record_Count` | `Count` (also kept as `Record_Count`) |

---

## Change Log

| Version | Date | Description |
|---|---|---|
| v1.17.21 | 2026-03-09 | Dynamic source discovery, NaT coercion monitoring, per-type response time caps |
| v1.17.20 | 2026-02-27 | Baseline run — 13 months from raw exports only |
| v1.17.19 | 2026-02-27 | Peer-review corrections to incident exclusion list |
| v1.17.18 | 2026-02-27 | Three-layer filter expansion (analyst specification) |
| v1.17.17 | 2026-02-26 | Admin list runtime count confirmation |
| v1.17.16 | 2026-02-26 | Initial 92-type administrative incident filter |
