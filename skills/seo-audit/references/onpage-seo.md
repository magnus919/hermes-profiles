# On-Page SEO Reference

On-page optimization ensures each piece of content is structured and written to communicate relevance to search engines while serving the reader.

## Title Tags

The title tag is the single most important on-page SEO element. It appears in SERPs as the clickable headline.

### Best Practices
- **Length:** 50-60 characters (Google typically displays the first 50-60 chars; titles longer than ~580px get truncated)
- **Keyword placement:** Primary keyword near the beginning (front-loaded)
- **Uniqueness:** Every page has a unique title tag — no duplicates
- **Branding:** Include site/brand name at the end (separated by `—` or `|` in SERPs, but per Magnus's voice rule, NO emdashes in prose — for title tags, use `|` as separator)
  - Example: `"SEO Audit for Ghost CMS Sites | Groktopus"`
  - Example: `"The Artifact Pyramid: Progressive Disclosure for Agent Outputs | Magnus Hedemark"`
- **Compelling:** Includes a value proposition or hook that earns the click
- **No keyword stuffing:** Sounds natural, not like a list of keywords

### Magnus's Sites — Patterns

**magnus919.com (Hugo, PaperMod theme):**
- Title set in frontmatter: `title: "..."` 
- Hugo auto-generates `<title>` from the title field
- Verify: `title` in frontmatter is 50-60 chars
- Site name appended automatically by PaperMod: `"Title | Magnus Hedemark"`

**groktop.us (Ghost Pro):**
- Meta title set in Ghost post settings → Meta Data → Custom Meta Title
- Default: Post title (which may be too long — always set a custom meta title)
- Ghost appends site name automatically in the `<title>` tag
- Verify: custom meta title under 60 chars

**rdumesh.org / southeastme.sh (Ghost, self-hosted):**
- Same as groktop.us — custom meta title in Ghost post settings

## Meta Descriptions

Not a direct ranking factor, but the second most important element for click-through rate from SERPs.

### Best Practices
- **Length:** 150-160 characters (longer descriptions may be truncated)
- **Includes primary keyword + secondary keyword naturally**
- **Includes a call to action** ("Learn how...", "Discover why...", "Read the analysis")
- **Unique per page** — no duplicate or auto-generated descriptions
- **Matches search intent** — if someone searches for "progressive disclosure for agents," the description should signal that the page delivers on that query
- **Contractions and natural language** — reads like a person wrote it

### Magnus's Sites — Patterns

**magnus919.com (Hugo, PaperMod):**
- Hugo auto-generates meta description from page summary/content if not specified
- Always set a `description:` field in frontmatter that's 150-160 chars
- This is the meta description and also used in card previews

**groktop.us (Ghost Pro):**
- Custom Meta Description in post settings → Meta Data
- Ghost also uses this for Open Graph description
- If not set, Ghost uses the post excerpt (which may be longer or shorter than ideal)

## Heading Structure

Headings communicate content hierarchy to search engines and provide scanability for readers.

### Hierarchy Rules
- **H1:** Exactly one per page. Should match the title tag (or be a slightly more readable version). Contains the primary keyword.
- **H2:** Major sections of the content. Each H2 should contain a related keyword or subtopic. Used as navigation anchors.
- **H3-H6:** Subsections under H2s. Deeper hierarchy for complex content.
- **No skipping levels:** Don't jump from H1 to H3. Hierarchically nested.

### Checklist
- [ ] Exactly one H1 per page
- [ ] H1 matches or closely relates to the title tag
- [ ] H1 contains primary keyword
- [ ] Headings form a logical outline of the page when read alone
- [ ] No empty headings or headings used purely for styling
- [ ] Keywords appear naturally in headings (not stuffed)
- [ ] H2s and H3s are descriptive, not generic ("Introduction" is weak; "Why Progressive Disclosure Matters for AI Agents" is strong)

## Content Quality

### Keyword Usage
- **Primary keyword appears in:** H1, first paragraph, at least one H2, URL slug
- **Keyword density:** Natural usage — don't target specific percentages. If the keyword appears naturally 3-5 times in a 1500-word article, that's fine.
- **LSI / related keywords:** Include semantically related terms that help establish topical relevance (e.g., for an article about "artifact pyramids," include terms like "progressive disclosure," "multi-agent pipelines," "agent collaboration")
- **No keyword stuffing:** Don't repeat the same phrase unnaturally

### Content Length
- **Blog posts:** 1500-2500 words is typical for long-form content. Magnus's articles often run longer because they're deep analytical pieces. Longer is fine if every word earns its place.
- **Minimum to rank:** 300 words for very simple queries; 1000+ for competitive terms
- **Quality over quantity:** A tight 800-word post that answers the query completely beats a padded 2000-word post that repeats itself

### Readability
- Short paragraphs (2-4 sentences for web reading)
- Bullet points and numbered lists for scannable information
- Bold key terms for emphasis (sparingly)
- Clear section breaks with descriptive headings

### Freshness
- Update dates on evergreen content when significantly revised
- Add "Last updated" or "Updated" notation for major content refreshes
- Google favors freshness for certain query types (news, recent events, technology)

## Internal Linking

Internal links distribute page authority throughout the site and help crawlers discover content.

### Best Practices
- **Link to related content:** Every post should link to 2-5 other posts/pages on the same site
- **Descriptive anchor text:** Use the target topic's keyword as the link text (not "click here" or "read more")
- **Link to cornerstone content:** Important pillar pages should receive more internal links
- **Natural placement:** Links should serve the reader — if it genuinely helps to read more about X, link it
- **Avoid:** Links in navigation that aren't needed, links to the same target with different anchor text, links on every instance of a term

### Magnus's Sites — Patterns

**magnus919.com:** Magnus uses [[wikilinks]] in draft which Hugo converts to hyperlinks. Check that wikilinks are rendering as live HTML links and pointing to existing pages.

**groktop.us (Ghost):** Manual internal links in the editor. Verify that linked posts exist and are published.

## Image Optimization

### Alt Text
- **Purpose:** Accessibility for screen readers + context for search engines (Google Images)
- **Every image** must have a descriptive alt attribute
- **Descriptive:** "Close-up of a Portia labiata spider's principal eyes showing the characteristic three-lens system" — not "Portia spider" or "image001.jpg"
- **Keyword-optimized:** Include relevant keywords naturally when they describe the image
- **No keyword stuffing:** Alt text is first for accessibility, second for SEO
- **Decorative images:** alt="" (empty alt) for purely decorative images so screen readers skip them

### File Names
- Descriptive, hyphenated: `portia-spider-eyes-closeup.jpg` not `IMG_4732.jpg`
- Include target keyword when appropriate
- Use hyphens, not underscores

### File Size
- Compress images before upload (target < 100KB for standard inline images)
- Use next-gen formats: WebP (with JPEG fallback for older browsers)
- Hugo: Use `.WebP` processing or serve via CDN that auto-converts
- Ghost: Compress before uploading — Ghost does minimal image optimization

## URL Structure

### Best Practices
- **Short, descriptive:** `/seo-audit-ghost-cms/` not `/post/12345/`
- **Include primary keyword:** When natural
- **Hyphens, not underscores:** Google treats hyphens as word separators
- **Lowercase:** /seo-audit not /SEO-Audit
- **Stop words:** Remove unnecessary "and", "the", "of", "for" where they don't add meaning
- **Stable:** Once published, never change a URL (breaks all inbound links)

### Magnus's Sites — Patterns
- **magnus919.com:** Hugo uses the post slug from frontmatter or filename. Verify slug is short and contains primary keyword.
- **groktop.us:** Ghost auto-generates slug from title. Set a custom slug in post settings if the auto-generated one is too long or doesn't contain the keyword.
- **Never change published slugs** without explicit instruction from Magnus.
