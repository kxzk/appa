# ☁️ Appa

> **Yip yip, ship ship.**

Describe a task. Get back a PR.

<br>

### Inspiration
> "I need Linear but where every task is automatically an AI agent session that at least takes a first stab at the task. Basically a todo list that tries to do itself"
>
> — [@jeffzwang](https://x.com/jeffzwang/)
<details>
  <summary>Original X Post</summary>

  ![IMG_4399](https://github.com/user-attachments/assets/783d9e0f-6f27-4148-bd0f-173fd987b783)

</details>

<br>

> [!WARNING]
> 🚧 Highly, highly, highly experimental (safety goggles advised). The main caveat: you must **manually assign issues to yourself** in Linear after creation. [Linearite](https://github.com/kxzk/linearite) doesn't support setting assignees on create yet - the remote agent polls for issues assigned to you (it takes two seconds two vibe code a Linear CLI).

<br>

### Takeaways

This is a proof of concept - rough edges included. The core ideas matter more than the implementation:

1. **High-level input → detailed PRD** — Claude Code explores your codebase and writes a thorough plan
2. **PRD → Linear issue** — plans become trackable work items automatically
3. **Issue → PR** — assigned issues get implemented without intervention

The unlock: `cd` into a repo, describe what you want in plain English, walk away. You get a tracked issue and a draft PR. Even at 60-80% quality, that's a meaningful starting point to iterate on.

Zooming out: every Linear issue becomes a potential agent session. That's the shift from AI-assisted to AI-driven development - you describe intent, agents execute, you review.

<br>

## How it works

```
appa "add dark mode support to the settings page for team:ENG project:Mobile"
```

1. **You invoke** — describe what you want, specifying the team and project by name

2. **Local agent plans** — Claude Code explores your codebase and writes a PRD

3. **Issue created** — the plan becomes a [Linear](https://linear.app) issue via [Linearite](https://github.com/kxzk/linearite) (invoked via Claude Code Skill)

4. **You assign** — assign the issue to yourself in Linear (triggers the remote agent)

5. **Remote agent builds** — server-side Claude Code picks it up and implements

6. **PR opens** — you review the draft PR on GitHub

```
☁️  Planning...
☁️  Created issue: ENG-142 "Add dark mode support to settings page"
☁️  Assign to yourself in Linear to queue for implementation

    ↓ (after assignment)

☁️  PR #87 opened: https://github.com/you/repo/pull/87
```

<br>

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│  LOCAL                                                          │
│                                                                 │
│  appa.sh ─────► Claude Code ─────► Linearite ─────► Linear      │
│                 (plans task)       (creates issue)              │
└─────────────────────────────────────────────────────────────────┘
                                            │
                                            ▼
                                     manual assignment
                                            │
                                            ▼
┌─────────────────────────────────────────────────────────────────┐
│  REMOTE (server)                                                │
│                                                                 │
│  cron ─► appa_remote.sh ─► linear_cli.py ─► Claude Code ─► PR   │
│          (polls issues)     (fetches mine)   (implements)       │
└─────────────────────────────────────────────────────────────────┘
```

### Local (`appa.sh` + Linearite)

The local side handles planning and issue creation:

- Invokes Claude Code with `--dangerously-skip-permissions`
- Agent spawns sub-agents to explore codebase and craft a detailed PRD
- Uses [Linearite](https://github.com/kxzk/linearite) to resolve team/project names → IDs
- Creates the Linear issue with the PRD as the body

### Remote (`appa_remote.sh` + `linear_cli.py`)

The remote side handles execution:

- `linear_cli.py` — minimal GraphQL client to list/get Linear issues
- `appa_remote.sh` — polls for issues assigned to you (created in last 15 min)
- On new issue: fetches details, invokes Claude Code to implement
- Agent creates branch, commits, pushes, opens draft PR

<br>

## Setup

### Requirements

**Local**
- [Claude Code](https://github.com/anthropics/claude-code)
- [Linearite](https://github.com/kxzk/linearite) (`curl -fsSL https://kade.work/linearite/install | sh`)
- `LINEAR_API_KEY` env var ([get one here](https://linear.app/settings/api))

**Remote**
- [Claude Code](https://github.com/anthropics/claude-code)
- [uv](https://docs.astral.sh/uv/) (`curl -LsSf https://astral.sh/uv/install.sh | sh`)
- `LINEAR_API_KEY` env var
- `gh` CLI authenticated for PR creation

### Local

```bash
# Add to PATH or alias
alias appa="/path/to/appa.sh"
```

### Remote

```bash
# On your server, set up cron to poll
*/5 * * * * /home/ubuntu/appa_remote.sh >> /home/ubuntu/appa.log 2>&1
```

Ensure repos are cloned locally on the server and `gh` is authenticated.

<br>

## Name

[Appa](https://avatar.fandom.com/wiki/Appa) carries the team, flies through clouds, and gets everyone where they need to go. Yip yip.
