# researcher-workflow — Agent Loading Instructions

## Skills

| Phase | Skill Name | File |
|-------|-----------|------|
| 1 | `researcher-workflow/receive-mission` | `skills/receive-mission.md` |
| 2 | `researcher-workflow/research-gather` | `skills/research-gather.md` |
| 3 | `researcher-workflow/evaluate-gaps` | `skills/evaluate-gaps.md` |
| 4 | `researcher-workflow/build-pyramid` | `skills/build-pyramid.md` |
| 5 | `researcher-workflow/deliver-findings` | `skills/deliver-findings.md` |

## Loading

Load the umbrella first to activate trigger detection:
```
skill_view(name='researcher-workflow')
```

Then load individual phase skills as needed:
```
skill_view(name='researcher-workflow/<skill-name>')
```

## Prohibitions

- Do NOT use web_search or web_extract tools — use groktocrawl
- Do NOT skip Phase 1 (receive-mission) — the orchestrator's brief needs interpolation
- Do NOT clean up /tmp/ artifacts — they expire naturally
