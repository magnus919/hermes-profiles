# /llms.txt Standard — Reference

## Summary

Proposal by Jeremy Howard (2024-09-03) for a site-root markdown file that provides an LLM-friendly entry point to a site's content. Published at [llmstxt.org](https://llmstxt.org/).

**The Problem:** LLMs have small context windows — they can't handle full websites. Converting complex HTML (ads, JS, nav) to plain text is imprecise and wasteful. Sitemaps are too large; robots.txt only governs crawling policy.

**The Solution:** A curated markdown file at `/llms.txt` that tells an LLM what's important, why, and where to find the clean markdown version.

## Format (Strict Section Order)

```markdown
# Title (H1 — required)

> Summary (blockquote — required, key info for understanding the rest)

Optional details (any markdown except headings)

## Section Name (H2)
- [Link title](url): Optional description

## Optional
- [Link title](url): URLs here can be skipped for shorter context
```

### Rules
- **`## Optional`** has special semantics — tools like `llms_txt2ctx` omit this section by default, include with `--optional True`
- Each link should have a **brief, informative description** telling the LLM what it'll find
- Links should point to **markdown files** where possible (same URL + `.md`)
- No heading levels between H1 and H2 — only H1 (title), then H2 sections

## Relationship to Existing Standards

| Standard | Purpose | Context |
|----------|---------|---------|
| `robots.txt` | Crawling **policy** (what bots may access) | Training/index bots |
| `sitemap.xml` | **Exhaustive** URL listing (often too large for LLM context) | Crawlers |
| `llms.txt` | **Curated, concise** overview for inference-time use | LLM agents |

llms.txt supplements, not replaces, these standards.

## Best Practices

- **Concise, clear language** — every word earns its place
- **Informative descriptions** on every link — tell the LLM why it matters
- **Avoid unexplained jargon or ambiguous terms**
- **Test with multiple models** after expanding into a context file
- Markdown pages should be available at `url.md` (e.g., `docs/page.html.md`)
- The `/llms.txt` file itself should be at the site root
- Can include **external URLs** (GitHub, community, etc.)
- The blockquote summary is the most-read line — make it dense with signals

## CLI Tool

The `llms-txt` Python package provides `llms_txt2ctx`:

```bash
pip install llms-txt
llms_txt2ctx llms.txt > llms.md          # without Optional section
llms_txt2ctx llms.txt --optional True > llms-ctx-full.md  # with Optional
```

Output is XML-wrapped context suitable for Claude and other LLMs.

## Python API

```python
from llms_txt import *
parsed = parse_llms_file(text)  # returns {title, summary, info, sections}
ctx = create_ctx(text)           # returns XML context string
```

A reference parser exists in <20 lines of Python with no deps (see llmstxt.org's intro page).

## Implementation Approaches

### Static SSG (Hugo, Jekyll)
- Create `/llms.txt` as a custom output format — see magnus919.com's Hugo implementation (custom LLMTXT output format at `layouts/index.llmtxt.txt`)
- Per-page markdown via Accept: text/markdown content negotiation and built-in MARKDOWN output format
- Fully static, no runtime overhead

### Dynamic CMS (Ghost, WordPress)
- Ghost: Manually maintain `/llms.txt` as a custom template page, or via Ghost's API to auto-generate from content
- WordPress: Plugins like `serve-md` or `markdown-negotiation-for-agents`; Cloudflare's "Markdown for Agents" (edge HTML→MD, free for Pro+)
- WordPress honors Accept: text/markdown across the entire domain (verified May 2026) with proper Vary: Accept headers

### JS-Framework Sites (Next.js, Remix)
- Serve `/llms.txt` as a static route or API endpoint returning markdown content
- Point to existing `/docs/llms.txt` if the docs platform (Mintlify, etc.) already generates one
- Provide markdown equivalents of key pages if the framework doesn't auto-render them

## Directory of Existing llms.txt Files

- [llmstxt.site](https://llmstxt.site/)
- [directory.llmstxt.cloud](https://directory.llmstxt.cloud/)

## Content Negotiation (Accept: text/markdown)

As an alternative or supplement to llms.txt, HTTP content negotiation can serve markdown directly:

```
curl -s -H "Accept: text/markdown" -L https://example.com/page/
```

- WordPress.org honors this across its entire domain (54x bandwidth savings vs HTML)
- RFC 7763 registered `text/markdown` as IANA media type in March 2016
- Cloudflare's "Markdown for Agents" (Feb 2026) provides edge HTML→MD conversion
- Static Web Server (Rust) has a `--accept-markdown` flag
- Claude Code and OpenCode already send `Accept: text/markdown` by default

## See Also

- [llmstxt.org](https://llmstxt.org/) — official proposal and docs
- [llms.txt proposal (full)](https://llmstxt.org/index.md) — original proposal
- `hugo-blog` skill — has reference Hugo-specific llms.txt implementation details
- Content negotiation pre-check: before scraping any docs site, try `curl -s -i -H "Accept: text/markdown"` first
