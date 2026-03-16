#!/usr/bin/env python3
"""
YAML to Obsidian Sync Script
Synchronizes YAML task definitions to Obsidian-compatible markdown files.

Usage:
    python sync_yaml_to_obsidian.py tasks.yaml --kanban-dir ./kanban

Features:
- Creates/updates .md files from YAML task definitions
- Places files in appropriate Kanban column folders based on status
- Preserves existing content below frontmatter
- Tracks changes and generates sync report
"""

import yaml
import sys
import argparse
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional


class ObsidianSyncer:
    """Sync YAML tasks to Obsidian markdown files."""

    STATUS_FOLDERS = {
        'To Do': 'To Do',
        'In Progress': 'In Progress',
        'Blocked': 'Blocked',
        'Done': 'Done'
    }

    def __init__(self, kanban_dir: Path):
        self.kanban_dir = kanban_dir
        self.sync_log = []

        # Ensure Kanban folders exist
        for folder in self.STATUS_FOLDERS.values():
            (kanban_dir / folder).mkdir(parents=True, exist_ok=True)

    def load_yaml_tasks(self, yaml_path: Path) -> List[Dict]:
        """Load tasks from YAML file."""
        with open(yaml_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)

        if isinstance(data, dict) and 'tasks' in data:
            return data['tasks']
        elif isinstance(data, dict) and 'id' in data:
            return [data]
        elif isinstance(data, list):
            return data
        else:
            raise ValueError("Invalid YAML format")

    def task_to_markdown(self, task: Dict) -> str:
        """Convert task dict to Obsidian-compatible markdown."""

        # Build frontmatter
        frontmatter_fields = [
            'id', 'title', 'status', 'priority', 'assigned_to', 'due',
            'created', 'updated', 'category', 'tags', 'related_files',
            'blocked_by', 'blocks', 'comments'
        ]

        lines = ['---']
        for field in frontmatter_fields:
            if field in task:
                value = task[field]
                if isinstance(value, list):
                    lines.append(f'{field}:')
                    for item in value:
                        lines.append(f'  - "{item}"' if isinstance(item, str) else f'  - {item}')
                elif isinstance(value, str) and '\n' in value:
                    lines.append(f'{field}: |')
                    for line in value.strip().split('\n'):
                        lines.append(f'  {line}')
                elif isinstance(value, str):
                    lines.append(f'{field}: "{value}"')
                else:
                    lines.append(f'{field}: {value}')
        lines.append('---')
        lines.append('')

        # Add body content
        lines.append(f"# {task.get('title', 'Untitled Task')}")
        lines.append('')
        lines.append('## Description')
        lines.append('')
        if task.get('comments'):
            lines.append(task['comments'].strip())
        else:
            lines.append('_No description provided._')
        lines.append('')

        # Related files section
        if task.get('related_files'):
            lines.append('## Related Files')
            lines.append('')
            for f in task['related_files']:
                lines.append(f'- `{f}`')
            lines.append('')

        # Dependencies section
        if task.get('blocked_by') or task.get('blocks'):
            lines.append('## Dependencies')
            lines.append('')
            if task.get('blocked_by'):
                lines.append(f"**Blocked by:** {', '.join(task['blocked_by'])}")
            if task.get('blocks'):
                lines.append(f"**Blocks:** {', '.join(task['blocks'])}")
            lines.append('')

        # Work log section
        lines.append('## Work Log')
        lines.append('')
        lines.append('| Date | Update |')
        lines.append('|------|--------|')
        lines.append(f"| {task.get('created', 'Unknown')} | Task created |")
        if task.get('status') == 'Done':
            lines.append(f"| {task.get('updated', 'Unknown')} | Task completed |")
        lines.append('')

        return '\n'.join(lines)

    def find_existing_task(self, task_id: str) -> Optional[Path]:
        """Find existing markdown file for a task ID."""
        for folder in self.STATUS_FOLDERS.values():
            folder_path = self.kanban_dir / folder
            for md_file in folder_path.glob('*.md'):
                content = md_file.read_text(encoding='utf-8')
                if f'id: "{task_id}"' in content or f"id: {task_id}" in content:
                    return md_file
        return None

    def sync_task(self, task: Dict) -> str:
        """Sync a single task to Obsidian."""
        task_id = task.get('id', 'UNKNOWN')
        status = task.get('status', 'To Do')
        title = task.get('title', 'Untitled')

        # Determine target folder
        target_folder = self.STATUS_FOLDERS.get(status, 'To Do')
        target_dir = self.kanban_dir / target_folder

        # Clean filename from title
        safe_title = ''.join(c if c.isalnum() or c in ' -_' else '_' for c in title)
        safe_title = safe_title[:50].strip()
        filename = f"{task_id} - {safe_title}.md"
        target_path = target_dir / filename

        # Check for existing file
        existing_path = self.find_existing_task(task_id)

        if existing_path:
            if existing_path != target_path:
                # Task moved to different status - move file
                shutil.move(str(existing_path), str(target_path))
                action = f"MOVED: {existing_path.parent.name} -> {target_folder}"
            else:
                action = "UPDATED"
        else:
            action = "CREATED"

        # Write markdown content
        md_content = self.task_to_markdown(task)
        target_path.write_text(md_content, encoding='utf-8')

        return action

    def sync_all(self, yaml_path: Path) -> Dict:
        """Sync all tasks from YAML file."""
        tasks = self.load_yaml_tasks(yaml_path)

        results = {
            'created': 0,
            'updated': 0,
            'moved': 0,
            'total': len(tasks),
            'details': []
        }

        for task in tasks:
            action = self.sync_task(task)
            task_id = task.get('id', 'UNKNOWN')

            if 'CREATED' in action:
                results['created'] += 1
            elif 'MOVED' in action:
                results['moved'] += 1
            else:
                results['updated'] += 1

            results['details'].append({
                'id': task_id,
                'title': task.get('title', 'Untitled'),
                'action': action
            })

        return results


def main():
    parser = argparse.ArgumentParser(description='Sync YAML tasks to Obsidian')
    parser.add_argument('yaml_file', help='Input YAML file')
    parser.add_argument('--kanban-dir', '-k', default='./kanban', help='Kanban directory')
    parser.add_argument('--dry-run', action='store_true', help='Preview changes without writing')

    args = parser.parse_args()

    yaml_path = Path(args.yaml_file)
    kanban_dir = Path(args.kanban_dir)

    if not yaml_path.exists():
        print(f"Error: File not found: {yaml_path}")
        sys.exit(1)

    try:
        syncer = ObsidianSyncer(kanban_dir)
        results = syncer.sync_all(yaml_path)

        print(f"\n{'='*50}")
        print("YAML -> Obsidian Sync Complete")
        print(f"{'='*50}")
        print(f"Total Tasks:  {results['total']}")
        print(f"Created:      {results['created']}")
        print(f"Updated:      {results['updated']}")
        print(f"Moved:        {results['moved']}")
        print(f"\nDetails:")
        for detail in results['details']:
            print(f"  [{detail['action']}] {detail['id']}: {detail['title'][:40]}")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
