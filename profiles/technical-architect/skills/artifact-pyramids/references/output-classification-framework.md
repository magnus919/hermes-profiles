# Output Classification Framework

A role-agnostic system for mapping any specialist's outputs into the artifact pyramid, with strict layer-specific content contracts to eliminate duplication.

## The Problem

Every specialist profile (editor, researcher, technical-architect, product-manager, copy-editor, SEO specialist) independently answers the same question: *"Where does my stuff go in the pyramid?"*

Without a shared framework, this produces inconsistent mappings. The same type of output ends up in different layers across profiles. Content duplicates between `00-index.md` and `01-summary/`. The boundary between "navigation" and "verdict" blurs.

This framework fixes that by providing three classification questions any specialist can ask about their outputs, independent of domain.

## The Three Classification Questions

For every distinct type of output a specialist produces, ask:

### 1. Who consumes this?

The consumer determines the layer, because each consumer needs a different level of abstraction.

| Consumer | Example roles | What they need | Layer |
|----------|---------------|----------------|-------|
| **Decider** | Orchestrator, author, pipeline gate | A verdict and priority actions. "Should I ship this? What should I fix first?" | **L1 (Summary)** |
| **Practitioner** | The specialist's counterpart, downstream implementer | Evidence organized by dimension. "Why is this broken? How do I fix it?" | **L2 (Analysis)** |
| **Skeptic** | Verifier, proofreader, challenger, reviewer | Raw material to verify claims. "Is this source real? Show me the test output." | **L3 (Dossiers)** |

**Rule:** If a piece of output serves more than one consumer, it belongs at the layer of the *least* abstract consumer who needs it. If both the decider and practitioner need it, put it in L2 — the decider can still read it there (they just descend one level).

### 2. How often is it consumed?

Consumption frequency confirms the layer assignment and tells you how many files to create.

| Frequency | Pattern | Layer | Cardinality |
|-----------|---------|-------|-------------|
| **Every pipeline handoff** | The first thing anyone reads to decide whether to proceed | **L1** | Exactly one file per project |
| **Per dimension, on demand** | Someone drills into this only when they need that specific dimension | **L2** | One file per analytical dimension |
| **On challenge or deep review** | Rarely accessed — pulled only when someone needs to verify | **L3** | One file per evidence set |

**Rule:** If an output is consumed every time the artifact is touched, it belongs in L1 or the 00-index. If it's consumed only when someone needs a specific question answered, it belongs in L2 or L3.

### 3. What question does it answer?

This is the content boundary check — the rule that prevents duplication.

| Question | Layer | File answers | File does NOT answer |
|----------|-------|--------------|---------------------|
| "What should I do?" | **L1** | The verdict, the score, the priority actions | How the verdict was reached (that's L2), where the raw data lives (that's L3) |
| "Why should I do it?" | **L2** | Evidence, analysis, reasoning per dimension | What to do (that's L1), the primary sources (that's L3) |
| "Is this real / can I prove it?" | **L3** | Raw output, test results, source excerpts, capture metadata | What it means (that's L2), what to do about it (that's L1) |

**Rule:** Every sentence in a file must answer its layer's assigned question. If a sentence answers a different layer's question, it belongs in that other layer. If a sentence answers no layer's question, it doesn't belong in the pyramid at all.

## Applying the Framework

### Step-by-step

1. **Inventory your outputs:** List every distinct type of artifact your specialist produces. (A copy-editor produces: a verdict, mechanical findings, line-edit findings, consistency findings, cross-reference results, a style sheet, a change log, a query list, verified source links.)

2. **For each output, ask the three questions:**
   - *Who consumes this?* → Decider, practitioner, or skeptic?
   - *How often?* → Every handoff, per dimension, or on challenge?
   - *What question does it answer?* → "What should I do?", "Why?", or "Is this real?"

3. **Classify to layer:** The answers determine the layer. If they disagree (e.g., consumed every handoff but answers "why"), the stricter constraint wins — protect the consumer who needs it the least.

4. **Verify with the quality gate:** For each file, check every sentence against its layer's question.

### Worked Example: Copy-Editor

