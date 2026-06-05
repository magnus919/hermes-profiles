# Hermes Profiles — Agent Guide

This file helps AI agents understand how to interact with this repository.

## Repository Structure

```
hermes-profiles/
├── skills/                          ← Shared skill pool (actual files)
│   ├── artifact-pyramids/
│   ├── architecture/
│   │   ├── adr-authoring/
│   │   ├── arc42-context/
│   │   ├── architect-pyramid/
│   │   └── c4-diagramming/
│   ├── mermaid-diagrams/
│   └── product-methodology/
├── profiles/                        ← Agent profiles (symlinks to skills)
│   ├── technical-architect/
│   ├── product-manager/
│   └── site-reliability-engineer/
├── .github/ISSUE_TEMPLATE/
├── CONTRIBUTING.md
├── LICENSE
└── README.md
```

## How Profiles Work

Each profile is a directory containing:

| File | Purpose |
|---|---|
| `SOUL.md` | Identity document — first principles, methodology, output contract |
| `profile.yaml` | Metadata — description, required/recommended skills |
| `README.md` | Human-facing usage guide |
| `AGENTS.md` | Agent-facing trigger patterns and handoff protocol |

Profiles do NOT contain skill files directly. Each profile's `skills/`
directory contains **relative symlinks** back to the shared `skills/`
pool at the repo root. This means one copy of each skill serves every
profile.

## Skill Conventions

Skills in the shared pool follow progressive disclosure:
- `SKILL.md` is a thin index with trigger conditions and loading instructions
- Methodology detail lives in `references/` loaded on demand via `skill_view(name, file_path=path)`
- Skills should work on a vanilla Hermes install — no dependencies on council, cashew, or agent-specific infrastructure

## Symlink Rules

- All symlinks must be **relative**, not absolute
- From `profiles/<name>/skills/`, target is `../../../skills/<skill-name>`
- From `profiles/<name>/skills/<category>/`, target is `../../../../skills/<category>/<skill-name>` (or make the category itself a symlink)
- Symlinks are tracked by git (mode 120000). They recreate correctly on `git clone` (macOS/Linux).

## Contribution Workflow

1. Branch from `main`
2. Add or modify profile files
3. If adding a new skill, place the skill directory in `skills/` first, then symlink from the profile
4. Ensure all symlinks resolve — check with `test -e`
5. Open a PR with a clear description of what the profile does and what skills it needs

## Verifying a Profile

Before submitting a PR, check:

- [ ] `SOUL.md` exists — first principles, output contract
- [ ] `profile.yaml` exists — valid YAML, required skills listed
- [ ] `README.md` exists — installation, quick start, skill reference
- [ ] `AGENTS.md` exists — trigger patterns, loading order, handoff
- [ ] All symlinks in `skills/` resolve to real files in the shared pool
- [ ] No absolute paths in symlinks
- [ ] No duplicate skill files — use symlinks to the shared pool

## Related Repositories

- https://github.com/magnus919/hermes-profiles — this repo
- https://github.com/groktopus/artifact-pyramids — artifact pyramid specification
- https://github.com/architecture-decision-record/architecture-decision-record — ADR community standards
