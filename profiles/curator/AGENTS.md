# Curator Profile — Agent Guidance

## Trigger Patterns

| User Says | What It Means |
|---|---|
| "Organize these notes on X" | Full curation: ingest → atomize → link → structure → pyramid |
| "Connect Y to related topics" | Cross-linking and relationship discovery |
| "Synthesize information about Z" | Multi-source synthesis into connected knowledge structure |
| "Clean up the vault on topic W" | Vault maintenance: deduplication, broken links, consistency |

## Loading Order

```python
skill_view('artifact-pyramids')  # 1. Output format
```

## Output Contract

Artifact pyramid. Response is the absolute path to `00-index.md`.
