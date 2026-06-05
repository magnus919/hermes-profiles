---
name: seo-content-optimization
title: SEO Content Optimization
description: Audit and optimize content sites for search — page title audits, schema injection (Organization, FAQ, LocalBusiness), meta description rewrites, URL hygiene, local landing pages, and measurement. Complements /content-strategy (what to write next) by optimizing what already exists.
domain: devops
---

# SEO Content Optimization

Audit-and-fix workflow for improving search rankings on Magnus's content sites. This is the "optimize what exists" counterpart to /content-strategy's "what to write next."

**Sites in scope:** magnus919.com (Hugo), rdumesh.org (Ghost), groktop.us (Ghost Pro), southeastme.sh (Ghost)

## Signals to Run This

- User says "we're not ranking for X" or "SEO is bad"
- User asks to audit a site's search presence
- User mentions poor Google visibility for local terms
- As part of site launch / relaunch

## Process

### 1. Audit page titles and meta descriptions

Fetch the site's sitemap to get all published URLs (see content-strategy skill for sitemap-fetching protocol — try bare domain, www subdomain, Ghost split-sitemaps).

For each published page:
- Check the `<title>` tag via curl
  ```bash
  curl -s https://example.com/page/ | grep -i '<title'
  ```
- Check meta description
  ```bash
  curl -s https://example.com/page/ | grep -i 'name="description"'
  ```
- Evaluate against:
  - Does the title include the primary keyword near the front?
  - Does it include location terms (for local sites)?
  - Is it under 60 characters (Google display limit)?
  - Is the meta description under 160 chars, compelling, and keyword-rich?

### 2. Audit structured data

Check for existing schema:
```javascript
// in browser console
document.querySelectorAll('script[type="application/ld+json"]')
```

For each JSON-LD block, verify:
- Is there an Organization or LocalBusiness schema?
- Does it include `areaServed` with specific cities?
- Is there FAQPage schema on FAQ content?
- Is there BreadcrumbList?
- Is Article schema correctly populated?

### 3. Inject missing schema

**Organization schema** — site-wide (Ghost Code Injection → `ghost_head`). The critical fields for local SEO:

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Site Name",
  "description": "Description with city and keyword signals.",
  "url": "https://example.com",
  "areaServed": [
    {"@type": "City", "name": "City1", "sameAs": "https://en.wikipedia.org/wiki/City1,_NC"},
    {"@type": "City", "name": "City2"}
  ],
  "sameAs": [
    "https://discord.gg/..."
  ]
}
</script>
```

**FAQ schema** — page-level. Enables rich FAQ results in search. For Ghost sites, use the ghost-cli `schema inject` command instead of post-level code injection — it's cleaner and doesn't require editing the post HTML:

```bash
ghost-cli --site rdumesh schema validate --json '{"@context":"...","@type":"FAQPage",...}'
ghost-cli --site rdumesh schema inject my-post --file /tmp/faq-schema.json
```

FAQPage JSON-LD structure:
```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "Question text?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Answer text."
      }
    }
  ]
}
```

**TechArticle schema** — for hardware/software/technical blog posts. More specific than `Article` (which Ghost outputs by default), gives Google better content classification. Include `proficiencyLevel` and `about` for deeper signals:

```json
{
  "@type": "TechArticle",
  "headline": "Post Title",
  "proficiencyLevel": "Beginner|Intermediate|Advanced",
  "about": {
    "@type": "Thing",
    "name": "Topic name"
  }
}
```

**Hybrid @graph pattern** — when a post benefits from multiple schema types (FAQPage + HowTo + TechArticle), wrap them in a `@graph` array in a single injection:

```json
{
  "@context": "https://schema.org",
  "@graph": [
    {"@type": "TechArticle", "headline": "..."},
    {"@type": "FAQPage", "mainEntity": [...]},
    {"@type": "HowTo", "name": "...", "step": [...]}
  ]
}
```

This is cleaner than multiple separate JSON-LD blocks and ensures all types are processed together by Google.

**When to use each type:**
| Type | Article Content Signal | SERP Impact |
|---|---|---|
| `TechArticle` | Technical hardware/software content | Better classification, no visual rich result |
| `FAQPage` | 3+ natural Q&A pairs (headings + paragraph answers) | Expandable FAQ rich result (high CTR) |
| `HowTo` | Step-by-step procedures, CLI commands, build instructions | Step preview rich result |

**Fallback for non-Ghost sites:** For Hugo sites (magnus919.com), schema is baked into static HTML at build time via Hugo partials — see the magnus919.com section below for implementation approaches. For Ghost sites, always prefer `schema inject` via ghost-cli over manual code injection.

### 4. Rewrite page titles (meta_title, not H1)

In Ghost CMS, page titles and H1s are independent. Set `meta_title` via the Admin API or Ghost post settings — it controls the `<title>` tag and what shows in search results. The visible H1 on the page stays unchanged.

**Pattern:** Primary keyword near front | pipe-separated site name suffix. For local sites, include city names. For Ghost sites, use the ghost-cli to set these:

```bash
ghost-cli --site rdumesh meta set <slug> \
  --meta-title "Primary Keyword Context | Site Name" \
  --meta-description "150-160 char summary with keyword and call to action."
