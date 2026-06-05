# Hermes Profiles

Curated Hermes Agent profiles for specialist swarms. Each profile packages a role identity (SOUL.md), skill dependencies, and configuration for a specific architecture/engineering capability that can be deployed as a Hermes agent.

These profiles are **opinionated** — they use Hermes-native patterns:
- Artifact-pyramid output format (progressive disclosure, path-as-handoff)
- skill-based methodology loading (`skill_view` → load references)
- Hermes kanban for multi-agent orchestration
- Hermes profile system for role isolation

They may or may not work in other harnesses. No promises.

## Repository Structure

```
hermes-profiles/
├── skills/                     ← Shared skill pool (single copy)
│   ├── artifact-pyramids/
│   ├── architecture/
│   │   ├── adr-authoring/
│   │   ├── arc42-context/
│   │   ├── architect-pyramid/
│   │   └── c4-diagramming/
│   ├── curation-methodology/
│   ├── data-architect/
│   ├── data-scientist/
│   ├── debugging-methodology/
│   ├── editorial-methodology/
│   ├── mermaid-diagrams/
│   ├── product-methodology/
│   ├── research-methodology/
│   ├── researcher-workflow/
│   ├── review-methodology/
│   └── ux-methodology/
└── profiles/
    ├── technical-architect/    ← Systems architecture: C4 + ADRs + arc42
    ├── product-manager/        ← Product management: specs, prioritization
    ├── data-architect/         ← Data modeling, pipelines, governance
    ├── implementation-planner/ ← Work breakdown, critical path
    ├── researcher/             ← Deep investigation, evidence synthesis
    ├── writer/                 ← Drafting, voice, narrative flow
    ├── debugger/               ← Root cause analysis, error diagnosis
    ├── reviewer/               ← Code/architecture review, quality gates
    ├── data-scientist/         ← Stats, causal inference, experimental design
    ├── ux-designer/            ← User journeys, interaction design, accessibility
    └── curator/                ← Knowledge management, atomic notes, cross-links
```

Profiles symlink to the shared `skills/` directory, so one copy of each
skill serves every profile. Git tracks symlinks by reference, not by
duplicating content.

## Using a Profile

```bash
# Clone the repo
git clone https://github.com/magnus919/hermes-profiles.git ~/hermes-profiles

# Symlink the profile you want into ~/.hermes/profiles/
# (11 profiles available — pick one)
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
