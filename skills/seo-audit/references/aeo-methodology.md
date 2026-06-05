# Answer Engine Optimization (AEO) Methodology

AEO (also called GEO — Generative Engine Optimization) is the practice of structuring content so AI-powered answer engines (ChatGPT, Perplexity, Gemini, Claude, Google AI Overviews) extract, cite, and surface it in their generated responses.

**Core insight:** ChatGPT traffic converts 6× better than Google search (Ethan Smith, Graphite). Content that ranks in Google is 3× more likely to appear in LLM citations. SEO and AEO are complementary — the SEO foundation feeds AEO performance.

## How LLMs Surface Content

Modern LLMs with web access use Retrieval-Augmented Generation (RAG):

1. **Query expansion** — User prompt is expanded into related sub-queries
2. **Retrieval** — Web search or vector DB finds candidate pages
3. **Re-ranking** — Chunks scored by relevance to query
4. **Synthesis** — LLM generates answer grounded in top chunks
5. **Citation** — Sources appended as footnotes or inline links

### Key Signals for Citation Selection

**Semantic relevance** — content must match semantic meaning, not just keywords. Named entities (people, products, brands, places) boost relevance scoring.

**Answer placement** — First 1-2 sentences of a section are the most extractable. Pages with clean heading hierarchy earn 2.8× higher citation rates (AirOps 2026).

**Authority** — 96% of AI Overview citations come from sources Google already trusts (Ziptie.dev). E-E-A-T functions as a binary gatekeeper, not just a ranking signal.

**Freshness** — Pages accessible to GPTBot, ClaudeBot, PerplexityBot. AI Overviews favors recently crawled content.

**FAQPage schema** — Pages with FAQPage schema appear in AI Overviews 3.2× more often (SearchAtlas data).

## Content Structure for AEO

### Answer-First Architecture

Every section should follow the inverted pyramid:

```
┌──────────────────────────────────┐
│ Direct answer (first 1-2 sentences) │ ← Most extractable
├──────────────────────────────────┤
│ Supporting details / evidence       │ ← Reinforces citation confidence
├──────────────────────────────────┤
│ Background / context                │ ← For human readers
└──────────────────────────────────┘
```

### Structural Requirements

- **One clear H1** aligned with the primary topic
- **Question-based H2s** — Write headings as standalone user questions ("How does X work?")
- **Answer in the opening sentence** — Every section's first sentence directly answers the heading
- **Short paragraphs** — 2-4 sentences max
- **Consistent terminology** — One term per concept; don't rotate synonyms (helps entity recognition)
- **TL;DR / Summary block** — Quick-extractable answer at the top of the article
- **FAQ sections** — Self-contained Q&A pairs matching how users query AI assistants
- **Lists and tables** — LLMs efficiently extract structured data from ordered/unordered lists
- **Quote-worthy claims** — Key numbers in the first sentence of their paragraph; specific, confident, unhedged language

### What NOT to Do

- Long intros / historical context before the answer
- Delaying the answer to increase time-on-page (penalized by LLMs)
- Creative/metaphorical headings ("The Dance of Algorithms")
- Redundant restatements of the same point
- Relying solely on schema to compensate for vague content

## AEO-Specific Structured Data

| Schema Type | AEO Impact | Priority |
|-------------|-----------|----------|
| **FAQPage** | 3.2× more citations in AI Overviews. LLMs directly extract Q&A pairs. | Highest |
| **HowTo** | Step-by-step instructions extracted for procedural queries | High |
| **Article / TechArticle** | Signals content type, authorship, publication date | Required |
| **Organization** | Establishes publisher identity and authority | Required |
| **Person** | Author credentials and authority signals | High |
| **BreadcrumbList** | Helps LLMs understand site hierarchy | Medium |

**Key rules:**
- JSON-LD is the preferred format
- Schema must match visible content exactly (misleading schema damages trust)
- Pages using 3+ relevant schema types show ~13% higher citation likelihood (AirOps)
- FAQPage schema provides compounding benefits when paired with FAQ formatting in visible content

