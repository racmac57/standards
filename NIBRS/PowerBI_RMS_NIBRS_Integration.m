// 🕒 2026-01-16-09-45-30
// UCR_NIBRS_Standards/PowerBI_RMS_NIBRS_Integration.m
// Author: R. A. Carucci
// Purpose: Power BI M-code queries for RMS-to-NIBRS mapping integration and validation

// ================================================================================
// QUERY 1: Load RMS-to-NIBRS Mapping from JSON
// ================================================================================
let
    // Load the JSON mapping file
    Source = Json.Document(File.Contents("rms_to_nibrs_offense_map.json")),
    
    // Extract the rms_to_nibrs mappings
    RMSMappings = Source[rms_to_nibrs],
    
    // Convert to table
    MappingsTable = Record.ToTable(RMSMappings),
    
    // Expand the mapping details
    ExpandedRecords = Table.ExpandRecordColumn(
        MappingsTable, 
        "Value", 
        {
            "nibrs_code", 
            "nibrs_name", 
            "confidence", 
            "crime_type", 
            "notes", 
            "validation_required", 
            "possible_codes",
            "classification_logic"
        }
    ),
    
    // Rename columns for clarity
    RenamedColumns = Table.RenameColumns(
        ExpandedRecords,
        {
            {"Name", "RMS_Incident_Type"},
            {"nibrs_code", "NIBRS_Code"},
            {"nibrs_name", "NIBRS_Name"},
            {"confidence", "Confidence"},
            {"crime_type", "Crime_Type"},
            {"notes", "Mapping_Notes"},
            {"validation_required", "Validation_Required"},
            {"possible_codes", "Possible_Codes"},
            {"classification_logic", "Classification_Logic"}
        }
    ),
    
    // Add mapping status based on confidence
    AddMappingStatus = Table.AddColumn(
        RenamedColumns, 
        "Mapping_Status", 
        each 
            if [Confidence] >= 0.9 and [NIBRS_Code] <> null then "Auto-Map"
            else if [Confidence] >= 0.7 then "Review Required"
            else if [Confidence] > 0 then "Manual Review"
            else "Non-Crime"
    ),
    
    // Add confidence category
    AddConfidenceCategory = Table.AddColumn(
        AddMappingStatus,
        "Confidence_Category",
        each 
            if [Confidence] >= 0.9 then "High"
            else if [Confidence] >= 0.7 then "Medium"
            else if [Confidence] > 0 then "Low"
            else "Zero"
    ),
    
    // Set data types
    TypedTable = Table.TransformColumnTypes(
        AddConfidenceCategory,
        {
            {"RMS_Incident_Type", type text},
            {"NIBRS_Code", type text},
            {"NIBRS_Name", type text},
            {"Confidence", type number},
            {"Crime_Type", type text},
            {"Mapping_Notes", type text},
            {"Mapping_Status", type text},
            {"Confidence_Category", type text}
        }
    )
in
    TypedTable


