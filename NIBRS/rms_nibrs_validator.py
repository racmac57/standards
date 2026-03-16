# 🕒 2026-01-16-09-30-15
# UCR_NIBRS_Standards/rms_nibrs_validator.py
# Author: R. A. Carucci
# Purpose: Validate RMS incident types against NIBRS mappings and generate data quality reports

import json
import pandas as pd
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple
import re

class RMSNIBRSValidator:
    """Validate RMS incident types against NIBRS offense classifications."""
    
    def __init__(self, rms_mapping_path: str, nibrs_definitions_path: str):
        """Initialize validator with mapping files."""
        print("🔧 Initializing RMS-to-NIBRS Validator...")
        
        # Load mapping files
        with open(rms_mapping_path, 'r') as f:
            self.rms_mapping = json.load(f)
        
        with open(nibrs_definitions_path, 'r') as f:
            self.nibrs_definitions = json.load(f)
        
        print(f"✅ Loaded {len(self.rms_mapping['rms_to_nibrs'])} RMS mappings")
        print(f"✅ Loaded {self.nibrs_definitions['metadata']['total_offenses']} NIBRS definitions")
    
    def clean_incident_type(self, incident_type: str) -> str:
        """Clean RMS incident type by removing statute codes."""
        if pd.isna(incident_type):
            return ""
        
        # Convert to string and strip
        incident_type = str(incident_type).strip()
        
        # Remove NJ statute codes (e.g., " - 2C:20-3")
        incident_type = re.split(r'\s*-\s*2C:', incident_type)[0]
        
        # Remove other common suffixes
        incident_type = incident_type.strip()
        
        return incident_type
    
    def map_rms_to_nibrs(self, rms_incident_type: str) -> Dict:
        """Map single RMS incident type to NIBRS code with validation info."""
        
        # Clean incident type
        cleaned = self.clean_incident_type(rms_incident_type)
        
        if not cleaned:
            return {
                'status': 'empty',
                'rms_type': rms_incident_type,
                'cleaned_type': cleaned,
                'action': 'No incident type provided'
            }
        
        # Check if mapped
        if cleaned not in self.rms_mapping['rms_to_nibrs']:
            return {
                'status': 'unmapped',
                'rms_type': rms_incident_type,
                'cleaned_type': cleaned,
                'nibrs_code': None,
                'confidence': None,
                'action': 'UNMAPPED - Add to mapping file'
            }
        
        mapping = self.rms_mapping['rms_to_nibrs'][cleaned]
        
        # Non-crime (administrative code)
        if mapping['confidence'] == 0.0:
            return {
                'status': 'non_crime',
                'rms_type': rms_incident_type,
                'cleaned_type': cleaned,
                'nibrs_code': None,
                'confidence': 0.0,
                'notes': mapping['notes'],
                'action': 'Exclude from NIBRS reporting'
            }
        
        # High confidence mapping
        if mapping['confidence'] >= 0.9 and mapping.get('nibrs_code'):
            return {
                'status': 'mapped',
                'rms_type': rms_incident_type,
                'cleaned_type': cleaned,
                'nibrs_code': mapping['nibrs_code'],
                'nibrs_name': mapping['nibrs_name'],
                'confidence': mapping['confidence'],
                'crime_type': mapping['crime_type'],
                'action': 'Auto-map approved'
            }
        
        # Medium confidence or ambiguous
        return {
            'status': 'review_required',
            'rms_type': rms_incident_type,
            'cleaned_type': cleaned,
            'nibrs_code': mapping.get('nibrs_code'),
            'possible_codes': mapping.get('possible_codes', []),
            'confidence': mapping['confidence'],
            'validation_required': mapping.get('validation_required', []),
            'classification_logic': mapping.get('classification_logic', ''),
            'action': 'Manual review required'
        }
    
    def validate_dataframe(self, df: pd.DataFrame, 
                          incident_type_cols: List[str] = ['Incident Type_1', 'Incident Type_2', 'Incident Type_3']
                          ) -> pd.DataFrame:
        """Validate all incident types in dataframe."""
        
        print(f"\n📊 Validating {len(df)} records...")
        
        results = []
        
        for idx, row in df.iterrows():
            for col in incident_type_cols:
                if col in df.columns and pd.notna(row[col]) and str(row[col]).strip():
                    incident_type = row[col]
                    mapping_result = self.map_rms_to_nibrs(incident_type)
                    
                    # Add case context
                    result = {
                        'Case_Number': row.get('Case Number', row.get('CaseNumber', idx)),
                        'Incident_Date': row.get('Incident Date', row.get('IncidentDate', '')),
                        'Field_Position': col,
                        **mapping_result
                    }
                    results.append(result)
        
        results_df = pd.DataFrame(results)
        print(f"✅ Validated {len(results_df)} incident type entries")
        
        return results_df
    
    def generate_summary_stats(self, validation_df: pd.DataFrame) -> Dict:
        """Generate summary statistics from validation results."""
        
        total = len(validation_df)
        
        stats = {
            'total_entries': total,
            'by_status': validation_df['status'].value_counts().to_dict(),
            'by_confidence': {},
            'high_confidence_count': len(validation_df[validation_df['confidence'] >= 0.9]),
            'medium_confidence_count': len(validation_df[
                (validation_df['confidence'] >= 0.7) & 
                (validation_df['confidence'] < 0.9)
            ]),
            'low_confidence_count': len(validation_df[
                (validation_df['confidence'] > 0) & 
                (validation_df['confidence'] < 0.7)
            ]),
            'non_crime_count': len(validation_df[validation_df['confidence'] == 0.0]),
            'unmapped_count': len(validation_df[validation_df['status'] == 'unmapped']),
            'auto_mappable_pct': 0,
            'review_required_pct': 0,
            'unmapped_types': [],
            'top_incident_types': {}
        }
        
        # Calculate percentages
        if total > 0:
            stats['auto_mappable_pct'] = round((stats['high_confidence_count'] / total) * 100, 1)
            review_count = stats['medium_confidence_count'] + stats['low_confidence_count']
            stats['review_required_pct'] = round((review_count / total) * 100, 1)
        
        # Get unmapped types
        unmapped = validation_df[validation_df['status'] == 'unmapped']
        if len(unmapped) > 0:
            stats['unmapped_types'] = unmapped['cleaned_type'].unique().tolist()
        
        # Top incident types
        stats['top_incident_types'] = validation_df['cleaned_type'].value_counts().head(10).to_dict()
        
        return stats
    
    def create_review_report(self, validation_df: pd.DataFrame, output_path: str):
        """Create Excel report with separate sheets for different validation statuses."""
        
        print(f"\n📄 Creating validation report: {output_path}")
        
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            
            # Summary sheet
            summary_stats = self.generate_summary_stats(validation_df)
            summary_df = pd.DataFrame([
                {'Metric': 'Total Incident Entries', 'Value': summary_stats['total_entries']},
                {'Metric': 'High Confidence (Auto-Map)', 'Value': summary_stats['high_confidence_count']},
                {'Metric': 'Medium Confidence', 'Value': summary_stats['medium_confidence_count']},
                {'Metric': 'Low Confidence', 'Value': summary_stats['low_confidence_count']},
                {'Metric': 'Non-Crime Codes', 'Value': summary_stats['non_crime_count']},
                {'Metric': 'Unmapped Types', 'Value': summary_stats['unmapped_count']},
                {'Metric': '% Auto-Mappable', 'Value': f"{summary_stats['auto_mappable_pct']}%"},
                {'Metric': '% Requires Review', 'Value': f"{summary_stats['review_required_pct']}%"},
            ])
            summary_df.to_excel(writer, sheet_name='Summary', index=False)
            
            # Auto-mapped (high confidence)
            auto_mapped = validation_df[validation_df['status'] == 'mapped'].copy()
            if len(auto_mapped) > 0:
                auto_mapped_display = auto_mapped[[
                    'Case_Number', 'Incident_Date', 'Field_Position', 
                    'cleaned_type', 'nibrs_code', 'nibrs_name', 'confidence'
                ]].copy()
                auto_mapped_display.to_excel(writer, sheet_name='Auto-Mapped', index=False)
            
            # Review required
            review = validation_df[validation_df['status'] == 'review_required'].copy()
            if len(review) > 0:
                review_display = review[[
                    'Case_Number', 'Incident_Date', 'Field_Position',
                    'cleaned_type', 'possible_codes', 'confidence',
                    'validation_required', 'classification_logic'
                ]].copy()
                review_display.to_excel(writer, sheet_name='Review Required', index=False)
            
            # Unmapped
            unmapped = validation_df[validation_df['status'] == 'unmapped'].copy()
            if len(unmapped) > 0:
                unmapped_display = unmapped[[
                    'Case_Number', 'Incident_Date', 'Field_Position',
                    'cleaned_type', 'action'
                ]].copy()
                unmapped_display.to_excel(writer, sheet_name='Unmapped', index=False)
            
            # Non-crimes
            non_crimes = validation_df[validation_df['status'] == 'non_crime'].copy()
            if len(non_crimes) > 0:
                non_crimes_display = non_crimes[[
                    'Case_Number', 'Incident_Date', 'Field_Position',
                    'cleaned_type', 'notes'
                ]].copy()
                non_crimes_display.to_excel(writer, sheet_name='Non-Crimes', index=False)
            
            # Top incident types
            top_types = pd.DataFrame([
                {'Incident Type': k, 'Count': v} 
                for k, v in summary_stats['top_incident_types'].items()
            ])
            top_types.to_excel(writer, sheet_name='Top Types', index=False)
        
        print(f"✅ Report saved: {output_path}")
        
        return summary_stats
    
    def create_mapping_guide(self, output_path: str):
        """Create user-friendly mapping guide document."""
        
        print(f"\n📖 Creating mapping guide: {output_path}")
        
        guide_content = []
        
        # Header
        guide_content.append("# RMS to NIBRS Offense Mapping Guide")
        guide_content.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        guide_content.append(f"**Version:** {self.rms_mapping['metadata']['version']}")
        guide_content.append("\n---\n")
        
        # Quick reference
        guide_content.append("## Quick Reference\n")
        
        # Group by confidence level
        mappings = self.rms_mapping['rms_to_nibrs']
        
        high_conf = [(k, v) for k, v in mappings.items() if v.get('confidence', 0) >= 0.9 and v.get('nibrs_code')]
        medium_conf = [(k, v) for k, v in mappings.items() if 0.7 <= v.get('confidence', 0) < 0.9]
        low_conf = [(k, v) for k, v in mappings.items() if 0 < v.get('confidence', 0) < 0.7]
        non_crimes = [(k, v) for k, v in mappings.items() if v.get('confidence', 0) == 0]
        
        # High confidence mappings
        guide_content.append("### ✅ High Confidence Mappings (Auto-Map)\n")
        guide_content.append("| RMS Incident Type | NIBRS Code | NIBRS Name | Crime Type |")
        guide_content.append("|-------------------|------------|------------|------------|")
        for rms_type, mapping in sorted(high_conf, key=lambda x: x[0]):
            guide_content.append(
                f"| {rms_type} | {mapping['nibrs_code']} | {mapping['nibrs_name']} | {mapping['crime_type']} |"
            )
        
        # Medium confidence
        guide_content.append("\n### ⚠️ Medium Confidence (Validation Recommended)\n")
        guide_content.append("| RMS Incident Type | NIBRS Code | Confidence | Notes |")
        guide_content.append("|-------------------|------------|------------|-------|")
        for rms_type, mapping in sorted(medium_conf, key=lambda x: x[0]):
            code = mapping.get('nibrs_code', 'Multiple')
            notes = mapping.get('notes', '')[:50]
            guide_content.append(
                f"| {rms_type} | {code} | {mapping['confidence']} | {notes} |"
            )
        
        # Ambiguous
        guide_content.append("\n### 🔴 Ambiguous (Manual Review Required)\n")
        guide_content.append("| RMS Incident Type | Possible NIBRS Codes | Validation Needed |")
        guide_content.append("|-------------------|----------------------|-------------------|")
        for rms_type, mapping in sorted(low_conf, key=lambda x: x[0]):
            codes = ', '.join(mapping.get('possible_codes', ['Multiple']))
            validation = ', '.join(mapping.get('validation_required', [])[:3])
            guide_content.append(
                f"| {rms_type} | {codes} | {validation} |"
            )
        
        # Non-crimes
        guide_content.append("\n### 🚫 Non-Crimes (Do Not Report)\n")
        guide_content.append("| RMS Incident Type | Notes |")
        guide_content.append("|-------------------|-------|")
        for rms_type, mapping in sorted(non_crimes, key=lambda x: x[0]):
            notes = mapping.get('notes', '')[:60]
            guide_content.append(f"| {rms_type} | {notes} |")
        
        # Special notes
        guide_content.append("\n---\n")
        guide_content.append("## Special Classification Notes\n")
        
        special_notes = self.rms_mapping.get('special_classification_notes', {})
        for topic, note in special_notes.items():
            guide_content.append(f"### {topic.replace('_', ' ').title()}")
            guide_content.append(f"{note}\n")
        
        # Save
        with open(output_path, 'w') as f:
            f.write('\n'.join(guide_content))
        
        print(f"✅ Mapping guide saved: {output_path}")


