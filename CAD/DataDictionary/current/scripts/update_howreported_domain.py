"""
Update ArcGIS Field Domain for How Reported
============================================

This script updates the HowReported field domain in an ArcGIS feature class
to match the canonical schema values.

Author: Standards Repository
Date: 2026-02-03
Related: CAD/DataDictionary/current/HOW_REPORTED_FIX_SUMMARY.md

Canonical Values (authoritative source):
    unified_data_dictionary/schemas/canonical_schema.json (line 292)
"""

import arcpy
import sys
from pathlib import Path

# Canonical values for HowReported field
CANONICAL_VALUES = {
    "9-1-1": "Emergency 911 call",
    "Phone": "Non-emergency phone call", 
    "Walk-in": "Walk-in to station",
    "Self-Initiated": "Officer self-initiated",
    "Radio": "Radio dispatch",
    "Other": "Other method"
}

# Legacy values to map to canonical
LEGACY_MAPPING = {
    "eMail": "Other",
    "Mail": "Other",
    "Virtual patrol": "Other",
    "Virtual Patrol": "Other",
    "Cancelled": "Other",
    "Canceled Call": "Other",
    "Fax": "Phone",
    "Teletype": "Phone",
    "Other - See Notes": "Other"
}

def update_domain(workspace_path, domain_name="HowReported_Domain"):
    """
    Update or create the HowReported field domain.
    
    Args:
        workspace_path: Path to the geodatabase
        domain_name: Name of the domain to create/update
    """
    try:
        arcpy.env.workspace = workspace_path
        
        # Delete old domain if it exists
        domains = arcpy.da.ListDomains(workspace_path)
        for domain in domains:
            if domain.name == domain_name:
                print(f"Deleting existing domain: {domain_name}")
                arcpy.management.DeleteDomain(workspace_path, domain_name)
                break
        
        # Create new domain
        print(f"Creating domain: {domain_name}")
        arcpy.management.CreateDomain(
            in_workspace=workspace_path,
            domain_name=domain_name,
            domain_description="Method by which call was reported (canonical values)",
            field_type="TEXT",
            domain_type="CODED"
        )
        
        # Add coded values
        print("Adding coded values to domain:")
        for code, description in CANONICAL_VALUES.items():
            print(f"  - {code}: {description}")
            arcpy.management.AddCodedValueToDomain(
                in_workspace=workspace_path,
                domain_name=domain_name,
                code=code,
                code_description=description
            )
        
        print(f"\n✅ Domain '{domain_name}' created successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error updating domain: {str(e)}")
        return False


def assign_domain_to_field(workspace_path, feature_class, field_name="HowReported", 
                          domain_name="HowReported_Domain"):
    """
    Assign the domain to a specific field in a feature class.
    
    Args:
        workspace_path: Path to the geodatabase
        feature_class: Name of the feature class
        field_name: Name of the field to assign domain to
        domain_name: Name of the domain to assign
    """
    try:
        arcpy.env.workspace = workspace_path
        
        print(f"\nAssigning domain '{domain_name}' to field '{field_name}' in '{feature_class}'...")
        arcpy.management.AssignDomainToField(
            in_table=feature_class,
            field_name=field_name,
            domain_name=domain_name
        )
        
        print(f"✅ Domain assigned successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error assigning domain: {str(e)}")
        return False


def clean_data(workspace_path, feature_class, field_name="HowReported"):
    """
    Clean existing data by mapping legacy values to canonical values.
    
    Args:
        workspace_path: Path to the geodatabase
        feature_class: Name of the feature class
        field_name: Name of the field to clean
    """
    try:
        arcpy.env.workspace = workspace_path
        fc_path = f"{workspace_path}/{feature_class}"
        
        print(f"\nCleaning data in '{feature_class}.{field_name}'...")
        
        # Count records to update
        updates = {}
        with arcpy.da.SearchCursor(fc_path, [field_name]) as cursor:
            for row in cursor:
                old_value = row[0]
                if old_value in LEGACY_MAPPING:
                    new_value = LEGACY_MAPPING[old_value]
                    updates[old_value] = updates.get(old_value, 0) + 1
        
        if not updates:
            print("✅ No legacy values found - data is already clean!")
            return True
        
        print(f"\nFound {sum(updates.values())} records with legacy values:")
        for old_val, count in updates.items():
            print(f"  - '{old_val}': {count} records → '{LEGACY_MAPPING[old_val]}'")
        
        response = input("\nProceed with data cleanup? (yes/no): ")
        if response.lower() not in ['yes', 'y']:
            print("Data cleanup cancelled.")
            return False
        
        # Update records
        update_count = 0
        with arcpy.da.UpdateCursor(fc_path, [field_name]) as cursor:
            for row in cursor:
                old_value = row[0]
                if old_value in LEGACY_MAPPING:
                    row[0] = LEGACY_MAPPING[old_value]
                    cursor.updateRow(row)
                    update_count += 1
        
        print(f"\n✅ Updated {update_count} records successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error cleaning data: {str(e)}")
        return False


