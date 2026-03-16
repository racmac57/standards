# RMS Export — Field Definitions (v1.0)

**Document Version**: 1.0
**Last Updated**: 2025-12-30
**Purpose**: Comprehensive documentation of RMS export field definitions for CAD-RMS integration

---

## Overview

This document provides detailed definitions for all RMS export fields used in CAD data cleaning, enrichment, and integration workflows. Fields are organized by functional group and include validation rules, format specifications, and usage notes for multi-column matching strategies.

---

## Column Name Mapping (Export → Standard)

Some RMS export headers contain spaces; the "standard" name is what we use in mapping/schema work.

| Export Header | Standard Name | Group |
|--------------|---------------|-------|
| `Case Number` | `CaseNumber` | Incident |
| `Incident Date` | `IncidentDate` | Temporal |
| `Incident Time` | `IncidentTime` | Temporal |
| `Incident Date_Between` | `IncidentDateBetween` | Temporal |
| `Incident Time_Between` | `IncidentTimeBetween` | Temporal |
| `Report Date` | `ReportDate` | Temporal |
| `Report Time` | `ReportTime` | Temporal |
| `Incident Type_1` | `IncidentType1` | Incident Classification |
| `Incident Type_2` | `IncidentType2` | Incident Classification |
| `Incident Type_3` | `IncidentType3` | Incident Classification |
| `FullAddress` | `FullAddress` | Location |
| `Grid` | `Grid` | Location |
| `Zone` | `Zone` | Location |
| `Narrative` | `Narrative` | Incident Details |
| `Total Value Stolen` | `TotalValueStolen` | Property |
| `Total Value Recover` | `TotalValueRecover` | Property |
| `Registration 1` | `Registration1` | Vehicle |
| `Make1` | `Make1` | Vehicle |
| `Model1` | `Model1` | Vehicle |
| `Reg State 1` | `RegState1` | Vehicle |
| `Registration 2` | `Registration2` | Vehicle |
| `Reg State 2` | `RegState2` | Vehicle |
| `Make2` | `Make2` | Vehicle |
| `Model2` | `Model2` | Vehicle |
| `Reviewed By` | `ReviewedBy` | Case Management |
| `CompleteCalc` | `CompleteCalc` | Case Management |
| `Officer of Record` | `OfficerOfRecord` | Personnel |
| `Squad` | `Squad` | Personnel |
| `Det_Assigned` | `DetAssigned` | Personnel |
| `Case_Status` | `CaseStatus` | Case Management |
| `NIBRS Classification` | `NIBRSClassification` | Incident Classification |

---

## Field Definitions by Group

---

## 🔖 Incident Identification

### CaseNumber

**Export Header**: `Case Number`

- **Definition**: RMS case identifier serving as the primary key and primary join key to CAD `ReportNumberNew`.
- **Source Field**: `Case Number` (RMS export)
- **Format**: `YY-NNNNNN` with optional supplemental suffix letter
  - **Examples**: `25-000001`, `25-000001A`, `25-000001B`
  - **Regex**: `^\d{2}-\d{6}([A-Z])?$`
- **Logic**:
  - `YY` = last two digits of the year the case was created
  - `NNNNNN` = sequential number starting at `000001` on January 1st each year
  - **Supplementals**: same base number with a suffix letter starting at `A` (then `B`, `C`, etc.)
- **Validation Rules**:
  - Must be non-null
  - Must match the regex pattern
  - Must be stored as text (not numeric) to preserve leading zeros
  - Case-insensitive matching recommended (though typically uppercase)
- **Mapping Notes**:
  - Primary join key to CAD `ReportNumberNew`
  - Used in primary key matching strategy (confidence: 1.0)
  - Normalized for matching: trim whitespace, collapse internal spaces, remove non-printable characters
- **Group**: Incident

---

## 📅 Temporal Fields

### IncidentDate

**Export Header**: `Incident Date`

- **Definition**: Date when the incident occurred (not necessarily when it was reported).
- **Source Field**: `Incident Date` (RMS export)
- **Format**: Date type, exported as Excel date serial or `MM/dd/yyyy` format
  - **Accepted Formats**:
    - Excel date serial number
    - `MM/dd/yyyy`
    - `M/d/yyyy`
    - ISO 8601 date (`YYYY-MM-DD`)
