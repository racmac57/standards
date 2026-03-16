# Obsidian Task Tracker System

A YAML-based task management system designed for Obsidian with Kanban support.

## Directory Structure

```
task_templates/
├── README.md                    # This file
├── kanban/                      # Kanban board templates
│   ├── board.md                 # Main Kanban board (Obsidian Kanban plugin)
│   ├── To Do/                   # Tasks in queue
│   ├── In Progress/             # Active tasks
│   ├── Blocked/                 # Blocked tasks
│   └── Done/                    # Completed tasks
├── examples/                    # Example task files
│   ├── task_template.md         # Blank task template
│   ├── task.yaml                # YAML task definition
│   └── sample_tasks.yaml        # Example tasks from CAD/ETL workflows
├── scripts/                     # Automation scripts
│   ├── yaml_to_csv.py           # Convert YAML tasks → CSV audit log
│   ├── yaml_to_html.py          # Generate HTML summary report
│   └── sync_yaml_to_obsidian.py # Sync YAML → Obsidian .md files
└── tasks.yaml                   # Master task registry
```

## YAML Frontmatter Schema

Each task in Obsidian uses YAML frontmatter with these fields:

```yaml
---
id: TASK-001                    # Unique identifier
title: "Task title"             # Short descriptive title
status: "To Do"                 # To Do | In Progress | Blocked | Done
priority: "High"                # Critical | High | Medium | Low
assigned_to: "R. Carucci"       # Responsible person
due: 2026-02-15                 # Due date (YYYY-MM-DD)
created: 2026-01-30             # Creation date
updated: 2026-01-30             # Last update date
category: "ETL"                 # Category tag
tags:
  - cad
  - export
  - esri
related_files:
  - "_CAD/yearly/2024_CAD_ALL.xlsx"
  - "scripts/export_esri_cad.py"
blocked_by: []                  # IDs of blocking tasks
blocks: []                      # IDs of tasks this blocks
comments: |
  Additional notes go here.
  Can be multiline.
---
```

## Workflow

### 1. Create Tasks

**Option A: Direct in Obsidian**
- Create a new note in the appropriate Kanban column folder
- Use the task template to add frontmatter
- Fill in task details

**Option B: YAML Registry**
- Add task to `tasks.yaml` master file
- Run `sync_yaml_to_obsidian.py` to generate .md files
- Tasks appear in Kanban automatically

### 2. Update Tasks

- Edit the frontmatter `status` field to move between columns
- Update `updated` date when making changes
- Add comments as work progresses

### 3. Track & Report

- Run `yaml_to_csv.py` to generate audit logs
- Run `yaml_to_html.py` for stakeholder summaries
- Use Obsidian Dataview queries for custom views

## Obsidian Plugin Requirements

| Plugin | Purpose |
|--------|---------|
| **Kanban** | Visual board view of tasks |
| **Dataview** | Query and filter tasks by frontmatter |
| **Templater** | Quick task creation from templates |
| **YAML Frontmatter** | Edit frontmatter easily |

## Dataview Query Examples

### All High Priority Tasks
```dataview
TABLE status, due, assigned_to
FROM "task_templates/kanban"
WHERE priority = "High" OR priority = "Critical"
SORT due ASC
```

### Tasks Due This Week
```dataview
LIST
FROM "task_templates/kanban"
WHERE due >= date(today) AND due <= date(today) + dur(7 days)
SORT due ASC
```

### Tasks by Category
```dataview
TABLE status, priority, due
FROM "task_templates/kanban"
WHERE category = "ETL"
SORT priority DESC
```

## Scripts

### yaml_to_csv.py
Converts tasks.yaml to a CSV audit log for spreadsheet analysis or archival.

```bash
python scripts/yaml_to_csv.py tasks.yaml --output audit_log.csv
```

### yaml_to_html.py
Generates an HTML summary report for stakeholders without Obsidian access.

```bash
python scripts/yaml_to_html.py tasks.yaml --output task_report.html
```

### sync_yaml_to_obsidian.py
Synchronizes YAML task definitions to Obsidian markdown files.

```bash
python scripts/sync_yaml_to_obsidian.py tasks.yaml --kanban-dir ./kanban
```

## Version History

| Date | Version | Changes |
|------|---------|---------|
| 2026-01-30 | 1.0.0 | Initial release |
