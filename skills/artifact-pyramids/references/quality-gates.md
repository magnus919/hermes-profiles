# Quality Gates: Verification at Each Layer

Each layer of the Artifact Pyramid has a quality gate — checks that material must pass before it can flow between layers. Because the pyramid is consumed **top-down** (L1 → L2 → L3) but produced **bottom-up** (L3 → L2 → L1), gates verify both directions: upward production quality and downward navigability.

## How to Use Quality Gates

Run the appropriate gate checklist when:
- Moving from dossiers (L3) into an analysis file (L2) — use Gate C
- Moving from analysis (L2) into the summary (L1) — use Gate B
- Auditing a completed artifact pyramid for publication — use Gate A

Each gate has three categories:
- **Critical** — must pass or the artifact cannot proceed
- **Standard** — should pass; flag exceptions explicitly
- **Advisory** — aspirational; note gaps for future improvement

---

## Gate A: Summary Integrity (L1 — Summary)

Run this before publishing or delivering the summary.

### Critical

- [ ] **Claim traceability**: Every claim in the summary links to a specific Layer 2 analysis file via the SOURCES section. No orphan claims.
- [ ] **Self-containment**: The summary makes sense without reading lower layers. No "as discussed in the analysis" without a link.
- [ ] **Implications stated**: The summary doesn't stop at findings — it states what they mean for the intended audience.

### Standard

- [ ] **Audience fit**: Language, depth, and format match the intended audience (PM agent vs. executive vs. technical lead).
- [ ] **Scope fidelity**: The summary addresses the mission brief's research questions. Out-of-scope findings are flagged as such.
- [ ] **Internal consistency**: The summary doesn't contradict itself.

### Advisory

- [ ] **Version tracking**: The summary has a version identifier.
- [ ] **Downstream navigation**: Every SOURCES reference answers "what will I find if I go deeper?"

---

## Gate B: Analysis Integrity (L2 → L1)

Run this before an analysis file feeds into the summary.

### Critical

- [ ] **Full traceability**: Every claim in the analysis file traces to specific Layer 3 sources via the SOURCES section.
- [ ] **Self-containment**: Each analysis file makes sense on its own — a consumer reading only this file should understand the dimension.
- [ ] **Interpretive value**: The analysis adds value beyond raw data. If it's just reformatted dossiers, it's not analysis.

### Standard

- [ ] **Conflict transparency**: If sources disagree, the analysis surfaces the conflict rather than picking one side.
- [ ] **Narrative structure**: The analysis has a clear thesis, evidence section, and conclusion.
- [ ] **Quantitative precision**: Numbers are preserved and contextualized (not "most showed improvement" but "7 of 12 improved by ≥5%").

### Advisory

- [ ] **Source diversity**: The analysis draws from multiple sources, not a single dossier.
- [ ] **Cross-dimension links**: Analysis files reference each other when findings overlap.

---

## Gate C: Dossier Completeness (L3 → L2)

Run this before dossiers feed into analysis files.

### Critical

- [ ] **Source attribution**: Every dossier entry has source metadata (URL, timestamp, title, author, capture date).
- [ ] **Faithful extraction**: Extracts are faithful to the original. No misrepresentation or cherry-picking.
- [ ] **Methodology documentation**: How was the data collected, processed, or transcribed?

### Standard

- [ ] **Organizational discoverability**: Dossiers are organized for consumption (not a raw dump). Named, attributed, searchable.
- [ ] **Coverage completeness**: The dossier layer covers all sources referenced by analysis files above it.
- [ ] **Contradictory evidence**: Counter-evidence to expected findings is included, not suppressed.

### Advisory

- [ ] **Metadata completeness**: Publication date, author, access timestamp for every source.
- [ ] **Semantic tagging**: Descriptive tags for cross-discovery.

---

## Gate Failure Recovery

| Gate | Failure | Recovery |
|------|---------|----------|
| A | Orphan claim (no L2 link) | Either add the supporting analysis file or remove the claim |
| A | Audience mismatch | Rewrite or re-format for the target audience |
| B | No interpretive value | Re-examine: reformatted dossiers aren't analysis. Find the thesis. |
| B | Orphan claim (no L3 link) | Either add the supporting dossier or remove the claim |
| C | Missing source attribution | Re-extract from source, add metadata |
| C | Cherry-picked evidence | Go back to sources, include contradicting evidence |
