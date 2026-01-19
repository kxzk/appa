#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "click",
#     "httpx",
# ]
# ///
import os
import sys
from datetime import datetime, timedelta, timezone

import click
import httpx

API_URL = "https://api.linear.app/graphql"


def get_api_key() -> str:
    """Get Linear API key from environment."""
    api_key = os.environ.get("LINEAR_API_KEY")
    if not api_key:
        click.echo("Error: LINEAR_API_KEY environment variable not set", err=True)
        sys.exit(1)
    return api_key


def execute_query(query: str, variables: dict | None = None) -> dict:
    """Execute a GraphQL query against Linear API."""
    headers = {"Authorization": get_api_key(), "Content-Type": "application/json"}
    payload = {"query": query}
    if variables:
        payload["variables"] = variables

    response = httpx.post(API_URL, json=payload, headers=headers)
    response.raise_for_status()
    result = response.json()

    if "errors" in result:
        for error in result["errors"]:
            click.echo(f"GraphQL Error: {error.get('message', error)}", err=True)
        sys.exit(1)

    return result["data"]


@click.group()
def cli():
    """Linear CLI - Interact with Linear issues."""
    pass


@cli.command("list")
@click.option("--team", "-t", help="Filter by team key (e.g., 'ENG')")
@click.option("--mine", "-m", is_flag=True, help="Show only issues assigned to me")
@click.option(
    "--limit", "-l", default=25, help="Number of issues to fetch (default: 25)"
)
@click.option(
    "--recent",
    "-r",
    type=click.IntRange(1, 30),
    help="Only issues created in last N minutes (max 30)",
)
def list_issues(team: str | None, mine: bool, limit: int, recent: int | None):
    """List issues from Linear."""
    # Calculate created_after timestamp if filtering by recent
    created_after = None
    if recent:
        created_after = (
            datetime.now(timezone.utc) - timedelta(minutes=recent)
        ).isoformat()

    if mine:
        if recent:
            query = """
            query ListMyIssues($first: Int!, $createdAfter: DateTimeOrDuration!) {
                viewer {
                    assignedIssues(first: $first, orderBy: updatedAt, filter: { createdAt: { gte: $createdAfter } }) {
                        nodes {
                            identifier
                            title
                            state { name }
                        }
                    }
                }
            }
            """
            data = execute_query(query, {"first": limit, "createdAfter": created_after})
        else:
            query = """
            query ListMyIssues($first: Int!) {
                viewer {
                    assignedIssues(first: $first, orderBy: updatedAt) {
                        nodes {
                            identifier
                            title
                            state { name }
                        }
                    }
                }
            }
            """
            data = execute_query(query, {"first": limit})
        issues = data["viewer"]["assignedIssues"]["nodes"]
    elif team:
        if recent:
            query = """
            query ListTeamIssues($teamKey: String!, $first: Int!, $createdAfter: DateTimeOrDuration!) {
                team(id: $teamKey) {
                    issues(first: $first, filter: { createdAt: { gte: $createdAfter } }) {
                        nodes {
                            identifier
                            title
                            state { name }
                        }
                    }
                }
            }
            """
            data = execute_query(
                query, {"teamKey": team, "first": limit, "createdAfter": created_after}
            )
        else:
            query = """
            query ListTeamIssues($teamKey: String!, $first: Int!) {
                team(id: $teamKey) {
                    issues(first: $first) {
                        nodes {
                            identifier
                            title
                            state { name }
                        }
                    }
                }
            }
            """
            data = execute_query(query, {"teamKey": team, "first": limit})
        if not data.get("team"):
            click.echo(f"Team '{team}' not found", err=True)
            sys.exit(1)
        issues = data["team"]["issues"]["nodes"]
    else:
        if recent:
            query = """
            query ListIssues($first: Int!, $createdAfter: DateTimeOrDuration!) {
                issues(first: $first, filter: { createdAt: { gte: $createdAfter } }) {
                    nodes {
                        identifier
                        title
                        state { name }
                    }
                }
            }
            """
            data = execute_query(query, {"first": limit, "createdAfter": created_after})
        else:
            query = """
            query ListIssues($first: Int!) {
                issues(first: $first) {
                    nodes {
                        identifier
                        title
                        state { name }
                    }
                }
            }
            """
            data = execute_query(query, {"first": limit})
        issues = data["issues"]["nodes"]

    if not issues:
        click.echo("No issues found")
        return

    for issue in issues:
        click.echo(f"[{issue['identifier']}] {issue['title']}")


@cli.command("get")
@click.argument("issue_id")
def get_issue(issue_id: str):
    """Get a specific issue by identifier (e.g., 'ENG-123')."""
    query = """
    query GetIssue($id: String!) {
        issue(id: $id) {
            identifier
            title
            description
            branchName
        }
    }
    """
    data = execute_query(query, {"id": issue_id})

    if not data.get("issue"):
        click.echo(f"Issue '{issue_id}' not found", err=True)
        sys.exit(1)

    issue = data["issue"]

    click.echo(f"DESCRIPTION: {issue.get('description') or 'No description'}")
    click.echo(f"ISSUE_ID: {issue['identifier']} - {issue['title']}")
    click.echo(f"BRANCH_NAME: {issue.get('branchName') or 'N/A'}")


if __name__ == "__main__":
    cli()
