"""
Clean and Normalize How Reported Values in CAD ESRI Polished Data
==================================================================

This script cleans the How Reported field in the ESRI Polished baseline data
to match canonical schema values.

Author: Standards Repository
Date: 2026-02-03
"""

import pandas as pd
import numpy as np
import re
from pathlib import Path
from datetime import datetime

# Canonical values (authoritative)
CANONICAL_VALUES = ['9-1-1', 'Phone', 'Walk-in', 'Self-Initiated', 'Radio', 'Other']

# Comprehensive mapping of all observed invalid values
VALUE_MAPPING = {
    # 911 variations
    '911': '9-1-1',
    '9-1-1': '9-1-1',  # Keep as-is
    '9155': '9-1-1',
    'Phone/911': '9-1-1',
    
    # Phone variations
    'phone': 'Phone',
    'Phone': 'Phone',  # Keep as-is
    'PHONE': 'Phone',
    'Fax': 'Phone',
    'Teletype': 'Phone',
    'ppp': 'Phone',  # Likely data entry error
    
    # Walk-in variations
    'Walk-In': 'Walk-in',
    'Walk-in': 'Walk-in',  # Keep as-is
    'WALK-IN': 'Walk-in',
    'walkin': 'Walk-in',
    
    # Self-Initiated variations
    'Self-Initiated': 'Self-Initiated',  # Keep as-is
    'SELF-INITIATED': 'Self-Initiated',
    'Self Initiated': 'Self-Initiated',
    'self-initiated': 'Self-Initiated',
    
    # Radio variations  
    'Radio': 'Radio',  # Keep as-is
    'RADIO': 'Radio',
    'r': 'Radio',  # Likely abbreviation
    
    # Other variations
    'Other': 'Other',  # Keep as-is
    'OTHER': 'Other',
    'Other - See Notes': 'Other',
    'eMail': 'Other',
    'Mail': 'Other',
    'Virtual patrol': 'Other',
    'Virtual Patrol': 'Other',
    'Cancelled': 'Other',
    'Canceled Call': 'Other',
    
    # Data quality issues (appear to be data entry errors)
    'u': 'Other',
    'y789': 'Other',
    '0': 'Other',
    'pLito': 'Other',
    'hackensack': 'Other',
    'mv': 'Other',
}


def normalize_how_reported(value):
    """
    Normalize a How Reported value to canonical form.
    
    Args:
        value: Raw value from data
        
    Returns:
        Normalized canonical value
    """
    if pd.isna(value):
        return 'Other'  # Default for missing values
    
    # Convert to string and strip whitespace
    value_str = str(value).strip()
    
    # Direct mapping
    if value_str in VALUE_MAPPING:
        return VALUE_MAPPING[value_str]
    
    # Case-insensitive check for known values
    value_lower = value_str.lower()
    for key, canonical in VALUE_MAPPING.items():
        if key.lower() == value_lower:
            return canonical
    
    # Pattern matching for common variations
    
    # 911 patterns
    if re.match(r'^9[-./ ]?1[-./ ]?1$', value_str, re.IGNORECASE):
        return '9-1-1'
    
    # Check if it contains "911" anywhere
    if '911' in value_str.lower():
        return '9-1-1'
    
    # Phone patterns
    if 'phone' in value_lower or 'fax' in value_lower or 'tele' in value_lower:
        return 'Phone'
    
    # Walk-in patterns
    if 'walk' in value_lower:
        return 'Walk-in'
    
    # Self-initiated patterns
    if 'self' in value_lower or 'initiated' in value_lower:
        return 'Self-Initiated'
    
    # Radio patterns
    if 'radio' in value_lower:
        return 'Radio'
    
    # If we still don't have a match, default to Other
    print(f"⚠️ Unknown value: '{value_str}' -> mapping to 'Other'")
    return 'Other'


