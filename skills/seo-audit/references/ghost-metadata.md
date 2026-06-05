# Ghost CMS Metadata & Schema Completion

For Ghost CMS sites (groktop.us, rdumesh.org, southeastme.sh), the SEO specialist is responsible for completing all metadata on every published or draft article. This covers three distinct layers: Ghost CMS metadata fields, social media cards, and code-injected structured data.

## Layer 1: Ghost CMS Metadata Fields

Every Ghost post and page has a set of metadata fields in the post settings panel (or settable via the Ghost Admin API / ghost-cli). These must be filled for every article.

### Fields

| Field | Required | Purpose | Best Practice |
|-------|----------|---------|---------------|
| **Meta Title** | Always | Overrides the post title for SEO. Controls the `<title>` tag. | 50-60 chars, primary keyword front-loaded. If not set, Ghost uses the post title (which may be too long or lack keyword focus). |
| **Meta Description** | Always | Overrides excerpt for SEO. Controls the meta description tag. | 150-160 chars, includes primary keyword + CTA, reads naturally. |
| **Custom Excerpt** | Always | Used in card previews, RSS feeds, and as fallback for meta description. | 1-2 sentences capturing the article's core argument. Shorter than meta description (~120 chars). NOT the same as meta description — serves different contexts (card previews, not SERPs). |
| **OG Title** | Recommended | Overrides the title for social sharing (Facebook, LinkedIn, Discord). | Defaults to meta title. Only needed if the social version should differ. |
| **OG Description** | Recommended | Overrides the description for social sharing. | Defaults to meta description. Only needed if the social version should differ. |
| **OG Image** | Always | The image that appears in social card previews. | Should be the article's feature/cover image. If not set, Ghost uses the feature image from the post. Set explicitly to ensure correct crop and fallback. |
| **Twitter Title** | Recommended | Overrides the title for Twitter/X card previews. | Defaults to OG title. Only needed if the Twitter version should differ. |
| **Twitter Description** | Recommended | Overrides the description for Twitter/X. | Defaults to OG description. |
| **Twitter Image** | Recommended | Overrides the image for Twitter/X. | Defaults to OG image. Twitter's card crop differs from OG — set explicitly if the feature image crop doesn't work well as a square. |
| **Canonical URL** | As needed | Overrides the canonical URL. | Only needed if the post is syndicated or republished from another source. Ghost auto-generates self-referencing canonicals. |
| **Slug** | As needed | URL path. | Set before publish. Never change after publish without a 301 redirect. |

### Setting via ghost-cli

The `ghost-cli` tool has a `meta set` command for individual fields:

```bash
# Set meta title and description
ghost-cli --site groktopus meta set <slug> \
  --meta-title "Primary Keyword Context | Groktopus" \
  --meta-description "150-160 char summary with keyword and call to action."

# Set OG and Twitter fields
ghost-cli --site rdumesh meta set <slug> \
  --og-title "Optional: different from meta title" \
  --og-description "Optional: different from meta description" \
  --twitter-title "Optional: different from OG title"
```

### Setting via Ghost Admin API

For bulk operations or automation, use the Admin API directly. The key fields in the post object are:

```json
{
  "posts": [{
    "id": "post-id",
    "meta_title": "SEO Title",
    "meta_description": "SEO Description",
    "custom_excerpt": "Brief excerpt for cards",
    "og_image": "https://example.com/image.jpg",
    "og_title": "Social Title",
    "og_description": "Social Description",
    "twitter_image": "https://example.com/twitter-image.jpg",
    "twitter_title": "Twitter Title",
    "twitter_description": "Twitter Description",
    "canonical_url": null,
    "codeinjection_head": "<script type=\"application/ld+json\">...</script>",
    "codeinjection_foot": ""
  }]
}
```

**Important:** When updating a post via PUT, you must include `updated_at` from the current post data — Ghost uses it for optimistic locking. Always fetch first, modify, then PUT.

## Layer 2: Social Media Cards

Social media cards control what appears when an article is shared on Facebook, LinkedIn, Discord, Twitter/X, Slack, and other platforms.

### How Ghost Generates Cards

Ghost automatically generates Open Graph and Twitter Card meta tags from the post's metadata fields:

```html
<meta property="og:site_name" content="Groktopus">
<meta property="og:type" content="article">
<meta property="og:title" content="[OG Title or Meta Title or Post Title]">
<meta property="og:description" content="[OG Description or Meta Description or Excerpt]">
<meta property="og:image" content="[OG Image or Feature Image]">
<meta property="og:url" content="[Post URL]">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="[Twitter Title or OG Title or Meta Title]">
<meta name="twitter:description" content="[Twitter Description or OG Description or Meta Description]">
<meta name="twitter:image" content="[Twitter Image or OG Image or Feature Image]">
<meta name="twitter:site" content="@groktopus">
<meta name="twitter:creator" content="@magnus919">
```

