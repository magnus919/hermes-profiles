# SkillOpt Pipeline Integration

The SkillOpt skill (magnus919/hermes-SkillOpt) uses artifact-pyramids as its native output format for all phase artifacts. This is a worked example of using pyramids for **pipeline outputs** — not research reports, but structured evaluation results consumed by downstream pipeline phases.

## Architecture

SkillOpt phases produce per-epoch dossiers that all land in a **single unified pyramid** at the run's state directory root. All raw JSON data goes flat into `03-dossiers/` with epoch-prefixed filenames. Root-level files (`00-index.md`, `01-summary/findings.md`, `02-analysis/`) are **amended** as epochs complete.

```
<state_dir>/
├── 00-index.md                     ← amended per epoch: epoch list, navigation
├── 01-summary/findings.md          ← amended per epoch: final_epoch, scores
├── 02-analysis/
│   ├── epoch-trajectory.md         ← amended per epoch: trend row appended
│   └── epoch-1-overview.md         ← new per epoch: phase results + SOURCES
└── 03-dossiers/                    ← flat, no subdirectories
    ├── epoch-1-baseline.json
    ├── epoch-1-validation-edit-1.json
    └── epoch-2-baseline.json
```

Each epoch overview is consumed by the next pipeline phase — the merge phase reads dossiers from `03-dossiers/` to find accepted edit IDs, then loads individual result JSON files. This is the **composite pyramid synthesis** pattern: the merge phase synthesizes results from multiple L3 dossiers into a decision.

**Key constraint:** `03-dossiers/` contains only flat files. Subdirectories are not allowed. Use epoch-prefixed filenames instead: `epoch-1-baseline.json`, `epoch-2-validation-edit-3.json`, etc.

## Key Differences from Research Pyramids

| Dimension | Research pyramid | Pipeline pyramid |
|-----------|-----------------|-----------------|
| Consumer | Human or downstream agent | Automated pipeline phase |
| L1 format | Free-text summary | YAML frontmatter (machine-parseable) |
| L3 schema | Source excerpts, transcripts | Structured JSON with fixed schema |
| Navigation | SOURCES links to analysis files | SOURCES links to L3 by edit/task ID |
| Update pattern | Written once, read by humans | Read programmatically, amended per epoch into root pyramid |

## Pattern: L1 Frontmatter for Machine Consumers

Pipeline pyramids store structured metrics in YAML frontmatter that downstream phases parse via `json.loads()`:

```yaml
epoch: 2
total_edits: 4
accepted: 3
rejected: 1
accept_rate: 0.75
avg_pass_rate_delta: 0.08
accepted_edits:
  - edit_id: edit-1
    acceptance_reason: weighted_score_non_regression
  - edit_id: edit-2
    acceptance_reason: weighted_score_non_regression
rejected_edits:
  - edit_id: edit-3
    acceptance_reason: pass_rate_regression
```

## Pattern: L2 Analysis as Decision Support

L2 files are structured as per-item sections with consistent fields — the merge phase reads L2 to find which edits to apply and which to skip:

```markdown
## edit-1 (replace)
- **Reason:** weighted_score_non_regression
- **Delta:** +0.33 pass rate
- **Score delta:** +0.2359 weighted score

SOURCES (LAYER 3 NAVIGATION)
03-dossiers/edit-1.json
 -> Raw validation result for edit-1
```

## Reference

- SkillOpt repo: https://github.com/magnus919/hermes-SkillOpt
- Artifact-pyramid phase outputs tracking: skillopt/references/artifact-pyramid-phase-outputs.md
- Baseline cache: PR #23
- Validation results: PR #29, issue #24