- **Logic**: User-entered or system-derived from incident details
- **Validation Rules**:
  - May be null (incidents without confirmed dates)
  - If present, must be a valid date
  - Should be ≤ `ReportDate` (flag if incident date is after report date)
  - Timezone: `America/New_York` (recommended documentation standard)
- **Mapping Notes**:
  - Used in **temporal_address_match** strategy (weight: 0.4 for date component)
  - Used in **officer_temporal_match** strategy (weight: 0.3 for date component)
  - Used in **address_zone_match** strategy (weight: 0.2, optional)
  - Can backfill CAD `TimeofCall` date component in validation workflows
- **Group**: Temporal

---

### IncidentTime

**Export Header**: `Incident Time`

- **Definition**: Time when the incident occurred (not necessarily when it was reported).
- **Source Field**: `Incident Time` (RMS export)
- **Format**: Time type, exported as Excel time serial or `HH:mm` format
  - **Accepted Formats**:
    - Excel time serial number
    - `HH:mm`
    - `H:mm`
    - `HH:mm:ss`
- **Logic**: User-entered or system-derived from incident details
- **Validation Rules**:
  - May be null
  - If present, must be a valid time-of-day (00:00 to 23:59)
  - Timezone: `America/New_York` (recommended documentation standard)
- **Mapping Notes**:
  - Used in **temporal_address_match** strategy (weight: 0.3 with 1-hour tolerance)
  - Used in **officer_temporal_match** strategy (weight: 0.2 with 2-hour tolerance)
  - Combined with `IncidentDate` for temporal matching to CAD `TimeofCall`
- **Group**: Temporal

---

### IncidentDateBetween

**Export Header**: `Incident Date_Between`

- **Definition**: End date of a date range for incidents occurring "between" two dates.
- **Source Field**: `Incident Date_Between` (RMS export)
- **Format**: Date type (same formats as `IncidentDate`)
- **Logic**: User-entered for date range incidents (e.g., theft discovered between two dates)
- **Validation Rules**:
  - May be null (most incidents are point-in-time)
  - If present, should be ≥ `IncidentDate`
  - Flag if date range exceeds reasonable threshold (e.g., > 30 days without justification)
- **Mapping Notes**:
  - Not currently used in multi-column matching strategies
  - Useful for incident analysis and reporting
- **Group**: Temporal

---

### IncidentTimeBetween

**Export Header**: `Incident Time_Between`

- **Definition**: End time of a time range for incidents occurring "between" two times.
- **Source Field**: `Incident Time_Between` (RMS export)
- **Format**: Time type (same formats as `IncidentTime`)
- **Logic**: User-entered for time range incidents
- **Validation Rules**:
  - May be null (most incidents are point-in-time)
  - If present and `IncidentDateBetween` matches `IncidentDate`, should be ≥ `IncidentTime`
- **Mapping Notes**:
  - Not currently used in multi-column matching strategies
  - Useful for incident analysis and reporting
- **Group**: Temporal

---

### ReportDate

**Export Header**: `Report Date`

- **Definition**: Date when the report was filed/created in RMS.
- **Source Field**: `Report Date` (RMS export)
- **Format**: Date type (same formats as `IncidentDate`)
- **Logic**: System-generated timestamp when report is created
- **Validation Rules**:
  - May be null (rare)
  - If both present, should be ≥ `IncidentDate`
  - Flag if report date precedes incident date by unreasonable threshold (e.g., > 30 days)
  - Timezone: `America/New_York` (recommended documentation standard)
- **Mapping Notes**:
  - Used for data quality validation
  - Can help identify delayed reporting patterns
- **Group**: Temporal

---

### ReportTime

**Export Header**: `Report Time`

- **Definition**: Time when the report was filed/created in RMS.
- **Source Field**: `Report Time` (RMS export)
- **Format**: Time type (same formats as `IncidentTime`)
- **Logic**: System-generated timestamp when report is created
- **Validation Rules**:
  - May be null
  - Timezone: `America/New_York` (recommended documentation standard)
- **Mapping Notes**:
  - Used for data quality validation
  - Combined with `ReportDate` provides full report creation timestamp
- **Group**: Temporal

---

