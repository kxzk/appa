---
name: linear
description: This skill should be used when the user needs to interact with Linear issues - listing their assigned issues, creating new issues, getting issue details, or listing teams and projects. Triggers on requests involving Linear, issue tracking, or task management.
---

# Linear CLI

Interact with Linear issues using the bundled script.

Script location: `linear/linear.py`

## Commands

### List My Issues

```bash
linear/linear.py list-issues
linear/linear.py list-issues --recent 10  # Issues created in last 10 minutes
```

### Get Issue Details

```bash
linear/linear.py get-issue ENG-123
```

Output format:
```
DESCRIPTION: <description>
ISSUE_ID: <identifier> - <title>
BRANCH_NAME: <branch>
```

### Create Issue

```bash
linear/linear.py create-issue --team <TEAM_ID> --title "Issue title"
linear/linear.py create-issue --team <TEAM_ID> --project <PROJECT_ID> --title "Title" -d "Description"
```

Issues are created in backlog by default.

### List Teams

```bash
linear/linear.py list-teams
```

Output: `<name> (<key>): <id>`

### List Projects

```bash
linear/linear.py list-projects
linear/linear.py list-projects --team <TEAM_ID>  # Filter by team
```

Output: `<name>: <id>`

## Workflow

1. Run `list-teams` to get team IDs
2. Run `list-projects --team <ID>` to get project IDs for that team
3. Use those IDs with `create-issue`

## Requirements

- `LINEAR_API_KEY` environment variable must be set
