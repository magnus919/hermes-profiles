# Journalistic Research Track

For the publication investigative pieces — source-heavy, narrative-driven work where facts must survive public scrutiny.

## The Core Difference From Academic Research

Academic research assumes all sources are published and findable. Journalistic research assumes the best sources are people, documents that weren't meant to be public, and observations the researcher makes firsthand. The evidence is messier, the verification burden is higher, and the stakes for getting it wrong are immediate.

## Primary Source Handling

### The Hierarchy of Journalistic Evidence

| Tier | Source type | How to treat it |
|------|-------------|-----------------|
| 1 | **Primary documents** — emails, internal memos, court filings, financial statements, code commits, leaked data | Highest weight. Corroborate authenticity, then treat as ground truth for what the document says |
| 2 | **Firsthand testimony** — someone who was there, saw it happen, or did the thing | Named sources are stronger than anonymous. Corroborate specifics against documents when possible |
| 3 | **Contemporary records** — meeting notes, chat logs, recordings made at the time | Stronger than memory. Memory is unreliable within weeks |
| 4 | **Published reporting** — other journalists who covered the story | Cite them, don't re-report their work. If you stand on their reporting, make it visible |
| 5 | **Secondhand accounts** — someone who heard from someone who was there | Weakest tier. Only use if primary sources are unavailable and the chain is short |

### The Named Source Standard

**Always prefer named sources.** A named source who is proven wrong damages your credibility. An anonymous source who is proven right also damages your credibility — because the reader can't verify who said it.

When a source requests anonymity:

1. **Establish why.** Is it fear of retaliation, a non-disclosure agreement, or discomfort with public attribution? The reason determines how much weight to give the information.
2. **Know their identity.** The reader may not know who they are, but you must. Record it. The source must be verifiable to you even if not to the reader.
3. **Corroborate their claims.** An anonymous source making a verifiable claim is useful. An anonymous source making an unverifiable claim is hearsay.
4. **Never grant anonymity to a source you haven't spoken to directly.** Secondhand anonymous sourcing is not sourcing.
5. **Disclose what you can.** "A current employee who spoke on condition of anonymity because they were not authorized to discuss internal matters" is better than "sources say."

### Interview Integrity

- **Record the conversation.** Always ask permission. If they decline, take contemporaneous notes and read critical quotes back during the interview for confirmation.
- **Verify identity.** If you haven't met the person before, verify who they are before treating their information as source material. LinkedIn, corporate website, cross-reference with others.
- **Context matters.** What else was happening when they said this? Under what circumstances did they share this information? A source who is angry may overstate. A source who is afraid may understate.
- **Follow up.** The best quote often comes after you've turned off the recorder — or in a second conversation after they've had time to think.

## Document Investigation

Not all valuable evidence comes from people. Some of the best sources are documents that exist in plain sight.

### Types of Documents Worth Finding

| Document type | What to look for | Where to find it |
|--------------|-----------------|------------------|
| **Git history** | When was a feature added? Who committed it? What was the commit message? Was it reviewed? | GitHub, git log, pull request discussions |
| **Earnings transcripts** | What does leadership actually say about their strategy? Compare with what they do. | SEC.gov, investor relations pages, earnings call transcripts |
| **Job postings** | What skills are they hiring for? What does the job description reveal about priorities or problems? | Company career pages, LinkedIn |
| **Support forums** | What are users actually struggling with? What workarounds have they developed? | GitHub issues, community forums, subreddits |
| **Change logs** | What did the product look like 6 months ago vs now? What features were removed? | Changelog archives, Wayback Machine |
| **Filing/pipeline documents** | SEC filings, patent applications, regulatory submissions | EDGAR, patent databases, FCC filings |

### Reading With Intent

Don't just read a document — interrogate it:

- **Who created this, and why?** Every document has an intended audience and a purpose. A press release is meant to make the company look good. An internal memo is meant to communicate operational direction. A patent application stakes a legal claim.
- **What's missing?** Absences are often more revealing than presences. A security audit that doesn't mention authentication is a finding. A press release that doesn't name the CEO is a signal.
- **What assumptions does it rely on?** "Q4 revenue grew 15% year-over-year" assumes the previous year's Q4 is the right baseline. What if they had an acquisition that quarter?
- **Does the headline match the body?** Press releases, blog posts, and reports often have headlines that overstate the findings in the body. Read past the lede.

## The Three-Source Rule (Journalism Version)

For any factual claim that:
- Accuses someone of wrongdoing
- Relies on a surprising statistic
- Is contested by other sources
- Would be damaging if wrong

**Require three independent sources.** Not three articles citing each other. Three genuinely independent sources — different people, different documents, different methodologies — all pointing to the same fact.

If you can't get three, report the confidence gap: "Only one person with direct knowledge would speak about it, but their account was consistent with internal documents reviewed by [publication]."

## Researching Across a Series

When researching article 3 of a 5-part series, the trap is re-researching what was already established.

### Per-Installment Research Map

For each article in a series:

| Dimension | Done in earlier installment | Needs research for this one |
|-----------|---------------------------|----------------------------|
| **Shared context** | What the reader already knows from parts 1-2 | What new context does this installment need? |
| **Sources to revisit** | Experts who were informative earlier | Is there a new angle that warrants a follow-up conversation? |
| **Claims that need updating** | Facts established in earlier parts | Have any changed since publication? |
| **Recurring characters** | People introduced in earlier parts | Do they appear in this installment? Do they need re-introduction? |
| **Thematic throughline** | What theme has connected the series so far | Does this installment advance it, complicate it, or branch? |

### The Series Brief

Before starting research on a new installment, write a one-paragraph "where we are" summary that answers:
1. What has the series established definitively so far?
2. What open questions remain from earlier installments?
3. What new ground does this installment cover?
4. What sources from earlier installments could speak to this new ground?

This prevents re-researching and keeps each installment building on the last.

## Pre-Publication Verification Protocol

Before any the publication piece with investigative stakes ships:

1. **Read every quote in the draft against the source.** Not from memory. From the recording or notes. Word for word.
2. **Open every link in the draft.** Does the source say what the draft claims? Numbers match? Quotes exact?
3. **Triangulate every surprise claim.** If a finding would change what the reader thinks, it needs at least two sources.
4. **Check recency.** Statistics cited as "current" within 2 years for fast-moving tech, 5 years for slower domains. Flag outdated data explicitly.
5. **Audit for paraphrase drift.** The draft may accurately cite a source but mis-state the strength of the claim. A paper that says "suggests" should not be paraphrased as "proves."
6. **Flag single-source claims.** Any claim that rests on a single source should be called out in the draft. The reader deserves to know the evidence base.
7. **Run the "what if I'm wrong" test.** If every claim in this article turned out to be false, which ones would do the most damage? Verify those hardest.