// ================================================================================
// QUERY 2: Load NIBRS Offense Definitions from JSON
// ================================================================================
let
    Source = Json.Document(File.Contents("ucr_offense_classification.json")),
    
    // Combine Group A and Group B offenses
    GroupA = Source[group_a_offenses],
    GroupB = Source[group_b_offenses],
    
    // Convert Group A to table
    GroupATable = Record.ToTable(GroupA),
    GroupAExpanded = Table.ExpandRecordColumn(
        GroupATable,
        "Value",
        {"offense_name", "category", "crime_type", "definition", "ncic_codes", "federal_tribal_only"},
        {"Offense_Name", "Category", "Crime_Type", "Definition", "NCIC_Codes", "Federal_Tribal_Only"}
    ),
    GroupAWithGroup = Table.AddColumn(GroupAExpanded, "Offense_Group", each "Group A"),
    
    // Convert Group B to table
    GroupBTable = Record.ToTable(GroupB),
    GroupBExpanded = Table.ExpandRecordColumn(
        GroupBTable,
        "Value",
        {"offense_name", "crime_type", "definition", "ncic_codes"},
        {"Offense_Name", "Crime_Type", "Definition", "NCIC_Codes"}
    ),
    GroupBWithCategory = Table.AddColumn(GroupBExpanded, "Category", each null),
    GroupBWithFederal = Table.AddColumn(GroupBWithCategory, "Federal_Tribal_Only", each false),
    GroupBWithGroup = Table.AddColumn(GroupBWithFederal, "Offense_Group", each "Group B"),
    
    // Combine both groups
    CombinedOffenses = Table.Combine({GroupAWithGroup, GroupBWithGroup}),
    
    // Rename code column
    RenamedColumns = Table.RenameColumns(CombinedOffenses, {{"Name", "NIBRS_Code"}}),
    
    // Set data types
    TypedTable = Table.TransformColumnTypes(
        RenamedColumns,
        {
            {"NIBRS_Code", type text},
            {"Offense_Name", type text},
            {"Category", type text},
            {"Crime_Type", type text},
            {"Definition", type text},
            {"Federal_Tribal_Only", type logical},
            {"Offense_Group", type text}
        }
    )
in
    TypedTable


// ================================================================================
// QUERY 3: Clean RMS Incident Types (Function)
// ================================================================================
let
    // Function to clean RMS incident types by removing statute codes
    CleanIncidentType = (incidentType as nullable text) as nullable text =>
        let
            // Handle null values
            Result = if incidentType = null then null
            else
                let
                    // Trim whitespace
                    Trimmed = Text.Trim(incidentType),
                    
                    // Remove NJ statute codes (pattern: " - 2C:...")
                    WithoutStatute = 
                        if Text.Contains(Trimmed, " - 2C:") then
                            Text.BeforeDelimiter(Trimmed, " - 2C:", 0)
                        else if Text.Contains(Trimmed, " - N.J.S.A.") then
                            Text.BeforeDelimiter(Trimmed, " - N.J.S.A.", 0)
                        else
                            Trimmed,
                    
                    // Final trim
                    Cleaned = Text.Trim(WithoutStatute)
                in
                    if Cleaned = "" then null else Cleaned
        in
            Result
in
    CleanIncidentType