| Output | Who consumes? | How often? | Answers? | Layer |
|--------|-------------|-----------|----------|-------|
| Verdict, key counts, top findings | Decider (orchestrator, author) | Every handoff | "What should I do?" | **L1** |
| Mechanical edit findings | Practitioner (author, writer) | Per dimension | "Why fix this?" | **L2** |
| Line-edit findings | Practitioner (author, writer) | Per dimension | "Why rephrase this?" | **L2** |
| Consistency findings | Practitioner (author, writer) | Per dimension | "Why standardize this?" | **L2** |
| Cross-referencing results | Practitioner (author) | Per dimension | "Which links are broken?" | **L2** |
| Style sheet | Practitioner (proofreader) | Per project, on demand | "What style conventions were applied?" | **L3** |
| Change log | Skeptic (challenger) | On challenge | "What exactly changed?" | **L3** |
| Verified sources | Skeptic (verifier) | On challenge | "Which links actually resolve?" | **L3** |
| Query list | Decider (author) | Every handoff | "What questions remain open?" | **L1** (adjunct) |

### Worked Example: SEO Specialist

| Output | Who consumes? | How often? | Answers? | Layer |
|--------|-------------|-----------|----------|-------|
| Overall verdict + score | Decider (pipeline, author) | Every handoff | "What should I fix?" | **L1** |
| Technical SEO findings | Practitioner (developer) | Per dimension | "Why is this a problem?" | **L2** |
| On-page findings | Practitioner (writer, editor) | Per dimension | "Why optimize this?" | **L2** |
| Schema validation | Practitioner (developer) | Per dimension | "What's broken in my schema?" | **L2** |
| Ghost metadata audit | Practitioner (editor) | Per dimension | "Which fields are missing?" | **L2** |
| AEO analysis | Practitioner (writer, editor) | Per dimension | "Why isn't this LLM-visible?" | **L2** |
| Raw crawl output | Skeptic (verifier) | On challenge | "What actual HTTP responses were seen?" | **L3** |
| Raw schema test results | Skeptic (verifier) | On challenge | "What did the validator say?" | **L3** |

## The 00-index / L1 Boundary

The most common duplication failure is between `00-index.md` and files inside `01-summary/`. The solution is to assign them distinct questions:

| File | Answers | Contains | Does NOT contain |
|------|---------|----------|-----------------|
| **00-index.md** | "Where do I find what I need?" | Navigation tree, project metadata, 1-sentence orientation, SOURCES | Findings, verdict, scores, priority actions, analysis, raw data |
| **01-summary/*** | "What should I do?" | Verdict, score, priority findings, recommended actions | Navigation, metadata, file lists, raw evidence, methodology |

**00-index.md exists only to get the consumer to the right layer file.** It is navigation and provenance, not analysis. If the consumer reads 00-index.md and can decide whether to proceed, they don't need more from the index. If they need to decide *what to do*, they descend to 01-summary.

## Quality Gates

Every file in the pyramid must pass its layer's gate. The gate is a single question:

| Layer | Gate Question | Pass condition |
|-------|---------------|----------------|
| **00-index** | "Is this file only navigation and provenance?" | No findings, verdict, scores, or analysis sentences |
| **L1 (Summary)** | "Does every sentence tell me what to do or what's most important?" | No raw data, no methodology, no file listings |
| **L2 (Analysis)** | "Does every sentence give me evidence organized by dimension?" | No verdict statements, no primary source text |
| **L3 (Dossiers)** | "Does every sentence present raw material without interpreting it?" | No recommendations, no judgments, no analytical framing |

### How to audit

For each file, read every sentence and ask: *"Does this answer my layer's question?"* If the answer is no for any sentence, that sentence belongs in a different layer or doesn't belong at all.

**Common failure patterns:**
- 00-index.md contains "Top 3 Critical Findings" → belongs in 01-summary
- 01-summary/verdict.md contains metadata (author, date, word count) → belongs in 00-index
- 02-analysis/findings.md contains "Recommendation: fix X" → this is a verdict (L1), not evidence (L2)
- 03-dossiers/raw-data.md contains "this suggests that..." → interpretation (L2), not raw material (L3)

## Relationship to Other References

| Reference | How this framework extends it |
|-----------|------------------------------|
| `pipeline-stages.md` | Defines what the layers ARE. This framework defines how to DECIDE what goes WHERE. |
| `methodology-to-pyramid-mapping.md` | Shows how specific roles (technical-architect, researcher) map their domain. This framework is the ROLE-AGNOSTIC abstraction they all follow. |
| `quality-gates.md` | Defines verification for a finished pyramid. This framework defines the CONTENT CONTRACTS that prevent violations from being created in the first place. |
