# RMS Data Quality Report

## 1. Missing Values & Data Types Summary

| Column                |   Missing Count |   Missing % | Dtype          |   Unique Values |
|:----------------------|----------------:|------------:|:---------------|----------------:|
| Case Number           |               0 |        0    | object         |             134 |
| Incident Date         |               4 |        2.99 | datetime64[ns] |              97 |
| Incident Time         |               5 |        3.73 | object         |              97 |
| Incident Date_Between |              75 |       55.97 | datetime64[ns] |              51 |
| Incident Time_Between |              76 |       56.72 | object         |              45 |
| Report Date           |               0 |        0    | datetime64[ns] |             101 |
| Report Time           |               0 |        0    | object         |             133 |
| Incident Type_1       |               0 |        0    | object         |              15 |
| Incident Type_2       |              75 |       55.97 | object         |              27 |
| Incident Type_3       |             108 |       80.6  | object         |              19 |
| FullAddress           |               0 |        0    | object         |             119 |
| Grid                  |               7 |        5.22 | object         |              22 |
| Zone                  |              11 |        8.21 | float64        |               5 |
| Narrative             |               0 |        0    | object         |             134 |
| Total Value Stolen    |             130 |       97.01 | float64        |               4 |
| Total Value Recover   |             132 |       98.51 | float64        |               1 |
| Registration 1        |              65 |       48.51 | object         |              69 |
| Make1                 |              65 |       48.51 | object         |              25 |
| Model1                |              66 |       49.25 | object         |              56 |
| Reg State 1           |              67 |       50    | object         |               8 |
| Registration 2        |             130 |       97.01 | object         |               4 |
| Reg State 2           |             131 |       97.76 | object         |               1 |
| Make2                 |             130 |       97.01 | object         |               4 |
| Model2                |             131 |       97.76 | object         |               3 |
| Reviewed By           |               1 |        0.75 | object         |              25 |
| CompleteCalc          |               0 |        0    | object         |               1 |
| Officer of Record     |               0 |        0    | object         |              47 |
| Squad                 |               1 |        0.75 | object         |              14 |
| Det_Assigned          |               4 |        2.99 | object         |              16 |
| Case_Status           |               4 |        2.99 | object         |              10 |
| NIBRS Classification  |              31 |       23.13 | object         |              10 |

## 2. Case Number Pattern Check

| Pattern        |   Count |   Pct (%) |
|:---------------|--------:|----------:|
| Matches Format |     134 |       100 |
| Non-Matches    |       0 |         0 |

## 3. Date Columns Summary

| Column                |   Missing Count |   Missing % | Min Date            | Max Date            |   Years ≠ 2025 |
|:----------------------|----------------:|------------:|:--------------------|:--------------------|---------------:|
| Incident Date         |               4 |        2.99 | 2017-06-20 00:00:00 | 2025-07-27 00:00:00 |              5 |
| Incident Date_Between |              75 |       55.97 | 2024-09-20 00:00:00 | 2025-07-27 00:00:00 |             76 |

## 4. Time Columns Summary

| Column                |   Missing Count |   Missing % | Min Time   | Max Time   |
|:----------------------|----------------:|------------:|:-----------|:-----------|
| Incident Time         |             133 |       99.25 | 04:00:00   | 04:00:00   |
| Incident Time_Between |             134 |      100    |            |            |

## Findings and Recommendations


1. **Missing Values & Data Types**  
   Review null counts and data types to identify columns requiring cleaning or type conversion.

2. **Case Number Format**  
   Ensure all case numbers adhere to `DD-DDDDDD`. Non-matches should be corrected or validated.

3. **Date Columns**  
   Check for missing dates and entries outside 2025. Correct any incorrect year values.

4. **Time Columns**  
   Verify missing time entries and ensure valid time ranges (00:00:00–23:59:59).