// ================================================================================
// QUERY 4: Apply RMS-to-NIBRS Mapping to Your Data
// ================================================================================
let
    // Load your RMS data (adjust source as needed)
    Source = Excel.Workbook(File.Contents("YOUR_RMS_FILE.xlsx"), null, true),
    YourData = Source{[Item="Sheet1",Kind="Sheet"]}[Data],
    PromotedHeaders = Table.PromoteHeaders(YourData, [PromoteAllScalars=true]),
    
    // Clean Incident Type fields
    CleanIncidentType1 = Table.AddColumn(
        PromotedHeaders,
        "Incident_Type_1_Clean",
        each CleanIncidentType([#"Incident Type_1"])
    ),
    CleanIncidentType2 = Table.AddColumn(
        CleanIncidentType1,
        "Incident_Type_2_Clean",
        each CleanIncidentType([#"Incident Type_2"])
    ),
    CleanIncidentType3 = Table.AddColumn(
        CleanIncidentType2,
        "Incident_Type_3_Clean",
        each CleanIncidentType([#"Incident Type_3"])
    ),
    
    // Merge with RMS-to-NIBRS mapping for Type 1
    MergeMapping1 = Table.NestedJoin(
        CleanIncidentType3,
        {"Incident_Type_1_Clean"},
        #"RMS_NIBRS_Mapping",
        {"RMS_Incident_Type"},
        "Mapping1",
        JoinKind.LeftOuter
    ),
    ExpandMapping1 = Table.ExpandTableColumn(
        MergeMapping1,
        "Mapping1",
        {"NIBRS_Code", "NIBRS_Name", "Confidence", "Crime_Type", "Mapping_Status"},
        {"Type1_NIBRS_Code", "Type1_NIBRS_Name", "Type1_Confidence", "Type1_Crime_Type", "Type1_Status"}
    ),
    
    // Merge with RMS-to-NIBRS mapping for Type 2
    MergeMapping2 = Table.NestedJoin(
        ExpandMapping1,
        {"Incident_Type_2_Clean"},
        #"RMS_NIBRS_Mapping",
        {"RMS_Incident_Type"},
        "Mapping2",
        JoinKind.LeftOuter
    ),
    ExpandMapping2 = Table.ExpandTableColumn(
        MergeMapping2,
        "Mapping2",
        {"NIBRS_Code", "NIBRS_Name", "Confidence", "Crime_Type", "Mapping_Status"},
        {"Type2_NIBRS_Code", "Type2_NIBRS_Name", "Type2_Confidence", "Type2_Crime_Type", "Type2_Status"}
    ),
    
    // Merge with RMS-to-NIBRS mapping for Type 3
    MergeMapping3 = Table.NestedJoin(
        ExpandMapping2,
        {"Incident_Type_3_Clean"},
        #"RMS_NIBRS_Mapping",
        {"RMS_Incident_Type"},
        "Mapping3",
        JoinKind.LeftOuter
    ),
    ExpandMapping3 = Table.ExpandTableColumn(
        MergeMapping3,
        "Mapping3",
        {"NIBRS_Code", "NIBRS_Name", "Confidence", "Crime_Type", "Mapping_Status"},
        {"Type3_NIBRS_Code", "Type3_NIBRS_Name", "Type3_Confidence", "Type3_Crime_Type", "Type3_Status"}
    ),
    
    // Add validation flag
    AddValidationFlag = Table.AddColumn(
        ExpandMapping3,
        "Requires_Validation",
        each 
            [Type1_Status] = "Review Required" or 
            [Type1_Status] = "Manual Review" or
            [Type2_Status] = "Review Required" or
            [Type2_Status] = "Manual Review" or
            [Type3_Status] = "Review Required" or
            [Type3_Status] = "Manual Review"
    )
in
    AddValidationFlag


// ================================================================================
// QUERY 5: Validation Dashboard Summary
// ================================================================================
let
    // Reference the mapped data
    Source = #"RMS_Data_with_NIBRS_Mapping",
    
    // Create summary of mapping results
    SummaryMetrics = [
        Total_Records = Table.RowCount(Source),
        
        // Type 1 statistics
        Type1_Mapped = Table.RowCount(Table.SelectRows(Source, each [Type1_Status] = "Auto-Map")),
        Type1_Review = Table.RowCount(Table.SelectRows(Source, each [Type1_Status] = "Review Required")),
        Type1_Manual = Table.RowCount(Table.SelectRows(Source, each [Type1_Status] = "Manual Review")),
        Type1_NonCrime = Table.RowCount(Table.SelectRows(Source, each [Type1_Status] = "Non-Crime")),
        Type1_Unmapped = Table.RowCount(Table.SelectRows(Source, each [Type1_Status] = null)),
        
        // Overall validation needed
        Total_Requires_Validation = Table.RowCount(Table.SelectRows(Source, each [Requires_Validation] = true)),
        
        // Confidence statistics
        Avg_Type1_Confidence = List.Average(Table.SelectRows(Source, each [Type1_Confidence] <> null)[Type1_Confidence]),
        High_Confidence_Count = Table.RowCount(Table.SelectRows(Source, each [Type1_Confidence] >= 0.9)),
        Medium_Confidence_Count = Table.RowCount(Table.SelectRows(Source, each [Type1_Confidence] >= 0.7 and [Type1_Confidence] < 0.9)),
        Low_Confidence_Count = Table.RowCount(Table.SelectRows(Source, each [Type1_Confidence] > 0 and [Type1_Confidence] < 0.7))
    ],
    
    // Convert to table
    SummaryTable = Record.ToTable(SummaryMetrics)
in
    SummaryTable


// ================================================================================
// DAX MEASURES FOR POWER BI VISUALS
// ================================================================================

// Measure: Total Mapped Incidents
Total Mapped = 
COUNTROWS(
    FILTER(
        'RMS_Data_with_NIBRS_Mapping',
        'RMS_Data_with_NIBRS_Mapping'[Type1_Status] = "Auto-Map"
    )
)

// Measure: Requires Validation Count
Requires Validation = 
COUNTROWS(
    FILTER(
        'RMS_Data_with_NIBRS_Mapping',
        'RMS_Data_with_NIBRS_Mapping'[Requires_Validation] = TRUE()
    )
)

// Measure: Mapping Success Rate
Mapping Success Rate = 
DIVIDE(
    [Total Mapped],
    COUNTROWS('RMS_Data_with_NIBRS_Mapping'),
    0
) * 100

// Measure: Average Confidence
Average Confidence = 
AVERAGEX(
    FILTER(
        'RMS_Data_with_NIBRS_Mapping',
        NOT(ISBLANK('RMS_Data_with_NIBRS_Mapping'[Type1_Confidence]))
    ),
    'RMS_Data_with_NIBRS_Mapping'[Type1_Confidence]
)

// Measure: High Confidence Count
High Confidence Count = 
COUNTROWS(
    FILTER(
        'RMS_Data_with_NIBRS_Mapping',
        'RMS_Data_with_NIBRS_Mapping'[Type1_Confidence] >= 0.9
    )
)

// Measure: Crime Type Distribution
Crime Type Counts = 
CALCULATE(
    COUNTROWS('RMS_Data_with_NIBRS_Mapping'),
    ALLEXCEPT(
        'RMS_Data_with_NIBRS_Mapping',
        'RMS_Data_with_NIBRS_Mapping'[Type1_Crime_Type]
    )
)

// Measure: Validation Status Color
Validation Status Color = 
VAR Status = SELECTEDVALUE('RMS_Data_with_NIBRS_Mapping'[Type1_Status])
RETURN
    SWITCH(
        Status,
        "Auto-Map", "#00B050",        // Green
        "Review Required", "#FFC000",  // Yellow
        "Manual Review", "#FF0000",    // Red
        "Non-Crime", "#808080",        // Gray
        "#C0C0C0"                      // Light gray for unmapped
    )

// Measure: NIBRS Submission Ready
NIBRS Submission Ready = 
VAR ReadyRecords = 
    COUNTROWS(
        FILTER(
            'RMS_Data_with_NIBRS_Mapping',
            'RMS_Data_with_NIBRS_Mapping'[Type1_Status] = "Auto-Map" &&
            NOT(ISBLANK('RMS_Data_with_NIBRS_Mapping'[Type1_NIBRS_Code]))
        )
    )
VAR TotalRecords = COUNTROWS('RMS_Data_with_NIBRS_Mapping')
RETURN
    FORMAT(
        DIVIDE(ReadyRecords, TotalRecords, 0),
        "0.0%"
    )


// ================================================================================
// IMPLEMENTATION NOTES
// ================================================================================

/*
SETUP INSTRUCTIONS:

1. Save both JSON files in an accessible location
2. Update file paths in Query 1 and Query 2
3. Import all queries into Power BI
4. Update Query 4 to point to your actual RMS data source
5. Create relationships:
   - RMS_NIBRS_Mapping[NIBRS_Code] → NIBRS_Definitions[NIBRS_Code]
6. Add DAX measures to your data model
7. Create visuals using the validation status fields

RECOMMENDED VISUALS:

1. Card: Total Mapped, Requires Validation, Mapping Success Rate
2. Donut Chart: Distribution by Mapping_Status (with Status Color measure)
3. Bar Chart: Top 10 RMS Incident Types by frequency
4. Table: Records requiring validation (filter: Requires_Validation = TRUE)
5. Gauge: NIBRS Submission Ready percentage
6. Matrix: Incident Type vs NIBRS Code with counts

DATA QUALITY CHECKS:

- Filter to Mapping_Status = null to find unmapped types
- Filter to Confidence < 0.7 to review ambiguous mappings
- Check Type1_Status = "Non-Crime" to exclude from NIBRS
- Validate all incidents before NIBRS submission

*/
