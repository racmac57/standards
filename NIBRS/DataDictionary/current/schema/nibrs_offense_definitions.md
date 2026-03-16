# NIBRS Offense Definitions

**Version**: 1.0 (Based on 2023.0 FBI NIBRS User Manual)  
**Date**: 2026-01-16  
**Author**: R. A. Carucci  
**Source**: FBI NIBRS User Manual 2023.0 (Released 06/30/2023)  
**Purpose**: Authoritative reference for UCR/NIBRS offense classification in Hackensack PD analytics and reporting

---

## Table of Contents

1. [Overview](#overview)
2. [Group A Offenses (28 Categories, 71 Offenses)](#group-a-offenses)
3. [Group B Offenses (10 Categories, 10 Offenses)](#group-b-offenses)
4. [Classification Guidelines](#classification-guidelines)
5. [Offense Lookup Quick Reference](#offense-lookup-quick-reference)

---

## Overview

### Purpose and Scope

This document provides comprehensive definitions for all NIBRS offenses used in the FBI's Uniform Crime Reporting (UCR) Program. These definitions serve as the "single source of truth" for crime classification in Hackensack Police Department data systems.

### Key Principles

**Standardized Definitions**: UCR definitions transcend varying state and local laws, providing a common language for crime reporting across the United States.

**Generic Application**: Definitions are intentionally generic to accommodate varying state statutes relating to the same type of crime.

**Crime Classification**: Offenses are classified after preliminary investigation is complete, based on the facts of the case, not court findings or prosecution decisions.

### Source of Definitions

NIBRS offense definitions are based on:
- Common-law definitions from Black's Law Dictionary
- NCIC 2000 Uniform Offense Classifications
- FBI UCR Program standards and guidance

### Crime Categories

All offenses fall into one of three categories:

| Category | Description | Victim/Target | Examples |
|----------|-------------|---------------|----------|
| **Crime Against Person** | Offenses whose victims are always individuals | Individual person | Murder, Rape, Assault |
| **Crime Against Property** | Object is to obtain money, property, or benefit | Property/Asset | Robbery, Burglary, Fraud |
| **Crime Against Society** | Society's prohibition against certain activities | Society/Public | Drug Violations, Gambling, Prostitution |

---

## Group A Offenses

Group A offenses require full incident reporting including administrative, offense, property, victim, offender, and arrestee information. LEAs must report all Group A offenses (up to 10) within a particular incident.

**Total**: 28 offense categories comprising 71 distinct offenses

---

### 09A-09C: Homicide Offenses

**General Definition**: The killing of one human being by another.

#### 09A - Murder and Nonnegligent Manslaughter

| Field | Value |
|-------|-------|
| **NIBRS Code** | 09A |
| **NCIC Codes** | 0901-0908, 0911-0912 |
| **Crime Type** | Crime Against Person |

**Definition**: The willful (nonnegligent) killing of one human being by another.

**Classification Guidelines**:
- As a general rule, any death due to injuries received in a fight, argument, quarrel, assault, or commission of a crime
- Includes deaths where the killing was willful or intentional, regardless of lesser charges filed
- Court findings, coroner's inquest, etc. should NOT influence reporting

**Exclusions** (NOT counted as murder):
- Suicides
- Traffic fatalities (including DUI-related deaths)
- Fetal deaths
- Assaults to murder (report as Aggravated Assault)
- Attempted murders (report as Aggravated Assault)
- Accidental deaths
- Heart attacks during commission of a crime (not direct injury)

**Reporting Notes**: Report circumstances in Data Element 31 (Aggravated Assault/Homicide Circumstances).

---

#### 09B - Negligent Manslaughter

| Field | Value |
|-------|-------|
| **NIBRS Code** | 09B |
| **NCIC Codes** | 0910 |
| **Crime Type** | Crime Against Person |

**Definition**: The killing of another person through gross negligence.

**Includes**:
- Hunting accidents
- Gun cleaning accidents
- Children playing with guns
- Traffic accidents involving:
  - Driving under the influence
  - Distracted driving (cell/smartphone use)
  - Reckless driving

**Exclusions**:
- Deaths due to the victim's own negligence
- Accidental deaths not resulting from gross negligence
- Accidental traffic fatalities (non-negligent)

**Reporting Notes**: 
- Firearm-related negligent manslaughter uses Data Values 30-33 in Data Element 31
- Other negligent killings use Data Value 34 = Other Negligent Killing

---

#### 09C - Justifiable Homicide (Not a Crime)

| Field | Value |
|-------|-------|
| **NIBRS Code** | 09C |
| **NCIC Codes** | None |
| **Crime Type** | Not a Crime |

**Definition**: The killing of a perpetrator of a serious criminal offense by:
- A law enforcement officer in the line of duty, OR
- A private individual during the commission of a serious criminal offense

**Critical Reporting Requirements**:

1. **Always Multiple Incidents**: Justifiable homicide requires at least TWO separate incident reports:
   - **Incident 1**: The underlying serious criminal offense being committed
   - **Incident 2**: The justifiable homicide itself
   - **Incident 3** (if applicable): Any offense by the "justified" killer (e.g., illegal weapon possession)

2. **Rationale**: The criminal killed did not "act in concert" with the officer/civilian who killed them; therefore, these cannot be part of the same incident under NIBRS definitions.

**Reporting Notes**: Report additional circumstances in Data Element 32 (Additional Justifiable Homicide Circumstances).

---

### 11A-11D, 36A-36B, 360: Sex Offenses

#### 11A - Rape

| Field | Value |
|-------|-------|
| **NIBRS Code** | 11A |
| **NCIC Codes** | 1101-1103 |
| **Crime Type** | Crime Against Person |

**Definition**: The penetration, no matter how slight, of the vagina or anus with any body part or object, or oral penetration by a sex organ of another person, without the consent of the victim. This offense includes the rape of both males and females.

**Key Elements**:
- Penetration (any degree)
- Without consent
- Can be reported regardless of victim gender
- Includes penetration by body parts or objects

**2023.0 Updates**:
- Starting 2023: Sodomy (11B) and Sexual Assault with Object (11C) are recoded to 11A for reporting purposes
- Starting 2025: 11B and 11C will be rejected; agencies must use 11A

---

#### 11B - Sodomy* (*Converts to 11A as of 2023)

| Field | Value |
|-------|-------|
| **NIBRS Code** | 11B (converts to 11A) |
| **NCIC Codes** | 1104-1115 |
| **Crime Type** | Crime Against Person |

**Status**: As of 2023, this offense recodes to 11A = Rape for reporting purposes. Will be rejected starting in 2025.

---

#### 11C - Sexual Assault With An Object* (*Converts to 11A as of 2023)

| Field | Value |
|-------|-------|
| **NIBRS Code** | 11C (converts to 11A) |
| **NCIC Codes** | None |
| **Crime Type** | Crime Against Person |

**Status**: As of 2023, this offense recodes to 11A = Rape for reporting purposes. Will be rejected starting in 2025.

---

#### 11D - Fondling

| Field | Value |
|-------|-------|
| **NIBRS Code** | 11D |
| **NCIC Codes** | 3601 (Child) |
| **Crime Type** | Crime Against Person |

**Definition**: The touching of the private body parts of another person for the purpose of sexual gratification, without the consent of the victim, including instances where the victim is incapable of giving consent because of his/her age or because of his/her temporary or permanent mental incapacity.

---

#### 36A - Incest

| Field | Value |
|-------|-------|
| **NIBRS Code** | 36A |
| **NCIC Codes** | 3604, 3607 |
| **Crime Type** | Crime Against Person |

**Definition**: Sexual intercourse between persons who are related to each other within the degrees wherein marriage is prohibited by law.

---

#### 36B - Statutory Rape

| Field | Value |
|-------|-------|
| **NIBRS Code** | 36B |
| **NCIC Codes** | 1116 |
| **Crime Type** | Crime Against Person |

**Definition**: Sexual intercourse with a person who is under the statutory age of consent.

---

#### 360 - Failure to Register as a Sex Offender*

| Field | Value |
|-------|-------|
| **NIBRS Code** | 360 |
| **NCIC Codes** | 3612 |
| **Crime Type** | Crime Against Society |

**Definition**: Failure to comply with sex offender registration requirements.

**Note**: Only federal and tribal LEAs may report this offense.

---

### 13A-13C: Assault Offenses

**General Definition**: An unlawful attack by one person upon another.

**Classification Factors**:
1. Type of weapon employed or use of object as weapon
2. Seriousness of the injury
3. Intent and capability of assailant to cause serious injury

**Critical Rule**: By definition, there can be no attempted assaults, only completed assaults. Therefore, Data Element 7 (Offense Attempted/Completed) must ALWAYS be C = Completed for all assault offenses.

---

#### 13A - Aggravated Assault

| Field | Value |
|-------|-------|
| **NIBRS Code** | 13A |
| **NCIC Codes** | 1301-1312, 1314-1315 |
| **Crime Type** | Crime Against Person |

**Definition**: An unlawful attack by one person upon another wherein the offender uses a dangerous weapon or displays it in a threatening manner, OR the victim suffers obvious severe or aggravated bodily injury, OR where there was a risk for serious injury/intent to seriously injure.

**Severe/Aggravated Bodily Injury Includes**:
- Apparent broken bones
- Loss of teeth
- Possible internal injury
- Severe laceration (requiring medical attention)
- Loss of consciousness (must be direct result of force)
- **Strangulation/Choking** (common signs):
  - Loss of consciousness/blacking out
  - Petechiae (small broken blood vessels in eyes, earlobes, scalp)
  - Bruising/marks on neck
  - Respiratory distress
  - Nausea/vomiting
  - Light-headedness
  - Involuntary urination/defecation

**Weapons**:
- Firearms, knives, blunt objects
- **Mace and pepper spray are considered weapons**
- Broken bottles, rocks, shoes, or any object used to harm

---

#### 13B - Simple Assault

| Field | Value |
|-------|-------|
| **NIBRS Code** | 13B |
| **NCIC Codes** | 1313 |
| **Crime Type** | Crime Against Person |

**Definition**: An unlawful physical attack by one person upon another where neither the offender displays a dangerous weapon, nor the victim suffers obvious severe or aggravated bodily injury involving apparent broken bones, loss of teeth, possible internal injury, severe laceration, or loss of consciousness.

**Includes**:
- Minor assault
- Hazing
- Assault and battery
- Injury caused by culpable negligence
- Attempts to commit simple assault

---

#### 13C - Intimidation

| Field | Value |
|-------|-------|
| **NIBRS Code** | 13C |
| **NCIC Codes** | 1316, 5215-5216 |
| **Crime Type** | Crime Against Person |

**Definition**: To unlawfully place another person in reasonable fear of harm through the use of threatening words and/or other conduct without displaying a dangerous weapon or subjecting the victim to an actual physical attack.

**Includes**:
- Stalking
- Threats made in person
- Threats made over telephone
- Threats made in writing (including electronic communications)

---

### 100: Kidnapping/Abduction

| Field | Value |
|-------|-------|
| **NIBRS Code** | 100 |
| **NCIC Codes** | 1001-1009, 1099 |
| **Crime Type** | Crime Against Person |

**Definition**: The unlawful seizure, transportation, and/or detention of a person against his/her will or of a minor without the consent of his/her custodial parent(s) or legal guardian.

**Includes**:
- Hostage situations
- Parental abductions

**Special Property Reporting**:
- **ONLY Crime Against Person offense that requires property reporting**
- Property segment used to report ransom information
- If no ransom paid, Data Element 14 (Type Property Loss/Etc.) = 1 = None

**Victim Reporting**:
- Report ONLY persons actually kidnapped/abducted/detained as victims
- Do NOT count persons/organizations paying ransom as victims

---

### 120: Robbery

| Field | Value |
|-------|-------|
| **NIBRS Code** | 120 |
| **NCIC Codes** | 1201-1211, 1299 |
| **Crime Type** | Crime Against Property |

**Definition**: The taking or attempting to take anything of value from the care, custody, or control of a person or persons by force or threat of force or violence and/or by putting the victim in fear.

**Key Elements**:
- Personal confrontation between victim and offender
- Property taken from person or immediate presence
- Force, threat of force, or fear employed

**Classification Notes**:
- Object is property; therefore Crime Against Property (despite person being victimized)
- Every robbery includes some type of assault, but assault is integral element
- Report as Robbery only; do NOT add separate assault offense
- If sexual assault occurs during robbery, report BOTH Robbery and Rape (not integral elements)

**Carjacking**:
- Report as 120 = Robbery
- Vehicle type identified in property description
- Do NOT also report as 240 = Motor Vehicle Theft (vehicle is proceeds of robbery)

---

### 200: Arson

| Field | Value |
|-------|-------|
| **NIBRS Code** | 200 |
| **NCIC Codes** | 2001-2009, 2099 |
| **Crime Type** | Crime Against Property |

**Definition**: To unlawfully and intentionally damage or attempt to damage any real or personal property by fire or incendiary device.

**Reporting Requirements**:
- Report ONLY fires determined through investigation to be unlawfully and intentionally set
- Include attempts to burn
- Do NOT include fires of suspicious or unknown origin
- Report one incident for each distinct arson operation

**Multi-Jurisdiction Fires**:
- LEA where fire started reports incident and ALL dollar value damage
- Even if fire spreads to another jurisdiction

**Fire Marshal Data**:
- LEA with jurisdiction should gather data from fire marshal and report
- Unless fire marshal has valid UCR ORI

**Deaths and Injuries**:
- Exclude arson-related deaths/injuries of police/firefighters
- Unless determined as willful murders or assaults
- Rationale: Hazardous nature of professions

**Property Reporting**:
- Data Element 15 (Property Description): Type of property burned
- Data Element 16 (Value of Property): Value of property + incidental fire-fighting damage

**Abandoned Structures**: Arson of abandoned structures is still reportable as arson.

---

### 220: Burglary/Breaking & Entering

| Field | Value |
|-------|-------|
| **NIBRS Code** | 220 |
| **NCIC Codes** | 2201-2205, 2207, 2299 |
| **Crime Type** | Crime Against Property |

**Definition**: The unlawful entry into a building or some other structure to commit a felony or a theft.

**Key Element**: Trespass is essential to burglary.

**Structure Definition** (must have):
- Four walls
- Roof
- Door

**Structures Include**:
- Apartment, barn, cabin, church, condominium
- Dwelling house, factory, garage
- House trailer/houseboat (if used as permanent dwelling)
- Mill, office, outbuilding, public building
- Railroad car, room, school, stable, vessel/ship, warehouse
- Mobile units permanently fixed as office/residence/storehouse

**NOT Structures** (report as larceny):
- Tents, tent trailers, motor homes
- House trailers/mobile units used for recreational purposes

**Larceny Element**:
- Larceny is an element of burglary
- Do NOT report separate larceny offense if associated with unlawful entry

---

#### Hotel Rule (Special Reporting)

**Apply to**: Hotels, motels, lodging houses, temporary rental storage facilities (mini-storage, self-storage)

**Single Incident** (report as one incident):
- Multiple units under single manager
- Manager likely to report (not individual tenants)
- Transient occupancy
- **Examples**: Hotel rooms, motel rooms, flop houses, youth hostels

**Separate Incidents** (report each burglary separately):
- Multiple occupants rent/lease individual areas for non-transient periods
- Individual occupants would report separately
- **Examples**: Apartment buildings, office buildings, college dormitories

**Number of Premises Entered**:
- Data Element 10: Report number of rooms/suites/units/storage compartments

---

#### Method of Entry

**Data Element 11**: Method of Entry

**F = Force**:
- Force of any degree used
- Mechanical contrivance used (passkey, skeleton key, etc.)

**N = No Force**:
- Entry through unlocked door or window

**If both**: Report F = Force

---

#### Incidental Damage

Report as separate offense (Destruction/Damage/Vandalism) ONLY if substantial:
- Forced door
- Broken window
- Hole in wall
- Dynamited safe

---

#### Critical Classification Notes

**NOT Burglary** (despite state statutes):
- Shoplifting from commercial establishments
- Theft from automobile (locked or unlocked)
- Theft from coin boxes/machines

**Burglary + Motor Vehicle Theft**:
- If vehicle stolen from garage during burglary:
  - Report BOTH 220 = Burglary AND 240 = Motor Vehicle Theft
  - Vehicle type in property description

---

### 23A-23H: Larceny/Theft Offenses

**General Definition**: The unlawful taking, carrying, leading, or riding away of property from the possession or constructive possession of another person.

**Key Principles**:
- Larceny and Theft are synonymous in UCR
- Local classifications (grand theft, petty larceny, felony/misdemeanor) have NO bearing on reporting
- Report one offense for each distinct operation, regardless of property value
- When multiple types of larceny occur in single incident, report ALL types

**NOT Larceny**:
- Embezzlement
- Fraud
- Counterfeiting/Forgery
- Conversion of entrusted property
- Check fraud

**Property Description**: Always enter type of property stolen in Data Element 15.

**Motor Vehicle Theft**: Counted separately, NOT included in Larceny/Theft category.

---

#### 23A - Pocket-picking

| Field | Value |
|-------|-------|
| **NIBRS Code** | 23A |
| **NCIC Codes** | 2301 |
| **Crime Type** | Crime Against Property |

**Definition**: The theft of articles from another person's physical possession by stealth where the victim is not immediately aware a theft occurred.

**Typical Scenarios**:
- Removal of wallets from purses or pockets
- Usually occurs in crowded areas or public transportation
- Victim in unconscious state (including intoxication)

**If Force Used**: If offender manhandles victim or uses force beyond simple jostling, classify as Strong-Arm Robbery (not pocket-picking).

---

#### 23B - Purse-snatching

| Field | Value |
|-------|-------|
| **NIBRS Code** | 23B |
| **NCIC Codes** | 2302 |
| **Crime Type** | Crime Against Property |

**Definition**: The grabbing or snatching of a purse, handbag, etc., from the physical possession of another person.

**Physical Possession Required**: Item must be on victim's person.

**If Force/Resistance**: If offender uses more force than necessary to snatch, or victim resists, classify as Strong-Arm Robbery.

**Unattended Items**: If purse left unattended in public location and stolen, classify as:
- 23D = Theft From Building
- 23F = Theft From Motor Vehicle
- Other appropriate larceny category

---

#### 23C - Shoplifting

| Field | Value |
|-------|-------|
| **NIBRS Code** | 23C |
| **NCIC Codes** | 2303 |
| **Crime Type** | Crime Against Property |

**Definition**: The unlawful taking of goods or merchandise exposed for sale by a person (other than an employee).

**Key Assumption**: Offender had legal access to premises (no trespass/unlawful entry).

**Includes**:
- Merchandise displayed inside buildings
- Merchandise displayed outside buildings as part of stock (fruit stands, hardware displays, etc.)

**If Employee**: Employee theft is NOT shoplifting (classify as Embezzlement or other appropriate offense).

---

#### 23D - Theft From Building

| Field | Value |
|-------|-------|
| **NIBRS Code** | 23D |
| **NCIC Codes** | 2308, 2311 |
| **Crime Type** | Crime Against Property |

**Definition**: The unlawful taking of items from within a building which is either open to the general public or to which the offender has legal access.

**Examples**:
- Churches, restaurants, schools, libraries
- Public buildings, professional offices
- During hours when facilities are open to public

**Legal Access Scenario**:
- Guest invited to home for meal
- Guest steals item during visit
- Classify as Theft From Building (had right to be there)

**Exclusions**:
- Shoplifting (separate classification)
- Theft From Coin-Operated Machines (separate classification)

**If Illegal Entry**: Report as 220 = Burglary/Breaking & Entering (not Theft From Building).

---

#### 23E - Theft From Coin-Operated Machine or Device

| Field | Value |
|-------|-------|
| **NIBRS Code** | 23E |
| **NCIC Codes** | 2307 |
| **Crime Type** | Crime Against Property |

**Definition**: The unlawful taking of items from a machine or device that is operated or activated by the use of coins.

**Includes**:
- Machines accepting coins OR paper bills
- Candy/food vending machines
- Telephone coin boxes
- Parking meters
- Pinball machines
- Washers/dryers in laundromats

**Key**: No breaking or illegal entry of building involved.

**If Breaking/Illegal Entry**: Report as 220 = Burglary.

---

#### 23F - Theft From Motor Vehicle (except Theft of Motor Vehicle Parts or Accessories)

| Field | Value |
|-------|-------|
| **NIBRS Code** | 23F |
| **NCIC Codes** | 2305 |
| **Crime Type** | Crime Against Property |

**Definition**: The unlawful taking of articles from a motor vehicle, locked or unlocked.

**Vehicle Types**:
- Automobiles, trucks, truck trailers, buses
- Motorcycles, motor homes, recreational vehicles

**Areas of Vehicle**:
- Trunk, glove compartment, other enclosures
- Any area in vehicle

**Items Stolen**:
- Cameras, suitcases, apparel, packages, etc.
- NOT integral parts of vehicle (those are 23G)

**Multiple Theft Types**:
- If both articles AND parts/accessories stolen:
  - Report BOTH 23F and 23G
  - Each with corresponding property type/loss

**State Statute Note**: Some states classify as burglary; still report as larceny for UCR.

**With Motor Vehicle Theft**:
- Usually report as 240 = Motor Vehicle Theft only
- Record stolen property in appropriate property categories
- **Exception**: If contents were real object (not vehicle):
  - Report 240 = Motor Vehicle Theft AND 23F = Theft From Motor Vehicle
  - Example: Tractor-trailer stolen for TV shipment; truck found abandoned and empty

---

#### 23G - Theft of Motor Vehicle Parts or Accessories

| Field | Value |
|-------|-------|
| **NIBRS Code** | 23G |
| **NCIC Codes** | 2304, 2407 |
| **Crime Type** | Crime Against Property |

**Definition**: The unlawful taking of any part or accessory affixed to the interior or exterior of a motor vehicle in a manner which would make the item an attachment of the vehicle or necessary for its operation.

**Includes**:
- Motors, transmissions
- Radios, heaters
- Hubcaps, wheel covers
- Manufacturers' emblems
- License plates
- Side-view mirrors
- Siphoned gasoline
- Built-in DVD players
- Mounted GPS devices
- Catalytic converters
- Tires on car

**If NOT Attached**: Items only being transported (not attached) = 23F = Theft From Motor Vehicle.

---

#### 23H - All Other Larceny

| Field | Value |
|-------|-------|
| **NIBRS Code** | 23H |
| **NCIC Codes** | 2306, 2309-2310, 2312-2316, 2410 |
| **Crime Type** | Crime Against Property |

**Definition**: All thefts which do not fit any of the specific Larceny/Theft subcategories.

**Includes**:
- Thefts from fenced enclosures
- Thefts from boats (houseboats if recreational)
- Thefts from airplanes
- Illegal entry of tent/tent trailer/travel trailer (recreational) followed by theft
- Animals
- Lawnmowers
- Lawn furniture
- Hand tools
- Farm/construction equipment
- **Gasoline "drive-offs" from self-service stations**

**Gasoline Theft Classification**:
- **Self-Service Station**: 23H = All Other Larceny (no contract/agreement for payment)
- **Full-Service Station**: 26A = False Pretenses/Swindle (tacit agreement to pay for service)

---

### 240: Motor Vehicle Theft

| Field | Value |
|-------|-------|
| **NIBRS Code** | 240 |
| **NCIC Codes** | 2401-2405, 2408, 2412, 2499 |
| **Crime Type** | Crime Against Property |

**Definition**: The theft of a motor vehicle.

**Motor Vehicle Definition**: A self-propelled vehicle that runs on the surface of land and not on rails, that is not proceeds of another crime, and fits one of the following:

---

#### Automobiles

**Includes**:
- Sedans, coupes, station wagons, convertibles
- Taxicabs
- Minivans (primarily transport people)
- Sport-utility vehicles (Explorers, Highlanders, 4Runners, Pathfinders, Hummers)
- Automobile derivative vehicles (Ranchero, El Camino, Caballero, Brat)

**Primary Purpose**: Transporting people

---

#### Buses

**Definition**: Motor vehicles specifically designed (but not necessarily used) to transport groups of people on a commercial basis.

**Van Classification**:
- Full-size vans with rows of seats = Buses
- Custom vans with temporary lodging = Recreational Vehicles
- Work vans with cargo areas = Trucks

---

#### Recreational Vehicles

**Definition**: Motor vehicles specifically designed (but not necessarily used) to transport people and provide them with temporary lodging for recreational purposes.

---

#### Trucks

**Definition**: Motor vehicles specifically designed (but not necessarily used) to transport cargo on a commercial basis.

**Includes**:
- Pickup trucks
- Pickup trucks with campers

**Rationale**: Meet definition of "specifically designed to transport cargo" even if not used commercially.

---

#### Other Motor Vehicles

**Definition**: Other motorized vehicles whose primary purpose is to transport people.

**Includes**:
- Motorcycles
- Motor scooters
- Trail bikes
- Mopeds
- Snowmobiles
- All-terrain vehicles
- Golf carts

---

#### Property Description

**Data Element 15**: Enter specific vehicle type:
- 03 = Automobiles
- 05 = Buses
- 24 = Recreational Vehicles
- 28 = Trucks
- 37 = Other Motor Vehicles

---

#### Special Situations

**Carjacking**:
- Report as 120 = Robbery
- Vehicle type in property description
- Do NOT report 240 = Motor Vehicle Theft (vehicle is proceeds of robbery)
- Do NOT use Data Elements 18 or 19 (Stolen/Recovered Vehicles)

**Burglary + Motor Vehicle**:
- Vehicle stolen from garage during burglary
- Report as 220 = Burglary/Breaking & Entering
- Vehicle type in property description
- Report 240 = Motor Vehicle Theft ONLY if clearly separate operation

---

### 250: Counterfeiting/Forgery

| Field | Value |
|-------|-------|
| **NIBRS Code** | 250 |
| **NCIC Codes** | 2501-2507, 2509-2510, 2589, 2599 |
| **Crime Type** | Crime Against Property |

**Definition**: The altering, copying, or imitating of something, without authority or right, with the intent to deceive or defraud by passing the copy or thing altered or imitated as that which is original or genuine, OR the selling, buying, or possession of an altered, copied, or imitated thing with the intent to deceive or defraud.

**Includes**:
- Altering/forging public and other records
- Making/altering/forging/counterfeiting bills, notes, drafts, tickets, checks, credit cards
- Forging wills, deeds, notes, bonds, seals, trademarks
- Counterfeiting coins, plates, banknotes, checks
- Possessing forged/counterfeit instruments
- Erasures
- Signing name of another/fictitious person with intent to defraud
- Using forged labels
- Possession/manufacture of counterfeiting apparatus
- Selling goods with altered/forged/counterfeit trademarks

**Relationship to Fraud**: Though elements of fraud may be present, counterfeiting/forgery is treated separately due to unique nature.

---

#### Type of Activity

**Data Element 12**: Type Criminal Activity/Gang Information
- Publishing
- Distributing
- Selling
- Buying
- Possessing
- Transporting

---

#### Property Description

**Data Element 15**: Type of property altered/counterfeited/forged

---

#### Type Property Loss/Etc.

**For Completed Counterfeiting/Forgery**:
- Can ONLY be:
  - 3 = Counterfeited/Forged
  - 5 = Recovered
  - 6 = Seized

**Items obtained by passing forged/counterfeit instruments are NOT reported here.**

---

#### Passing Forged/Counterfeit Instruments

**Problem**: When forged check/counterfeit money is used to obtain items, how to capture fraudulently obtained items?

**Solution**: Report TWO offenses:

1. **Offense 1**: 250 = Counterfeiting/Forgery
   - Type Property Loss/Etc.: 3 = Counterfeited/Forged
   - Property Description: 21 = Negotiable Instruments
   - Value: Face value of check/instrument

2. **Offense 2**: 26A = False Pretense/Swindle/Confidence Game
   - Type Property Loss/Etc.: 7 = Stolen/Etc.
   - Property Description: Items obtained
   - Value: Wholesale value of stolen property

---

#### Example: Department Store Forged Check

**Scenario**:
- Offender purchases $400 TV and $300 DVD player with forged check
- Store manager discovers forgery and calls police

**Report As**:

**Offense 1**:
- UCR Offense Code: 250 = Counterfeiting/Forgery
- Type Property Loss: 3 = Counterfeited/Forged
- Property Description: 21 = Negotiable Instruments
- Value: $700

**Offense 2**:
- UCR Offense Code: 26A = False Pretense/Swindle/Confidence Game
- Type Property Loss: 7 = Stolen/Etc.
- Property Description: 26 = Radios/TVs/DVDs
- Value: $550 (wholesale value)

**Note**: Once forged check is countersigned by manager, it becomes a negotiable instrument.

---

### 26A-26H: Fraud Offenses (except Counterfeiting/Forgery)

**General Definition**: The intentional perversion of the truth for the purpose of inducing another person or other entity in reliance upon it to part with something of value or to surrender a legal right.

**Key Distinction from Larceny**:
- **Fraud**: Achieved through deceit or lying
- **Larceny**: Physical taking of something

**Benefits/Detriments**:
- Can be tangible OR intangible
- **Intangibles**: Rights, privileges, promotions, reputation, entry to restricted areas, etc.

**Classification Rule**: Report most specific subcategory when circumstances fit multiple definitions.

**Exclusion**: Counterfeiting/Forgery has separate classification.

---

#### Bailee Conversion (Common Fraud)

**Scenario**: Offender rents equipment/automobile, promises to return it, but keeps it.

**Classification**: 26A = False Pretenses/Swindle/Confidence Game (NOT Larceny)

**Rationale**: Offender had lawful possession originally; through deceit (false promise to return) kept property.

---

#### Gasoline Theft Classification

**Self-Service Station**:
- Offender pumps gas and leaves without paying
- **Classification**: 23H = All Other Larceny
- **Rationale**: No contract/agreement for payment made

**Full-Service Station**:
- Offender requests service, gets gas, drives off without paying
- **Classification**: 26A = False Pretenses/Swindle/Confidence Game
- **Rationale**: Tacit agreement for product/service rendered

---

#### 26A - False Pretenses/Swindle/Confidence Game

| Field | Value |
|-------|-------|
| **NIBRS Code** | 26A |
| **NCIC Codes** | 2601-2603, 2607, 2699 |
| **Crime Type** | Crime Against Property |

**Definition**: The intentional misrepresentation of existing fact or condition or the use of some other deceptive scheme or device to obtain money, goods, or other things of value. Only includes fraud offenses that do not fit any of the specific subcategories.

**Elements**:
- **False Pretenses**: Premeditated/calculated act misrepresenting facts/situation to defraud
- **Swindling**: Cheating and defrauding grossly with deliberate artifice
- **Confidence Game**: Swindler gains confidence of victim before swindle

**Scope**: Acquisition of property, money, or valuable instruments by false/deceitful pretense or fraudulent representation.

---

#### 26B - Credit Card/Automated Teller Machine Fraud

| Field | Value |
|-------|-------|
| **NIBRS Code** | 26B |
| **NCIC Codes** | 2605 |
| **Crime Type** | Crime Against Property |

**Definition**: The unlawful use of a credit/debit card, credit/debit card number, or automatic teller machine for fraudulent purposes.

**Applies To**: Fraudulent USE of card/number (not theft of card itself).

---

#### 26C - Impersonation

| Field | Value |
|-------|-------|
| **NIBRS Code** | 26C |
| **NCIC Codes** | 2604 |
| **Crime Type** | Crime Against Property |

**Definition**: Unlawfully representing one's position and acting in the character or position to deceive others and thereby gain a profit or advantage, or enjoy some right or privilege.

**Example**:
- Individual puts on military uniform to receive business discounts
- Individual is not military service member
- Purpose: Impersonate service member to receive discount

**NOT Impersonation**: Fraudulent use of credit card number = 26B = Credit Card Fraud.

---

#### 26D - Welfare Fraud

| Field | Value |
|-------|-------|
| **NIBRS Code** | 26D |
| **NCIC Codes** | None |
| **Crime Type** | Crime Against Property |

**Definition**: The use of deceitful statements, practices, or devices to unlawfully obtain welfare benefits.

**Includes**: Electronic Benefit Transfer (EBT) card when utilized with welfare transaction.

---

#### 26E - Wire Fraud

| Field | Value |
|-------|-------|
| **NIBRS Code** | 26E |
| **NCIC Codes** | 2608 |
| **Crime Type** | Crime Against Property |

**Definition**: The use of an electric or electronic communications facility to intentionally transmit a false and/or deceptive message in furtherance of a fraudulent activity.

**Applies To**:
- Telephone, teletype, computers
- E-mail, text messages
- Any electronic communication used in commission/furtherance of fraud

**Example**:
- Using computer to order products through fraudulent online auction site
- Paying for products but never receiving them
- Classify as 26E = Wire Fraud

---

#### 26F - Identity Theft

| Field | Value |
|-------|-------|
| **NIBRS Code** | 26F |
| **NCIC Codes** | 2610 |
| **Crime Type** | Crime Against Property |

**Definition**: Wrongfully obtaining and/or using another person's personal data (e.g., name and date of birth, Social Security number, driver's license number).

**Includes**:
- Opening credit card using person's information
- Opening bank account using person's information
- Possession of another person's personal data

**NOT Identity Theft**: 26C = Impersonation (falsely acting in character/position without possessing personal data).

---

#### 26G - Hacking/Computer Invasion

| Field | Value |
|-------|-------|
| **NIBRS Code** | 26G |
| **NCIC Codes** | 2609 |
| **Crime Type** | Crime Against Property |

**Definition**: Gaining access to another person's or institution's computer software, hardware, or networks without authorized permissions.

---

#### 26H - Money Laundering*

| Field | Value |
|-------|-------|
| **NIBRS Code** | 26H |
| **NCIC Codes** | 6300 |
| **Crime Type** | Crime Against Society |

**Definition**: The process of transforming the profits of a crime into a legitimate asset.

**Crime Type**: Crime Against Society with Property

**Note**: Only federal and tribal LEAs may report this offense.

---

### 270: Embezzlement

| Field | Value |
|-------|-------|
| **NIBRS Code** | 270 |
| **NCIC Codes** | 2701-2705, 2799 |
| **Crime Type** | Crime Against Property |

**Definition**: The unlawful misappropriation by an offender to his/her own use or purpose of money, property, or some other thing of value entrusted to his/her care, custody, or control.

**Key Requirements**:
- Employer/employee OR legal agent relationship must exist
- Property was entrusted to offender's care/custody/control

**Typical Victims**:
- Businesses
- Financial institutions
- Government entities
- Individuals

**Data Element 25**: Type of Victim (financial institution, business, government, individual, religious organization, society/public, other)

---

### 280: Stolen Property Offenses

| Field | Value |
|-------|-------|
| **NIBRS Code** | 280 |
| **NCIC Codes** | 2801-2805, 2899 |
| **Crime Type** | Crime Against Property |

**Definition**: Buying, receiving, possessing, selling, concealing, or transporting any property with the knowledge that it has been unlawfully taken, as by Burglary, Embezzlement, Fraud, Larceny, Robbery, etc.

**Key Element**: Offender KNEW or had reason to believe property was stolen.

---

### 290: Destruction/Damage/Vandalism of Property (except Arson)

| Field | Value |
|-------|-------|
| **NIBRS Code** | 290 |
| **NCIC Codes** | 2901-2906, 2999 |
| **Crime Type** | Crime Against Property |

**Definition**: To willfully or maliciously destroy, damage, deface, or otherwise injure any public or private property without the consent of the owner or the person having custody or control of it.

**General Rule**: Report ONLY if substantial damage occurred.

**Substantial Damage**:
- Major structural damage
- Property damage generally classified as felony destruction
- Damage requiring significant repair/replacement

**Do NOT Report**:
- Insubstantial damage (broken window, minor damage)
- Determination left to LEA discretion

**Incidental Damage from Other Offenses**:
- Report as 290 ONLY if substantial
- **Example**: Burglary with kicked-in door → Report as Destruction/Damage ONLY if deemed substantial
- **Arson Exception**: Include incidental fire-fighting damage as part of arson loss

---

### 35A-35B: Drug/Narcotic Offenses

**General Definition**: The violation of laws prohibiting the production, distribution, and/or use of certain controlled substances and the equipment or devices utilized in their preparation and/or use.

**Data Element 12**: Type Criminal Activity/Gang Information (up to 3):
- Cultivating
- Manufacturing
- Distributing
- Selling
- Buying
- Using
- Possessing
- Transporting
- Importing

---

#### 35A - Drug/Narcotic Violations

| Field | Value |
|-------|-------|
| **NIBRS Code** | 35A |
| **NCIC Codes** | 3501-3505, 3510-3513, 3520-3523, 3530-3533, 3540-3543, 3560-3564, 3570-3573, 3580-3583, 3599 |
| **Crime Type** | Crime Against Society |

**Definition**: The unlawful cultivation, manufacture, distribution, sale, purchase, use, possession, transportation, or importation of any controlled substance.

**Property Reporting** (Special Rules):
- Do NOT enter value in Data Element 16 (Value of Property)
- **Rationale**: Difficult to determine street value

**Required Reporting**:
- Data Element 20 (Suspected Drug Type)
- Data Element 21 (Estimated Drug Quantity)
- Data Element 22 (Type Drug Measurement) - e.g., kilograms, liquid ounces

---

#### 35B - Drug Equipment Violations

| Field | Value |
|-------|-------|
| **NIBRS Code** | 35B |
| **NCIC Codes** | 3550 |
| **Crime Type** | Crime Against Society |

**Definition**: The unlawful manufacture, sale, purchase, possession, or transportation of equipment or devices utilized in preparing and/or using drugs or narcotics.

**Covers**:
- Drug paraphernalia
- Equipment
- Chemicals
- Illegal labs

**Note**: State/local statutes/codes vary in descriptions of unlawful equipment/paraphernalia.

---

### 210: Extortion/Blackmail

| Field | Value |
|-------|-------|
| **NIBRS Code** | 210 |
| **NCIC Codes** | 2101-2105, 2199 |
| **Crime Type** | Crime Against Property |

**Definition**: To unlawfully obtain money, property, or any other thing of value, either tangible or intangible, through the use or threat of force, misuse of authority, threat of criminal prosecution, threat of destruction of reputation or social standing, or through other coercive means.

**Key Distinction from Robbery**:
- **Extortion**: Non-confrontational circumstances; victim NOT in fear of immediate harm
- **Robbery**: Personal confrontation; offender has opportunity to carry out threat immediately

**Classification**:
- Object is to obtain money/property/intangibles
- Therefore: Crime Against Property (despite persons being involved/victimized)

**Intangible Benefits/Detriments**:
- If intangible benefit produced, report as:
  - Data Value 66 = Identity-Intangible (if agency has updated property descriptions), OR
  - Data Value 77 = Other (if agency has not programmed new property descriptions)

**Intangibles Include**:
- Rights, privileges
- Promotions
- Enhanced reputation
- Loss of reputation
- Injured feelings

---

### 39A-39D: Gambling Offenses

**General Definition**: To unlawfully bet or wager money or something else of value; assist, promote, or operate a game of chance for money or some other stake; possess or transmit wagering information; manufacture, sell, purchase, possess, or transport gambling equipment, devices, or goods; or tamper with the outcome of a sporting event or contest to gain a gambling advantage.

**Legal Gambling Exception**: In areas where gambling is legal, report ONLY violations of local statutes.

**Property Reporting**:
- If seizure involved, report in Data Element 15 (Property Description)
- Report value in Data Element 16 (Value of Property)
- Examples: Money, gambling equipment

---

#### 39A - Betting/Wagering

| Field | Value |
|-------|-------|
| **NIBRS Code** | 39A |
| **NCIC Codes** | None |
| **Crime Type** | Crime Against Society |

**Definition**: To unlawfully stake money or something else of value on the happening of an uncertain event or on the ascertainment of a fact in dispute.

---

#### 39B - Operating/Promoting/Assisting Gambling

| Field | Value |
|-------|-------|
| **NIBRS Code** | 39B |
| **NCIC Codes** | 3901-3902, 3904-3905, 3907, 3915-3916, 3918, 3920-3921 |
| **Crime Type** | Crime Against Society |

**Definition**: To unlawfully operate, promote, or assist in the operation of a game of chance, lottery, or other gambling activity.

**Includes**:
- Bookmaking
- Numbers running
- Transmitting wagering information

---

#### 39C - Gambling Equipment Violations

| Field | Value |
|-------|-------|
| **NIBRS Code** | 39C |
| **NCIC Codes** | 3908-3914 |
| **Crime Type** | Crime Against Society |

**Definition**: To unlawfully manufacture, sell, buy, possess, or transport equipment, devices, and/or goods used for gambling purposes.

**Also Known As**: Gambling paraphernalia

**Data Element 12**: Type of Activity
- Manufacturing
- Selling
- Buying
- Possessing
- Transporting

---

#### 39D - Sports Tampering

| Field | Value |
|-------|-------|
| **NIBRS Code** | 39D |
| **NCIC Codes** | 3919 |
| **Crime Type** | Crime Against Society |

**Definition**: To unlawfully alter, meddle in, or otherwise interfere with a sporting contest or event for the purpose of gaining a gambling advantage.

**Includes**: Bribery for gambling purposes.

**Example**: Bribing jockey to lose horse race = Sports Tampering (NOT 510 = Bribery).

---

### 40A-40C: Prostitution Offenses

#### 40A - Prostitution

| Field | Value |
|-------|-------|
| **NIBRS Code** | 40A |
| **NCIC Codes** | 4003-4004 |
| **Crime Type** | Crime Against Society |

**Definition**: To unlawfully engage in or promote sexual activity for profit.

---

#### 40B - Assisting or Promoting Prostitution

| Field | Value |
|-------|-------|
| **NIBRS Code** | 40B |
| **NCIC Codes** | 4001-4002, 4006-4009, 4099 |
| **Crime Type** | Crime Against Society |

**Definition**: To unlawfully assist or promote prostitution activities.

**Includes**:
- Pimping
- Pandering
- Maintaining brothels
- Transporting persons for prostitution

---

#### 40C - Purchasing Prostitution

| Field | Value |
|-------|-------|
| **NIBRS Code** | 40C |
| **NCIC Codes** | 4005 |
| **Crime Type** | Crime Against Society |

**Definition**: To unlawfully purchase sexual activity for profit.

---

### 370: Pornography/Obscene Material

| Field | Value |
|-------|-------|
| **NIBRS Code** | 370 |
| **NCIC Codes** | 3700-3706, 3799 |
| **Crime Type** | Crime Against Society |

**Definition**: The violation of laws or ordinances prohibiting the manufacture, publishing, sale, purchase, or possession of sexually explicit material, e.g., literature, photographs, etc.

---

### 510: Bribery

| Field | Value |
|-------|-------|
| **NIBRS Code** | 510 |
| **NCIC Codes** | 5101-5113, 5199 |
| **Crime Type** | Crime Against Property |

**Definition**: The offering, giving, receiving, or soliciting anything of value (e.g., a bribe, gratuity, or kickback) to sway the judgement or action of a person in a position of trust or influence.

**"Anything of Value" Includes**:
- Bribes
- Gratuities
- Kickbacks
- Favors
- Anything else used illegally to influence outcomes governed by:
  - Law
  - Fair play
  - Contractual agreement
  - Other guidelines

**Scope**: Influences outcome outside realm of reasonableness; result could be predicted based on bribe/influence.

**EXCLUDES**: Sports bribery → Report as 39D = Sports Tampering (NOT Bribery).

---

### 520-522, 526: Weapon Law Violations

#### 520 - Weapon Law Violations

| Field | Value |
|-------|-------|
| **NIBRS Code** | 520 |
| **NCIC Codes** | 5201-5214, 5299 |
| **Crime Type** | Crime Against Society |

**Definition**: The violation of laws or ordinances prohibiting the manufacture, sale, purchase, transportation, possession, concealment, or use of firearms, cutting instruments, explosives, incendiary devices, or other deadly weapons.

---

#### 521 - Violation of National Firearm Act of 1934*

| Field | Value |
|-------|-------|
| **NIBRS Code** | 521 |
| **NCIC Codes** | None |
| **Crime Type** | Crime Against Society |

**Definition**: Violations of federal firearm regulations under the National Firearm Act of 1934.

**Note**: Only federal and tribal LEAs may report this offense.

---

#### 522 - Weapons of Mass Destruction*

| Field | Value |
|-------|-------|
| **NIBRS Code** | 522 |
| **NCIC Codes** | None |
| **Crime Type** | Crime Against Society |

**Definition**: Offenses involving weapons of mass destruction.

**Note**: Only federal and tribal LEAs may report this offense.

---

#### 526 - Explosives*

| Field | Value |
|-------|-------|
| **NIBRS Code** | 526 |
| **NCIC Codes** | 5204-5206, 5211 |
| **Crime Type** | Crime Against Society |

**Definition**: Violations involving explosives.

**Note**: Only federal and tribal LEAs may report this offense.

---

### 64A-64B: Human Trafficking Offenses

**General Definition**: The inducement of a person to perform a commercial sex act, or labor, or services, through force, fraud, or coercion.

**Minors**: Human trafficking has occurred if person under 18 has been induced/enticed to perform commercial sex act, REGARDLESS of force, fraud, or coercion.

---

#### 64A - Human Trafficking, Commercial Sex Acts

| Field | Value |
|-------|-------|
| **NIBRS Code** | 64A |
| **NCIC Codes** | 6411 |
| **Crime Type** | Crime Against Person |

**Definition**: Inducing a person by force, fraud, or coercion to participate in commercial sex acts, OR in which the person induced to perform such act(s) has not attained 18 years of age.

**Juveniles**: All juveniles considered victims if induced to perform commercial sex acts.

**Key**: Involves "exploitation" of individual; not based on commercial sex act alone.

**Survival Sex Counted**: Sex acts for food, shelter, etc.

---

#### 64B - Human Trafficking, Involuntary Servitude

| Field | Value |
|-------|-------|
| **NIBRS Code** | 64B |
| **NCIC Codes** | 6411 |
| **Crime Type** | Crime Against Person |

**Definition**: The obtaining of person(s) through recruitment, harboring, transportation, or provision, and subjecting such persons by force, fraud, or coercion into involuntary servitude, peonage, debt bondage, or slavery (not to include commercial sex acts).

---

### 720: Animal Cruelty

| Field | Value |
|-------|-------|
| **NIBRS Code** | 720 |
| **NCIC Codes** | 7201 |
| **Crime Type** | Crime Against Society |

**Definition**: Intentionally, knowingly, or recklessly taking an action that mistreats or kills any animal without just cause, such as torturing, tormenting, mutilation, maiming, poisoning, or abandonment.

**Includes**:
- Duty to provide care failures (shelter, food, water, care if sick/injured)
- Transporting/confining animal to fight with another
- Inflicting excessive/repeated unnecessary pain/suffering
- Using objects to beat/injure animal

**EXCLUDES**:
- Proper maintenance of animals for show or sport
- Use of animals for food
- Lawful hunting, fishing, trapping

**Data Element 12**: Type Criminal Activity/Gang Information (at least 1, up to 3):
- Simple/gross neglect
- Organized abuse
- Intentional abuse or torture
- Animal sexual abuse

---

### Federal/Tribal Only Offenses

The following offenses are ONLY reported by federal and tribal law enforcement agencies:

---

#### 30A - Illegal Entry into the United States*

| Field | Value |
|-------|-------|
| **NIBRS Code** | 30A |
| **NCIC Codes** | 0301 |
| **Crime Type** | Crime Against Society |

**Definition**: To attempt to enter the U.S. at any time or place other than as designated; or eludes examination/inspection by immigration officers.

---

#### 30B - False Citizenship*

| Field | Value |
|-------|-------|
| **NIBRS Code** | 30B |
| **NCIC Codes** | 0302 |
| **Crime Type** | Crime Against Society |

**Definition**: Falsely and willfully representing oneself to be a citizen of the United States.

---

#### 30C - Smuggling Aliens*

| Field | Value |
|-------|-------|
| **NIBRS Code** | 30C |
| **NCIC Codes** | 0303 |
| **Crime Type** | Crime Against Society |

**Definition**: To knowingly assist, abet, or aid another person to enter, or try to enter, the United States illegally.

---

#### 30D - Re-entry after Deportation*

| Field | Value |
|-------|-------|
| **NIBRS Code** | 30D |
| **NCIC Codes** | 0399 |
| **Crime Type** | Crime Against Society |

**Definition**: The act of entering, attempting to enter, or being found in the United States after being removed, excluded, deported, or has departed the United States while an order of removal exclusion or deportation is outstanding.

---

#### 49A - Harboring Escapee/Concealing from Arrest*

| Field | Value |
|-------|-------|
| **NIBRS Code** | 49A |
| **NCIC Codes** | 4904, 4901 |
| **Crime Type** | Crime Against Society |

**Definition**: To harbor or conceal any person for whose arrest, a warrant or process has been issued, so as to prevent the fugitive's discovery and arrest, after having notice or knowledge that a warrant or process has been issued for the fugitive's apprehension.

---

#### 49B - Flight to Avoid Prosecution*

| Field | Value |
|-------|-------|
| **NIBRS Code** | 49B |
| **NCIC Codes** | 4902 |
| **Crime Type** | Crime Against Society |

**Definition**: To knowingly leave the jurisdiction where charges were filed with intent to avoid prosecution, custody, confinement, or to avoid giving testimony in any criminal proceedings.

---

#### 49C - Flight to Avoid Deportation*

| Field | Value |
|-------|-------|
| **NIBRS Code** | 49C |
| **NCIC Codes** | 4902 |
| **Crime Type** | Crime Against Society |

**Definition**: To knowingly leave the jurisdiction with intent to avoid deportation.

---

#### 58A - Import Violations*

| Field | Value |
|-------|-------|
| **NIBRS Code** | 58A |
| **NCIC Codes** | None |
| **Crime Type** | Crime Against Society |

**Definition**: To knowingly or willfully defraud the United States by smuggling, importing, or clandestinely introducing merchandise that should have been invoiced, received, bought, sold, or facilitate the transportation, the concealment, or sale of such merchandise after importation.

---

#### 58B - Export Violations*

| Field | Value |
|-------|-------|
| **NIBRS Code** | 58B |
| **NCIC Codes** | None |
| **Crime Type** | Crime Against Society |

**Definition**: To knowingly or willfully defraud the United States by smuggling, exporting, or clandestinely distributing merchandise that should have been invoiced, received, bought, sold, or facilitate the transportation, the concealment, or sale of such merchandise after exportation.

---

#### 61A - Federal Liquor Offenses*

| Field | Value |
|-------|-------|
| **NIBRS Code** | 61A |
| **NCIC Codes** | 4101-4104, 4199, 6103 |
| **Crime Type** | Crime Against Society |

**Definition**: The unlawful production (using an unregistered still), transportation (without proper bill of lading), receipt, distribution, or smuggling of distilled spirits on which federal tax has not been paid. Acting as a distiller, a winery, or a wholesaler of distilled spirits, wine, or malt beverages without a federal permit.

---

#### 61B - Federal Tobacco Offenses*

| Field | Value |
|-------|-------|
| **NIBRS Code** | 61B |
| **NCIC Codes** | 6102 |
| **Crime Type** | Crime Against Society |

**Definition**: The unlawful possession and/or distribution of contraband tobacco products; including any quantity of cigarettes in excess of 10,000 or other tobacco products if the cigarettes/products bear no evidence of the payment of applicable state taxes in the state where the cigarettes are found. Engaging in interstate commerce in tobacco products without registering with, and reporting to, the federal government and applicable state tax administrators.

---

#### 90K - Failure to Appear (Bond Default)*

| Field | Value |
|-------|-------|
| **NIBRS Code** | 90K |
| **NCIC Codes** | 5015 |
| **Crime Type** | Group B Offense |

**Definition**: Failure to appear as required by bond conditions.

---

#### 90L - Federal Resource Violations*

| Field | Value |
|-------|-------|
| **NIBRS Code** | 90L |
| **NCIC Codes** | None |
| **Crime Type** | Group B Offense |

**Definition**: Violations of federal resource protection laws.

---

#### 90M - Perjury*

| Field | Value |
|-------|-------|
| **NIBRS Code** | 90M |
| **NCIC Codes** | 5003, 5004 |
| **Crime Type** | Group B Offense |

**Definition**: Making false statements under oath.

---

#### 101 - Treason*

| Field | Value |
|-------|-------|
| **NIBRS Code** | 101 |
| **NCIC Codes** | 0101 |
| **Crime Type** | Crime Against Society |

**Definition**: Violation of allegiance toward one's country; betrayal of one's country.

---

#### 103 - Espionage*

| Field | Value |
|-------|-------|
| **NIBRS Code** | 103 |
| **NCIC Codes** | 0103 |
| **Crime Type** | Crime Against Society |

**Definition**: The act of obtaining, delivering, transmitting, communicating, or receiving national security or national defense information with an intent, or reason to believe, that the information may be used to the injury of the United States or to the advantage of any foreign nation.

---

#### 620 - Wildlife Trafficking*

| Field | Value |
|-------|-------|
| **NIBRS Code** | 620 |
| **NCIC Codes** | None |
| **Crime Type** | Crime Against Society |

**Definition**: The poaching or other illegal taking of protected or managed species and the illegal trade in wildlife and their related parts and products.

---

## Group B Offenses

Group B offenses require ONLY arrest data reporting. LEAs do NOT report incidents for Group B offenses, only arrests.

**Total**: 10 offense categories comprising 10 distinct offenses

---

### 90B - Curfew/Loitering/Vagrancy Violations

| Field | Value |
|-------|-------|
| **NIBRS Code** | 90B |
| **NCIC Codes** | None |
| **Crime Type** | Group B Arrest Only |

**Definition**: Violations of curfew, loitering, or vagrancy ordinances.

**Arrest Data Only**: Report only when arrest made.

---

### 90C - Disorderly Conduct

| Field | Value |
|-------|-------|
| **NIBRS Code** | 90C |
| **NCIC Codes** | 5310-5311, 5399 |
| **Crime Type** | Group B Arrest Only |

**Definition**: Unlawful interruption of peace, quiet, or order of a community.

**Arrest Data Only**: Report only when arrest made.

---

### 90D - Driving Under the Influence

| Field | Value |
|-------|-------|
| **NIBRS Code** | 90D |
| **NCIC Codes** | 5403-5404 |
| **Crime Type** | Group B Arrest Only |

**Definition**: Driving or operating any vehicle or common carrier while drunk or under the influence of liquor or drugs.

**Arrest Data Only**: Report only when arrest made.

**Note**: DUI-related fatalities are reported as 09B = Negligent Manslaughter (Group A incident).

---

### 90F - Family Offenses, Nonviolent

| Field | Value |
|-------|-------|
| **NIBRS Code** | 90F |
| **NCIC Codes** | 3801-3803, 3806-3808, 3899 |
| **Crime Type** | Group B Arrest Only |

**Definition**: Unlawful nonviolent acts by a family member (or legal guardian) that threaten the physical, mental, or economic well-being or morals of another family member and that are not classifiable as other offenses.

**Arrest Data Only**: Report only when arrest made.

**Note**: Violent family offenses (assault, etc.) are reported as appropriate Group A offenses.

---

### 90G - Liquor Law Violations

| Field | Value |
|-------|-------|
| **NIBRS Code** | 90G |
| **NCIC Codes** | 4101-4104, 4199 |
| **Crime Type** | Group B Arrest Only |

**Definition**: State or local liquor law violations, except drunkenness and driving under the influence.

**Arrest Data Only**: Report only when arrest made.

**Federal Liquor Offenses**: See 61A (federal/tribal only).

---

### 90J - Trespass of Real Property

| Field | Value |
|-------|-------|
| **NIBRS Code** | 90J |
| **NCIC Codes** | 5707 |
| **Crime Type** | Group B Arrest Only |

**Definition**: To unlawfully enter land, a dwelling, or other real property.

**Arrest Data Only**: Report only when arrest made.

**Note**: Trespass with intent to commit felony/theft = 220 = Burglary (Group A).

---

### 90Z - All Other Offenses

| Field | Value |
|-------|-------|
| **NIBRS Code** | 90Z |
| **NCIC Codes** | Various |
| **Crime Type** | Group B Arrest Only |

**Definition**: All violations of state or local laws not specifically identified as Group A or Group B offenses, except traffic violations.

**Arrest Data Only**: Report only when arrest made.

**Includes**:
- Offenses of General Applicability when substantive offense is Group A:
  - Accessory Before/After the Fact
  - Aiding/Abetting
  - Conspiracy to Commit
  - Enticement
  - Facilitation of
  - Solicitation to Commit
  - Threat to Commit

**If Group B Substantive Offense**: Report in appropriate Group B category.

**Excludes**: Traffic offenses (except DUI, hit-and-run of person, vehicular manslaughter).

---

## Classification Guidelines

### Acting in Concert

**Definition**: All offenders must actually commit or assist in the commission of ALL crimes in an incident.

**Requirements**:
- Offenders aware of and consent to commission of all offenses, OR
- Even if nonconsenting, their actions assist in commission of all offenses

**NIBRS Principle**: All offenders in an incident committed all offenses in the incident.

**Arrest Impact**: Arrest of ANY offender clears ALL offenses in incident.

**If NOT Acting in Concert**: Report as separate incidents.

---

#### Example 1: Acting in Concert (Robbery + Rape)

**Scenario**:
- Bar robbery by two offenders
- One offender rapes victim
- Other offender tells rapist to stop, only rob

**Analysis**:
- One incident, two offenses (Robbery + Rape)
- Although second offender did not consent to rape, displaying gun prevented assistance
- Therefore assisted in commission of rape

**Reporting**: One incident; both offenders connected to victim through Robbery AND Rape.

---

#### Example 2: NOT Acting in Concert (Domestic Violence)

**Scenario**:
- Domestic argument escalates
- Husband beats wife (aggravated assault)
- Wife shoots and kills husband in self-defense

**Analysis**:
- Husband could NOT have been acting in concert in his own killing
- TWO separate incidents required

**Reporting**:
- **Incident 1**: Aggravated assault by husband
- **Incident 2**: Justifiable homicide by wife

---

#### Example 3: NOT Acting in Concert (Robbery + Rape)

**Scenario**:
- Two offenders rob bar at gunpoint
- Take money from register and three customers
- One robber finds female customer in restroom
- Rapes her without other offender's knowledge
- Rapist returns, both leave

**Analysis**:
- Offenders NOT acting in concert in both offenses
- Other offender unaware of rape

**Reporting**:
- **Incident 1**: Robbery (one offense)
- **Incident 2**: Rape (one offense)

---

### Same Time and Place

**Definition**: If same person/group committed more than one crime and time/space intervals separating them were insignificant, all crimes constitute single incident.

**Normally**:
- Offenses during unbroken time period
- At same or adjoining locations

**Exception**: Offenses involving continuing criminal activity by same offenders at different times/places can constitute single incident if LE deems single criminal transaction.

---

#### Example: Same Time and Place (Embezzlement)

**Scenario**:
- Computer programmer systematically embezzled $70,000 over 18 months
- Manipulated bank's computer

**Analysis**:
- Continuing criminal activity against same victim
- Constitutes single incident

**Reporting**: One incident, Embezzlement offense.

---

### Attempted Crimes

**General Rule**: Report attempted crimes same as substantive offense.

**Data Element 7**: Offense Attempted/Completed
- Enter: A = Attempted

**Exception**: Attempted murders are reported as 13A = Aggravated Assault (not 09A).

**Assault Exception**: All assaults are C = Completed (by definition, no attempted assaults exist).

---

### Offenses of General Applicability

**Definition**: When offense includes these words/phrases:
- Accessory Before/After the Fact
- Aiding/Abetting
- Conspiracy to Commit
- Enticement
- Facilitation of
- Solicitation to Commit
- Threat to Commit

**If Group A Substantive Offense**: Report as 90Z = All Other Offenses (Group B arrest).

**If Group B Substantive Offense**: Report in appropriate Group B category.

**Exception**: If component of Group A offense (e.g., Human Trafficking), report as that Group A offense.

---

#### Example 1: Conspiracy (Murder)

**Scenario**:
- Three motorcycle gang members arrested for conspiracy to commit murder

**Reporting**: Three Group B Arrest Reports; UCR Arrest Offense Code = 90Z = All Other Offenses.

---

#### Example 2: Conspiracy (Liquor Tax Evasion)

**Scenario**:
- Five liquor store owners arrested for conspiring to avoid local liquor taxes

**Reporting**: Five Group B Arrest Reports; UCR Arrest Offense Code = 90G = Liquor Law Violations.

---

#### Example 3: Attempted Arson

**Scenario**:
- Two teenagers observed trying to set fire to abandoned building
- Scared away by witness

**Reporting**: Group A Incident Report; UCR Offense Code = 200 = Arson; Offense Attempted/Completed = A = Attempted.

---

### Lesser Included Offenses

**Definition**: Offenses where one offense is an element of another offense.

**Rule**: Cannot report BOTH offenses as having happened to same victim.

**Example**: Robbery includes assault as integral element.
- Report: 120 = Robbery ONLY
- Do NOT also report: 13A = Aggravated Assault

**Exception**: If non-integral offense occurs during incident.
- Example: Robbery + Rape
- Report: BOTH 120 = Robbery AND 11A = Rape
- Rationale: Sexual assault is NOT integral element of robbery

---

### Mutually Exclusive Offenses

**Definition**: Offenses that cannot occur to same victim according to UCR definitions.

**Example**: 09A = Murder and 13A = Aggravated Assault
- Cannot occur to same victim
- If person dies, it's murder (not murder + assault)

**Refer to**: NIBRS Technical Specification, Data Element 24 (Victim Connected to UCR Offense Code) for complete list.

---

### Traffic Offenses (Generally NOT Reported)

**UCR Program Does NOT Collect**:
- Parking violations
- Moving violations

**EXCEPTIONS (DO Report)**:
- 90D = Driving Under the Influence (Group B)
- Hit and Run (of a person) - report as appropriate assault/homicide
- 09B = Negligent Manslaughter (vehicular) (Group A)

---

### State Statute Interpretation

**UCR Principle**: Classify offenses according to NIBRS definitions, NOT state/local codes.

**Example**:
- Some state statutes classify shoplifting as burglary
- UCR: Report as 23C = Shoplifting (larceny)

**Rationale**: Common language transcending varying state laws.

---

### Unusual Situations

**Guidance**:
1. Consider nature of crime
2. Apply guidelines provided in this document
3. Use Offense Lookup Table (Section 5)
4. Contact FBI UCR Program Office if concerns persist

---

## Offense Lookup Quick Reference

### Group A Offenses by NIBRS Code

| Code | Offense | Crime Type |
|------|---------|------------|
| 09A | Murder and Nonnegligent Manslaughter | Person |
| 09B | Negligent Manslaughter | Person |
| 09C | Justifiable Homicide | Not a Crime |
| 100 | Kidnapping/Abduction | Person |
| 11A | Rape | Person |
| 11D | Fondling | Person |
| 120 | Robbery | Property |
| 13A | Aggravated Assault | Person |
| 13B | Simple Assault | Person |
| 13C | Intimidation | Person |
| 200 | Arson | Property |
| 210 | Extortion/Blackmail | Property |
| 220 | Burglary/Breaking & Entering | Property |
| 23A | Pocket-picking | Property |
| 23B | Purse-snatching | Property |
| 23C | Shoplifting | Property |
| 23D | Theft From Building | Property |
| 23E | Theft From Coin-Operated Machine | Property |
| 23F | Theft From Motor Vehicle | Property |
| 23G | Theft of Motor Vehicle Parts/Accessories | Property |
| 23H | All Other Larceny | Property |
| 240 | Motor Vehicle Theft | Property |
| 250 | Counterfeiting/Forgery | Property |
| 26A | False Pretenses/Swindle/Confidence Game | Property |
| 26B | Credit Card/ATM Fraud | Property |
| 26C | Impersonation | Property |
| 26D | Welfare Fraud | Property |
| 26E | Wire Fraud | Property |
| 26F | Identity Theft | Property |
| 26G | Hacking/Computer Invasion | Property |
| 270 | Embezzlement | Property |
| 280 | Stolen Property Offenses | Property |
| 290 | Destruction/Damage/Vandalism | Property |
| 35A | Drug/Narcotic Violations | Society |
| 35B | Drug Equipment Violations | Society |
| 36A | Incest | Person |
| 36B | Statutory Rape | Person |
| 370 | Pornography/Obscene Material | Society |
| 39A | Betting/Wagering | Society |
| 39B | Operating/Promoting/Assisting Gambling | Society |
| 39C | Gambling Equipment Violations | Society |
| 39D | Sports Tampering | Society |
| 40A | Prostitution | Society |
| 40B | Assisting or Promoting Prostitution | Society |
| 40C | Purchasing Prostitution | Society |
| 510 | Bribery | Property |
| 520 | Weapon Law Violations | Society |
| 64A | Human Trafficking, Commercial Sex Acts | Person |
| 64B | Human Trafficking, Involuntary Servitude | Person |
| 720 | Animal Cruelty | Society |

### Group A Federal/Tribal Only Offenses

| Code | Offense | Crime Type |
|------|---------|------------|
| 30A | Illegal Entry into the United States* | Society |
| 30B | False Citizenship* | Society |
| 30C | Smuggling Aliens* | Society |
| 30D | Re-entry after Deportation* | Society |
| 49A | Harboring Escapee/Concealing from Arrest* | Society |
| 49B | Flight to Avoid Prosecution* | Society |
| 49C | Flight to Avoid Deportation* | Society |
| 58A | Import Violations* | Society |
| 58B | Export Violations* | Society |
| 61A | Federal Liquor Offenses* | Society |
| 61B | Federal Tobacco Offenses* | Society |
| 101 | Treason* | Society |
| 103 | Espionage* | Society |
| 26H | Money Laundering* | Society |
| 360 | Failure to Register as a Sex Offender* | Society |
| 521 | Violation of National Firearm Act of 1934* | Society |
| 522 | Weapons of Mass Destruction* | Society |
| 526 | Explosives* | Society |
| 620 | Wildlife Trafficking* | Society |

### Group B Offenses by NIBRS Code

| Code | Offense |
|------|---------|
| 90B | Curfew/Loitering/Vagrancy Violations |
| 90C | Disorderly Conduct |
| 90D | Driving Under the Influence |
| 90F | Family Offenses, Nonviolent |
| 90G | Liquor Law Violations |
| 90J | Trespass of Real Property |
| 90Z | All Other Offenses |

### Group B Federal/Tribal Only Offenses

| Code | Offense |
|------|---------|
| 90K | Failure to Appear (Bond Default)* |
| 90L | Federal Resource Violations* |
| 90M | Perjury* |

---

## Version History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2026-01-16 | Initial creation based on 2023.0 FBI NIBRS User Manual | R. A. Carucci |

---

## References

- FBI NIBRS User Manual 2023.0 (Released 06/30/2023)
- FBI UCR Technical Specifications
- NCIC 2000 Uniform Offense Classifications
- Black's Law Dictionary

---

## Notes for Hackensack PD Implementation

**Integration Points**:
1. **Arrest Analytics**: Validate UCR code assignments against these definitions
2. **Monthly Reports**: Use for crime classification verification
3. **RMS Mapping**: Cross-reference RMS incident types to NIBRS codes
4. **Data Quality**: Authority file for disputed classifications

**Next Steps**:
1. Create JSON version for automated validation
2. Build RMS-to-NIBRS mapping file
3. Integrate into arrest analytics Python script
4. Add to Power BI reference tables

---

**End of Document**
