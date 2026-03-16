# 🕒 2026-01-16-09-30-15
# UCR_NIBRS_Standards/validate_rms_nibrs_mapping.py
# Author: R. A. Carucci
# Purpose: Validate RMS-to-NIBRS offense mappings against actual data and generate comprehensive data quality report

import json
import pandas as pd
from pathlib import Path
from datetime import datetime
from collections import Counter, defaultdict
import re

class RMSNIBRSValidator:
    """Validate and analyze RMS-to-NIBRS offense mappings."""
    
    def __init__(self, rms_mapping_path, nibrs_classification_path):
        """Initialize with mapping files."""
        self.rms_mapping = self._load_json(rms_mapping_path)
        self.nibrs_classification = self._load_json(nibrs_classification_path)
        self.validation_results = {}
        
    def _load_json(self, filepath):
        """Load JSON file."""
        with open(filepath, 'r') as f:
            return json.load(f)
    
    def clean_incident_type(self, incident_type):
        """
        Clean RMS incident type by removing statute codes.
        
        Example: 'THEFT - 2C:20-3' -> 'THEFT'
        """
        if pd.isna(incident_type):
            return None
        
        # Convert to string and strip whitespace
        cleaned = str(incident_type).strip()
        
        # Remove NJ statute codes (pattern: " - 2C:...")
        cleaned = re.split(r'\s*-\s*2C:', cleaned)[0].strip()
        
        # Remove other common statute patterns
        cleaned = re.split(r'\s*-\s*N\.?J\.?S\.?A\.?', cleaned)[0].strip()
        
        return cleaned if cleaned else None
    
    def map_rms_to_nibrs(self, rms_incident_type):
        """
        Map RMS incident type to NIBRS code with confidence and validation info.
        
        Returns dict with mapping status, codes, and validation requirements.
        """
        # Clean the incident type
        cleaned = self.clean_incident_type(rms_incident_type)
        
        if not cleaned:
            return {
                'status': 'invalid',
                'original': rms_incident_type,
                'cleaned': cleaned,
                'message': 'Empty or null incident type'
            }
        
        # Lookup in mapping
        rms_mappings = self.rms_mapping.get('rms_to_nibrs', {})
        
        if cleaned not in rms_mappings:
            return {
                'status': 'unmapped',
                'original': rms_incident_type,
                'cleaned': cleaned,
                'message': 'No mapping found - manual review required',
                'confidence': 0.0
            }
        
        mapping = rms_mappings[cleaned]
        confidence = mapping.get('confidence', 0.0)
        
        # High confidence mapping (>= 0.9) with single code
        if confidence >= 0.9 and mapping.get('nibrs_code'):
            return {
                'status': 'mapped',
                'original': rms_incident_type,
                'cleaned': cleaned,
                'nibrs_code': mapping['nibrs_code'],
                'nibrs_name': mapping['nibrs_name'],
                'confidence': confidence,
                'crime_type': mapping.get('crime_type'),
                'notes': mapping.get('notes', ''),
                'validation_required': []
            }
        
        # Medium/Low confidence - requires validation
        elif confidence >= 0.5:
            return {
                'status': 'review_required',
                'original': rms_incident_type,
                'cleaned': cleaned,
                'possible_codes': mapping.get('possible_codes', []),
                'confidence': confidence,
                'crime_type': mapping.get('crime_type'),
                'validation_required': mapping.get('validation_required', []),
                'classification_logic': mapping.get('classification_logic', ''),
                'notes': mapping.get('notes', '')
            }
        
        # Administrative code or non-crime
        else:
            return {
                'status': 'non_crime',
                'original': rms_incident_type,
                'cleaned': cleaned,
                'confidence': 0.0,
                'notes': mapping.get('notes', ''),
                'classification_logic': mapping.get('classification_logic', ''),
                'message': 'Not a reportable offense'
            }
    
    def validate_dataframe(self, df, incident_type_columns=['Incident Type_1', 'Incident Type_2', 'Incident Type_3']):
        """
        Validate all incident types in a DataFrame.
        
        Args:
            df: DataFrame with RMS data
            incident_type_columns: List of column names containing incident types
            
        Returns:
            DataFrame with validation results added
        """
        print(f"\n🔍 Validating {len(df)} records...")
        
        # Validate each incident type column
        for col in incident_type_columns:
            if col not in df.columns:
                print(f"   ⚠️  Column '{col}' not found, skipping")
                continue
            
            print(f"   📋 Processing {col}...")
            
            # Apply mapping
            df[f'{col}_Mapping'] = df[col].apply(self.map_rms_to_nibrs)
            
            # Extract key fields
            df[f'{col}_Status'] = df[f'{col}_Mapping'].apply(lambda x: x.get('status') if isinstance(x, dict) else None)
            df[f'{col}_NIBRS_Code'] = df[f'{col}_Mapping'].apply(lambda x: x.get('nibrs_code') if isinstance(x, dict) else None)
            df[f'{col}_Confidence'] = df[f'{col}_Mapping'].apply(lambda x: x.get('confidence', 0.0) if isinstance(x, dict) else 0.0)
            df[f'{col}_Crime_Type'] = df[f'{col}_Mapping'].apply(lambda x: x.get('crime_type') if isinstance(x, dict) else None)
        
        return df
    
    def generate_quality_report(self, df, incident_type_columns=['Incident Type_1', 'Incident Type_2', 'Incident Type_3']):
        """
        Generate comprehensive data quality report.
        
        Returns dict with statistics and findings.
        """
        print("\n📊 Generating Data Quality Report...")
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'total_records': len(df),
            'summary': {},
            'by_column': {},
            'unmapped_types': {},
            'confidence_distribution': {},
            'non_crimes': {},
            'recommendations': []
        }
        
        # Analyze each incident type column
        all_statuses = []
        all_confidences = []
        all_unmapped = []
        all_non_crimes = []
        
        for col in incident_type_columns:
            status_col = f'{col}_Status'
            confidence_col = f'{col}_Confidence'
            
            if status_col not in df.columns:
                continue
            
            # Count by status
            status_counts = df[status_col].value_counts().to_dict()
            
            # Get unique unmapped types
            unmapped = df[df[status_col] == 'unmapped'][col].dropna().unique().tolist()
            
            # Get non-crime types
            non_crimes = df[df[status_col] == 'non_crime'][col].dropna().unique().tolist()
            
            # Confidence distribution
            confidence_dist = df[confidence_col].describe().to_dict()
            
            report['by_column'][col] = {
                'status_counts': status_counts,
                'unmapped_types': unmapped,
                'non_crime_types': non_crimes,
                'confidence_stats': confidence_dist
            }
            
            # Aggregate
            all_statuses.extend(df[status_col].dropna().tolist())
            all_confidences.extend(df[confidence_col].dropna().tolist())
            all_unmapped.extend(unmapped)
            all_non_crimes.extend(non_crimes)
        
        # Overall summary
        status_summary = Counter(all_statuses)
        report['summary'] = {
            'mapped': status_summary.get('mapped', 0),
            'review_required': status_summary.get('review_required', 0),
            'unmapped': status_summary.get('unmapped', 0),
            'non_crime': status_summary.get('non_crime', 0),
            'invalid': status_summary.get('invalid', 0)
        }
        
        # Calculate percentages
        total_valid = sum(status_summary.values())
        if total_valid > 0:
            report['summary']['mapped_pct'] = round(status_summary.get('mapped', 0) / total_valid * 100, 1)
            report['summary']['review_required_pct'] = round(status_summary.get('review_required', 0) / total_valid * 100, 1)
            report['summary']['unmapped_pct'] = round(status_summary.get('unmapped', 0) / total_valid * 100, 1)
        
        # Confidence distribution
        if all_confidences:
            conf_series = pd.Series(all_confidences)
            report['confidence_distribution'] = {
                'mean': round(conf_series.mean(), 2),
                'median': round(conf_series.median(), 2),
                'high_confidence_count': len([c for c in all_confidences if c >= 0.9]),
                'medium_confidence_count': len([c for c in all_confidences if 0.7 <= c < 0.9]),
                'low_confidence_count': len([c for c in all_confidences if 0.5 <= c < 0.7]),
                'zero_confidence_count': len([c for c in all_confidences if c == 0])
            }
        
        # Unique unmapped and non-crimes
        report['unmapped_types'] = {
            'count': len(set(all_unmapped)),
            'types': sorted(set(all_unmapped))
        }
        
        report['non_crimes'] = {
            'count': len(set(all_non_crimes)),
            'types': sorted(set(all_non_crimes))
        }
        
        # Generate recommendations
        report['recommendations'] = self._generate_recommendations(report)
        
        return report
    
    def _generate_recommendations(self, report):
        """Generate actionable recommendations based on report findings."""
        recommendations = []
        
        summary = report.get('summary', {})
        unmapped_count = summary.get('unmapped', 0)
        review_count = summary.get('review_required', 0)
        mapped_pct = summary.get('mapped_pct', 0)
        
        # High unmapped rate
        if unmapped_count > 10:
            recommendations.append({
                'priority': 'HIGH',
                'category': 'Unmapped Types',
                'issue': f'Found {unmapped_count} unmapped incident types',
                'action': 'Review unmapped types and add to rms_to_nibrs_offense_map.json',
                'impact': 'Cannot generate NIBRS reports for these incidents'
            })
        
        # High review required rate
        if review_count > 0:
            recommendations.append({
                'priority': 'MEDIUM',
                'category': 'Ambiguous Mappings',
                'issue': f'Found {review_count} incidents requiring manual review',
                'action': 'Create validation workflow for ambiguous incident types',
                'impact': 'Manual classification needed before NIBRS submission'
            })
        
        # Low mapping rate
        if mapped_pct < 60:
            recommendations.append({
                'priority': 'HIGH',
                'category': 'Mapping Coverage',
                'issue': f'Only {mapped_pct}% of incidents auto-mapped',
                'action': 'Improve mapping coverage by adding more RMS incident types',
                'impact': 'High manual effort required for classification'
            })
        
        # Non-crimes being reported
        non_crime_count = summary.get('non_crime', 0)
        if non_crime_count > 0:
            recommendations.append({
                'priority': 'MEDIUM',
                'category': 'Data Quality',
                'issue': f'Found {non_crime_count} administrative codes being processed',
                'action': 'Filter out non-crime codes before NIBRS classification',
                'impact': 'May inflate crime statistics if not excluded'
            })
        
        return recommendations
    
    def print_report(self, report):
        """Print formatted report to console."""
        print("\n" + "="*80)
        print("📊 RMS-TO-NIBRS MAPPING VALIDATION REPORT")
        print("="*80)
        
        print(f"\n🕒 Generated: {report['timestamp']}")
        print(f"📁 Total Records: {report['total_records']:,}")
        
        # Summary
        print("\n" + "─"*80)
        print("📈 SUMMARY STATISTICS")
        print("─"*80)
        summary = report['summary']
        print(f"✅ Mapped (Auto):          {summary.get('mapped', 0):>6,}  ({summary.get('mapped_pct', 0):>5.1f}%)")
        print(f"⚠️  Review Required:       {summary.get('review_required', 0):>6,}  ({summary.get('review_required_pct', 0):>5.1f}%)")
        print(f"❌ Unmapped:              {summary.get('unmapped', 0):>6,}  ({summary.get('unmapped_pct', 0):>5.1f}%)")
        print(f"🚫 Non-Crime:             {summary.get('non_crime', 0):>6,}")
        print(f"⚠️  Invalid:               {summary.get('invalid', 0):>6,}")
        
        # Confidence distribution
        if 'confidence_distribution' in report:
            print("\n" + "─"*80)
            print("🎯 CONFIDENCE DISTRIBUTION")
            print("─"*80)
            conf = report['confidence_distribution']
            print(f"Mean Confidence:          {conf.get('mean', 0):.2f}")
            print(f"Median Confidence:        {conf.get('median', 0):.2f}")
            print(f"High (≥0.9):             {conf.get('high_confidence_count', 0):>6,}")
            print(f"Medium (0.7-0.9):        {conf.get('medium_confidence_count', 0):>6,}")
            print(f"Low (0.5-0.7):           {conf.get('low_confidence_count', 0):>6,}")
            print(f"Zero (Administrative):   {conf.get('zero_confidence_count', 0):>6,}")
        
        # Unmapped types
        if report['unmapped_types']['count'] > 0:
            print("\n" + "─"*80)
            print(f"❌ UNMAPPED INCIDENT TYPES ({report['unmapped_types']['count']})")
            print("─"*80)
            for unmapped_type in report['unmapped_types']['types'][:20]:  # Show first 20
                print(f"   • {unmapped_type}")
            if report['unmapped_types']['count'] > 20:
                print(f"   ... and {report['unmapped_types']['count'] - 20} more")
        
        # Non-crimes
        if report['non_crimes']['count'] > 0:
            print("\n" + "─"*80)
            print(f"🚫 NON-CRIME CODES IDENTIFIED ({report['non_crimes']['count']})")
            print("─"*80)
            for non_crime in report['non_crimes']['types'][:10]:  # Show first 10
                print(f"   • {non_crime}")
        
        # Recommendations
        if report['recommendations']:
            print("\n" + "─"*80)
            print("💡 RECOMMENDATIONS")
            print("─"*80)
            for i, rec in enumerate(report['recommendations'], 1):
                print(f"\n{i}. [{rec['priority']}] {rec['category']}")
                print(f"   Issue:  {rec['issue']}")
                print(f"   Action: {rec['action']}")
                print(f"   Impact: {rec['impact']}")
        
        print("\n" + "="*80 + "\n")
    
    def export_results(self, df, report, output_dir='.'):
        """Export validation results and report to files."""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Export validated dataframe
        csv_path = output_path / f'rms_nibrs_validated_{timestamp}.csv'
        df.to_csv(csv_path, index=False)
        print(f"✅ Validated data: {csv_path}")
        
        # Export report as JSON
        report_path = output_path / f'validation_report_{timestamp}.json'
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        print(f"✅ Report JSON: {report_path}")
        
        # Export unmapped types list
        if report['unmapped_types']['count'] > 0:
            unmapped_path = output_path / f'unmapped_types_{timestamp}.txt'
            with open(unmapped_path, 'w') as f:
                f.write("UNMAPPED RMS INCIDENT TYPES\n")
                f.write("="*80 + "\n\n")
                for unmapped_type in report['unmapped_types']['types']:
                    f.write(f"{unmapped_type}\n")
            print(f"✅ Unmapped types: {unmapped_path}")
        
        # Export recommendations
        if report['recommendations']:
            rec_path = output_path / f'recommendations_{timestamp}.txt'
            with open(rec_path, 'w') as f:
                f.write("RMS-TO-NIBRS MAPPING RECOMMENDATIONS\n")
                f.write("="*80 + "\n\n")
                for i, rec in enumerate(report['recommendations'], 1):
                    f.write(f"{i}. [{rec['priority']}] {rec['category']}\n")
                    f.write(f"   Issue:  {rec['issue']}\n")
                    f.write(f"   Action: {rec['action']}\n")
                    f.write(f"   Impact: {rec['impact']}\n\n")
            print(f"✅ Recommendations: {rec_path}")
        
        return {
            'validated_data': str(csv_path),
            'report': str(report_path),
            'unmapped_types': str(unmapped_path) if report['unmapped_types']['count'] > 0 else None,
            'recommendations': str(rec_path) if report['recommendations'] else None
        }


