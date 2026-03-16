#!/usr/bin/env python3
"""
YAML Tasks to CSV Converter
Converts YAML task definitions to CSV audit log format.

Usage:
    python yaml_to_csv.py tasks.yaml --output audit_log.csv
"""

import yaml
import csv
import sys
import argparse
from pathlib import Path
from datetime import datetime


def load_yaml_tasks(yaml_path: Path) -> list:
    """Load tasks from YAML file."""
    with open(yaml_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    # Handle both single task and task list formats
    if isinstance(data, dict) and 'tasks' in data:
        return data['tasks']
    elif isinstance(data, dict) and 'id' in data:
        return [data]
    elif isinstance(data, list):
        return data
    else:
        raise ValueError("Invalid YAML format: expected 'tasks' list or single task")


def tasks_to_csv(tasks: list, output_path: Path):
    """Convert tasks to CSV format."""

    # Define CSV columns
    columns = [
        'id', 'title', 'status', 'priority', 'assigned_to', 'due',
        'created', 'updated', 'category', 'tags', 'related_files',
        'blocked_by', 'blocks', 'comments'
    ]

    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()

        for task in tasks:
            row = {}
            for col in columns:
                value = task.get(col, '')

                # Convert lists to semicolon-separated strings
                if isinstance(value, list):
                    value = '; '.join(str(v) for v in value)
                # Convert multiline strings
                elif isinstance(value, str) and '\n' in value:
                    value = value.replace('\n', ' ').strip()

                row[col] = value

            writer.writerow(row)

    print(f"Exported {len(tasks)} tasks to: {output_path}")


def main():
    parser = argparse.ArgumentParser(description='Convert YAML tasks to CSV')
    parser.add_argument('yaml_file', help='Input YAML file')
    parser.add_argument('--output', '-o', default='tasks_audit.csv', help='Output CSV file')

    args = parser.parse_args()

    yaml_path = Path(args.yaml_file)
    output_path = Path(args.output)

    if not yaml_path.exists():
        print(f"Error: File not found: {yaml_path}")
        sys.exit(1)

    try:
        tasks = load_yaml_tasks(yaml_path)
        tasks_to_csv(tasks, output_path)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
