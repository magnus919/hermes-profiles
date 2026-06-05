# Report Templates

Standardized output formats for each editorial pass. Consistent structure means the consumer (author, writer, copy-editor, orchestrator) knows where to look in any report.

## Editorial Verdict (L1)

```markdown
# Editorial Verdict: <draft title>

**Verdict:** Ready to publish | Needs revision | Needs substantial rework

| Priority | Count |
|----------|-------|
| Publication-blocking | N |
| Substantive findings | N |
| Voice drift flags | N |
| Engagement opportunities | N |

**Key finding:** <One sentence: the single biggest thing holding this piece back, or what makes it strong enough to publish.>

**Draft status:** Humanize pass applied. Modified draft at `<absolute path>`.

---

## SOURCES (LAYER 2 NAVIGATION)

<pyramid-root>/02-analysis/structural-findings.md
 -> Argument coherence, section ordering, cuts, and additions
<pyramid-root>/02-analysis/fact-check-report.md
 -> Per-claim verification audit
<pyramid-root>/02-analysis/voice-drift-report.md
 -> Tone and persona consistency findings
<pyramid-root>/02-analysis/engagement-report.md
 -> Reader connection opportunities and anecdote prompts
<pyramid-root>/02-analysis/recommended-actions.md
 -> Prioritized action list grouped by severity
<draft-path>
 -> The humanize-modified draft file
```

## Structural Findings (L2)

```markdown
# Structural Findings: <draft title>

**Overall:** <One sentence: Coherent | Mostly coherent with flags | Needs restructuring>

## Argument thread

<One paragraph: what the piece is arguing, stated in the editor's words. Does the argument hold? Where does it break down?>

## Findings

### Cuts recommended

**<Section or paragraph>** — <reason>
Current: "<excerpt>"
Suggestion: "<what to do: move to callout, separate piece, or remove>"
Why: <one line>

### Reorderings suggested

**Move <X> before <Y>** — <reason>
Why: <one line>

### Structural gaps

**<What's missing>** — <where it should go>
Why: <one line>

## Working well

- <Section or passage that's structurally sound>

---

## SOURCES (LAYER 3 NAVIGATION)

<pyramid-root>/03-dossiers/humanize-changelog.md
 -> What rhythm and voice changes the humanize pass applied
<draft-path>
 -> The humanize-modified draft file
```

## Fact-Check Report (L2)

```markdown
# Fact-Check Report: <draft title>

**Overall:** Clear to publish | Needs correction | Hold — significant issues

**Claims checked:** N | **Verified:** N | **Issues:** N

## Publication-blocking

**Claim:** "<exact quote from draft>"
**Status:** Unverified | Incorrect | Fabrication risk
**What the source actually says:** <evidence>
**Suggested revision:** "<rewording>" or "Remove claim / find alternative source"
**Source consulted:** <URL(s)>

## Needs qualification

**Claim:** "<quote>"
**Issue:** <e.g., "True in 2023; may have shifted. Draft presents as current.">
**Suggested revision:** "<rewording with appropriate hedge>"

## Verified

- "<claim>" — confirmed against <source>

## Unable to verify

- "<claim>" — couldn't find primary source. Recommendation: remove, or ask author for original source.

---

## SOURCES (LAYER 3 NAVIGATION)

<pyramid-root>/03-dossiers/fact-check-verification-log.md
 -> Every source consulted with full quotes and metadata
<draft-path>
 -> The humanize-modified draft file
```

## Voice Drift Report (L2)

```markdown
# Voice Drift Report: <draft title>

**Overall:** Consistent | Mostly consistent with flags | Inconsistent

## Flags

**<Section heading or "Paragraph N">** — <issue type>
Current: "<excerpt>"
Suggestion: "<specific rewording>"
Why: <one line>

## Site-specific drift

<If site profile was loaded, any deviations from the site's editorial stance.>

## Working well

- <Passage or section that's strongly in voice — preserve these>

---

## SOURCES (LAYER 3 NAVIGATION)

<pyramid-root>/03-dossiers/voice-consistency-map.md
 -> Full paragraph-level register analysis with surrounding context
<draft-path>
 -> The humanize-modified draft file
```

## Engagement Report (L2)

```markdown
# Engagement Report: <draft title>

**Overall:** Strong | Solid with opportunities | Flat

## Missed opportunities

**<Section or "Paragraph N">** — <type of opportunity>
Current: "<excerpt>"
Suggestion: "<specific wording>" or "Ask author: <prompt for real material>"
Why: <one line on what this adds>

## Anecdote prompts (author input needed)

- <claim in draft>: Do you have a specific experience you can attach here?
- <section>: This would land harder with a named real example. Any come to mind?

## Strong engagement moments

- <Passage that's landing well; preserve in future edits>

---

## SOURCES (LAYER 3 NAVIGATION)

<pyramid-root>/03-dossiers/engagement-rewrite-proposals.md
 -> Full proposed wording for each suggestion
<draft-path>
 -> The humanize-modified draft file
```

## Recommended Actions (L2 — author-facing)

```markdown
# Recommended Actions: <draft title>

**Verdict:** <from L1>

## Must-fix (publication-blocking)

1. **<Action>** — <from which L2 report> — <one-line reason>
2. ...

## Should-fix (substantive)

1. **<Action>** — <from which L2 report> — <one-line reason>
2. ...

## Consider (improvements)

1. **<Action>** — <from which L2 report> — <one-line reason>
2. ...

## Dependency notes

<Note any ordering dependencies: "Fix structural issue #1 before applying engagement suggestion #3, since the section may be cut.">

---

## SOURCES (LAYER 2 DETAIL)

<pyramid-root>/02-analysis/structural-findings.md
 -> Full structural analysis with cuts and reorderings
<pyramid-root>/02-analysis/fact-check-report.md
 -> Per-claim verification audit
<pyramid-root>/02-analysis/voice-drift-report.md
 -> Voice consistency findings with suggested rewordings
<pyramid-root>/02-analysis/engagement-report.md
 -> Reader connection opportunities and anecdote prompts
```

## Index File (00-index.md)

```markdown
# Editorial Review: <draft title>

## Navigation

| Layer | File | Description |
|-------|------|-------------|
| **L1** | `01-summary/editorial-verdict.md` | Overall verdict, priority counts, key finding |
| **L2** | `02-analysis/recommended-actions.md` | Prioritized action list (start here after L1) |
| **L2** | `02-analysis/structural-findings.md` | Argument coherence, section ordering |
| **L2** | `02-analysis/fact-check-report.md` | Per-claim verification audit |
| **L2** | `02-analysis/voice-drift-report.md` | Tone and persona consistency |
| **L2** | `02-analysis/engagement-report.md` | Reader connection opportunities |
| **L3** | `03-dossiers/fact-check-verification-log.md` | Every source consulted, full quotes |
| **L3** | `03-dossiers/voice-consistency-map.md` | Paragraph-level register analysis |
| **L3** | `03-dossiers/engagement-rewrite-proposals.md` | Full wording for each suggestion |
| **L3** | `03-dossiers/humanize-changelog.md` | Rhythm and voice change log |

## Draft file

The humanize-modified draft is at: `<absolute path>`

---

## SOURCES

<pyramid-root>/01-summary/editorial-verdict.md
 -> The one-paragraph editorial verdict
<pyramid-root>/02-analysis/recommended-actions.md
 -> What to fix, in priority order
<draft-path>
 -> The modified draft file
```