## 🏷️ Incident Classification

### IncidentType1

**Export Header**: `Incident Type_1`

- **Definition**: Primary incident type classification code or description.
- **Source Field**: `Incident Type_1` (RMS export)
- **Format**: Text string
  - **Examples**: `THEFT`, `ASSAULT`, `BURGLARY`, `MOTOR VEHICLE THEFT`, `VANDALISM`
- **Logic**: User-selected from RMS incident type dropdown/lookup
- **Validation Rules**:
  - May be null (though strongly recommended to populate)
  - Should match controlled vocabulary from RMS incident type reference table
  - Case-insensitive validation recommended
- **Mapping Notes**:
  - **Priority 1** for backfilling CAD `Incident` field when CAD incident is null or blank
  - Mapped to CAD `Incident` field
  - Backfill condition: `update_when: cad_null_or_blank`, `accept_when: rms_not_null_or_blank`
- **Group**: Incident Classification

---

### IncidentType2

**Export Header**: `Incident Type_2`

- **Definition**: Secondary incident type classification (if multiple types apply to the same incident).
- **Source Field**: `Incident Type_2` (RMS export)
- **Format**: Text string (same format as `IncidentType1`)
- **Logic**: User-selected from RMS incident type dropdown/lookup
- **Validation Rules**:
  - May be null
  - Should match controlled vocabulary from RMS incident type reference table
- **Mapping Notes**:
  - **Priority 2** for backfilling CAD `Incident` field (used if `IncidentType1` is null)
  - Backfill order: `IncidentType1` → `IncidentType2` → `IncidentType3`
- **Group**: Incident Classification

---

### IncidentType3

**Export Header**: `Incident Type_3`

- **Definition**: Tertiary incident type classification (if multiple types apply to the same incident).
- **Source Field**: `Incident Type_3` (RMS export)
- **Format**: Text string (same format as `IncidentType1`)
- **Logic**: User-selected from RMS incident type dropdown/lookup
- **Validation Rules**:
  - May be null
  - Should match controlled vocabulary from RMS incident type reference table
- **Mapping Notes**:
  - **Priority 3** for backfilling CAD `Incident` field (used if `IncidentType1` and `IncidentType2` are null)
  - Backfill order: `IncidentType1` → `IncidentType2` → `IncidentType3`
- **Group**: Incident Classification

---

### NIBRSClassification

**Export Header**: `NIBRS Classification`

- **Definition**: NIBRS (National Incident-Based Reporting System) classification code for the incident.
- **Source Field**: `NIBRS Classification` (RMS export)
- **Format**: Text string
  - **Examples**: `13A - Aggravated Assault`, `23F - Theft from Motor Vehicle`, `220 - Burglary/Breaking & Entering`
- **Logic**: System-derived or user-selected based on incident type and details
- **Validation Rules**:
  - May be null (not all incidents have NIBRS classifications)
  - If present, should match NIBRS code structure and valid code list
  - Recommend validation against official NIBRS code reference
- **Mapping Notes**:
  - Used for UCR/NIBRS reporting compliance
  - Can be used for incident categorization in analysis workflows
- **Group**: Incident Classification

---

## 📍 Location Fields

### FullAddress

**Export Header**: `FullAddress`

- **Definition**: Full incident location address string.
- **Source Field**: `FullAddress` (RMS export)
- **Format**: Text string containing comma-separated address components
  - **Example Pattern**: `123 Main Street, Hackensack, NJ 07601`
  - **Components**: Street, City, State, ZIP
- **Logic**: User-entered or geocoded from address components
- **Validation Rules**:
  - May be null (some incidents may not have specific addresses, e.g., city-wide alerts)
  - If present, should contain at least one comma
  - Recommend validation against geocoding service or master address list
- **Mapping Notes**:
  - Backfills CAD `FullAddress2` when CAD address is null or blank
  - Used in **temporal_address_match** strategy (weight: 0.3, fuzzy match threshold: 0.85)
  - Used in **address_zone_match** strategy (weight: 0.5, fuzzy match threshold: 0.90)
  - Address normalization recommended: lowercase, remove punctuation, normalize street suffixes
- **Group**: Location

---

### Grid

**Export Header**: `Grid`

