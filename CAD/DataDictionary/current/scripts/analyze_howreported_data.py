import pandas as pd
import sys

print("Loading Excel file...")
df = pd.read_excel(r'C:\Users\carucci_r\OneDrive - City of Hackensack\13_PROCESSED_DATA\ESRI_Polished\base\CAD_ESRI_Polished_Baseline.xlsx')

print(f"Total records: {len(df)}")
print(f"\nColumns: {df.columns.tolist()}")

# Find How Reported column
col = None
for c in df.columns:
    if 'how' in c.lower() and 'report' in c.lower():
        col = c
        break

if col:
    print(f"\nFound column: '{col}'")
    print(f"\nUnique values ({df[col].nunique()}):")
    print(df[col].value_counts().to_string())
    
    # Check for invalid values
    valid_values = ['9-1-1', 'Phone', 'Walk-in', 'Self-Initiated', 'Radio', 'Other']
    invalid = df[~df[col].isin(valid_values) & df[col].notna()]
    
    if len(invalid) > 0:
        print(f"\n⚠️ WARNING: {len(invalid)} records with invalid values!")
        print("\nInvalid value counts:")
        print(invalid[col].value_counts().to_string())
else:
    print("Could not find How Reported column!")
    print("Available columns:", df.columns.tolist())
