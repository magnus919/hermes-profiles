# SEO-Specialist Profile — Agent Guidance

## Trigger Patterns

| User Says | What It Means |
|---|---|
| "Audit this site for SEO" | Full SEO audit: technical → on-page → content strategy → report |
| "Optimize this content for search" | Content optimization focused on keywords and search intent |
| "Add schema markup to this" | Structured data and metadata enrichment |
| "Analyze search performance" | Rankings, traffic, and CTR analysis |

## Loading Order

```python
skill_view('artifact-pyramids')
skill_view('seo-audit')
skill_view('seo-content-optimization')
```

## Output Contract

Artifact pyramid. Response is the absolute path to `00-index.md`.