def clean_excel_file(input_path, output_path=None, backup=True):
    """
    Clean How Reported values in an Excel file.
    
    Args:
        input_path: Path to input Excel file
        output_path: Path to output file (if None, overwrites input)
        backup: Whether to create backup of original file
    """
    input_path = Path(input_path)
    
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")
    
    print("=" * 70)
    print("CAD How Reported Data Cleaning")
    print("=" * 70)
    print(f"\nInput file: {input_path}")
    print(f"File size: {input_path.stat().st_size / 1024 / 1024:.2f} MB")
    
    # Create backup if requested
    if backup:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = input_path.parent / f"{input_path.stem}_backup_{timestamp}{input_path.suffix}"
        print(f"\nCreating backup: {backup_path.name}")
        import shutil
        shutil.copy2(input_path, backup_path)
    
    # Load data
    print("\nLoading Excel file (this may take a minute)...")
    df = pd.read_excel(input_path)
    print(f"✅ Loaded {len(df):,} records")
    
    # Find How Reported column
    how_reported_col = None
    for col in df.columns:
        if 'how' in col.lower() and 'report' in col.lower():
            how_reported_col = col
            break
    
    if not how_reported_col:
        raise ValueError("Could not find 'How Reported' column in data!")
    
    print(f"\nFound column: '{how_reported_col}'")
    
    # Analyze current values
    print(f"\n{'='*70}")
    print("BEFORE CLEANING")
    print("=" * 70)
    print(f"\nUnique values: {df[how_reported_col].nunique()}")
    print("\nValue counts:")
    print(df[how_reported_col].value_counts().head(20))
    
    # Count invalid values
    valid_mask = df[how_reported_col].isin(CANONICAL_VALUES)
    invalid_count = (~valid_mask & df[how_reported_col].notna()).sum()
    print(f"\n⚠️ Records with invalid values: {invalid_count:,} ({invalid_count/len(df)*100:.2f}%)")
    
    if invalid_count > 0:
        print("\nTop invalid values:")
        invalid_values = df[~valid_mask & df[how_reported_col].notna()][how_reported_col]
        print(invalid_values.value_counts().head(20))
    
    # Apply cleaning
    print(f"\n{'='*70}")
    print("CLEANING DATA")
    print("=" * 70)
    
    original_values = df[how_reported_col].copy()
    df[how_reported_col] = df[how_reported_col].apply(normalize_how_reported)
    
    # Count changes
    changes = (original_values != df[how_reported_col]) & original_values.notna()
    change_count = changes.sum()
    
    print(f"\n✅ Cleaned {change_count:,} values")
    
    if change_count > 0:
        print("\nMost common transformations:")
        changes_df = pd.DataFrame({
            'Original': original_values[changes],
            'Cleaned': df[how_reported_col][changes]
        })
        print(changes_df.value_counts().head(20))
    
    # Analyze cleaned values
    print(f"\n{'='*70}")
    print("AFTER CLEANING")
    print("=" * 70)
    print(f"\nUnique values: {df[how_reported_col].nunique()}")
    print("\nValue counts:")
    print(df[how_reported_col].value_counts())
    
    # Verify all values are valid
    still_invalid = ~df[how_reported_col].isin(CANONICAL_VALUES)
    if still_invalid.any():
        print(f"\n⚠️ WARNING: {still_invalid.sum()} records still have invalid values!")
        print(df[still_invalid][how_reported_col].value_counts())
    else:
        print("\n✅ All values are now valid!")
    
    # Save cleaned data
    if output_path is None:
        output_path = input_path
    else:
        output_path = Path(output_path)
    
    print(f"\n{'='*70}")
    print("SAVING")
    print("=" * 70)
    print(f"\nSaving to: {output_path}")
    
    df.to_excel(output_path, index=False)
    
    print(f"✅ File saved successfully!")
    print(f"\nOutput file size: {output_path.stat().st_size / 1024 / 1024:.2f} MB")
    
    # Generate report
    report_path = output_path.parent / f"{output_path.stem}_cleaning_report.txt"
    with open(report_path, 'w') as f:
        f.write("How Reported Data Cleaning Report\n")
        f.write("=" * 70 + "\n")
        f.write(f"Date: {datetime.now()}\n")
        f.write(f"Input file: {input_path}\n")
        f.write(f"Output file: {output_path}\n")
        f.write(f"\nTotal records: {len(df):,}\n")
        f.write(f"Values cleaned: {change_count:,} ({change_count/len(df)*100:.2f}%)\n")
        f.write(f"\nFinal value distribution:\n")
        f.write(df[how_reported_col].value_counts().to_string())
    
    print(f"\n📄 Report saved: {report_path.name}")
    
    return df, change_count


def main():
    """Main execution."""
    import sys
    
    # Get file path
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        output_file = sys.argv[2] if len(sys.argv) > 2 else None
    else:
        input_file = r'C:\Users\carucci_r\OneDrive - City of Hackensack\13_PROCESSED_DATA\ESRI_Polished\base\CAD_ESRI_Polished_Baseline.xlsx'
        output_file = None
    
    try:
        df, changes = clean_excel_file(input_file, output_file, backup=True)
        
        print("\n" + "=" * 70)
        print("✅ CLEANING COMPLETE!")
        print("=" * 70)
        print("\nNext steps:")
        print("1. Review the cleaning report")
        print("2. Upload the cleaned file to ArcGIS")
        print("3. Republish the feature service")
        print("4. Update the field domain (see update_howreported_domain.py)")
        print("5. Verify the dashboard shows only canonical values")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    main()
