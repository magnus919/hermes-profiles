# Case Study: Hermes Agent CONTRIBUTING.md

This is a real-world example of a well-written CONTRIBUTING.md from a project we've contributed to. It demonstrates everything a good contributing guide can cover.

**Source:** https://github.com/NousResearch/hermes-agent/blob/main/CONTRIBUTING.md

## What It Covers

| Section | What We Learn |
|---|---|
| **Contribution Priorities** | Not all contributions are equal. This project explicitly prioritizes: bug fixes > cross-platform compatibility > security > performance > new skills > new tools > docs. Knowing this tells you where your contribution effort is most welcome. |
| **Skill vs Tool Decision Guide** | A detailed framework for deciding whether a capability should be a skill or a tool. The answer is almost always "skill." Also covers bundled vs optional vs Skills Hub placement. |
| **Development Setup** | Exact commands needed to set up a local dev environment. If we'd read this, we'd have known about `--recurse-submodules`, the specific `uv venv --python 3.11`, and `uv pip install -e ".[all,dev]"`. |
| **Project Structure** | Maps the entire codebase so you know where your change goes. |
| **Architecture Overview** | Core loop, key design patterns, provider abstraction. Essential context before modifying agent behavior. |
| **Code Style** | PEP 8 with practical exceptions. Comments only for non-obvious intent. Cross-platform rules. |
| **Adding a New Tool** | Self-registering pattern with `registry.register()`, auto-discovery, toolset wiring in `toolsets.py`. |
| **Adding a Skill** | SKILL.md format with frontmatter, platform-specific skills, conditional activation, required env vars, skill guidelines (no external deps, progressive disclosure). |
| **Cross-Platform Compatibility** | Extensive rules for Windows compatibility (16 specific rules). This is a huge section — cross-platform care matters to this project. |
| **Security Considerations** | Existing protection layers, what to do when contributing security-sensitive code. |
| **PR Process** | Branch naming (`fix/`, `feat/`, etc.), what to test before submitting, PR description format, Conventional Commits. |
| **License** | By contributing, you agree to MIT licensing. |

## Common Contributor Mistakes This Prevents

Reading the contributing guide *before* starting work prevents common mismatches between contributor intent and maintainer expectations:

1. **Branch naming** — Using project-standard prefixes (`fix/`, `feat/`) instead of arbitrary names
2. **Commit messages** — Following the project's commit format requirements instead of defaulting to freeform
3. **Tests** — Running the project's test suite before submission
4. **Development setup** — Using the project's exact dev environment commands instead of guessing
5. **PR description format** — Filling out the project's PR template rather than writing a freeform summary
6. **Skill/tool classification** — Understanding where different types of changes belong in the project structure
7. **Cross-platform considerations** — Checking for platform-specific requirements the project enforces

## Key Takeaway

Even a single READ of CONTRIBUTING.md before starting work would have caught most of these. The document exists to prevent exactly this kind of mismatch between contributor intent and maintainer expectations.
