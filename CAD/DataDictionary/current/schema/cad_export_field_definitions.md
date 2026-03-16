# CAD Export (SCRPA) — Field Definitions (Draft v1)

This document summarizes **CAD export columns** currently observed in `CAD\SCRPA\cad_data_quality_report.md` and standardizes naming, allowed values, and calculation logic.

## Column name mapping (export → standard)

Some CAD export headers contain spaces; the “standard” name is what we use in mapping/schema work.

- `ReportNumberNew` → `ReportNumberNew`
- `Incident` → `Incident`
- `How Reported` → `HowReported`
- `FullAddress2` → `FullAddress2`
- `Grid` → `Grid`
- `PDZone` → `ZoneCalc` *(standard name; export header is `PDZone`)*
- `Time of Call` → `TimeofCall`
- `cYear` → `cYear`
- `cMonth` → `cMonth`
- `HourMinuetsCalc` → `Hour_Calc` *(standard name; export header contains a typo)*
- `DayofWeek` → `DayofWeek`
- `Time Dispatched` → `TimeDispatched`
- `Time Out` → `TimeOut`
- `Time In` → `TimeIn`
- `Time Spent` → `TimeSpent`
- `Time Response` → `TimeResponse`
- `Officer` → `Officer`
- `Disposition` → `Disposition`
- `latitude` → `latitude` *(if present in the export)*
- `longitude` → `longitude` *(if present in the export)*

## Field-by-field definitions

### `ReportNumberNew`

- **Definition**: CAD report identifier (primary key / join key to RMS Case Number).
- **Format**: `YY-NNNNNN` with optional supplemental suffix letter, e.g. `25-000001`, `25-000001A`.
  - **Regex**: `^\d{2}-\d{6}([A-Z])?$`
- **Logic**:
  - `YY` = last two digits of the **year the report was created**
  - `NNNNNN` = sequential number starting at `000001` on January 01 each year
  - **Supplementals**: same base number, with a suffix letter starting at `A` (then `B`, `C`, …)
- **Validation rules**:
  - Must be non-null.
  - Must match the regex.
  - Must not be parsed as numeric (keep as text to preserve leading zeros).

### `Incident`

- **Definition**: Incident type descriptor (typically a code + description).
- **Expected format**: Contains a delimiter `" - "` between parts (observed 100% in sample).
  - **Regex (minimum)**: `^.+\s-\s.+$`
- **Validation rules**:
  - Must be non-null.
  - Must contain `" - "` (flag rows missing delimiter).

### `HowReported`

- **Definition**: Method by which the call/incident was reported/initiated.
- **Type**: text (string).
- **Allowed values (domain)**:
  - `9-1-1`
  - `Phone`
  - `Walk-in`
  - `Self-Initiated`
  - `Radio`
  - `Other`
- **Important**:
  - `9-1-1` **must be kept as text** and must not be displayed/parsed as a date (e.g., Excel auto-formatting).
  - All values should be normalized to match the canonical schema values listed above.
  - Legacy values such as `Teletype`, `Fax`, `eMail`, `Mail`, `Virtual Patrol`, and `Canceled Call` should be mapped to the appropriate canonical value (typically `Other` or `Phone`).
- **Observed in sample** (from `cad_data_quality_report.md`): `Phone`, `9-1-1`, `Walk-In`, `Other - See Notes`, `Radio`.

### `FullAddress2`

- **Definition**: Full incident location address string.
- **Expected format**: Contains commas (observed 100% in sample).
  - **Example pattern**: `Street, City, State ZIP` (exact components may vary)
- **Validation rules**:
  - Must be non-null.
  - Must contain at least one comma.

### `Grid`

- **Definition**: CAD grid / map grid identifier.
- **Type**: text (string).
- **Validation rules**:
  - May be null (missing observed in sample).
  - If present, should match a controlled list of known grid codes (to be defined from GIS/grid reference).

### `ZoneCalc` *(export header: `PDZone`)*

- **Definition**: Patrol/PD zone code assigned to the incident.
- **Type**: integer (stored as numeric; observed as float in analysis due to missing values).
- **Observed range in sample**: `5`–`9` (integers only).
- **Validation rules**:
  - May be null.
  - If present: must be an integer and within the valid zone domain (recommended to define explicit allowed set once confirmed).

### `TimeofCall` *(export header: `Time of Call`)*

- **Definition**: Timestamp when the call was created/received.
- **Type**: datetime.
- **Validation rules**:
  - Must be non-null.
  - Should be in local agency timezone (recommend documenting as `America/New_York`).

