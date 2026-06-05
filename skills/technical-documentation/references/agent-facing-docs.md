# Agent-Facing Documentation

## AGENTS.md Structure

Agent-facing docs have different requirements than human-facing docs. Agents read the entire file sequentially, so structure matters differently.

### Required Sections

```markdown
# Project Name — Agent Guidance

## Trigger Patterns

| User Says | What It Means |
|---|---|
| "Deploy this service" | Full deployment: build → configure → deploy → verify |
| "Check service status" | Status check with health endpoint verification |

## Loading Order

Specify which skills to load and in what order. Skills should be loaded explicitly,
not assumed.

\`\`\`python
skill_view('artifact-pyramids')    # 1. Output format
skill_view('deployment-methodology')  # 2. Methodology
\`\`\`

## Output Contract

Be explicit about what the agent produces and how to interpret it. If using
artifact pyramids, say so.
```

## Skill Documentation

When documenting a skill for agent consumption:

| Element | Required | Purpose |
|---------|----------|---------|
| Trigger conditions | Yes | When does an agent know to load this skill? |
| Loading order | Yes | What to load first, what depends on what |
| Reference files table | Yes | What each reference is for and when to load it |
| Output contract | Yes | What format does the agent produce? |
| Pitfalls | Recommended | What commonly goes wrong? |
