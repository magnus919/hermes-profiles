# Nested Pyramid Pattern — Unified Single Hierarchy for Multi-Artifact Systems

When a single system produces multiple distinct artifact streams (rollout records, validation results, proposals, baseline metrics, meta-reflections), the natural instinct is to create a separate pyramid directory for each stream:

```
❌ Scatter — 6 independent pyramids
<state_dir>/
├── baseline/epoch-N/00-index.md
├── validation/epoch-N/00-index.md
├── rollout/epoch-N/00-index.md
├── reflection/epoch-N/00-index.md
├── proposal/epoch-N/00-index.md
├── slow-meta/epoch-N/00-index.md
└── run-summary.json
```

This forces a consumer to check 6 entry points to understand what's available. Each pyramid is disconnected from the others — no cross-referencing, no shared navigation.

## The Unified Alternative

Nest all artifact streams under a single root pyramid. Each epoch's data lives flat in `03-dossiers/` with epoch-prefixed filenames. Root-level files are **amended** as new epochs complete — they grow to reflect the current state.

```
✅ Unified — single navigable tree (flat 03-dossiers/)
<state_dir>/
├── 00-index.md                          ← AMENDED per epoch: navigation links, epoch list
├── 01-summary/findings.md              ← AMENDED per epoch: updated final_epoch, scores
├── 02-analysis/
│   ├── epoch-trajectory.md             ← AMENDED per epoch: appended trend row
│   └── epoch-1-overview.md             ← NEW per epoch: phase summary + SOURCES → dossiers
└── 03-dossiers/                        ← FLAT: no subdirectories
    ├── epoch-1-baseline.json
    ├── epoch-1-validation-edit-1.json
    ├── epoch-1-validation-edit-2.json
    ├── epoch-1-rollout-task-train-1.json
    ├── epoch-1-reflection.json
    ├── epoch-1-proposals.json
    ├── epoch-2-baseline.json
    ├── epoch-2-validation-edit-1.json
    └── epoch-2-slowmeta.json
```

### Critical constraint: 03-dossiers/ is flat

**03-dossiers/ MUST NOT contain subdirectories.** The artifact-pyramid spec defines the dossier layer as the broadest, flattest reference library. Subdirectories inside 03-dossiers/ violate the spec's flat-file contract.

Use epoch-prefixed filenames instead of nested directories:

| ❌ Wrong (subdirectories) | ✅ Correct (flat naming) |
|---|---|
| `03-dossiers/epoch-1/baseline.json` | `03-dossiers/epoch-1-baseline.json` |
| `03-dossiers/epoch-1/rollout/task-1.json` | `03-dossiers/epoch-1-rollout-task-1.json` |
| `03-dossiers/epoch-1/validation/edit-1.json` | `03-dossiers/epoch-1-validation-edit-1.json` |

Naming convention: `epoch-<N>-<phase>[-<item>].json`

### Amending pattern

Root-level files are never rewritten from scratch. They are amended as epochs complete:

| File | Action per epoch |
|---|---|
| `00-index.md` | Update epoch list + navigation links to new epoch overview |
| `01-summary/findings.md` | Update final_epoch, final_pass_rate, epoch count |
| `02-analysis/epoch-trajectory.md` | Append new row to trajectory table |
| `02-analysis/epoch-N-overview.md` | Always new — never modifies a previous epoch |
| `03-dossiers/epoch-N-*.json` | Always new — never modifies previous epoch files |

The amending pattern means a consumer reading `00-index.md` sees the current state of the entire run. Progressively deeper files (epoch overviews, dossiers) are fixed once written and never change.

## Navigation Flow

```
00-index.md
  └─ SOURCES → 01-summary/findings.md
                  └─ SOURCES → 02-analysis/epoch-trajectory.md
                  └─ SOURCES → 02-analysis/epoch-1-overview.md
                                  └─ SOURCES → 03-dossiers/epoch-1-baseline.json
                                  └─ SOURCES → 03-dossiers/epoch-1-validation-edit-1.json
```

A consumer reading the root `00-index.md` can navigate to any epoch or any phase by following SOURCES links directly to the flat dossiers in `03-dossiers/`. No nested 00-index to traverse — the epoch overview IS the entry point for that epoch.

## When to Use

Use the nested pyramid pattern when:
- A system produces 3+ distinct artifact types over time
- Artifacts share a common temporal dimension (epochs, rounds, iterations)
- A consumer needs to understand the system's full output at a glance
- You want to avoid filesystem sprawl from parallel directory structures

## When NOT to Use

- Single-turn research tasks that produce one artifact (use the standard flat pyramid)
- Systems where artifact streams are owned by completely independent subsystems (use composite pyramid synthesis instead)

## Relationship to Composite Pyramid Synthesis

The composite pyramid pattern merges outputs from **multiple independent agents** (e.g., a research pipeline where each subagent produces its own pyramid). The nested pyramid pattern organizes outputs from **a single system** into one hierarchy. They solve different problems:
- Composite: merging independent agent pyramids into a root-level synthesis
- Nested: designing a single system's output tree from scratch

## Implementation Pattern

When building a nested pyramid, use a shared writer function that all phases call after writing their L3 dossiers:

```python
def rebuild_epoch_pyramid(state_dir, epoch):
    """After any phase writes L3 dossiers, rebuild the epoch-level index/summary/analysis."""
    epoch_dir = os.path.join(state_dir, "03-dossiers", f"epoch-{epoch}")
    if not os.path.exists(epoch_dir):
        return
    # Scan for existing L3 dossiers
    # Read board-metadata.json for pass_rate_history
    # Write 00-index.md, 01-summary/findings.md, all 02-analysis/ files
    # Each 02-analysis file has SOURCES linking to its L3 dossiers
```

This centralizes the pyramid writing logic so each phase only produces its raw data (L3), and a single function handles the progressive disclosure wrapper.

## In This Session

This pattern was developed during the SkillOpt artifact-pyramid conversion session (2026-06-03). The pre-existing pattern was scatter (6 parallel directories for baseline, validation, rollout, reflection, proposal, slow-meta). The unified pattern consolidates everything under `<state_dir>/` with epoch-level nesting inside `03-dossiers/epoch-N/`.
