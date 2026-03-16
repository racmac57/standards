#!/usr/bin/env python3
"""
YAML Tasks to HTML Report Generator
Generates styled HTML summary reports from YAML task definitions.

Usage:
    python yaml_to_html.py tasks.yaml --output task_report.html
"""

import yaml
import sys
import argparse
from pathlib import Path
from datetime import datetime
from collections import Counter


def load_yaml_tasks(yaml_path: Path) -> list:
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


def generate_html_report(tasks: list, output_path: Path, title: str = "Task Report"):
    """Generate HTML report from tasks."""

    # Calculate statistics
    status_counts = Counter(t.get('status', 'Unknown') for t in tasks)
    priority_counts = Counter(t.get('priority', 'Unknown') for t in tasks)
    category_counts = Counter(t.get('category', 'Uncategorized') for t in tasks)

    # Sort tasks by status then priority
    status_order = {'To Do': 0, 'In Progress': 1, 'Blocked': 2, 'Done': 3}
    priority_order = {'Critical': 0, 'High': 1, 'Medium': 2, 'Low': 3}

    sorted_tasks = sorted(tasks, key=lambda t: (
        status_order.get(t.get('status', ''), 99),
        priority_order.get(t.get('priority', ''), 99)
    ))

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        :root {{
            --primary: #667eea;
            --success: #28a745;
            --warning: #ffc107;
            --danger: #dc3545;
            --info: #17a2b8;
        }}
        * {{ box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f7fa;
        }}
        .header {{
            background: linear-gradient(135deg, var(--primary), #764ba2);
            color: white;
            padding: 30px;
            border-radius: 12px;
            margin-bottom: 30px;
        }}
        .header h1 {{ margin: 0 0 10px 0; }}
        .header .timestamp {{ opacity: 0.8; font-size: 0.9em; }}
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .stat-card {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .stat-card h3 {{ margin: 0 0 15px 0; color: #666; font-size: 0.9em; text-transform: uppercase; }}
        .stat-item {{ display: flex; justify-content: space-between; padding: 5px 0; }}
        .stat-value {{ font-weight: bold; }}
        .task-list {{ background: white; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        .task {{
            padding: 20px;
            border-bottom: 1px solid #eee;
        }}
        .task:last-child {{ border-bottom: none; }}
        .task-header {{ display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 10px; }}
        .task-title {{ font-weight: 600; font-size: 1.1em; margin: 0; }}
        .task-id {{ color: #666; font-size: 0.85em; }}
        .task-meta {{ display: flex; gap: 10px; flex-wrap: wrap; margin-bottom: 10px; }}
        .badge {{
            display: inline-block;
            padding: 3px 10px;
            border-radius: 20px;
            font-size: 0.8em;
            font-weight: 500;
        }}
        .badge-todo {{ background: #e3f2fd; color: #1565c0; }}
        .badge-progress {{ background: #fff3e0; color: #e65100; }}
        .badge-blocked {{ background: #ffebee; color: #c62828; }}
        .badge-done {{ background: #e8f5e9; color: #2e7d32; }}
        .badge-critical {{ background: #d32f2f; color: white; }}
        .badge-high {{ background: #ff5722; color: white; }}
        .badge-medium {{ background: #ff9800; color: white; }}
        .badge-low {{ background: #4caf50; color: white; }}
        .task-details {{ color: #666; font-size: 0.9em; }}
        .task-details p {{ margin: 5px 0; }}
        .comments {{ background: #f9f9f9; padding: 10px; border-radius: 4px; margin-top: 10px; font-size: 0.9em; }}
        .tags {{ margin-top: 10px; }}
        .tag {{ background: #e0e0e0; padding: 2px 8px; border-radius: 4px; font-size: 0.8em; margin-right: 5px; }}
        .section-title {{ margin: 30px 0 15px 0; color: #333; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>{title}</h1>
        <div class="timestamp">Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>
    </div>

    <div class="stats">
        <div class="stat-card">
            <h3>By Status</h3>
"""

    for status, count in sorted(status_counts.items()):
        html += f'            <div class="stat-item"><span>{status}</span><span class="stat-value">{count}</span></div>\n'

    html += """        </div>
        <div class="stat-card">
            <h3>By Priority</h3>
"""

    for priority, count in sorted(priority_counts.items(), key=lambda x: priority_order.get(x[0], 99)):
        html += f'            <div class="stat-item"><span>{priority}</span><span class="stat-value">{count}</span></div>\n'

    html += """        </div>
        <div class="stat-card">
            <h3>By Category</h3>
"""

    for category, count in sorted(category_counts.items()):
        html += f'            <div class="stat-item"><span>{category}</span><span class="stat-value">{count}</span></div>\n'

    html += f"""        </div>
        <div class="stat-card">
            <h3>Summary</h3>
            <div class="stat-item"><span>Total Tasks</span><span class="stat-value">{len(tasks)}</span></div>
            <div class="stat-item"><span>Completed</span><span class="stat-value">{status_counts.get('Done', 0)}</span></div>
            <div class="stat-item"><span>In Progress</span><span class="stat-value">{status_counts.get('In Progress', 0)}</span></div>
            <div class="stat-item"><span>Blocked</span><span class="stat-value">{status_counts.get('Blocked', 0)}</span></div>
        </div>
    </div>

    <h2 class="section-title">All Tasks</h2>
    <div class="task-list">
"""

    for task in sorted_tasks:
        status = task.get('status', 'Unknown')
        priority = task.get('priority', 'Unknown')
        status_class = {
            'To Do': 'todo', 'In Progress': 'progress',
            'Blocked': 'blocked', 'Done': 'done'
        }.get(status, 'todo')
        priority_class = priority.lower() if priority else 'medium'

        html += f"""        <div class="task">
            <div class="task-header">
                <div>
                    <p class="task-title">{task.get('title', 'Untitled')}</p>
                    <span class="task-id">{task.get('id', 'N/A')}</span>
                </div>
            </div>
            <div class="task-meta">
                <span class="badge badge-{status_class}">{status}</span>
                <span class="badge badge-{priority_class}">{priority}</span>
            </div>
            <div class="task-details">
                <p><strong>Assigned:</strong> {task.get('assigned_to', 'Unassigned')}</p>
                <p><strong>Due:</strong> {task.get('due', 'No due date')}</p>
                <p><strong>Category:</strong> {task.get('category', 'Uncategorized')}</p>
"""

        if task.get('comments'):
            comments = task['comments'].replace('\n', '<br>') if isinstance(task['comments'], str) else str(task['comments'])
            html += f'                <div class="comments">{comments}</div>\n'

        if task.get('tags'):
            tags_html = ' '.join(f'<span class="tag">{tag}</span>' for tag in task['tags'])
            html += f'                <div class="tags">{tags_html}</div>\n'

        html += """            </div>
        </div>
"""

    html += """    </div>
</body>
</html>
"""

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"Generated HTML report: {output_path}")


def main():
    parser = argparse.ArgumentParser(description='Generate HTML report from YAML tasks')
    parser.add_argument('yaml_file', help='Input YAML file')
    parser.add_argument('--output', '-o', default='task_report.html', help='Output HTML file')
    parser.add_argument('--title', '-t', default='Task Report', help='Report title')

    args = parser.parse_args()

    yaml_path = Path(args.yaml_file)
    output_path = Path(args.output)

    if not yaml_path.exists():
        print(f"Error: File not found: {yaml_path}")
        sys.exit(1)

    try:
        tasks = load_yaml_tasks(yaml_path)
        generate_html_report(tasks, output_path, args.title)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