## Ethan Smith / Graphite's AEO Framework

### The 5% Principle
Only ~5% of SEO/AEO strategies drive outsized results. Process: Generate Ideas → Test & Evaluate → Reproduce Results.

### High-Impact AEO Tactics (the 5%)
1. **New AEO landing pages** — Create pages for topics you don't cover
2. **Content enhancement** — Fill answer gaps on existing pages
3. **Citation optimization** — Get mentioned on the most-cited URLs for target topics

### Biggest Waste of Time
Technical AEO (page speed, crawl errors) is low-impact. Priorities: content quality > question coverage > authority > technical tweaks.

### AEO Topics (Not Keywords)
An AEO topic = a cluster of questions targeting a single page. Questions have head, mid-tail, and long-tail varieties. Focus on "Product Questions" — those where answers suggest products or brands.

### Owned vs. Earned
- **Owned** (SEO-like): Directly ranking your page — more effective for specific, product-oriented questions
- **Earned**: Being cited as a source within the LLM's answer — more critical for general, high-level questions

### The 7-Step AEO Playbook
1. Identify target AEO topics (question clusters)
2. Audit current content for answer gaps
3. Create or enhance pages with answer-first structure
4. Add structured data (FAQPage, Article, etc.)
5. Build off-site authority (Reddit, YouTube, guest content)
6. Measure citation rate and iterate
7. Scale what works, kill what doesn't

## LLM-Friendly Content Formats

### llms.txt
A markdown file at the site root providing LLMs with background, guidance, and links. Functions as a foundational AEO element — provides curated context for LLMs, reduces hallucinations, and controls how your site is understood.

**Structure:**
```markdown
# Site Name
> Brief description

## Pages
- [Page Title](URL)

## Optional
- [Full content](llms-full.txt)
```

### Content Negotiation (Accept: text/markdown)
Serve Markdown to LLM agents and HTML to browsers. The agent sends `Accept: text/markdown` in the HTTP header; the server returns clean Markdown. Standards-compliant — no separate URL needed.

**Hugo:** Already implemented on magnus919.com — custom output format renders pages as Markdown. Serve via Hugo's built-in output format routing.

**Ghost:** Needs a reverse proxy (Nginx/Cloudflare Worker) or Ghost API-based solution. Ghost doesn't natively support content negotiation.

### Robots.txt for AI Crawlers
Allow GPTBot, ClaudeBot, PerplexityBot, Google-Extended, Applebot-Extended:
```txt
User-agent: GPTBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Google-Extended
Allow: /

User-agent: Applebot-Extended
Allow: /
```

## Measurement

### Core AEO Metrics
| Metric | What It Measures | How |
|--------|-----------------|-----|
| Citation Rate | How often AI cites your content | Manual LLM queries; tools like LLMrefs, AirOps Insights |
| AI Share of Voice | Brand mention frequency vs. competitors | Same prompt set across multiple LLMs |
| Query Coverage | Range of questions where content appears | Expand query into sub-questions; test each |
| AI Referral Traffic | Clicks from ChatGPT, Perplexity, etc. | GA4 source/medium reports |
| AI Overview Appearances | Visibility in Google AI Overviews | GSC → Search Appearance → AI Overviews |
| AEO Readiness Score | Site-level technical AEO readiness | AEOprobe, ansly scanners |

### Cadence
- **Weekly:** Test 5-10 key prompts per site against major LLMs
- **Monthly:** Citation rate audit, brand mention accuracy check
- **Quarterly:** Full AEO audit (structure, schema, llms.txt, crawlability)

### Key References
- Ethan Smith / Graphite: graphite.io/five-percent/aeo-is-the-new-seo
- Lenny's Podcast: "The ultimate guide to AEO" (Sept 2025)
- AirOps 2026 State of AI Search
- SearchAtlas: FAQPage schema → 3.2× AI Overview citations
- Ziptie.dev: 96% of AI Overviews cite already-trusted sources
- HubSpot: Page with 85 AI citations had only 1 backlink
