#!/bin/bash

if [[ -z "$1" ]]; then
    echo "Usage: appa \"<task description>\""
    exit 1
fi

TASK="$1"

PROMPT="Your goal is to create a high-quality PRD for the feature requested below. Use lots of sub-agents to explore the codebase to come up with a meticulously crafted plan:

$TASK

IMPORTANT:
- the user will specify the team and project to use by name
- you must use linearite to find the IDs for BOTH before creating the issue
- once you finish reviewing and have your final plan write it to: \`appa_plan.md\`
- please include the repository in the plan at the end like: REPOSITORY: <repo_name>
- then create an issue using linearite where appa_plan.md is the body of the issue
- come up with a title inspired by the plan but keep it short 72 chars or less
- once issue is created delete appa_plan.md"

claude -p --dangerously-skip-permissions "$PROMPT"
