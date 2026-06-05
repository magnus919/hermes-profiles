# Schema Markup / Structured Data Reference

Structured data helps search engines understand the content of a page and enables rich results in SERPs (FAQ snippets, HowTo steps, breadcrumbs, article previews).

## JSON-LD Format

Google's preferred format. All structured data on Magnus's sites should be JSON-LD injected via Ghost's Code Injection or Hugo's templates.

### Basic Structure

```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "Title of the Article",
  "description": "150-160 char meta description",
  "author": {
    "@type": "Person",
    "name": "Magnus Hedemark"
  },
  "datePublished": "2026-05-01",
  "dateModified": "2026-05-15",
  "image": "https://example.com/image.jpg",
  "publisher": {
    "@type": "Organization",
    "name": "Groktopus",
    "logo": {
      "@type": "ImageObject",
      "url": "https://www.groktop.us/favicon.png"
    }
  }
}
```

## Schema Types for Magnus's Sites

### TechArticle (groktop.us)
Use for technical/analytical content about AI, enterprise technology, and engineering.

```json
{
  "@context": "https://schema.org",
  "@type": "TechArticle",
  "headline": "Article Title",
  "description": "Description",
  "author": {
    "@type": "Person",
    "name": "Magnus Hedemark"
  },
  "datePublished": "2026-05-01",
  "dateModified": "2026-05-15",
  "proficiencyLevel": "Advanced",
  "about": {
    "@type": "Thing",
    "name": "Topic area"
  }
}
```

### Article / BlogPosting (magnus919.com)
Use for personal blog and analytical long-form content.

```json
{
  "@context": "https://schema.org",
  "@type": "BlogPosting",
  "headline": "Title",
  "description": "Description",
  "author": {
    "@type": "Person",
    "name": "Magnus Hedemark"
  },
  "datePublished": "2026-05-01",
  "dateModified": "2026-05-15"
}
```

For articles authored by Jasper:

```json
{
  "@context": "https://schema.org",
  "@type": "BlogPosting",
  "headline": "Title",
  "description": "Description",
  "author": {
    "@type": "Person",
    "name": "Jasper"
  },
  "datePublished": "2026-05-01",
  "dateModified": "2026-05-15"
}
```

### FAQPage (All Sites)
Use when the article answers multiple distinct questions. Enables FAQ rich results in SERPs.

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "Question 1?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Answer text here."
      }
    },
    {
      "@type": "Question",
      "name": "Question 2?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Answer text here."
      }
    }
  ]
}
```

**Requirements for Google rich result eligibility:**
- Minimum 2 questions
- Questions must be visible text on the page (not hidden)
- Each Question must match visible content
- Answers must be clearly visible to the user (not just in schema)
- Google may show up to 4 FAQ entries in the SERP

### HowTo (Tutorials, Technical Guides)
Use for step-by-step guides and tutorials on any site.

```json
{
  "@context": "https://schema.org",
  "@type": "HowTo",
  "name": "How to Title",
  "description": "Description of the tutorial",
  "step": [
    {
      "@type": "HowToStep",
      "position": 1,
      "name": "Step 1",
      "text": "Description of step 1."
    },
    {
      "@type": "HowToStep",
      "position": 2,
      "name": "Step 2",
      "text": "Description of step 2."
    }
  ]
}
```

### BreadcrumbList (Site Navigation)
Use on all sites to enable breadcrumb rich results in SERPs.

```json
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {
      "@type": "ListItem",
      "position": 1,
      "name": "Home",
      "item": "https://www.groktop.us/"
    },
    {
      "@type": "ListItem",
      "position": 2,
      "name": "Category",
      "item": "https://www.groktop.us/category/"
    },
    {
      "@type": "ListItem",
      "position": 3,
      "name": "Article Title",
      "item": "https://www.groktop.us/article-slug/"
    }
  ]
}
```

### Organization (Site-level)
Use on all sites for site-level schema (injected globally, not per-page).

```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Site Name",
  "url": "https://www.example.com/",
  "logo": "https://www.example.com/favicon.png",
  "sameAs": [
    "https://twitter.com/username",
    "https://github.com/username"
  ]
}
```

## Platform-Specific Implementation

### Ghost CMS (groktop.us, rdumesh.org, southeastme.sh)

**Per-page schema:**
- Ghost injects basic JSON-LD automatically (Article type with headline, dates, author)
- Custom schema (FAQPage, HowTo, TechArticle) goes in:
  - Post-level: Settings → Code Injection → Post Header (`<script type="application/ld+json">...</script>`)
  - Site-level: Settings → Code Injection → Site Header (BreadcrumbList, Organization)

**Verification:**
- View source → search for `application/ld+json`
- Test with Google Rich Results Test: https://search.google.com/test/rich-results
- Test with Schema.org Validator: https://validator.schema.org/

**Ghost auto-generated schema limitations:**
- Ghost only generates Article/BlogPosting schema by default
- FAQPage, HowTo, TechArticle, BreadcrumbList, Product all require custom injection
- Author info in Ghost's default schema may need enrichment (add author URL, sameAs)

### Hugo (magnus919.com)

**Per-page schema:**
- Add JSON-LD via Hugo template in `layouts/partials/head.html` or `layouts/_default/single.html`
- Use Hugo's `.Params` to inject article-specific values
- Conditional schema: `{{ if .Params.faq }}` for FAQPage, `{{ if .Params.howto }}` for HowTo

**Site-level schema:**
- Organization and BreadcrumbList in the base template (`baseof.html`)

## Validation Checklist

- [ ] JSON is valid (no trailing commas, properly closed braces)
- [ ] Required fields present for each @type
- [ ] URLs are absolute (including https://)
- [ ] Dates are in ISO 8601 format (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SSZ)
- [ ] Author names match the byline
- [ ] @context is set to "https://schema.org"
- [ ] No conflicting or duplicate schema on the page
- [ ] FAQPage content matches visible page content (no hidden answers)
- [ ] Google Rich Results Test passes without errors
- [ ] Schema content is visible to users where required (FAQPage, HowTo)
