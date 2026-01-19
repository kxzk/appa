#!/bin/bash

cd /home/ubuntu

SEEN_FILE="issues_seen.txt"

echo "☁️ [$(date '+%Y-%m-%d %H:%M:%S')] Checking for new issues..."

# List recent issues assigned to me (last 2 minutes)
output=$(./linear.py list-issues --recent 2 2>/dev/null)

# Extract issue ID (format: TEAM-123)
issue_id=$(echo "$output" | grep -oE '[A-Z]+-[0-9]+' | head -1)

if [[ -n "$issue_id" ]]; then
    # Check if issue has already been seen
    if [[ -f "$SEEN_FILE" ]] && grep -qx "$issue_id" "$SEEN_FILE"; then
        echo "☁️ [$(date '+%Y-%m-%d %H:%M:%S')] Issue $issue_id already processed, skipping"
        exit 0
    fi

    echo "☁️ [$(date '+%Y-%m-%d %H:%M:%S')] Found new issue: $issue_id"

    # Add issue to seen file
    echo "$issue_id" >> "$SEEN_FILE"

    echo "☁️ [$(date '+%Y-%m-%d %H:%M:%S')] Starting Claude Code to process issue..."

    # Get issue details and write to issue.md
    ./linear.py get-issue "$issue_id" > issue.md

    # Invoke claude code with the issue
    {
        cat issue.md
        cat <<'PROMPT'

## Instructions

You are being given a Linear issue to complete.

### Issue Format
The issue details above are in this format:
- DESCRIPTION: The task description
- ISSUE_ID: The issue identifier and title (e.g., "ML-488 - Add another param to X thing")
- BRANCH_NAME: The git branch name to use

### Workflow
1. Read the DESCRIPTION to understand the task
2. cd into the repository (name will be in the DESCRIPTION, repo is available locally)
3. Run `git pull` to get the latest changes
4. Create the branch using `git switch -c <BRANCH_NAME>`
5. Implement the task or take a first stab at it
6. Commit and push your changes
7. Create a draft PR
8. Switch back to main branch with `git switch -`

### Commit Message Format
Use the ISSUE_ID as the commit title:
```
[ML-488] Add another param to X thing
```
That should be the ONLY line in the commit title.

### Creating the Draft PR
Don't add a body and use the repo's default template instead.
```bash
gh pr create --draft --title "ISSUE_ID"
```
PROMPT
    } | claude -p --dangerously-skip-permissions --allowedTools "*" &
    echo "☁️ [$(date '+%Y-%m-%d %H:%M:%S')] Claude Code started in background (PID: $!)"
else
    echo "☁️ [$(date '+%Y-%m-%d %H:%M:%S')] No new issues found"
fi