- **Definition**: CAD grid / map grid identifier for the incident location.
- **Source Field**: `Grid` (RMS export)
- **Format**: Text string
  - **Examples**: Grid codes vary by jurisdiction (to be defined from GIS/grid reference)
- **Logic**: System-derived from geocoded address or user-selected
- **Validation Rules**:
  - May be null
  - If present, should match controlled list of known grid codes (same domain as CAD `Grid`)
- **Mapping Notes**:
  - Direct mapping to CAD `Grid` field
  - Backfills CAD `Grid` when CAD grid is null or blank
- **Group**: Location

---

### Zone

**Export Header**: `Zone`

- **Definition**: Patrol/police zone code assigned to the incident location.
- **Source Field**: `Zone` (RMS export)
- **Format**: Integer or text (stored as string in current schema; observed as integer in analysis)
  - **Observed Range**: `5`–`9` (integers only, consistent with CAD `PDZone`)
- **Logic**: System-derived from geocoded address or grid, or user-selected
- **Validation Rules**:
  - May be null
  - If present, must be an integer within valid zone domain (5-9)
  - Should align with CAD `ZoneCalc`/`PDZone` domain
- **Mapping Notes**:
  - Backfills CAD `PDZone` when CAD zone is null or blank (28.5% backfill rate observed in analysis)
  - Used in **address_zone_match** strategy (weight: 0.3, exact match required)
- **Group**: Location

---

## 📝 Incident Details

### Narrative

**Export Header**: `Narrative`

- **Definition**: Detailed narrative text describing the incident, actions taken by officers, witness statements, and case outcomes.
- **Source Field**: `Narrative` (RMS export)
- **Format**: Long-form text (may contain multiple paragraphs, newlines, special characters)
  - **Example Structure**:
    ```
    On [DATE] at [TIME], officers responded to [LOCATION] for a report of [INCIDENT TYPE].

    Upon arrival, officers observed [OBSERVATIONS].

    Investigation revealed [FINDINGS].

    [SUSPECT/VICTIM] was identified as [DESCRIPTION].

    [PROPERTY] was recovered/stolen with an estimated value of [VALUE].
    ```
- **Logic**: User-entered narrative by reporting officer
- **Extraction Hints**:
  - **Suspect Descriptions**: Look for keywords like "suspect", "male", "female", "white", "black", "hispanic", "height", "weight", "wearing"
  - **Vehicle Descriptions**: Look for keywords like "vehicle", "car", "sedan", "SUV", "color", "make", "model", "plate", "registration"
  - **Property Details**: Look for keywords like "stolen", "recovered", "value", "serial number", "item", "property"
  - **MO (Modus Operandi)**: Look for keywords describing method of operation, entry points, tools used
  - **Times/Dates**: Look for date/time patterns (e.g., `MM/DD/YYYY`, `HH:MM`, "approximately", "between")
- **Validation Rules**:
  - May be null (some reports may not have narratives, though strongly recommended)
  - If present, may contain unstructured text
  - Recommend checking for minimum length (e.g., > 10 characters) to ensure meaningful content
- **Mapping Notes**:
  - Can be used for fuzzy text matching when primary keys don't match (use with caution due to unstructured nature)
  - Useful for extracting additional context for CAD integration (e.g., officer actions, outcomes)
  - May contain information for derived fields (e.g., suspect vehicle description, property details)
- **Group**: Incident Details

---

## 💰 Property Fields

### TotalValueStolen

**Export Header**: `Total Value Stolen`

- **Definition**: Total monetary value of stolen property in US dollars.
- **Source Field**: `Total Value Stolen` (RMS export)
- **Format**: Numeric (decimal)
  - **Accepted Formats**:
    - Numeric value (e.g., `1500.00`)
    - Currency text with `$` and commas (e.g., `$1,500.00`)
- **Logic**: Sum of all stolen property item values entered in RMS
- **Validation Rules**:
  - May be null (not all incidents involve theft or property loss)
  - If present, must be ≥ 0
  - Recommend flagging extremely high values (e.g., > $100,000) for manual review
- **Mapping Notes**:
  - Used for property crime analysis
  - Can help identify high-value theft patterns
- **Group**: Property

---

### TotalValueRecover

**Export Header**: `Total Value Recover`