def main():
    """Main execution function."""
    print("\n" + "="*80)
    print("🚀 RMS-TO-NIBRS MAPPING VALIDATOR")
    print("="*80)
    
    # File paths
    rms_mapping_path = 'rms_to_nibrs_offense_map.json'
    nibrs_classification_path = 'ucr_offense_classification.json'
    
    # Check files exist
    if not Path(rms_mapping_path).exists():
        print(f"❌ Error: {rms_mapping_path} not found")
        return
    
    if not Path(nibrs_classification_path).exists():
        print(f"❌ Error: {nibrs_classification_path} not found")
        return
    
    # Initialize validator
    print(f"\n📂 Loading mapping files...")
    validator = RMSNIBRSValidator(rms_mapping_path, nibrs_classification_path)
    print(f"   ✅ Loaded {len(validator.rms_mapping['rms_to_nibrs'])} RMS mappings")
    print(f"   ✅ Loaded {len(validator.nibrs_classification['group_a_offenses']) + len(validator.nibrs_classification['group_b_offenses'])} NIBRS offenses")
    
    # Example: Test individual mappings
    print("\n" + "─"*80)
    print("🧪 TESTING SAMPLE MAPPINGS")
    print("─"*80)
    
    test_types = [
        "AGGRAVATED ASSAULT",
        "THEFT - 2C:20-3",  # With statute code
        "MOTOR VEHICLE THEFT",
        "THEFT",  # Ambiguous
        "CALLS FOR SERVICE",  # Non-crime
        "UNKNOWN TYPE"  # Unmapped
    ]
    
    for test_type in test_types:
        result = validator.map_rms_to_nibrs(test_type)
        status_icon = {
            'mapped': '✅',
            'review_required': '⚠️',
            'unmapped': '❌',
            'non_crime': '🚫',
            'invalid': '⚠️'
        }.get(result['status'], '❓')
        
        print(f"\n{status_icon} {test_type}")
        print(f"   Status: {result['status'].replace('_', ' ').title()}")
        if result.get('nibrs_code'):
            print(f"   NIBRS:  {result['nibrs_code']} - {result['nibrs_name']}")
            print(f"   Confidence: {result['confidence']:.1f}")
        elif result.get('possible_codes'):
            print(f"   Options: {', '.join(result['possible_codes'])}")
        if result.get('notes'):
            print(f"   Notes:  {result['notes']}")
    
    print("\n" + "="*80)
    print("\n💡 To validate actual RMS data:")
    print("   1. Load your RMS export data into a DataFrame")
    print("   2. Call: validated_df = validator.validate_dataframe(df)")
    print("   3. Call: report = validator.generate_quality_report(validated_df)")
    print("   4. Call: validator.print_report(report)")
    print("   5. Call: validator.export_results(validated_df, report, 'output_folder')")
    print("\n" + "="*80 + "\n")


if __name__ == "__main__":
    main()
