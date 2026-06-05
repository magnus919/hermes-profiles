# Editorial Pipeline Reference

The canonical five-pass sequence for editorial review before publication. Order matters. Skipping a pass is a deliberate decision, not an oversight.

## The Five Passes

### Pass 1: Humanize

**Purpose:** Rhythm, voice markers, AI-pattern elimination.
**Modifies file:** Yes. This is the only pass that writes to the draft.
**Duration:** Longest pass. Reads the full draft multiple times.

**What it does:**
- Varies sentence length and paragraph rhythm
- Eliminates AI enumeration patterns (3+ consecutive same-structure paragraphs)
- Replaces robotic transitions ("Furthermore", "Moreover", "Additionally")
- Enforces contractions in narrative prose
- Removes emdashes (replacing with semicolons, commas, colons, or sentence breaks)
- Adds natural voice markers where the text sounds too clinical

**What it does NOT do:**
- Rewrite arguments or change structure (that's structural editing)
- Verify facts (that's fact-check)
- Check tone consistency (that's voice-check)

**Verification:** After humanize completes, run:
- `grep -c '—' <path>` — should return 0 (or only hits in HTML cards/captions)
- `grep -nE '\b(is not|are not|do not|cannot)\b' <path>` — flag any remaining full-form negatives in narrative prose

**Artifacts produced:** `humanize-changelog.md` (L3 dossier)

### Pass 2: Fact-Check

**Purpose:** Verify factual claims against reputable sources.
**Modifies file:** No. Report only.
**Dependencies:** None. Can run in parallel with Pass 3 if needed.

**What it does:**
- Extracts every verifiable claim from the draft
- Checks each claim against its cited source (or searches for primary source)
- Cross-references when possible (two independent sources agreeing)
- Checks recency of statistics
- Flags paraphrase drift (draft misstates what its own source says)
- Catches quote fabrication or drift

**Severity levels:**
- Publication-blocking: wrong quotes, fabricated stats, misattributed research
- Needs qualification: dated data, context-dependent claims stated as universal
- Verified: confirmed against source (still reported as evidence of cleanliness)

**Artifacts produced:** `fact-check-report.md` (L2) + `fact-check-verification-log.md` (L3)

### Pass 3: Voice-Check

**Purpose:** Tone and persona consistency across the full draft.
**Modifies file:** No. Report only.
**Dependencies:** None. Can run in parallel with Pass 2.

**What it does:**
- Checks register consistency (formality level, contractions, pronouns)
- Checks tone consistency (warmth, humor flavor, confidence level)
- Checks complexity transfer (technical content presented conversationally)
- Checks transitions between sections
- Checks against site-specific voice (if site profile provided)
- Flags universal voice rule violations (emdashes, missing Oxford commas, AI phrases)

**Artifacts produced:** `voice-drift-report.md` (L2) + `voice-consistency-map.md` (L3)

### Pass 4: Engagement Review

**Purpose:** Reader connection opportunities.
**Modifies file:** No (report only), unless author explicitly asks to apply suggestions.
**Dependencies:** Should run after humanize (Pass 1) to avoid double-work.

**What it does:**
- Flags abstract passages without reader hooks
- Flags information dumps without reflective pauses
- Identifies missing personal anecdote opportunities (asks author, doesn't fabricate)
- Flags missing "imagine if" scenarios
- Catches unaddressed pushback to strong claims
- Evaluates conclusion strength
- Identifies missed calls to action

**Artifacts produced:** `engagement-report.md` (L2) + `engagement-rewrite-proposals.md` (L3)

**Critical note:** When engagement suggestions are applied to the draft, they often reintroduce emdashes and mechanical drift. The copy-editor pass MUST run after engagement suggestions are applied.

### Pass 5: Source Integrity

**Purpose:** Rules for handling AI-generated deliberation in published content.
**Modifies file:** No. Report only (or notes in recommended-actions).
**Dependencies:** Can run at any point.

**What it does:**
- Checks whether AI deliberation outputs (council debates, multi-agent discussions) are properly framed
- Ensures no simulated personas are presented as real authorities
- Verifies that speculative claims are labeled as such
- Flags any references to internal agent infrastructure

**Artifacts produced:** Noted in `recommended-actions.md` when issues are found. No separate file when clean.

## Pipeline Execution Order

```
Pass 1 (humanize) → Pass 2 (fact-check) → Pass 3 (voice-check) → Pass 4 (engagement) → Pass 5 (source-integrity)
```

**Why this order:**

1. **Humanize first** — does bulk rhythm work. Running it first means later passes don't create double-work by fixing rhythm that humanize already addressed.
2. **Fact-check and voice-check** produce reports without modifying the file. They can technically run in parallel, but running fact-check first is safer because a wrong claim might invalidate voice suggestions for that section.
3. **Engagement fourth** — its suggestions (when applied) introduce parenthetical asides and conversational transitions that often use emdashes. This is the primary source of emdash reintroduction after humanize has already cleaned them.
4. **Source-integrity last** — usually a quick check that doesn't depend on other passes.

## Post-Pipeline Synthesis

After all five passes complete:

1. **Write `recommended-actions.md`** — pull from all four L2 reports and synthesize into a prioritized action list:
   - Must-fix (publication-blocking): factual errors, fabrication risks, structural issues that invalidate downstream claims
   - Should-fix (substantive): missing sources, voice drift, engagement dead spots
   - Consider (surface): minor rhythm improvements, optional anecdote additions

2. **Write `editorial-verdict.md`** — L1 summary with the verdict, priority counts, and the single biggest finding.

3. **Write `00-index.md`** — navigation table linking to all pyramid files.

4. **Respond to caller** with the absolute path to `00-index.md`.

## Skipping Passes

Not every draft needs every pass:

- **Voice-check:** Skip if the draft is short (under 1,000 words) and the writer's voice is strong throughout.
- **Engagement-review:** Skip for technical reference content that isn't trying to engage (documentation, reference pages).
- **Source-integrity:** Skip if the draft has no AI deliberation artifacts and makes no speculative claims.
- **Fact-check:** Never skip on pieces making substantive factual claims. Only skip for purely opinion/perspective pieces with no verifiable claims.

When a pass is skipped, note it in `recommended-actions.md` as "Pass skipped: [reason]."

## Pipeline for Pulitzer-Style Pieces

Write-pulitzer pieces have different engagement dynamics:
- Engagement-review applies differently — don't suggest breaking the narrative frame with rhetorical questions
- Voice-check allows intentional register variation across dramatic beats
- The conclusion is a resonance, not a summary — engagement-review evaluates whether it lands rather than whether it hooks

When the draft is Pulitzer-style, note this in the L1 verdict and adjust engagement and voice criteria accordingly.
