# Tool Governance for Researcher Subagents

**ALL web research MUST use the groktocrawl suite. The built-in `web_search` and `web_extract` tools are explicitly prohibited.**

| Need | Required tool |
|------|---------------|
| Multi-source research + synthesis | `groktocrawl agent "<prompt>"` |
| Web search for discovery | `groktocrawl search "<query>" --limit N --json` |
| Single page content | `groktocrawl scrape <url>` |
| JS-heavy / bot-protected pages | groktocrawl browser suite |
| Binary files (PDFs, images) | `groktocrawl download <url>` |
| URL discovery on a site | `groktocrawl map <url>` |
| Site-wide extraction | `groktocrawl crawl <url>` |

**Fallback chain** (only when groktocrawl is genuinely unavailable):
1. `curl` — plain-text endpoints only (`.md`, `.txt`, `.json`, `.yaml`)
2. `web_extract` — last resort, known limitations

**Why:** The built-in tools are insufficient for systematic research. They return empty results, hit CAPTCHA walls, and cannot handle JS-rendered content. Groktocrawl is self-hosted, handles anti-bot measures, and returns clean markdown.

**What to do when you catch yourself reaching for web_search/web_extract:** Stop. Open a terminal and use the groktocrawl CLI instead. The extra step is worth the quality difference.
