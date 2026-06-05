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
├── profiles/
│   ├── technical-architect/    ← Example profile
│   │   ├── SOUL.md             ← Identity, first principles
│   │   ├── profile.yaml        ← Metadata, skill dependencies
│   │   ├── README.md           ← Usage guide
│   │   └── AGENTS.md           ← Agent trigger patterns, handoff
│   └── ... (more to come)
├── LICENSE
└── README.md
```

## Using a Profile

```bash
# Clone the repo
git clone https://github.com/magnus919/hermes-profiles.git

# Install profile into ~/.hermes/profiles/
cp -r profiles/technical-architect ~/.hermes/profiles/

# Install required skills (see profile.yaml for list)
hermes skills install <skill-name>

# Switch to profile
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