def main():
    """Main execution function."""
    
    print("=" * 70)
    print("🎯 RMS-to-NIBRS Validation System")
    print("=" * 70)
    
    # File paths
    rms_mapping_file = "rms_to_nibrs_offense_map.json"
    nibrs_definitions_file = "ucr_offense_classification.json"
    
    # Initialize validator
    try:
        validator = RMSNIBRSValidator(rms_mapping_file, nibrs_definitions_file)
    except FileNotFoundError as e:
        print(f"❌ Error: Could not find mapping file: {e}")
        print("\nPlease ensure these files are in the current directory:")
        print("  - rms_to_nibrs_offense_map.json")
        print("  - ucr_offense_classification.json")
        return
    
    # Create mapping guide
    print("\n" + "=" * 70)
    print("📖 Step 1: Creating Mapping Reference Guide")
    print("=" * 70)
    validator.create_mapping_guide("RMS_NIBRS_Mapping_Guide.md")
    
    # Demo validation with sample data
    print("\n" + "=" * 70)
    print("🧪 Step 2: Demonstrating Validation with Sample Data")
    print("=" * 70)
    
    # Create sample RMS data
    sample_data = pd.DataFrame([
        {'Case Number': '2024-001', 'Incident Date': '2024-01-15', 'Incident Type_1': 'AGGRAVATED ASSAULT', 'Incident Type_2': None, 'Incident Type_3': None},
        {'Case Number': '2024-002', 'Incident Date': '2024-01-16', 'Incident Type_1': 'THEFT', 'Incident Type_2': None, 'Incident Type_3': None},
        {'Case Number': '2024-003', 'Incident Date': '2024-01-17', 'Incident Type_1': 'MOTOR VEHICLE THEFT', 'Incident Type_2': None, 'Incident Type_3': None},
        {'Case Number': '2024-004', 'Incident Date': '2024-01-18', 'Incident Type_1': 'SHOPLIFTING', 'Incident Type_2': 'SIMPLE ASSAULT', 'Incident Type_3': None},
        {'Case Number': '2024-005', 'Incident Date': '2024-01-19', 'Incident Type_1': 'CALLS FOR SERVICE', 'Incident Type_2': None, 'Incident Type_3': None},
        {'Case Number': '2024-006', 'Incident Date': '2024-01-20', 'Incident Type_1': 'BURGLARY', 'Incident Type_2': None, 'Incident Type_3': None},
        {'Case Number': '2024-007', 'Incident Date': '2024-01-21', 'Incident Type_1': 'FRAUD', 'Incident Type_2': None, 'Incident Type_3': None},
        {'Case Number': '2024-008', 'Incident Date': '2024-01-22', 'Incident Type_1': 'AUTO BURGLARY', 'Incident Type_2': None, 'Incident Type_3': None},
        {'Case Number': '2024-009', 'Incident Date': '2024-01-23', 'Incident Type_1': 'ROBBERY', 'Incident Type_2': None, 'Incident Type_3': None},
        {'Case Number': '2024-010', 'Incident Date': '2024-01-24', 'Incident Type_1': 'UNKNOWN INCIDENT', 'Incident Type_2': None, 'Incident Type_3': None},
    ])
    
    print("\nSample RMS Data:")
    print(sample_data[['Case Number', 'Incident Type_1']].to_string(index=False))
    
    # Validate sample data
    validation_results = validator.validate_dataframe(sample_data)
    
    # Create report
    print("\n" + "=" * 70)
    print("📊 Step 3: Generating Validation Report")
    print("=" * 70)
    
    summary_stats = validator.create_review_report(
        validation_results, 
        "RMS_NIBRS_Validation_Report.xlsx"
    )
    
    # Print summary
    print("\n" + "=" * 70)
    print("📈 VALIDATION SUMMARY")
    print("=" * 70)
    print(f"Total Incident Entries:     {summary_stats['total_entries']}")
    print(f"✅ High Confidence (Auto):  {summary_stats['high_confidence_count']} ({summary_stats['auto_mappable_pct']}%)")
    print(f"⚠️  Medium Confidence:       {summary_stats['medium_confidence_count']}")
    print(f"🔴 Low Confidence:          {summary_stats['low_confidence_count']}")
    print(f"🚫 Non-Crime Codes:         {summary_stats['non_crime_count']}")
    print(f"❓ Unmapped Types:          {summary_stats['unmapped_count']}")
    
    if summary_stats['unmapped_types']:
        print(f"\n⚠️  Found {len(summary_stats['unmapped_types'])} unmapped incident types:")
        for utype in summary_stats['unmapped_types'][:5]:
            print(f"   - {utype}")
        if len(summary_stats['unmapped_types']) > 5:
            print(f"   ... and {len(summary_stats['unmapped_types']) - 5} more")
    
    print("\n" + "=" * 70)
    print("✅ VALIDATION COMPLETE")
    print("=" * 70)
    print("\nGenerated Files:")
    print("  📖 RMS_NIBRS_Mapping_Guide.md - User-friendly mapping reference")
    print("  📊 RMS_NIBRS_Validation_Report.xlsx - Detailed validation results")
    print("\nNext Steps:")
    print("  1. Review 'Review Required' sheet for ambiguous mappings")
    print("  2. Add unmapped types to rms_to_nibrs_offense_map.json")
    print("  3. Integrate validator into your RMS data processing pipeline")
    print("  4. Use mapping guide for manual classification decisions")
    print("=" * 70)


if __name__ == "__main__":
    main()