### Fallback Chain

- **OG Title:** OG Title → Meta Title → Post Title
- **OG Description:** OG Description → Meta Description → Custom Excerpt
- **OG Image:** OG Image → Feature Image
- **Twitter Title:** Twitter Title → OG Title → Meta Title → Post Title
- **Twitter Image:** Twitter Image → OG Image → Feature Image

### Verification

```bash
# Check what tags are being emitted
curl -s https://groktop.us/<slug>/ | grep -E 'og:|twitter:'

# Test with validators
# Facebook: https://developers.facebook.com/tools/debug/
# Twitter: https://cards-dev.twitter.com/validator
# LinkedIn: https://www.linkedin.com/post-inspector/
```

## Layer 3: Code-Injected Schema

Ghost CMS auto-generates basic Article/BlogPosting schema, but custom schema types (TechArticle, FAQPage, HowTo, Organization with areaServed) must be code-injected.

### Injection Points in Ghost

| Location | Scope | Method |
|----------|-------|--------|
| **Site-wide** (`ghost_head`) | Every page on the site | Settings → Code Injection → Site Header |
| **Per-post** | Single post only | Post Settings → Code Injection → Post Header |
| **Per-page** | Single page only | Page Settings → Code Injection → Post Header |
| **ghost-cli** | Per-post via API | `ghost-cli --site <name> schema inject <slug> --file <path>` |

### Per-Page Schema via ghost-cli

The ghost-cli `schema inject` command handles the API call and stores the schema in the post's `codeinjection_head` field:

```bash
# Validate and inject FAQPage schema
ghost-cli --site groktopus schema validate --json '{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":"Q?","acceptedAnswer":{"@type":"Answer","text":"A."}}]}'

ghost-cli --site groktopus schema inject my-post --file /tmp/faq-schema.json
```

### Injecting Multiple Schema Types with @graph

When a post benefits from multiple schema types (e.g., TechArticle + FAQPage), wrap them in a `@graph` array:

```json
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "TechArticle",
      "headline": "Post Title",
      "proficiencyLevel": "Advanced",
      "about": {"@type": "Thing", "name": "AI Agent Memory"}
    },
    {
      "@type": "FAQPage",
      "mainEntity": [
        {"@type": "Question", "name": "Q1?", "acceptedAnswer": {"@type": "Answer", "text": "A1."}},
        {"@type": "Question", "name": "Q2?", "acceptedAnswer": {"@type": "Answer", "text": "A2."}}
      ]
    }
  ]
}
```

### Schema Coverage by Site

| Site | Required Schema | Injection Method |
|------|----------------|------------------|
| **groktop.us** | Organization (site-wide), TechArticle (per-post), FAQPage (when applicable) | ghost-cli `schema inject` for per-post; Code Injection → Settings for site-wide |
| **rdumesh.org** | Organization + areaServed (site-wide), Article (auto), FAQPage (FAQ content), LocalBusiness if applicable | Same pattern |
| **southeastme.sh** | Organization (site-wide), Article (auto) | Same pattern |

### Validation

Every schema injection must be validated:

1. **Google Rich Results Test:** https://search.google.com/test/rich-results
2. **Schema.org Validator:** https://validator.schema.org/
3. **Manual check:** View page source → search for `application/ld+json`

## Completion Checklist

For every article publish:

- [ ] **Meta Title** set (50-60 chars, keyword front-loaded)
- [ ] **Meta Description** set (150-160 chars, includes keyword + CTA)
- [ ] **Custom Excerpt** set (1-2 sentence summary for cards)
- [ ] **OG Image** set (article feature image or explicit OG image)
- [ ] **OG Title** verified (at minimum, confirm it defaults acceptably)
- [ ] **OG Description** verified (at minimum, confirm it defaults acceptably)
- [ ] **Twitter card** type confirmed (summary_large_image)
- [ ] **Canonical URL** confirmed (self-referencing unless syndicated)
- [ ] **Schema injected** (TechArticle for groktop.us, FAQPage if applicable)
- [ ] **Schema validated** (Google Rich Results Test passes)
- [ ] **Feature image** has alt text and caption
- [ ] **Slug** is optimized (30-45 chars, primary keyword, stable)

## Post-Publish Verification

```bash
# 1. Check meta tags render
curl -s https://<site>/<slug>/ | grep -E '<title|name="description"|property="og:|name="twitter:'

# 2. Check schema renders
curl -s https://<site>/<slug>/ | grep 'application/ld+json'

# 3. Validate schema (requires the JSON block)
# Pipe the extracted JSON-LD to the Rich Results Test API
```