- **Definition**: Total monetary value of recovered property in US dollars.
- **Source Field**: `Total Value Recover` (RMS export)
- **Format**: Numeric (decimal, same format as `TotalValueStolen`)
- **Logic**: Sum of all recovered property item values entered in RMS
- **Validation Rules**:
  - May be null
  - If present, must be ≥ 0
  - Should be ≤ `TotalValueStolen` (flag if recovered exceeds stolen)
- **Mapping Notes**:
  - Used for property recovery analysis and clearance rate calculations
- **Group**: Property

---

## 🚗 Vehicle Fields

### Registration1

**Export Header**: `Registration 1`

- **Definition**: Vehicle registration/license plate number for the first vehicle involved in the incident.
- **Source Field**: `Registration 1` (RMS export)
- **Format**: Text string (format varies by state)
  - **Examples**: `ABC123` (NJ), `ABC1234` (NY), `ABC-1234` (PA)
- **Logic**: User-entered from observation or DMV lookup
- **Validation Rules**:
  - May be null (not all incidents involve vehicles)
  - Format varies by `RegState1`
  - Recommend validation against state-specific plate format patterns
- **Mapping Notes**:
  - Used for vehicle identification and tracking
  - Can be matched against stolen vehicle databases
- **Group**: Vehicle

---

### RegState1

**Export Header**: `Reg State 1`

- **Definition**: State abbreviation for the first vehicle registration.
- **Source Field**: `Reg State 1` (RMS export)
- **Format**: Two-letter US state abbreviation
  - **Examples**: `NJ`, `NY`, `PA`, `CT`, `DE`
- **Logic**: User-selected from state dropdown
- **Validation Rules**:
  - May be null
  - If present, should be valid US state abbreviation (50 states + DC + territories)
  - Recommend validation against official state code list
- **Mapping Notes**:
  - Used to determine plate format validation rules for `Registration1`
- **Group**: Vehicle

---

### Make1

**Export Header**: `Make1`

- **Definition**: Vehicle make (manufacturer) for the first vehicle involved in the incident.
- **Source Field**: `Make1` (RMS export)
- **Format**: Text string
  - **Examples**: `Ford`, `Toyota`, `Honda`, `Chevrolet`, `BMW`, `Mercedes-Benz`
- **Logic**: User-entered or selected from vehicle make lookup table
- **Validation Rules**:
  - May be null
  - Should match against known vehicle make list if available (e.g., NCIC vehicle make codes)
  - Recommend standardizing capitalization and spelling
- **Mapping Notes**:
  - Used for vehicle description and identification
  - Can be used for pattern analysis (e.g., most stolen makes)
- **Group**: Vehicle

---

### Model1

**Export Header**: `Model1`

- **Definition**: Vehicle model for the first vehicle involved in the incident.
- **Source Field**: `Model1` (RMS export)
- **Format**: Text string
  - **Examples**: `F-150`, `Camry`, `Civic`, `Silverado`, `3 Series`, `C-Class`
- **Logic**: User-entered or selected from vehicle model lookup table
- **Validation Rules**:
  - May be null
  - Should match against known vehicle model list if available
  - Recommend validation against make-model combinations (e.g., Ford Camry is invalid)
- **Mapping Notes**:
  - Used for vehicle description and identification
  - Combined with `Make1` provides full vehicle description
- **Group**: Vehicle

---

### Registration2

**Export Header**: `Registration 2`

- **Definition**: Vehicle registration/license plate number for the second vehicle involved in the incident.
- **Source Field**: `Registration 2` (RMS export)
- **Format**: Text string (same format as `Registration1`)
- **Logic**: User-entered from observation or DMV lookup
- **Validation Rules**: Same as `Registration1`
- **Mapping Notes**:
  - Used when multiple vehicles are involved (e.g., motor vehicle accidents, two-vehicle thefts)
- **Group**: Vehicle

---

### RegState2

**Export Header**: `Reg State 2`

- **Definition**: State abbreviation for the second vehicle registration.
- **Source Field**: `Reg State 2` (RMS export)
- **Format**: Two-letter US state abbreviation
- **Validation Rules**: Same as `RegState1`
- **Group**: Vehicle

---

### Make2

**Export Header**: `Make2`