def verify_data(workspace_path, feature_class, field_name="HowReported"):
    """
    Verify that all values in the field match canonical values.
    
    Args:
        workspace_path: Path to the geodatabase
        feature_class: Name of the feature class
        field_name: Name of the field to verify
    """
    try:
        arcpy.env.workspace = workspace_path
        fc_path = f"{workspace_path}/{feature_class}"
        
        print(f"\nVerifying data in '{feature_class}.{field_name}'...")
        
        # Get unique values and counts
        value_counts = {}
        invalid_values = {}
        
        with arcpy.da.SearchCursor(fc_path, [field_name]) as cursor:
            for row in cursor:
                value = row[0]
                value_counts[value] = value_counts.get(value, 0) + 1
                
                if value not in CANONICAL_VALUES and value is not None:
                    invalid_values[value] = invalid_values.get(value, 0) + 1
        
        print(f"\nValue Distribution:")
        for value, count in sorted(value_counts.items(), key=lambda x: x[1], reverse=True):
            status = "✅" if value in CANONICAL_VALUES or value is None else "❌"
            print(f"  {status} '{value}': {count} records")
        
        if invalid_values:
            print(f"\n⚠️ WARNING: Found {len(invalid_values)} invalid value(s):")
            for value, count in invalid_values.items():
                print(f"  - '{value}': {count} records")
            return False
        else:
            print(f"\n✅ All values are valid!")
            return True
            
    except Exception as e:
        print(f"❌ Error verifying data: {str(e)}")
        return False


def main():
    """Main execution function."""
    print("=" * 70)
    print("ArcGIS HowReported Field Domain Update")
    print("=" * 70)
    
    # Get parameters
    if len(sys.argv) > 1:
        workspace_path = sys.argv[1]
        feature_class = sys.argv[2] if len(sys.argv) > 2 else None
        field_name = sys.argv[3] if len(sys.argv) > 3 else "HowReported"
    else:
        workspace_path = input("\nEnter geodatabase path: ").strip('"')
        feature_class = input("Enter feature class name (or leave blank to only update domain): ").strip()
        if feature_class:
            field_name = input("Enter field name [HowReported]: ").strip() or "HowReported"
    
    # Validate workspace
    if not arcpy.Exists(workspace_path):
        print(f"❌ Error: Geodatabase not found: {workspace_path}")
        return False
    
    # Step 1: Update domain
    success = update_domain(workspace_path)
    if not success:
        return False
    
    # Step 2: Assign domain to field (if feature class specified)
    if feature_class:
        if not arcpy.Exists(f"{workspace_path}/{feature_class}"):
            print(f"❌ Error: Feature class not found: {feature_class}")
            return False
        
        success = assign_domain_to_field(workspace_path, feature_class, field_name)
        if not success:
            return False
        
        # Step 3: Clean data
        clean_data(workspace_path, feature_class, field_name)
        
        # Step 4: Verify data
        verify_data(workspace_path, feature_class, field_name)
    
    print("\n" + "=" * 70)
    print("✅ Process complete!")
    print("=" * 70)
    print("\nNext steps:")
    print("1. Republish the feature service in ArcGIS Online/Portal")
    print("2. Clear browser cache and refresh the dashboard")
    print("3. Verify dropdown shows only canonical values")
    
    return True


if __name__ == "__main__":
    main()
