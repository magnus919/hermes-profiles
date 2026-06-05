# Research Lifecycle

The full arc of a professional research engagement, from question formulation through reporting.

## Phase 1: Scope — Frame the research question

Before gathering a single source, define what you're looking for and why.

### The Research Brief

Every research project starts with a brief. Load `assets/research-brief.md` and fill it out before proceeding. The brief answers:

- **Core question:** What exactly are we trying to find out? Frame as a single, falsifiable question.
- **Scope boundaries:** What's in and what's out. Define inclusion/exclusion criteria before searching.
- **Depth required:** Quick scan (2-3 sources for an overview) vs comprehensive (exhaustive on a narrow question) vs deep-dive (multi-angle on a complex question)
- **Decision context:** Who needs this information and what will they do with it? A product decision needs different evidence than a research paper.

### Question Types

| Question type | What you're looking for | Example |
|--------------|------------------------|---------|
| **Descriptive** | What's happening? | "What architectures are used for local LLM inference on consumer GPUs?" |
| **Comparative** | How does X compare to Y? | "How does Qwen3.6 compare to Gemma 4 for tool calling?" |
| **Causal** | What drives X? | "Why do MoE models have lower inference latency at high batch sizes?" |
| **Evaluative** | Is X effective? | "What evidence exists that RAG improves accuracy over zero-shot?" |
| **Gap-finding** | What's not known? | "What hasn't been published about neuromorphic edge deployment?" |

### Inclusion/Exclusion Criteria

Before searching, define:
- **Date range:** How recent must sources be?
- **Source type:** Peer-reviewed, industry reports, blog posts, documentation?
- **Authority threshold:** What makes a source credible enough?
- **Language:** English only, or other languages?
- **Duplication rule:** Multiple sources reporting the same finding — count as one or many?

## Phase 2: Gather — Systematic source discovery

### Search Strategy

1. **Start broad, then narrow.** First query should be broad enough to map the territory. Subsequent queries narrow based on what you found.
2. **Use multiple search angles.** Don't rely on one query. Search by: keyword, author/institution, tool name, problem statement, related concept.
3. **Citation chaining.** From each promising source:
   - **Backward:** Follow the citations/bibliography to find the sources the author relied on
   - **Forward:** Search for papers that cite this source (Google Scholar "cited by")
4. **Source diversity.** Don't rely on one type of source. Mix:
   - Primary research (papers, technical reports)
   - Grey literature (blog posts, documentation, forum discussions)
   - Expert commentary (industry analysis, conference talks)
   - Empirical data (benchmarks, datasets, reproducible experiments)

### For Each Source Found, Record

| Field | Purpose |
|-------|---------|
| Title + URL | Find it again |
| Author/source | Credibility assessment |
| Date | Recency check |
| Key claims | What it says that's relevant |
| Supporting evidence | What backs the claims |
| Gaps/limitations | What it doesn't say |
| Connection to brief | How it answers the research question |

## Phase 6: Report — Structure the findings

A research brief should have this structure (see `assets/research-brief.md`):

1. **Executive summary** — One-paragraph answer to the research question
2. **Key findings** — 3-5 synthesized findings with confidence levels
3. **Evidence table** — Sources mapped to findings
4. **Confidence assessment** — What's solid, what's uncertain, what's missing
5. **Open questions** — What you still don't know
6. **Sources** — Full citations with URLs

## Decision Contexts

Different depths of research for different needs:

| Context | Depth | Sources | Time |
|---------|-------|---------|------|
| Quick answer for a decision | Scan | 2-3 targeted sources | Minutes |
| Briefing for a conversation | Light | 5-8 sources, 2 angles | 1 hour |
| Support for a recommendation | Moderate | 10-15 sources, 3+ angles | Half day |
| Foundation for a publication | Deep | 20+ sources, exhaustive | Days |