- **Definition**: Vehicle make (manufacturer) for the second vehicle involved in the incident.
- **Source Field**: `Make2` (RMS export)
- **Format**: Text string
- **Validation Rules**: Same as `Make1`
- **Group**: Vehicle

---

### Model2

**Export Header**: `Model2`

- **Definition**: Vehicle model for the second vehicle involved in the incident.
- **Source Field**: `Model2` (RMS export)
- **Format**: Text string
- **Validation Rules**: Same as `Model1`
- **Group**: Vehicle

---

## 👮 Personnel Fields

### OfficerOfRecord

**Export Header**: `Officer of Record`

- **Definition**: Primary officer assigned to the case in RMS.
- **Source Field**: `Officer of Record` (RMS export)
- **Format**: Text string
  - **Format Variations**: May include rank, badge number, or name variations
  - **Examples**: `Officer John Smith`, `Ofc. J. Smith`, `Smith, John (Badge 123)`
- **Logic**: User-selected from officer roster or auto-populated from CAD assignment
- **Validation Rules**:
  - May be null (some cases may not have assigned officers, e.g., administrative reports)
  - Should match standardized officer naming convention
  - Recommend aligning to officer standardization lookup (e.g., `Assignment_Master_V2.csv`)
- **Mapping Notes**:
  - Backfills CAD `Officer` when CAD officer is null or blank
  - Used in **officer_temporal_match** strategy (weight: 0.5, normalized officer match)
  - Officer normalization recommended: remove titles/prefixes, normalize name order, case-insensitive
- **Group**: Personnel

---

### Squad

**Export Header**: `Squad`

- **Definition**: Squad/unit identifier for the assigned officer.
- **Source Field**: `Squad` (RMS export)
- **Format**: Text string or code
  - **Examples**: `A-Squad`, `B-Squad`, `Day Shift`, `Night Shift`, `Detective Bureau`
- **Logic**: System-derived from officer assignment or user-selected
- **Validation Rules**:
  - May be null
  - Should match controlled squad/unit list if available
- **Mapping Notes**:
  - Used for squad-level analysis and reporting
  - Can help identify squad-specific patterns or workload
- **Group**: Personnel

---

### DetAssigned

**Export Header**: `Det_Assigned`

- **Definition**: Detective identifier assigned to the case (if applicable for follow-up investigation).
- **Source Field**: `Det_Assigned` (RMS export)
- **Format**: Text string (same format as `OfficerOfRecord`)
- **Logic**: User-selected from detective roster or assigned by supervisor
- **Validation Rules**:
  - May be null (not all cases require detective assignment, e.g., minor incidents)
  - Should match standardized officer naming convention
- **Mapping Notes**:
  - Used for case assignment tracking and follow-up management
  - Indicates cases requiring investigative follow-up
- **Group**: Personnel

---

## 📂 Case Management Fields

### ReviewedBy

**Export Header**: `Reviewed By`

- **Definition**: Officer or supervisor identifier who reviewed the case report.
- **Source Field**: `Reviewed By` (RMS export)
- **Format**: Text string (same format as `OfficerOfRecord`)
- **Logic**: Auto-populated when supervisor reviews/approves report
- **Validation Rules**:
  - May be null (cases may not yet be reviewed or may not require review)
  - Should match standardized officer naming convention (same as `OfficerOfRecord`)
- **Mapping Notes**:
  - Used for quality assurance and approval tracking
  - Indicates supervisory oversight
- **Group**: Case Management

---

### CompleteCalc

**Export Header**: `CompleteCalc`

- **Definition**: Boolean flag indicating whether the case is marked as complete.
- **Source Field**: `CompleteCalc` (RMS export)
- **Format**: Boolean or text
  - **Accepted Formats**:
    - Boolean (`true`/`false`)
    - Integer (`0`/`1`)
    - Text (`Y`/`N`, `Yes`/`No`, `Complete`/`Incomplete`)
- **Logic**: System-calculated or user-toggled based on case completion criteria
- **Validation Rules**:
  - May be null (defaults to incomplete)
  - If present, must be coercible to boolean
- **Mapping Notes**:
  - Used for case completion tracking and reporting
  - Helps identify incomplete or pending cases
- **Group**: Case Management

---

### CaseStatus

**Export Header**: `Case_Status`

