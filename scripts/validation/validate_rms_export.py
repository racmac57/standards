#!/usr/bin/env python3
"""
RMS Export Validator v1.0
Validates RMS export CSV files against field definitions from rms_export_field_definitions.md

Usage:
    python validate_rms_export.py input_file.csv [output_report.html]

Features:
    - Format validation (regex patterns, data types)
    - Required field checks
    - Cross-field validation (date logic, value constraints)
    - Controlled vocabulary checks
    - Detailed HTML report generation
"""

import csv
import re
import sys
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import pandas as pd
from pathlib import Path


class RMSFieldValidator:
    """Validator for RMS export fields based on comprehensive field definitions."""

    def __init__(self):
        self.validation_results = []
        self.error_count = 0
        self.warning_count = 0
        self.record_count = 0

        # Define validation rules from rms_export_field_definitions.md
        self.field_rules = {
            'CaseNumber': {
                'required': True,
                'type': 'text',
                'regex': r'^\d{2}-\d{6}([A-Z])?$',
                'example': '25-000001'
            },
            'IncidentDate': {
                'required': False,
                'type': 'date',
                'formats': ['%m/%d/%Y', '%Y-%m-%d'],
                'timezone': 'America/New_York'
            },
            'IncidentTime': {
                'required': False,
                'type': 'time',
                'formats': ['%H:%M', '%H:%M:%S']
            },
            'ReportDate': {
                'required': False,
                'type': 'date',
                'formats': ['%m/%d/%Y', '%Y-%m-%d']
            },
            'Zone': {
                'required': False,
                'type': 'integer',
                'valid_range': (5, 9)
            },
            'TotalValueStolen': {
                'required': False,
                'type': 'currency',
                'min_value': 0
            },
            'TotalValueRecover': {
                'required': False,
                'type': 'currency',
                'min_value': 0
            },
            'RegState1': {
                'required': False,
                'type': 'text',
                'regex': r'^[A-Z]{2}$',
                'controlled_vocab': ['NJ', 'NY', 'PA', 'CT', 'DE', 'MD', 'VA']
            },
            'RegState2': {
                'required': False,
                'type': 'text',
                'regex': r'^[A-Z]{2}$',
                'controlled_vocab': ['NJ', 'NY', 'PA', 'CT', 'DE', 'MD', 'VA']
            },
            'FullAddress': {
                'required': False,
                'type': 'text',
                'contains': ','  # Must contain at least one comma
            }
        }

    def validate_file(self, filepath: str) -> Dict:
        """Validate entire CSV file and return results."""
        try:
            # Read CSV file
            df = pd.read_csv(filepath)
            self.record_count = len(df)

            print(f"Validating {self.record_count} records from {filepath}...")

            # Validate each record
            for idx, row in df.iterrows():
                self._validate_record(idx + 1, row)

            # Perform cross-field validations
            self._validate_cross_field(df)

            return self._generate_summary()

        except FileNotFoundError:
            return {'error': f'File not found: {filepath}'}
        except Exception as e:
            return {'error': f'Error processing file: {str(e)}'}

    def _validate_record(self, row_num: int, record: pd.Series):
        """Validate a single record."""
        # Check required fields
        for field_name, rules in self.field_rules.items():
            if rules.get('required', False):
                if pd.isna(record.get(field_name)) or str(record.get(field_name)).strip() == '':
                    self._add_error(row_num, field_name, 'Required field is missing or empty')

            # Validate field if present
            if field_name in record and not pd.isna(record[field_name]):
                self._validate_field(row_num, field_name, record[field_name])

    def _validate_field(self, row_num: int, field_name: str, value):
        """Validate individual field based on type and rules."""
        rules = self.field_rules.get(field_name, {})
        value_str = str(value).strip()

        if not value_str:
            return  # Skip empty values for optional fields

        # Regex validation
        if 'regex' in rules:
            if not re.match(rules['regex'], value_str):
                self._add_error(row_num, field_name,
                               f"Value '{value_str}' does not match pattern {rules['regex']}")

        # Date validation
        if rules.get('type') == 'date':
            if not self._validate_date(value_str, rules.get('formats', [])):
                self._add_error(row_num, field_name,
                               f"Invalid date format: '{value_str}'")

        # Time validation
        if rules.get('type') == 'time':
            if not self._validate_time(value_str, rules.get('formats', [])):
                self._add_error(row_num, field_name,
                               f"Invalid time format: '{value_str}'")

        # Integer validation with range
        if rules.get('type') == 'integer':
            try:
                int_val = int(float(value_str))
                if 'valid_range' in rules:
                    min_val, max_val = rules['valid_range']
                    if not (min_val <= int_val <= max_val):
                        self._add_error(row_num, field_name,
                                       f"Value {int_val} out of valid range [{min_val}, {max_val}]")
            except ValueError:
                self._add_error(row_num, field_name,
                               f"Invalid integer value: '{value_str}'")

        # Currency validation
        if rules.get('type') == 'currency':
            try:
                # Remove currency symbols and commas
                clean_val = value_str.replace('$', '').replace(',', '')
                float_val = float(clean_val)
                if 'min_value' in rules and float_val < rules['min_value']:
                    self._add_error(row_num, field_name,
                                   f"Value {float_val} below minimum {rules['min_value']}")
            except ValueError:
                self._add_error(row_num, field_name,
                               f"Invalid currency value: '{value_str}'")

        # Contains validation
        if 'contains' in rules:
            if rules['contains'] not in value_str:
                self._add_warning(row_num, field_name,
                                 f"Expected to contain '{rules['contains']}'")

        # Controlled vocabulary
        if 'controlled_vocab' in rules:
            if value_str.upper() not in rules['controlled_vocab']:
                self._add_warning(row_num, field_name,
                                 f"Value '{value_str}' not in controlled vocabulary")

    def _validate_cross_field(self, df: pd.DataFrame):
        """Perform cross-field validation."""
        for idx, row in df.iterrows():
            row_num = idx + 1

            # Incident Date should be <= Report Date
            if not pd.isna(row.get('IncidentDate')) and not pd.isna(row.get('ReportDate')):
                try:
                    incident_date = pd.to_datetime(row['IncidentDate'])
                    report_date = pd.to_datetime(row['ReportDate'])
                    if incident_date > report_date:
                        self._add_error(row_num, 'IncidentDate',
                                       'Incident date is after report date')
                except:
                    pass  # Date parsing errors already caught in field validation

            # TotalValueRecover should be <= TotalValueStolen
            if not pd.isna(row.get('TotalValueStolen')) and not pd.isna(row.get('TotalValueRecover')):
                try:
                    stolen = float(str(row['TotalValueStolen']).replace('$', '').replace(',', ''))
                    recovered = float(str(row['TotalValueRecover']).replace('$', '').replace(',', ''))
                    if recovered > stolen:
                        self._add_warning(row_num, 'TotalValueRecover',
                                         f'Recovered value ({recovered}) exceeds stolen value ({stolen})')
                except:
                    pass

    def _validate_date(self, value: str, formats: List[str]) -> bool:
        """Validate date string against multiple formats."""
        for fmt in formats:
            try:
                datetime.strptime(value, fmt)
                return True
            except ValueError:
                continue
        # Try pandas parsing as fallback
        try:
            pd.to_datetime(value)
            return True
        except:
            return False

    def _validate_time(self, value: str, formats: List[str]) -> bool:
        """Validate time string against multiple formats."""
        for fmt in formats:
            try:
                datetime.strptime(value, fmt)
                return True
            except ValueError:
                continue
        return False

    def _add_error(self, row_num: int, field_name: str, message: str):
        """Add validation error."""
        self.validation_results.append({
            'row': row_num,
            'field': field_name,
            'severity': 'ERROR',
            'message': message
        })
        self.error_count += 1

    def _add_warning(self, row_num: int, field_name: str, message: str):
        """Add validation warning."""
        self.validation_results.append({
            'row': row_num,
            'field': field_name,
            'severity': 'WARNING',
            'message': message
        })
        self.warning_count += 1

    def _generate_summary(self) -> Dict:
        """Generate validation summary."""
        return {
            'record_count': self.record_count,
            'error_count': self.error_count,
            'warning_count': self.warning_count,
            'results': self.validation_results,
            'status': 'PASS' if self.error_count == 0 else 'FAIL'
        }

    def generate_html_report(self, summary: Dict, output_file: str):
        """Generate HTML validation report."""
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>RMS Export Validation Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        h1 {{ color: #333; border-bottom: 3px solid #667eea; padding-bottom: 10px; }}
        .summary {{ background: #f8f9fa; padding: 20px; border-radius: 6px; margin: 20px 0; }}
        .stat {{ display: inline-block; margin: 10px 20px 10px 0; }}
        .stat-label {{ font-weight: bold; color: #666; }}
        .stat-value {{ font-size: 24px; font-weight: bold; color: #667eea; }}
        .status-pass {{ color: #28a745; }}
        .status-fail {{ color: #dc3545; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
        th {{ background: #667eea; color: white; padding: 12px; text-align: left; }}
        td {{ padding: 10px; border-bottom: 1px solid #ddd; }}
        tr:hover {{ background: #f8f9fa; }}
        .error {{ color: #dc3545; font-weight: bold; }}
        .warning {{ color: #ffc107; font-weight: bold; }}
        .timestamp {{ color: #666; font-size: 0.9em; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>RMS Export Validation Report</h1>
        <p class="timestamp">Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>

        <div class="summary">
            <h2>Summary</h2>
            <div class="stat">
                <div class="stat-label">Total Records</div>
                <div class="stat-value">{summary['record_count']}</div>
            </div>
            <div class="stat">
                <div class="stat-label">Errors</div>
                <div class="stat-value" style="color: #dc3545;">{summary['error_count']}</div>
            </div>
            <div class="stat">
                <div class="stat-label">Warnings</div>
                <div class="stat-value" style="color: #ffc107;">{summary['warning_count']}</div>
            </div>
            <div class="stat">
                <div class="stat-label">Status</div>
                <div class="stat-value {'status-pass' if summary['status'] == 'PASS' else 'status-fail'}">
                    {summary['status']}
                </div>
            </div>
        </div>

        <h2>Validation Issues</h2>
        {self._generate_results_table(summary['results'])}
    </div>
</body>
</html>
"""
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html)

        print(f"HTML report generated: {output_file}")

    def _generate_results_table(self, results: List[Dict]) -> str:
        """Generate HTML table of validation results."""
        if not results:
            return '<p style="color: #28a745; font-weight: bold;">✓ No validation issues found!</p>'

        rows = []
        for result in results:
            severity_class = 'error' if result['severity'] == 'ERROR' else 'warning'
            rows.append(f"""
                <tr>
                    <td>{result['row']}</td>
                    <td>{result['field']}</td>
                    <td class="{severity_class}">{result['severity']}</td>
                    <td>{result['message']}</td>
                </tr>
            """)

        return f"""
        <table>
            <thead>
                <tr>
                    <th>Row</th>
                    <th>Field</th>
                    <th>Severity</th>
                    <th>Message</th>
                </tr>
            </thead>
            <tbody>
                {''.join(rows)}
            </tbody>
        </table>
        """


def main():
    """Main execution function."""
    if len(sys.argv) < 2:
        print("Usage: python validate_rms_export.py input_file.csv [output_report.html]")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else 'validation_report.html'

    # Validate file
    validator = RMSFieldValidator()
    summary = validator.validate_file(input_file)

    if 'error' in summary:
        print(f"Error: {summary['error']}")
        sys.exit(1)

    # Print summary
    print(f"\n{'='*60}")
    print("VALIDATION SUMMARY")
    print(f"{'='*60}")
    print(f"Records Validated: {summary['record_count']}")
    print(f"Errors Found:      {summary['error_count']}")
    print(f"Warnings Found:    {summary['warning_count']}")
    print(f"Status:            {summary['status']}")
    print(f"{'='*60}\n")

    # Generate HTML report
    validator.generate_html_report(summary, output_file)

    # Exit with error code if validation failed
    sys.exit(0 if summary['status'] == 'PASS' else 1)


if __name__ == '__main__':
    main()
