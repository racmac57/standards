# RMS to NIBRS Offense Mapping Guide
**Generated:** 2026-01-16 14:19:48
**Version:** 1.0

---

## Quick Reference

### ✅ High Confidence Mappings (Auto-Map)

| RMS Incident Type | NIBRS Code | NIBRS Name | Crime Type |
|-------------------|------------|------------|------------|
| AGG ASSAULT-DOM VIOLENCE VICTIM | 13A | Aggravated Assault | Crime Against Person |
| AGGRAVATED ASSAULT | 13A | Aggravated Assault | Crime Against Person |
| ANIMAL CRUELTY | 720 | Animal Cruelty | Crime Against Society |
| ARSON | 200 | Arson | Crime Against Property |
| AUTO BURGLARY | 23F | Theft From Motor Vehicle | Crime Against Property |
| BRIBERY | 510 | Bribery | Crime Against Property |
| BURGLARY | 220 | Burglary/Breaking & Entering | Crime Against Property |
| BURGLARY COMMERCIAL | 220 | Burglary/Breaking & Entering | Crime Against Property |
| BURGLARY FROM MOTOR VEHICLE | 23F | Theft From Motor Vehicle | Crime Against Property |
| BURGLARY RESIDENTIAL | 220 | Burglary/Breaking & Entering | Crime Against Property |
| BURGLARY/BREAKING AND ENTERING | 220 | Burglary/Breaking & Entering | Crime Against Property |
| COUNTERFEITING/FORGERY | 250 | Counterfeiting/Forgery | Crime Against Property |
| CRIMINAL MISCHIEF | 290 | Destruction/Damage/Vandalism of Property | Crime Against Property |
| CYBER HARASSMENT | 13C | Intimidation | Crime Against Person |
| DESTRUCTION/DAMAGE/VANDALISM OF PROPERTY | 290 | Destruction/Damage/Vandalism of Property | Crime Against Property |
| DISORDERLY CONDUCT | 90C | Disorderly Conduct | Group B Arrest Only |
| DRUG ABUSE VIOLATIONS | 35A | Drug/Narcotic Violations | Crime Against Society |
| DRUG/NARCOTIC OFFENSES | 35A | Drug/Narcotic Violations | Crime Against Society |
| EMBEZZLEMENT | 270 | Embezzlement | Crime Against Property |
| ENDANGERING-SEXUAL CONDUCT WITH CHILD | 11D | Fondling | Crime Against Person |
| EXTORTION/BLACKMAIL | 210 | Extortion/Blackmail | Crime Against Property |
| HARASSMENT | 13C | Intimidation | Crime Against Person |
| HARASSMENT-ANY OTHER ALARMING CONDUCT | 13C | Intimidation | Crime Against Person |
| KIDNAPPING/ABDUCTION | 100 | Kidnapping/Abduction | Crime Against Person |
| LARCENY FROM MOTOR VEHICLE | 23F | Theft From Motor Vehicle | Crime Against Property |
| MOTOR VEHICLE THEFT | 240 | Motor Vehicle Theft | Crime Against Property |
| MV THEFT | 240 | Motor Vehicle Theft | Crime Against Property |
| PORNOGRAPHY/OBSCENE MATERIAL | 370 | Pornography/Obscene Material | Crime Against Society |
| RECEIVING STOLEN PROPERTY-KNOWING PROP IS STOLEN | 280 | Stolen Property Offenses | Crime Against Property |
| ROBBERY | 120 | Robbery | Crime Against Property |
| SEXUAL ASSAULT | 11A | Rape | Crime Against Person |
| SHOPLIFTING | 23C | Shoplifting | Crime Against Property |
| SHOPLIFTING-TAKE MERCH W/O PAYING | 23C | Shoplifting | Crime Against Property |
| SIMPLE ASSAULT | 13B | Simple Assault | Crime Against Person |
| SIMPLE ASSAULT-PURP/KNOWING CAUSE BOD INJ | 13B | Simple Assault | Crime Against Person |
| TERRORISTIC THREATS | 13C | Intimidation | Crime Against Person |
| THEFT FROM AUTO | 23F | Theft From Motor Vehicle | Crime Against Property |
| THEFT FROM BUILDING | 23D | Theft From Building | Crime Against Property |
| THEFT FROM MOTOR VEHICLE | 23F | Theft From Motor Vehicle | Crime Against Property |
| TRESPASSING | 90J | Trespass of Real Property | Group B Arrest Only |
| UNDERAGE POSSESSION OF ALCOHOL | 90G | Liquor Law Violations | Group B Arrest Only |
| UNLAWFUL POSS WEAPON - OTHER WEAPONS | 520 | Weapon Law Violations | Crime Against Society |
| URINATING IN PUBLIC | 90Z | All Other Offenses | Group B Arrest Only |
| USE/POSS/W/INTENT TO USE DRUG PARAPHERNALIA | 35B | Drug Equipment Violations | Crime Against Society |
| WEAPONS | 520 | Weapon Law Violations | Crime Against Society |
| WEAPONS LAW VIOLATIONS | 520 | Weapon Law Violations | Crime Against Society |

### ⚠️ Medium Confidence (Validation Recommended)