```

| Type | Format | Example |
|------|--------|---------|
| Local landing | Keyword + city + site | "Free Mesh Network for Raleigh, Durham & Chapel Hill, NC | RDUMesh" |
| Technical guide | Keyword + site | "915 MHz Pine Tree Attenuation: What LoRa Mesh Operators Need to Know | RDUMesh" |
| Hardware guide | Product + keyword + site | "Heltec V4.3 Solar Repeater: Power Consumption & EasySkyMesh Firmware | RDUMesh" |
| FAQ | Keyword + cities + site | "Mesh Radio Network FAQ: RDUMesh for Raleigh, Durham, Chapel Hill" |
| Announcement | Topic + site | "Chapel Hill Mesh Network Expansion — RDUMesh Backhaul Case Study" |

Set via ghost-cli `meta set` for Ghost sites (see ghost-cli skill) or via Hugo template variables for magnus919.com.

### 5. Audit and optimize URL slugs

In Ghost CMS, slugs can be changed independently of titles and the ghost-cli doesn't have a dedicated slug command — use the Admin API directly (see ghost-cli skill's "Slug Optimization" section for the pattern). Issues to flag:

- `-2` suffixes (signal duplicate content) — fix slug, ensure 301 redirect from old URL
- Excessively long slugs (>55 chars) — shorten by removing filler words (why, what, the, a, of, and, how, for)
- Ghost auto-generates slugs from the initial post title, so if the title changes later, the slug doesn't update
- Target 30-45 characters, leading with the primary keyword
- OK to change before publish. Changing after publish requires a 301 redirect.

### 6. Create local landing pages (if applicable)

For sites serving specific geographic areas, create dedicated short pages (500-800 words) per city/region. These don't need to be deep essays — they exist to tell Google "this site serves this place."

**Ghost CMS: always create as Pages, not Posts.** Pages don't trigger email notifications to subscribers. Posts do.

Each should include:
- City name in H1 and first paragraph
- 2-3 paragraphs of substantive local content (not keyword stuffing)
- Link to the relevant coverage map or router page
- CTA to join/participate
- Internal links to 2-3 other relevant posts

**Ghost Admin API pitfall — Ghost v6 uses Lexical format, not raw HTML.** When creating pages via the API, sending `"html"` in the payload does NOT store the content. You must provide `"lexical"` as a JSON string in Ghost's Lexical editor format. The `html` field is read-only — derived from Lexical on the backend.

Minimal Lexical page structure for a short page with paragraphs and headings:
```python
lexical = json.dumps({
    "root": {
        "children": [
            {
                "children": [{"detail": 0, "format": 0, "mode": "normal", "style": "", "text": "Paragraph text.", "type": "text", "version": 1}],
                "direction": "ltr", "format": "", "indent": 0, "type": "paragraph", "version": 1
            },
            {
                "children": [{"detail": 0, "format": 0, "mode": "normal", "style": "", "text": "Section Heading", "type": "text", "version": 1}],
                "direction": "ltr", "format": "", "indent": 0, "type": "heading", "tag": "h2", "version": 1
            }
        ],
        "direction": "ltr", "format": "", "indent": 0, "type": "root", "version": 1
    }
})
```

For ordered lists, use `"type": "list", "listType": "number"` with `"type": "listitem"` children.

### 7. Measure

- **Immediate:** `curl | grep <title>` to confirm titles deployed
- **Schema validation:** Google Rich Results Test (https://search.google.com/test/rich-results)
- **Crawl:** Google Search Console after 1-2 weeks
- **Ranking:** Manual spot-checks for targeted queries (incognito browser)

## Site-Specific Notes

### rdumesh.org
- Self-hosted Ghost on Ubuntu. Admin API at same domain as public.
- Biggest gap: city-specific landing pages and schema with areaServed.
- FAQ schema on the FAQ page is a high-impact copy-paste.

### groktop.us
- Ghost Pro behind custom domain. Admin API at admin domain `groktopus-hybrid-workforce.ghost.io`.
- Enterprise AI audience — local SEO doesn't apply.
- Focus on meta title optimization and Article schema completeness.

### magnus919.com
- Hugo static site (Terminal theme v4). **Currently emits zero JSON-LD.** The Terminal theme's `head.html` partial does not include any schema markup.
- Hugo has no built-in runtime schema injection (unlike Ghost's `ghost_head`), but several zero-cost approaches exist:

  | Approach | Effort | Output |
  |----------|--------|--------|
  | **Hugo internal template** (`{{ template "_internal/schema.html" . }}`) | Add one line to `head.html` | Basic WebSite (home) + Article (pages) with Organization, dates, author |
  | **Custom partial** (`layouts/partials/schema.html`) | Write a Handlebars partial with per-page-kind conditionals | Full control over @type, fields, and which pages get which schema |
  | **PaperMod-style partial** (see `_vendor` for reference) | Adapt existing schema_json.html from vendored PaperMod theme | Organization + BreadcrumbList + BlogPosting with articleBody, wordCount, keywords |

  Unlike Ghost's injection-based approach, Hugo schema is baked into static HTML at build time — no runtime overhead, but changes require a rebuild.
- Site already has good organic content depth; focus on page title optimization and internal linking.

### southeastme.sh
- Nascent site — SEO work is premature. Focus on content strategy first.

## LLM-Friendly Content (/llms.txt)

An emerging complement to traditional SEO: making your site consumable by LLM agents during inference. While SEO targets Google's crawler, llms.txt targets the agents that visit your site looking for context.

**The standard:** A markdown file at `/llms.txt` providing a curated, concise overview — H1 title, blockquote summary, and H2 sections with link lists. The `## Optional` section can be skipped for tighter context.

**How it differs from SEO:**
- SEO optimizes for ranking in search results (traffic goal)
- llms.txt optimizes for LLM comprehension (utility goal)
- Both require clear, concise content architecture
- llms.txt is far simpler — one markdown file vs. structured data + meta + backlinks

**Quick check when evaluating a site:**
- `/llms.txt` exists? Read it first.
- No `/llms.txt`? Check `/sitemap.xml` for full page list.
- Neither? The site forces LLMs to parse HTML — opportunity to create one.

See `references/llmstxt-standard.md` for the full standard reference — format spec, best practices, implementation approaches for Hugo/Ghost/Next.js, the `llms_txt2ctx` CLI tool, and content negotiation via `Accept: text/markdown`.

## See Also

- `references/llmstxt-standard.md` — full /llms.txt standard reference
- `ghost-webhooks` skill reference `admin-api-content-editing.md` — Admin API auth and update patterns
- `content-strategy` skill — what to write next (complements this skill)
- `hugo-blog` skill — Hugo-specific llms.txt implementation details (custom output formats, content negotiation)
