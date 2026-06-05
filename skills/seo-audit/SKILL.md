---
name: seo-audit
description: "Full-spectrum SEO + AEO audit skill — technical crawl analysis, on-page content optimization, structured data (JSON-LD/Schema.org) validation, Ghost CMS metadata completion, answer engine optimization (AEO/GEO), content strategy gap analysis, and reporting. Produces artifact-pyramid-compliant output. Use when the seo-specialist profile needs to audit a site, optimize an article for search and AI citation, complete Ghost CMS metadata, or develop a content strategy."
---

# SEO Audit

Full-spectrum audit for sites, articles, and content strategies. Covers both traditional SEO and Answer Engine Optimization (AEO/GEO) — the practice of structuring content so LLMs and AI answer engines (ChatGPT, Perplexity, Gemini, Claude, Google AI Overviews) extract and cite it.

All output is artifact-pyramid-compliant. The only response to the caller is the absolute path to `00-index.md`.

## Output Contract

### Pyramid Structure

```
<slug>/
├── 00-index.md                    ← L1 summary + navigation
├── 01-summary/
│   └── seo-verdict.md             ← Overall score, priority findings, estimated impact
├── 02-analysis/
│   ├── technical-seo.md           ← Crawlability, indexability, speed, mobile, HTTPS
│   ├── onpage-seo.md              ← Title tags, meta, headings, content, internal links
│   ├── schema-validation.md       ← Structured data / JSON-LD audit
│   ├── ghost-metadata.md          ← Ghost CMS meta, social cards, code injection
│   ├── aeo-methodology.md         ← AEO / answer engine optimization
│   └── content-gap-analysis.md    ← Keyword gaps, topic clusters, SERP opportunities
└── 03-dossiers/
    ├── full-crawl-results.md      ← Raw technical findings
    ├── schema-test-results.md     ← Rich results test output
    └── keyword-research-data.md   ← Raw keyword and SERP data
```

### L1 Verdict Format

```
## SEO + AEO Audit: [Site/Page URL]

**Overall Health:** [Good / Fair / Poor]
**Score:** [N/100]

### SEO Priority Findings
1. [Critical] → [Action]

### AEO Priority Findings
1. [Critical] → [Action]

### Quick Wins
1. [Low effort, high impact] → [Action]

### Verdict
[One paragraph summarizing the single most important thing to fix and expected impact.]
```

## Contents

| File | What it covers |
|------|----------------|
| `references/technical-seo.md` | Crawlability, indexability, robots.txt, sitemaps, page speed, Core Web Vitals, mobile-friendliness, HTTPS, canonical URLs, hreflang |
| `references/onpage-seo.md` | Title tags, meta descriptions, heading hierarchy, keyword placement, content quality, internal linking, image optimization |
| `references/schema-markup.md` | Schema.org types (TechArticle, FAQPage, HowTo, Article, BlogPosting, BreadcrumbList, Organization), JSON-LD format, Google rich results, validation |
| `references/content-strategy-seo.md` | Topic clusters, pillar pages, keyword research, gap analysis, SERP feature targeting, topical authority |
| `references/ghost-metadata.md` | Ghost CMS metadata fields (meta_title, meta_description, custom_excerpt), social media cards (OG, Twitter), code-injected schema (JSON-LD, FAQPage, TechArticle, @graph), per-post and site-wide injection, validation |
| `references/aeo-methodology.md` | Answer Engine Optimization — LLM RAG pipeline, answer-first content architecture, AEO-specific schema (FAQPage 3.2× boost), Ethan Smith/Graphite frameworks, question clusters, llms.txt, content negotiation, measurement |
| `assets/audit-report-template.md` | Blank report scaffold for new audits |

## When to Use

Load this skill when:
- Auditing a site for technical SEO issues
- Optimizing a new article for search and AI citation before publication
- Validating structured data on an existing page
- Completing Ghost CMS metadata (meta, social cards, schema injection) before publish
- Running an AEO readiness audit (llms.txt, content negotiation, question-cluster coverage)
- Developing a content strategy with SEO + AEO in parallel
- Diagnosing why a site or page isn't performing in search or AI citation

Do NOT load when:
- Only mechanical content fixes are needed (use `copy-edit`)
- Only writing is needed (use `writer` profile)
