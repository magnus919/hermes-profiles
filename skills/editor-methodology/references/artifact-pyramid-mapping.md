# Artifact Pyramid Mapping — Editor Profile

How the editor's methodologies and passes map into the universal artifact pyramid structure. The artifact-pyramids skill owns the folder hierarchy and navigation rules. This reference owns the mapping of editorial outputs into that hierarchy.

## Editorial Outputs by Pass

| Pass | Modifies file? | Produces | Maps to |
|------|---------------|----------|---------|
| humanize | Yes | Changelog of rhythm/voice changes | L3 (`humanize-changelog.md`) |
| fact-check | No (report) | Per-claim audit with verification status | L2 (`fact-check-report.md`) + L3 (`fact-check-verification-log.md`) |
| voice-check | No (report) | Drift locations with suggested rewordings | L2 (`voice-drift-report.md`) + L3 (`voice-consistency-map.md`) |
| engagement-review | No (report) | Missed opportunities, anecdote prompts | L2 (`engagement-report.md`) + L3 (`engagement-rewrite-proposals.md`) |
| source-integrity | No (report) | AI deliberation handling issues | L2 (noted in `recommended-actions.md` when present) |
| structural editing | Judgment call | Section ordering, cuts, argument fixes | L2 (`structural-findings.md`) |

## Pyramid Directory Structure

```
<editor-output>/<draft-slug>/
├── 00-index.md
├── 01-summary/
│   └── editorial-verdict.md
├── 02-analysis/
│   ├── structural-findings.md
│   ├── fact-check-report.md
│   ├── voice-drift-report.md
│   ├── engagement-report.md
│   └── recommended-actions.md
├── 03-dossiers/
│   ├── fact-check-verification-log.md
│   ├── voice-consistency-map.md
│   ├── engagement-rewrite-proposals.md
│   └── humanize-changelog.md
```

## Layer Definitions

### L1 — Editorial Verdict (`01-summary/editorial-verdict.md`)

One file. The entry point for every downstream consumer.

**Contents:**
- Overall verdict: **Ready to publish** / **Needs revision** / **Needs substantial rework**
- Priority count table:
  - Publication-blocking issues: N
  - Substantive findings: N
  - Voice drift flags: N
  - Engagement opportunities: N
- The single biggest structural insight: what's the #1 thing holding this piece back?
- Draft status: humanize pass applied, draft modified at `<path>`

**Consumed by:** Orchestrator making a promote/block decision. Author needing the TL;DR. Copy-editor checking whether it's worth starting their pass.

### L2 — Analysis Collection (`02-analysis/`)

One file per editorial dimension. Each file is self-contained: you can read `fact-check-report.md` without loading any other L2 file.

| File | Purpose | Key sections |
|------|---------|-------------|
| `structural-findings.md` | Argument coherence, section ordering, cuts/additions | Cuts recommended, reorderings suggested, structural gaps identified |
| `fact-check-report.md` | Per-claim audit with status | Publication-blocking, needs qualification, verified, unable to verify |
| `voice-drift-report.md` | Tone/persona consistency findings | Drift locations with current/suggested/why per flag |
| `engagement-report.md` | Reader connection opportunities | Missed hooks, anecdote prompts, weak conclusions, transition gaps |
| `recommended-actions.md` | **Prioritized action list (author-facing)** | Grouped by severity: must-fix → should-fix → consider. Pulls from all four reports above |

**`recommended-actions.md` is the most-consumed L2 file.** It's the bridge between "here are the findings" and "here's what the author should do." It groups actions by severity and notes which L2 file each action came from.

**Consumed by:** Author deciding what to fix. Writer receiving the editorial report. Copy-editor preparing their pass.

### L3 — Dossiers (`03-dossiers/`)

Detailed work product pulled on demand — when someone challenges a specific finding or needs to verify the editing work.