### `cYear`

- **Definition**: Calendar year of `TimeofCall` (derived).
- **Logic**: `cYear = YEAR(TimeofCall)`
- **Type**: integer.
- **Validation rules**:
  - Must be non-null.
  - Must equal the year portion of `TimeofCall`.

### `cMonth`

- **Definition**: Calendar month of `TimeofCall` (derived).
- **Type**: text (string) in current profiling; exact representation must be standardized.
- **Recommended standard** (pick one and enforce):
  - `01`–`12` (two-digit month), **or**
  - `January`–`December` (English month name)
- **Logic**:
  - If numeric: `cMonth = FORMAT(TimeofCall, "MM")`
  - If name: `cMonth = FORMAT(TimeofCall, "MMMM")`

### `Hour_Calc` *(export header: `HourMinuetsCalc`)*

- **Definition**: Hour/minute bucket of `TimeofCall` (derived).
- **Recommended standard**: `HH:mm` (24-hour clock), e.g. `07:05`, `18:42`.
- **Logic**: `Hour_Calc = FORMAT(TimeofCall, "HH:mm")`
- **Validation rules**:
  - Must be non-null.
  - Must represent a valid time-of-day.

### `DayofWeek`

- **Definition**: Day name for `TimeofCall` (derived).
- **Recommended standard**: `Monday`…`Sunday`.
- **Logic**: `DayofWeek = FORMAT(TimeofCall, "dddd")`

### `TimeDispatched` *(export header: `Time Dispatched`)*

- **Definition**: Timestamp when units were dispatched/assigned.
- **Type**: datetime.
- **Validation rules**:
  - Must be non-null.
  - Should be ≥ `TimeofCall` (flag if earlier).

### `TimeOut` *(export header: `Time Out`)*

- **Definition**: Timestamp when unit goes “out” (often **arrived on scene**; confirm CAD meaning).
- **Type**: datetime.
- **Validation rules**:
  - Must be non-null.
  - Should be ≥ `TimeDispatched` (flag if earlier).

### `TimeIn` *(export header: `Time In`)*

- **Definition**: Timestamp when unit clears the call / is back in service.
- **Type**: datetime.
- **Validation rules**:
  - Must be non-null.
  - Should be ≥ `TimeOut` (flag if earlier).

### `TimeResponse` *(export header: `Time Response`)*

- **Definition**: Response duration.
- **Recommended logic (typical CAD)**: `TimeResponse = TimeOut - TimeDispatched`
- **Type**: duration (stored as text in current profiling).
- **Validation rules**:
  - Must be non-null.
  - Must be ≥ 0.
  - If stored as text, standardize to one format (recommended: total seconds, or `HH:mm:ss`).

### `TimeSpent` *(export header: `Time Spent`)*

- **Definition**: Time spent on scene / on the call.
- **Recommended logic (typical CAD)**: `TimeSpent = TimeIn - TimeOut`
- **Type**: duration (stored as text in current profiling).
- **Validation rules**:
  - Must be non-null.
  - Must be ≥ 0.
  - Standardize duration format (recommended: `HH:mm:ss`).

### `Officer`

- **Definition**: Officer identifier for the call (primary/assigned officer).
- **Type**: text (string).
- **Validation rules**:
  - Must be non-null.
  - Should match a standardized officer naming/badge convention (recommend aligning to `CAD/SCRPA/Assignment_Master_V2.csv` standardization outputs).

### `Disposition`

- **Definition**: Disposition / outcome code or label for the CAD call.
- **Type**: text (string).
- **Observed**: 1 unique value in the profiled sample (exact value not captured in the report).
- **Validation rules**:
  - Must be non-null.
  - Must be limited to a controlled domain (to be defined once the value list is extracted from the export).

### `latitude`

- **Definition**: Latitude of the incident location (WGS84).
- **Type**: number.
- **Validation rules**:
  - If present: must be between `-90` and `90`.

### `longitude`

- **Definition**: Longitude of the incident location (WGS84).
- **Type**: number.
- **Validation rules**:
  - If present: must be between `-180` and `180`.

## Open confirmations (to finalize v1)

1. Confirm `Time Out` meaning in your CAD (arrived on scene vs enroute vs other).
2. Confirm the canonical representation for `cMonth` (numeric vs month name).
3. Provide/confirm the official allowed domains for:
   - `Disposition`
   - `Grid`
   - `ZoneCalc` (PDZone)
4. Confirm whether supplementals can exceed `Z` (e.g., `AA`) or are limited to single-letter suffix.


