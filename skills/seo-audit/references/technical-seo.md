# Technical SEO Reference

Technical SEO ensures search engines can find, crawl, interpret, and index your content. If the technical foundation is broken, nothing else matters.

## Crawlability & Indexability

### Robots.txt
- **Purpose:** Directs crawlers which URLs to avoid
- **Check:** Does the site have a robots.txt at `/robots.txt`?
- **Check:** Are important pages accidentally disallowed? `Disallow: /` blocks ALL crawlers
- **Check:** Is the sitemap referenced? `Sitemap: https://example.com/sitemap.xml`
- **Best practice:** Allow CSS/JS files (modern crawlers need them for rendering)
- **Magnus's sites:** Ghost CMS auto-generates robots.txt; verify after any config change

### XML Sitemaps
- **Purpose:** Tells crawlers about all pages and their relative importance
- **Check:** Does the sitemap exist and is it referenced in robots.txt?
- **Check:** Are only canonical URLs included? (No pagination params, sort filters, etc.)
- **Check:** Are noindex pages excluded from the sitemap?
- **Check:** Lastmod dates are accurate (not all the same date)
- **Ghost split sitemaps:** Ghost generates `sitemap-posts.xml`, `sitemap-pages.xml`, `sitemap-tags.xml`, `sitemap-authors.xml`. Verify each is present and valid.
- **Hugo:** Verify sitemap.xml is generated with correct `changefreq` and `priority` settings

### Canonical URLs
- **Purpose:** Tells search engines which URL is the authoritative version of a page
- **Check:** Every page has a self-referencing canonical or points to the canonical version
- **Check:** No conflicting canonicals (page A canonicals to B, B canonicals to C)
- **Common issues:** HTTP/HTTPS duplication (canonical must use HTTPS if site is HTTPS), www/non-www duplication, trailing slash inconsistency
- **Ghost:** Canonical is auto-generated from the post/page slug. Verify no slug changes break inbound canonical signals.

### Meta Robots / Noindex
- **Purpose:** Prevents indexing of specific pages
- **Check:** Pages that should be indexed don't have `<meta name="robots" content="noindex">`
- **Check:** Thin pages (tag pages, author pages, pagination) have noindex if they shouldn't rank
- **Check:** Login/admin pages have noindex

## Page Speed

### Core Web Vitals (Google's ranking signals)
- **LCP (Largest Contentful Paint):** < 2.5s (good), 2.5-4.0s (needs improvement), > 4.0s (poor)
- **FID (First Input Delay) / INP (Interaction to Next Paint):** < 100ms (good), 100-300ms (needs improvement), > 300ms (poor)
- **CLS (Cumulative Layout Shift):** < 0.1 (good), 0.1-0.25 (needs improvement), > 0.25 (poor)

### Common Fixes by Platform

**Ghost CMS:**
- Enable lazy loading for images (Ghost 5+ has built-in)
- Use a CDN for image delivery (Ghost Pro includes; self-hosted needs Cloudflare or similar)
- Limit the number of visible posts on home/tag pages (paginate aggressively)
- Disable unused Ghost integrations and background tasks
- Verify the theme isn't loading unused CSS/JS (many Ghost themes are bloated)

**Hugo (magnus919.com):**
- Hugo generates static HTML — inherently fast
- Image processing: use Hugo's built-in image processing to serve appropriately sized images (`.Resize`, `.Fill`, `.Fit`)
- Minify HTML output: `minify: true` in config
- Avoid excessive JavaScript (Hugo sites shouldn't need much JS)
- Verify CSS is not render-blocking (inline critical CSS if needed)

### Tools for Measurement
- Google PageSpeed Insights (lab + field data)
- Lighthouse (Chrome DevTools)
- Web Vitals library (RUM data)
- GTmetrix / Pingdom (third-party)

## Mobile-Friendliness

- **Check:** Responsive design — does the site render correctly at all viewport widths?
- **Check:** Viewport meta tag present: `<meta name="viewport" content="width=device-width, initial-scale=1">`
- **Check:** Font sizes are readable on mobile (min 16px body text recommended)
- **Check:** Tap targets are adequately sized (min 48x48px recommended)
- **Check:** Content not hidden behind unplayable media or unsupported formats
- **Test:** Google's Mobile-Friendly Test

## HTTPS & Security

- **Check:** Valid SSL certificate (not expired, not self-signed)
- **Check:** All resources load over HTTPS (no mixed content warnings)
- **Check:** HSTS header present for repeat visitors (Strict-Transport-Security)
- **Check:** Redirects HTTP → HTTPS (301 permanent redirect)
- **Check:** No security warnings in browser (mixed content, invalid cert)

## International SEO (If Applicable)

- **hreflang tags:** Correctly implemented for multi-language/multi-region sites
- **Check:** Self-referencing hreflang (each page includes its own language tag as well)
- **Check:** No conflicting signals (hreflang says X, redirect says Y)

## Ghost-Specific Technical SEO

| Check | Where to look | Action |
|-------|---------------|--------|
| Canonical URLs | Post settings → canonical URL | Verify self-referencing or correct canonical |
| Meta robots | Code injection → per-page | No thin pages indexed |
| Sitemap | `/sitemap.xml` | Verify split sitemaps present |
| Robots.txt | `/robots.txt` | Verify sitemaps referenced, no accidental disallows |
| Structured data | Source HTML → JSON-LD | Verify Ghost's built-in JSON-LD is correct + any custom |
| AMP | Ghost settings | Verify AMP is enabled/disabled intentionally (Ghost defaults to disabled in v5+) |
| Open Graph / Twitter Cards | Post social settings | Verify Facebook and Twitter card previews |
