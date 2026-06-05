# OSS-Contributor Profile — Agent Guidance

## Trigger Patterns

| User Says | What It Means |
|---|---|
| "Contribute to this project" | Full workflow: assess → fork → branch → implement → PR → release |
| "File a bug report for X" | Issue-focused: reproduction, environment, expected behavior |
| "Review their CONTRIBUTING.md" | Project norms assessment |
| "Open a cross-fork PR" | Fork name differs from upstream — requires API workaround |
| "Cut a release for X" | Release lifecycle: version bump → CHANGELOG → tag → GitHub Release → publish |
| "Publish X to PyPI" | Package build, credential verification, idempotent publish, version check |

## Loading Order

```python
skill_view('artifact-pyramids')
skill_view('opensource-contributions')
```

## Output Contract

Artifact pyramid. Response is the absolute path to `00-index.md`.
