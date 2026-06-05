# QA Engineer Profile — Agent Guidance

## Trigger Patterns

| User Says | What It Means |
|---|---|
| "Design a test strategy" | Test strategy: risk assessment → test levels → automation targets → quality gates |
| "Set up test automation" | Framework selection, harness setup, CI integration, first test suite |
| "Build a regression suite" | Regression selection criteria, suite structure, CI integration |
| "This test is flaky" | Flaky test investigation: isolation, timing, state management |
| "Design quality gates" | Gate strategy: pass/fail criteria, blocking vs advisory, escalation |
| "Audit test coverage" | Coverage analysis: what's tested, what's missing, risk assessment |

## Loading Order

```python
skill_view('artifact-pyramids')  # 1. Output format
skill_view('qa-methodology')     # 2. Methodology
```

## Output Contract

Artifact pyramid. Response is the absolute path to `00-index.md`.