- **Definition**: Current status of the case in RMS workflow.
- **Source Field**: `Case_Status` (RMS export)
- **Format**: Text string
  - **Expected Values** (to be confirmed from RMS reference):
    - `Open`
    - `Closed`
    - `Pending`
    - `Under Investigation`
    - `Suspended`
    - `Cleared by Arrest`
    - `Cleared - Exceptional`
    - `Unfounded`
- **Logic**: User-selected or system-derived based on case actions and outcomes
- **Validation Rules**:
  - May be null
  - Should match controlled vocabulary from RMS case status domain
  - Recommend validation against official status code list
- **Mapping Notes**:
  - Used for case lifecycle tracking and clearance analysis
  - Critical for UCR/NIBRS reporting compliance
- **Group**: Case Management

---

## Multi-Column Matching Strategy Usage

The following table summarizes which RMS fields are used in each multi-column matching strategy:

| Strategy Name | RMS Fields Used | Confidence Threshold | Purpose |
|---------------|----------------|---------------------|---------|
| **Primary Key Match** | `CaseNumber` | 1.0 (100%) | Exact match on case number |
| **Temporal + Address Match** | `IncidentDate`, `IncidentTime`, `FullAddress` | 0.85 (85%) | Match on date/time + location |
| **Officer + Temporal Match** | `OfficerOfRecord`, `IncidentDate`, `IncidentTime` | 0.80 (80%) | Match on officer + date/time |
| **Address + Zone Match** | `FullAddress`, `Zone`, `IncidentDate` (optional) | 0.75 (75%) | Match on location + zone |

**Detailed Strategy Documentation**: See `multi_column_matching_strategy.md` for implementation details, scoring formulas, and workflow guidance.

---

## Data Quality Validation Rules Summary

| Field Group | Key Validation Rules |
|-------------|---------------------|
| **Temporal** | Incident date ≤ Report date; Date ranges logical; Times within 24-hour format |
| **Location** | Addresses contain commas; Zones in valid range (5-9); Grid codes match reference |
| **Incident Classification** | Types match controlled vocabulary; NIBRS codes valid |
| **Vehicle** | State codes valid (50 states + DC); Make-model combinations logical |
| **Property** | Values ≥ 0; Recovered ≤ Stolen |
| **Personnel** | Officer names standardized; Match officer roster |
| **Case Management** | Status values match controlled vocabulary; Complete flag valid boolean |

---

## Open Confirmations (To Finalize v1.0)

1. **Controlled Vocabularies**: Confirm canonical allowed domains for:
   - `CaseStatus` (status values)
   - `IncidentType1/2/3` (incident type codes/descriptions)
   - `NIBRSClassification` (NIBRS code structure and valid values)
   - `Grid` (grid codes)
   - `Squad` (squad/unit codes)

2. **Supplemental Case Numbers**: Confirm whether supplementals can exceed `Z` (e.g., `AA`) or are limited to single-letter suffix (same as CAD).

3. **Timezone**: Confirm timezone for all temporal fields (recommend documenting as `America/New_York`).

4. **Vehicle Reference Data**: Provide controlled vocabulary lists for vehicle makes and models (if available).

5. **Temporal Alignment**: Confirm whether `IncidentDate`/`IncidentTime` should always match or be close to CAD `TimeofCall` for the same case number (data quality validation threshold).

6. **Narrative Structure**: Confirm if narrative has any standardized section headers or required fields (for automated extraction).

---

## Change Log

| Date | Version | Changes |
|------|---------|---------|
| 2025-12-30 | 1.0 | Initial comprehensive field definitions document with field grouping, enhanced validation rules, and multi-column matching integration |

---

## Related Documentation

- **CAD Field Definitions**: `CAD/DataDictionary/current/schema/cad_export_field_definitions.md`
- **CAD-to-RMS Mapping Schema**: `CAD_RMS/DataDictionary/current/schema/cad_to_rms_field_map.json`
- **RMS-to-CAD Mapping Schema**: `CAD_RMS/DataDictionary/current/schema/rms_to_cad_field_map.json`
- **Multi-Column Matching Strategy**: `multi_column_matching_strategy.md`
- **Schema Files Summary**: `SCHEMA_FILES_SUMMARY.md`
