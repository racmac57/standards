# CAD Export Data Dictionary (AI Summary)

## Field map and definitions
- ReportNumberNew | source: ReportNumberNew | esri: ReportNumberNew | type: string | desc: CAD report identifier (primary key / join key to RMS Case Number).
- Incident | source: Incident | esri: Incident | type: string | desc: Incident type descriptor (typically a code + description).
- HowReported | source: How Reported | esri: How Reported | type: string | desc: Method by which the call/incident was reported/initiated.
- FullAddress2 | source: FullAddress2 | esri: FullAddress2 | type: string | desc: Full incident location address string.
- PDZone | source: PDZone | esri: PDZone
- Grid | source: Grid | esri: Grid | type: string | desc: CAD grid / map grid identifier.
- TimeOfCall | source: Time of Call | esri: TimeOfCall
- cYear | source: cYear | esri: cYear | type: integer | desc: Calendar year of `TimeofCall` (derived).
- cMonth | source: cMonth | esri: cMonth | type: string | desc: Calendar month of `TimeofCall` (derived).
- Hour | source: HourMinuetsCalc | esri: Hour
- DayofWeek | source: DayofWeek | esri: DayofWeek | type: datetime | desc: Day name for `TimeofCall` (derived).
- TimeDispatched | source: Time Dispatched
- TimeOut | source: Time Out
- TimeIn | source: Time In
- TimeSpent | source: Time Spent
- TimeResponse | source: Time Response
- Officer | source: Officer | esri: Officer | type: string | desc: Officer identifier for the call (primary/assigned officer).
- Disposition | source: Disposition | esri: Disposition | type: string | desc: Disposition / outcome code or label for the CAD call.
- Response_Type | source: Response Type | esri: Response_Type
- CADNotes | source: CADNotes

## Domains
- HowReported canonical: 9-1-1, Phone, Walk-in, Self-Initiated, Radio, Other
- Grid: see cad_domains.json notes
- PDZone: see cad_domains.json notes
- Disposition: see cad_domains.json notes