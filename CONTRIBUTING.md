# Contributing to Hermes Profiles

Thanks for considering adding a profile to the collection. Here's what makes a good profile.

## Profile Requirements

Every profile directory must contain these four files:

| File | Purpose |
|---|---|
| `SOUL.md` | Identity document — first principles, output contract, methodology mandate |
| `profile.yaml` | Metadata — description, required skills, recommended skills |
| `README.md` | Usage guide — installation, quick start, skill reference |
| `AGENTS.md` | Agent guidance — trigger patterns, loading order, handoff protocol |

## Skill Sharing

Profiles share skills through the root-level `skills/` directory. Each profile's
`skills/` directory contains **relative symlinks** back to the shared pool:

```
skills/                          ← Actual skill files (one copy)
└── some-skill/
    ├── SKILL.md
    └── references/
profiles/some-profile/skills/    ← Symlinks
    └── some-skill -> ../../../skills/some-skill
```

- **Do not** copy skill files into a profile directory. Use symlinks.
- **Do not** use absolute symlink paths. Use relative paths from the profile's
  `skills/` directory back to the repo root `skills/` directory.
- If a profile needs a skill that doesn't exist in the shared pool, add the
  skill to `skills/` first, then symlink from the profile.

## Skill Design Guidelines

Skills in the shared pool should:

- Have a clear, single responsibility
- Be Hermes-native (artifact-pyramid output, skill-based methodology loading)
- Use progressive disclosure — SKILL.md as thin index, methodology in references/
- Not depend on agent-specific infrastructure (council, cashew, etc.)
- Work on a vanilla Hermes install

## Profile Design Guidelines

- Each profile should have a clear role with distinct first principles
- SOUL.md should capture what makes this role think differently from others
- The output contract should be artifact-pyramid format (path-as-handoff)
- Cross-reference related profiles in SOUL.md (e.g., "works alongside technical-architect")

## Getting Started

```bash
# Fork the repo
gh repo fork magnus919/hermes-profiles --clone

# Create your profile
mkdir -p profiles/your-profile/skills
cp -r profiles/technical-architect/SOUL.md profiles/your-profile/
# ... edit SOUL.md, profile.yaml, README.md, AGENTS.md ...

# Link shared skills
ln -s ../../../skills/artifact-pyramids profiles/your-profile/skills/

# Commit and PR
git checkout -b feat/your-profile
git add profiles/your-profile
git commit -m "feat: add your-profile"
gh pr create
```

## License

By contributing, you agree that your contributions will be licensed under the
project's MIT license.
