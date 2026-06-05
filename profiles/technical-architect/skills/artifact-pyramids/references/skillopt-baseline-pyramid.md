# Worked Example: SkillOpt Baseline Cache as Artifact Pyramid

The SkillOpt validate phase uses the artifact pyramid as a **machine-readable cache format**, not just a research output structure. This is a novel application: the pyramid serves as both a human-readable summary and a data source for downstream pipeline phases.

## The Problem

The validate phase needs to compare each proposed edit's performance against the unedited skill's baseline. The baseline must be:

1. **Cached** — re-running validate on the same epoch should skip the baseline run
2. **Machine-readable** — the merge phase reads per-task verdicts to compute deltas
3. **Human-readable** — operators inspecting the state directory should immediately understand the results
4. **Portable** — survives directory moves and operates independently of the generating machine

A single JSON file satisfies (1) and (2) but fails (3) and (4). The artifact pyramid satisfies all four.

## The Structure

```
<state_dir>/baseline/epoch-<N>/
├── 00-index.md                  ← navigation + provenance only (NO findings)
├── 01-summary/
│   └── findings.md              ← L1: YAML frontmatter metrics + summary
├── 02-analysis/
│   └── per-task-evaluation.md   ← L2: per-task pass/fail + quality + reasons
├── 03-dossiers/
│   └── task-<id>.json           ← L3: raw oneshot stdout/stderr per task
└── baseline.json                ← companion JSON snapshot (backwards compat)
```

## Layer Design Decisions

### L1 (01-summary/findings.md)

The L1 file uses **YAML frontmatter** for machine-parseable metrics and a markdown body for human readers:

```yaml
---
epoch: 3
pass_rate: 0.6667
tasks_passed: 2
tasks_failed: 1
total_tasks: 3
avg_quality_score: 0.7667
weighted_score: 0.7234
validation_context: skill_workspace_v1
metric_weights: {"pass_rate": 0.35, "quality_score": 0.35, "speed_score": 0.15, "token_efficiency": 0.15}
target: /path/to/skill/SKILL.md
created_at: 2026-06-03T21:38:05Z
---
```

The frontmatter is `json.loads()`-compatible (no yaml dependency needed) and contains every metric the downstream merge phase needs. The body provides human context.

### L2 (02-analysis/per-task-evaluation.md)

Per-task breakdown — one section per task with status, quality score, and reason:

```markdown
## Task: validation-task-1
**Status:** PASS | **Quality:** 0.9
**Reason:** Correctly handles the edge case

## Task: validation-task-2
**Status:** FAIL | **Quality:** 0.0
**Reason:** Missed required output format
```

### L3 (03-dossiers/task-<id>.json)

Raw oneshot output, stored with `"result"` key matching the data structure the downstream phase expects:

```json
{
  "task_id": "validation-task-1",
  "stdout": "...",
  "stderr": "",
  "result": {
    "pass": true,
    "quality_score": 0.9,
    "reason": "Correctly handles the edge case",
    "duration_seconds": 2.345,
    "token_estimate": 485
  }
}
```

## Cache Hit / Miss

| Path | Check | Action |
|------|-------|--------|
| Cache hit | `00-index.md` exists | Read L1 frontmatter for metrics, scan L3 dossiers for per-task detail. Validates `validation_context` field for staleness. |
| Cache miss | `00-index.md` absent | Run baseline validation tasks, write full pyramid structure |
| Corruption | L1 frontmatter unparseable | Log error, fall through to cache-miss path (recompute) |

## Key Boundary Rules (from output-classification-framework.md)

- **00-index.md** is navigation + provenance ONLY — no findings, no metrics, no verdict sentences
- **L1** answers "what should I do?" — the pass rate and weighted score, not the per-task breakdown
- **L2** answers "why should I do it?" — per-task evidence organized by task dimension
- **L3** answers "is this real?" — raw oneshot output verbatim

## Companion JSON Snapshot

A `baseline.json` is written alongside the pyramid for tools that need raw JSON access without parsing markdown. This ensures backward compatibility during migration and allows external scripts to consume baseline data without markdown parsing.

## Pitfalls

- **Key naming consistency:** L3 dossiers must use `"result"` key (not `"verdict"`) for the normalized verdict — the downstream `baseline_by_task` dict comprehension uses `detail.get("result", ...)`. Mismatch causes the cache-hit path to fall through to heuristic fallbacks.
- **Relative paths in SOURCES:** Use `02-analysis/per-task-evaluation.md` not `/absolute/path/to/02-analysis/...` — the pyramid must be portable.
- **`state_dir` ordering:** The baseline directory path is computed from `state_dir`, which must be assigned before it's used (Python executes module-level assignments in order).