| RMS Incident Type | NIBRS Code | Confidence | Notes |
|-------------------|------------|------------|-------|
| CALLING 911 WITHOUT NEEDING 911 SERVICE | 90Z | 0.7 | May be prosecutable offense - Group B if arrest ma |
| CHILD ENDANGERMENT | 90Z | 0.7 | NJ statute - report as Group B unless results in s |
| GAMBLING OFFENSES | None | 0.7 | Requires activity analysis |
| HOMICIDE OFFENSES | None | 0.7 | Requires willfulness analysis |
| HUMAN TRAFFICKING | None | 0.7 | Requires commercial sex vs. servitude analysis |
| LURING | 100 | 0.7 | NJ statute - attempted kidnapping of minor |
| PROSTITUTION OFFENSES | None | 0.7 | Requires role analysis |
| SEX OFFENSES, NON-FORCIBLE | None | 0.7 | Non-forcible typically incest or statutory rape |
| THEFT BY UNLAWFUL TAKING/DISPO-MOVEABLE PROP | 23H | 0.7 | NJ general theft statute - default to All Other La |
| THEFT-VALUE BETWEEN $500-$74,999 | 23H | 0.7 | NJ degree classification - requires location analy |

### 🔴 Ambiguous (Manual Review Required)

| RMS Incident Type | Possible NIBRS Codes | Validation Needed |
|-------------------|----------------------|-------------------|
| ASSAULT OFFENSES | 13A, 13B, 13C | weapon_use, injury_severity, physical_contact |
| CHILD ABUSE | 13A, 13B, 11D | physical_abuse, sexual_abuse, injury_severity |
| DV OFFENSES | 13A, 13B, 13C | underlying_offense |
| FRAUD | 26A, 26B, 26C, 26D, 26E, 26F, 26G | fraud_method, electronic_communication |
| FRAUD OFFENSES | 26A, 26B, 26C, 26D, 26E, 26F, 26G | fraud_method, electronic_communication |
| LARCENY/THEFT OFFENSES | 23A, 23B, 23C, 23D, 23E, 23F, 23G, 23H | theft_location, victim_type, property_type |
| MISSING PERSON | 100 | criminal_abduction, parental_abduction |
| SEX OFFENSES | 11A, 11D, 36A, 36B | penetration, age_of_victim, relationship |
| SEXUAL OFFENSE | 11A, 11D, 36A, 36B | penetration, age_of_victim, relationship |
| THEFT | 23A, 23B, 23C, 23D, 23E, 23F, 23G, 23H | theft_location, victim_type, property_type |

### 🚫 Non-Crimes (Do Not Report)

| RMS Incident Type | Notes |
|-------------------|-------|
| BWC REVIEW | NOT A CRIME - Administrative activity, do not report to NIBR |
| CALLS FOR SERVICE | NOT A CRIME - Administrative call type, do not report to NIB |
| CONDITIONAL DISMISSAL PROGRAM-ELIGIBILITY AND APP | NOT A CRIME - Court diversion program, do not report to NIBR |
| DCPP NOTIFICATION | NOT A CRIME - Child protective services notification, do not |
| EDP JUVENILE | NOT A CRIME - Emotionally disturbed person call, do not repo |
| HANDLE WITH CARE NOTIFICATION | NOT A CRIME - Notification system, do not report to NIBRS |
| JUVENILE COMPLAINTS | NOT A CRIME CODE - Classify underlying offense, age of offen |
| JUVENILE SHORT-TERM CUSTODY | NOT A CRIME - Custody status, do not report to NIBRS |
| MEDICAL | NOT A CRIME - Medical assistance call, do not report to NIBR |
| STATION HOUSE ADJUSTMENTS | NOT A CRIME - Juvenile diversion, do not report to NIBRS |
| SUSPICIOUS PERSON | NOT A CRIME - Investigative call, do not report to NIBRS unl |
| WELFARE CHECKS | NOT A CRIME - Welfare check is service call, do not report t |

---

## Special Classification Notes

### Domestic Violence
Domestic Violence (DV) is a RELATIONSHIP indicator, not an offense type. Always classify the underlying offense (assault, harassment, etc.) and capture DV relationship in victim-offender data elements.

### Juvenile Offenses
Age of offender is captured separately. Classify the actual offense committed, not 'juvenile offense' as the crime type.

### Administrative Codes
Service calls, notifications, and administrative activities (BWC Review, Welfare Checks, Calls for Service, etc.) are NOT reportable offenses.

### Group B Offenses
Group B offenses (90B-90Z) require ONLY arrest data reporting. Do NOT create incident reports for Group B offenses unless arrest made.

### Ambiguous Theft
When RMS lists 'THEFT' without specifics, analyze Incident Type_2 and Type_3 fields, location data, and narrative to determine correct larceny subcategory.

### Statute Removal
Remove NJ statute codes from incident types before mapping (e.g., 'THEFT - 2C:20-3' → 'THEFT').

### Multiple Incident Types
When Incident Type_1/2/3 contain multiple offenses, report ALL offenses that occurred. Follow NIBRS 'Acting in Concert' rules.

### Carjacking Special
Carjacking = 120 (Robbery) ONLY. Do NOT also report 240 (Motor Vehicle Theft). Vehicle is proceeds of robbery.

### Attempted Offenses
Attempted crimes reported as substantive offense with Offense Attempted/Completed = 'A'. Exception: Attempted murder = 13A (Aggravated Assault).

### Lesser Included
Do NOT report lesser included offenses. Example: Robbery includes assault - report 120 only, NOT 120 + 13A.
