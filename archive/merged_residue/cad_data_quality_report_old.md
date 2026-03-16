# CAD Data Quality Report

## 1. Missing Values & Data Types Summary

| Column          |   Missing Count |   Missing % | Dtype          |   Unique Values |
|:----------------|----------------:|------------:|:---------------|----------------:|
| ReportNumberNew |               0 |     0       | object         |             114 |
| Incident        |               0 |     0       | object         |               7 |
| How Reported    |               0 |     0       | object         |               5 |
| FullAddress2    |               0 |     0       | object         |             101 |
| PDZone          |               4 |     3.50877 | float64        |               5 |
| Grid            |               7 |     6.14035 | object         |              22 |
| Time of Call    |               0 |     0       | datetime64[ns] |             114 |
| cYear           |               0 |     0       | int64          |               1 |
| cMonth          |               0 |     0       | object         |               7 |
| HourMinuetsCalc |               0 |     0       | object         |             109 |
| DayofWeek       |               0 |     0       | object         |               7 |
| Time Dispatched |               0 |     0       | datetime64[ns] |             114 |
| Time Out        |               0 |     0       | datetime64[ns] |             114 |
| Time In         |               0 |     0       | datetime64[ns] |             114 |
| Time Spent      |               0 |     0       | object         |             106 |
| Time Response   |               0 |     0       | object         |             101 |
| Officer         |               0 |     0       | object         |              39 |
| Disposition     |               0 |     0       | object         |               1 |
| Response Type   |               4 |     3.50877 | object         |               2 |
| CADNotes        |              18 |    15.7895  | object         |              96 |

## 2. ReportNumberNew Pattern Check

| Pattern        |   Count |   Pct |
|:---------------|--------:|------:|
| Matches Format |     114 |   100 |
| Non-Matches    |       0 |     0 |

## 3. Incident Format Check

| Format         |   Count |   Pct |
|:---------------|--------:|------:|
| Contains " - " |     114 |   100 |
| Missing " - "  |       0 |     0 |

## 4. How Reported Value Counts

| Value             |   Count |
|:------------------|--------:|
| Phone             |      55 |
| 9-1-1             |      29 |
| Walk-In           |      20 |
| Other - See Notes |       5 |
| Radio             |       5 |

## 5. FullAddress2 Format Check

| Format         |   Count |   Pct |
|:---------------|--------:|------:|
| Contains comma |     114 |   100 |
| No comma       |       0 |     0 |

## 6. PDZone Numeric Statistics

| Stat   |     Value |
|:-------|----------:|
| Count  | 110       |
| Min    |   5       |
| Max    |   9       |
| Mean   |   7.22727 |
| Std    |   1.31092 |

### 6.1 PDZone Integer vs Non-Integer

| Type        |   Count |
|:------------|--------:|
| Integer     |     110 |
| Non-Integer |       0 |

### 6.2 PDZone Outliers

No outliers detected beyond 3σ

## Findings and Recommendations

1. **Missing Values & Data Types Summary**
   - Shows count and percentage of nulls for every column
   - Lists each column’s data type and number of unique values

2. **ReportNumberNew Pattern Check**
   - Validates that every record number follows the `DD-DDDDDD` format (two digits, dash, six digits)
   - Reports counts and percentages of mismatches

3. **Incident Format Check**
   - Verifies whether each incident description contains the separator “ - ” between parts
   - Flags any entries missing this expected delimiter

4. **How Reported Value Counts**
   - Breaks down all reporting methods (Phone, Walk-In, 9-1-1, Radio, etc.) along with their frequencies

5. **FullAddress2 Format Check**
   - Ensures addresses include commas (i.e., “street, city, state, ZIP”)
   - Flags any addresses lacking comma separators

6. **PDZone Numeric Statistics**
   - Provides count, min, max, mean, and standard deviation of zone codes
   - Confirms that zone codes are integers (no non-integer values found)
   - Checks for any outliers beyond three standard deviations from the mean (none detected)
