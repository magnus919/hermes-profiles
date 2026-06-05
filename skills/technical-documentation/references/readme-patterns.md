# README Patterns

## Every README Needs

1. **Project name and one-line description** — What is this? Why should I care?
2. **Quickstart** — The fastest path from zero to running. Copy-paste friendly.
3. **Installation** — All methods (package manager, source, Docker)
4. **Configuration** — Environment variables, config files, CLI flags
5. **Usage** — Basic usage with examples. Show the common patterns.
6. **API reference** — If a library/SDK, link to full API docs
7. **Contributing** — Link to CONTRIBUTING.md
8. **License** — One line, link to LICENSE

## Quickstart Pattern

```markdown
## Quickstart

\`\`\`bash
# Install
pip install my-tool

# Run with default config
my-tool analyze path/to/file

# View output
cat results.json
\`\`\`

That's it. For detailed options, see [Configuration](#configuration).
```

Key rules:
- Three commands max from zero to visible output
- Defaults should be sensible — no required configuration to "just try it"
- If Docker is an option, show it as `docker run`

## Installation Variants

```markdown
## Installation

### pip (recommended)
\`\`\`bash
pip install my-tool
\`\`\`

### Homebrew
\`\`\`bash
brew install my-tool
\`\`\`

### From source
\`\`\`bash
git clone https://github.com/user/my-tool.git
cd my-tool
pip install -e .
\`\`\`
```

Always list in preference order. Pre-release/alpha installs should be marked clearly.