| File | Purpose | When to pull |
|------|---------|-------------|
| `fact-check-verification-log.md` | Every source consulted, what it actually said, full quotes | When challenging a fact-check finding, or verifying a specific claim |
| `voice-consistency-map.md` | Paragraph-level register analysis across the full draft | When the voice-drift report's flags need more surrounding context |
| `engagement-rewrite-proposals.md` | Full proposed wording for each engagement suggestion | When the author wants to evaluate a suggestion before applying it |
| `humanize-changelog.md` | Diff of rhythm/voice changes applied by the humanize pass | When the copy-editor needs to know what changed and why |

**Consumed by:** Anyone verifying a finding, the copy-editor (to understand what humanize changed), the author pushing back on a specific suggestion.

## SOURCES Navigation Convention

Every file at every layer ends with a SOURCES section. The format:

```
## SOURCES (LAYER N NAVIGATION)

/path/to/deeper/file.md
 -> Description: what will I find if I go deeper?
```

**L1 SOURCES** links to all five L2 files plus the draft file path.

**L2 SOURCES** links to the relevant L3 dossiers plus the draft file path.

**L3 SOURCES** links to the draft file path and any external sources consulted.

The draft file path appears in SOURCES at every layer — it's the primary material the editor worked on.

## Partial Pyramids

Not every editorial run produces all three layers:

- **Quick read (no facts to verify):** L1 verdict + L2 structural + voice + engagement. No L3 fact-check dossier. Omit `03-dossiers/fact-check-verification-log.md` and `03-dossiers/engagement-rewrite-proposals.md` if no rewrites were proposed.
- **Short piece under 1,500 words:** L1 + L2 only. Everything fits. Omit `03-dossiers/` entirely.
- **Full pipeline on 3,000+ word piece:** All three layers, all files.

Do NOT create empty directories or placeholder files. Only create what the editorial work actually produced.

## Dimension Boundaries

Each L2 file covers one editorial dimension. Cross-cutting findings go into `recommended-actions.md`, not into a separate cross-cutting file.

The dimension boundaries:

| Dimension | Owns | Does NOT own |
|-----------|------|-------------|
| Structural | Section ordering, argument coherence, cuts/additions | Sentence-level rhythm (humanize), factual accuracy (fact-check) |
| Factual | Claim verification, source checking, paraphrase drift | Whether the claim is well-argued (structural), whether it reads well (voice) |
| Voice | Tone consistency, register drift, persona matching | Grammar and punctuation (copy-editor), factual accuracy (fact-check) |
| Engagement | Reader connection, hooks, conclusions, transitions | Whether the argument is correct (structural), whether claims are true (fact-check) |

A finding that touches two dimensions goes into both files with a cross-reference. The `recommended-actions.md` file synthesizes them into a single action item.

## When the Draft Needs Restructuring

Sometimes the structural pass produces a recommendation to reorder or significantly reshape the draft. When that happens:

1. The recommendation goes into `structural-findings.md` with specific before/after ordering.
2. The `recommended-actions.md` file marks it as **must-fix** (highest severity).
3. The editor does NOT restructure the file — that's the author's or writer's decision.
4. The verdict in L1 becomes **Needs substantial rework** rather than **Needs revision**.

The copy-editor should NOT start their pass until structural issues are resolved. The `recommended-actions.md` file notes this dependency.

## Integration with the Editorial Pipeline

The artifact pyramid is produced across the full editorial pipeline:

```
humanize → fact-check → voice-check → engagement-review → source-integrity
   ↓            ↓             ↓               ↓                  ↓
 L3           L2+L3        L2+L3           L2+L3              L2 (if issues found)
 changelog    report+log   report+map      report+proposals   note in recommended-actions
```

After all five passes complete, the editor synthesizes:
1. Write `recommended-actions.md` by pulling from all four L2 reports.
2. Write `editorial-verdict.md` as the L1 summary.
3. Write `00-index.md` with the navigation table.
4. Respond to the caller with the path to `00-index.md`.
