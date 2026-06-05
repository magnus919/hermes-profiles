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
│   ├── mermaid-diagrams/
│   └── product-methodology/
└── profiles/
    ├── technical-architect/    ← Systems architecture: C4 + ADRs + arc42
    │   ├── SOUL.md
    │   ├── profile.yaml
    │   ├── README.md
    │   └── AGENTS.md
    └── product-manager/        ← Product management: specs, prioritization, strategy
        ├── SOUL.md
        ├── profile.yaml
        ├── README.md
        └── AGENTS.md
```

Profiles symlink to the shared `skills/` directory, so one copy of each
skill serves every profile. Git tracks symlinks by reference, not by
duplicating content.

## Using a Profile

```bash
# Clone the repo
git clone https://github.com/magnus919/hermes-profiles.git ~/hermes-profiles

# Symlink the profile you want into ~/.hermes/profiles/
ln -s ~/hermes-profiles/profiles/technical-architect ~/.hermes/profiles/
# or
ln -s ~/hermes-profiles/profiles/product-manager ~/.hermes/profiles/

# Switch to profile (skills are bundled — no separate install needed)
hermes --profile technical-architect
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
