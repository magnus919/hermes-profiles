# Content Strategy SEO Reference

Content strategy SEO ensures that what you write positions you to be discovered for the queries your audience actually searches for.

## Topic Clusters & Pillar Pages

The modern SEO content architecture replaces the old model of writing individual articles about individual keywords. Instead, content is organized into **topic clusters** centered on **pillar pages**.

### How It Works

- **Pillar page:** A comprehensive, long-form guide to a broad topic (e.g., "The Complete Guide to AI Agent Memory Systems"). It covers the topic broadly and links out to cluster content.
- **Cluster content:** Specific articles that dive deep into sub-topics (e.g., "What is a Vector Database?", "How RAG Works", "GraphRAG vs Vector Search"). Each cluster article links BACK to the pillar page.
- **Internal linking:** Cluster → pillar (always). Pillar → cluster (when relevant).

### Why It Works

- **Topical authority:** A group of pages all linking to each other around a common topic signals deep expertise to search engines
- **SERP dominance:** Instead of competing for one keyword, you compete for an entire topic area
- **User experience:** Readers naturally flow from intro content (pillar) to deep dives (clusters)

### Applying to Magnus's Sites

**magnus919.com — Example clusters:**
- Pillar: "AI Agent Memory Systems"
- Clusters: "Vector Databases for Agent Memory," "Knowledge Graphs vs Vector Search," "Cashew Thought-Graph Architecture," "What is GraphRAG?"

**groktop.us — Example clusters:**
- Pillar: "Enterprise AI Agent Deployment"
- Clusters: "RAG at Scale: Lessons from Production," "AI Agent Orchestration," "Security Considerations for Enterprise AI," "Cost Optimization for LLM Inference"

## Keyword Research

### Process
1. **Identify seed keywords** — the 3-5 core terms that define your site's domain
2. **Expand via SERP analysis** — search each seed keyword and analyze the "People also ask" box, related searches at page bottom, and the top-ranking pages' headlines
3. **Identify question-based queries** — "how does X work", "what is Y", "why Z matters" — these are excellent for featured snippet opportunities
4. **Analyze search intent** — is the query informational (learning), navigational (finding a specific site), commercial (comparing options), or transactional (buying)? Match your content type to intent.
5. **Assess competition** — are the top 10 results thin blog posts or deep authoritative guides? If the top results are weak, there's an opportunity.

### Keyword Mapping

Map each article to 1 primary keyword and 2-5 secondary/related keywords:

```
Article: "The Artifact Pyramid: Progressive Disclosure for Agent Outputs"
Primary:  "artifact pyramid"
Secondary: "progressive disclosure AI", "multi-agent output structure", 
           "agent collaboration format", "research output pyramid"
```

### Tools
- Google Search Console (what queries your site already ranks for)
- Google "People also ask" / related searches (free, authoritative)
- AnswerThePublic (question-based query discovery)
- Ahrefs / Semrush (paid — comprehensive keyword data)

## SERP Feature Targeting

Target specific SERP features by structuring content appropriately:

| SERP Feature | Best for | Content Structure |
|-------------|----------|-------------------|
| **Featured Snippet (Paragraph)** | "What is X" questions | Direct answer in first paragraph after H2. 40-50 words. |
| **Featured Snippet (List)** | "Steps to X", "Types of X" | Numbered or bulleted list in the content. |
| **Featured Snippet (Table)** | Comparisons, specifications | HTML table with clear headers and data. |
| **FAQ Rich Result** | Multiple related questions | FAQPage schema with 2+ Q&A pairs visible in content. |
| **HowTo Rich Result** | Tutorials, guides | HowTo schema with numbered steps. |
| **People Also Ask** | Question-based queries | Address each question in its own H2 section. |
| **Knowledge Panel** | Brand/organization queries | Organization schema, Wikipedia entry, verified social profiles. |

## Content Gap Analysis

### Process
1. **Identify your target keywords** (the terms you WANT to rank for)
2. **Check your current rankings** (do you already have content for these?)
3. **Analyze top 10 results** for each keyword:
   - What content format are they using? (listicle, guide, video, tool)
   - How long is the content?
   - What angle do they take?
   - What's missing from their coverage?
4. **Identify gaps:** Topics where your site has no content, or where your content is weaker than competitors'
5. **Prioritize:** Volume × difficulty × relevance — focus on high-volume gaps that you can credibly fill

### Gap Types
- **Missing topic:** No content exists on your site for a search-worthy topic
- **Thin content:** Content exists but is significantly weaker than competitors'
- **Outdated content:** Content exists but is no longer accurate or current
- **Format gap:** Competitors rank with a format you haven't used (e.g., video, interactive tool, data study)

## Topical Authority

Topical authority is built over time by publishing a breadth and depth of content on a subject. It's the most defensible SEO strategy because it can't be replicated quickly.

### Building Topical Authority
1. **Publish the pillar page first** — broad, comprehensive, definitive
2. **Publish cluster content regularly** — 2-3 sub-topic articles per month
3. **Interlink systematically** — every cluster article links to the pillar; the pillar links to clusters
4. **Refresh content** — update pillar pages annually, cluster content as needed
5. **Expand scope** — once you've covered the core topic, expand to adjacent topics

### Signals of Topical Authority
- Your content ranks for multiple related keywords
- Your content appears in "People also ask" for the topic
- Other sites link to your content as a reference
- Your content is cited in academic or industry publications

## Magnus's Sites — SEO Opportunity Assessment

| Site | Domain Authority | Primary Keyword Focus | Largest Gap |
|------|-----------------|----------------------|-------------|
| magnus919.com | Low (newer personal blog) | AI philosophy, neurodiversity, engineering | Few internal links between related posts; no topic cluster structure |
| groktop.us | Low (newer enterprise AI blog) | Enterprise AI strategy, agentic AI | Very new — needs pillar pages and cluster strategy from the start |
| rdumesh.org | Very low (community site) | Mesh networking, MeshCore, RDUMesh | Local SEO for Raleigh/Durham; community resource queries |
| southeastme.sh | Minimal | Southeast mesh networking | Mostly informational — just needs proper on-page SEO |

### Recommended Actions by Site

**magnus919.com:**
- Implement topic clusters retroactively (group existing posts into 3-4 clusters with pillar pages)
- Ensure every post links to 2-3 other posts
- Add FAQPage schema to posts that answer multiple questions
- Optimize for "People also ask" by structuring content around questions

**groktop.us:**
- Plan pillar pages first before creating more isolated content
- Target question-based keywords for featured snippet opportunities
- Implement TechArticle schema on all technical posts
- Focus on long-tail, low-competition keywords in the short term

**rdumesh.org:**
- Local SEO: "mesh network Raleigh," "MeshCore North Carolina"
- Community-Q&A content for FAQ rich results
- Event pages for meetup/community gathering SEO

## Content Calendar

SEO content strategy produces a **ranked list** of content opportunities, not a dated calendar. Magnus works in bursts, not on fixed schedules. Prioritize by:

1. **Search volume × relevance** — How many searches × how well it fits the site
2. **Competition gap** — How much better can we be than the current top results?
3. **Ease of creation** — Does the research already exist in the vault or is it a new domain?
4. **Pillar dependency** — Should this be created before or after the pillar page?
