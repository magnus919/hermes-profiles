# Hermes Profiles

Curated Hermes Agent profiles for specialist swarms. Each profile packages a role identity (SOUL.md), skill dependencies, and configuration for a specific architecture/engineering capability that can be deployed as a Hermes agent.

These profiles are **opinionated** — they use Hermes-native patterns:
- Artifact-pyramid output format (progressive disclosure, path-as-handoff)
- skill-based methodology loading (`skill_view` → load references)
- Hermes kanban for multi-agent orchestration
- Hermes profile system for role isolation

The **profiles** (SOUL.md + profile.yaml) are Hermes-specific and unlikely to work
in other harnesses. But the **skills** — the methodology directories in `skills/`
with their SKILL.md + references/ structure — follow the [Agent Skills open
standard](https://www.agensi.io/learn/agent-skills-open-standard) adopted by
Claude Code, Codex CLI, Cursor, Gemini CLI, OpenClaw, GitHub Copilot, Windsurf,
and 20+ other coding agents. Those should work anywhere.

## Repository Structure

```
hermes-profiles/
├── skills/
│   ├── architecture/
│   │   ├── adr-authoring/
│   │   ├── arc42-context/
│   │   ├── architect-pyramid/
│   │   └── c4-diagramming/
│   ├── artifact-pyramids/
│   ├── backend-engineering/
│   ├── brand-designer/
│   ├── copy-editor-methodology/
│   ├── curation-methodology/
│   ├── data-architect/
│   ├── data-engineering/
│   ├── data-scientist/
│   ├── debugging-methodology/
│   ├── docker-management/
│   ├── editor-methodology/
│   ├── editor-review-methodology/
│   ├── editorial-methodology/
│   ├── implementation-planning/
│   ├── kanban-guru/
│   ├── mermaid-diagrams/
│   ├── ml-engineering/
│   ├── opensource-contributions/
│   ├── orchestration-methodology/
│   ├── platform-engineering/
│   ├── product-methodology/
│   ├── qa-methodology/
│   ├── research-methodology/
│   ├── researcher-workflow/
│   ├── review-methodology/
│   ├── sdd-authoring/
│   ├── sdd-review/
│   ├── sdd-verification/
│   ├── sdd-work-decomposition/
│   ├── seo-audit/
│   ├── seo-content-optimization/
│   ├── security-audit-methodology/
│   ├── site-reliability-engineering/
│   ├── software-architecture-analysis/
│   ├── systematic-debugging/
│   ├── tailscale/
│   ├── technical-documentation/
│   ├── traefik/
│   ├── ux-methodology/
│   └── verification-methodology/
└── profiles/
    ├── backend-engineer/             ← API implementation, service logic, database access
    ├── brand-designer/               ← Brand identity, visual systems
    ├── copy-editor/                  ← Line-level editing, proofreading
    ├── curator/                      ← Knowledge management, atomic notes
    ├── data-architect/               ← Data modeling, pipelines, governance
    ├── data-engineer/                ← Database ops, ETL, migrations, data quality
    ├── data-scientist/               ← Stats, causal inference, ML
    ├── debugger/                     ← Root cause analysis, error diagnosis
    ├── editor/                       ← Structural editing, argument coherence
    ├── implementation-planner/       ← Work breakdown, critical path
    ├── kanban-strategist/            ← Flow optimization, WIP calibration
    ├── ml-engineer/                  ← Model training, fine-tuning, evaluation, deployment
    ├── orchestrator/                 ← Task decomposition, specialist routing
    ├── oss-contributor/              ← Open source contribution workflows
    ├── platform-engineer/            ← CI/CD, IaC, container orchestration, service networking
    ├── product-manager/              ← Specs, prioritization, strategy
    ├── qa-engineer/                  ← Test strategy, automation, quality gates
    ├── researcher/                   ← Deep investigation, evidence synthesis
    ├── reviewer/                     ← Code/architecture review, quality gates
    ├── security-engineer/            ← Threat modeling, vulnerability assessment, security architecture
    ├── seo-specialist/               ← Search optimization, metadata
    ├── site-reliability-engineer/    ← SRE: reliability engineering, incident command, observability
    ├── spec-driven-development/      ← SDD: spec authoring, task decomposition, verification, phase-gate review
    ├── technical-architect/          ← Systems architecture: C4 + ADRs + arc42
    ├── technical-writer/             ← API docs, READMEs, AGENTS.md, developer guides
    ├── ux-designer/                  ← User journeys, accessibility
    ├── verifier/                     ← Pass/fail gatekeeping, evidence
    └── writer/                       ← Drafting, voice, narrative flow
```

Profiles symlink to the shared `skills/` directory, so one copy of each
skill serves every profile. Git tracks symlinks by reference, not by
duplicating content.

## Using a Profile

```bash
# Clone the repo
git clone https://github.com/magnus919/hermes-profiles.git ~/hermes-profiles

# Symlink the profile you want into ~/.hermes/profiles/
# (28 profiles available — pick one)
ln -s ~/hermes-profiles/profiles/researcher ~/.hermes/profiles/

# Switch to profile (skills are bundled — no separate install needed)
hermes --profile researcher
```

Each profile's `profile.yaml` lists its required skills and any Hermes-specific configuration.

## Contributing

Open an issue or PR. Profiles should:
- Have a clear, single responsibility
- Include a SOUL.md with first principles and output contract
- List skill dependencies explicitly
- Be Hermes-native (artifact-pyramid output, skill-based methodology loading)
- Not depend on agent-specific infrastructure (council, cashew, etc.) — these must work on a vanilla Hermes install

## License

MIT
