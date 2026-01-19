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

Also, [Why We Built Our Own Background Agent](https://builders.ramp.com/post/why-we-built-our-background-agent).

<br>

> [!WARNING]
> 🚧 Don't actually use this. It's a POC to validate the idea.

<br>

### Takeaways

Ramp's background agent now produces **~30% of merged PRs** — in just a couple months.

The bar isn't perfect autonomous code. It's a meaningful first stab. Even at 60-80% quality, a draft PR beats a blank file. The worst work — spelunking, boilerplate, wiring — is handled.

That's the shift: from *building* to *reviewing*. Engineers describe intent, agents take the first pass, humans iterate. One person can parallelize across tasks. The bottleneck moves from hands-on-keyboard to review bandwidth.

Teams that operationalize this first won't ship incrementally faster. They'll ship *structurally* faster.

<br>

## How it works

```
appa "add dark mode support to the settings page for team:ENG project:Mobile"
```

1. **Invoke** — describe what you want in plain English
2. **Plan** — local agent explores codebase, writes a PRD
3. **Track** — PRD becomes a [Linear](https://linear.app) issue
4. **Build** — remote agent implements and opens a draft PR
5. **Review** — you iterate on the PR

```
☁️  Planning...
☁️  Created issue: ENG-142 "Add dark mode support to settings page"
☁️  PR #87 opened: https://github.com/you/repo/pull/87
```

<br>

## Architecture

```
  ╭───────────────────────── LOCAL ──────────────────────────╮
  │                                                          │
  │    appa.sh  ───▶  Claude Code  ───▶  /linear skill       │
  │                   (explores, plans)   (creates issue)    │
  │                                                          │
  ╰────────────────────────────┬─────────────────────────────╯
                               ▼
                         ┌──────────┐
                         │  Linear  │
                         └──────────┘
                               ▼
  ╭───────────────────────── REMOTE ─────────────────────────╮
  │                                                          │
  │    cron  ───▶  poll issues  ───▶  Claude Code  ───▶  PR  │
  │                                   (implements)           │
  │                                                          │
  ╰──────────────────────────────────────────────────────────╯
```

**Local** — `appa.sh` invokes Claude Code which explores the codebase, writes a PRD, and creates a Linear issue via the `/linear` skill.

**Remote** — `appa_remote.sh` polls for assigned issues, hands them to Claude Code for implementation, and opens draft PRs.

<br>

## Setup

### Requirements

- [Claude Code](https://github.com/anthropics/claude-code)
- [uv](https://docs.astral.sh/uv/) (`curl -LsSf https://astral.sh/uv/install.sh | sh`)
- [gh](https://cli.github.com/) CLI (remote only, for PR creation)
- `LINEAR_API_KEY` env var ([get one](https://linear.app/settings/api))

### Usage

```bash
# Local: alias the script
alias appa="/path/to/appa.sh"

# Remote: cron job to poll for issues
* * * * * /path/to/appa_remote.sh >> ~/appa.log 2>&1
```

<br>

## Name

[Appa](https://avatar.fandom.com/wiki/Appa) carries the team, flies through clouds, and gets everyone where they need to go. Yip yip.
