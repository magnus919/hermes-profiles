---
name: research-gather
description: >-
  Systematic multi-pass research gathering using the groktocrawl suite
  exclusively. Prohibits web_search and web_extract tools. Follows a
  deterministic fallback chain: agent → search → scrape → browser.
  When dispatched as a subagent, run this skill to execute the research
  phase of the researcher-workflow.
compatibility: Hermes Agent
metadata:
  tags: [research, gathering, groktocrawl, web-extraction]
  spec-version: "1.0"
---

# Research Gather

## When to Use

Load this skill after completing Phase 1 (Receive Mission) — the SCOPE.md document exists and the artifact directory is ready. This is the execution phase: turning the research questions into gathered material.

## TOOL PROHIBITION

**DO NOT USE `web_search` or `web_extract` tools.** They are insufficient for systematic research and frequently broken. ALL web research must go through the groktocrawl suite:

| Need | groktocrawl command | Why |
|------|---------------------|-----|
| Multi-source research + synthesis | `groktocrawl agent "<prompt>"` | Searches, scrapes, and synthesizes autonomously |
| Web search for discovery | `groktocrawl search "<query>" --limit N --json` | Returns structured search results |
| Single page content | `groktocrawl scrape <url>` | Clean markdown extraction |
| JS-heavy / bot-protected pages | `groktocrawl browser` suite | Headless browser with JS rendering |
| Binary files (PDFs, images) | `groktocrawl download <url>` | File download |
| URL discovery on a site | `groktocrawl map <url>` | Breadth-first route discovery |
| Site-wide extraction | `groktocrawl crawl <url>` | Recursive depth-first scraping |

## What to Do

### 1. Read the Scope

Read `/tmp/researcher-workflow/<mission-slug>/SCOPE.md`. Understand the research questions, scope boundaries, and known unknowns.

### 2. Load Research Methodology

If not already loaded, load the shared methodology references:

```
skill_view(name="research-methodology", file_path="references/source-evaluation.md")
skill_view(name="research-methodology", file_path="references/synthesis-patterns.md")
```

### 3. Execute First Research Pass

Use `groktocrawl agent` for the broadest coverage:

```bash
groktocrawl agent "Research the following: <reformulated questions from SCOPE.md>. Focus on: <domains from approach section>. Synthesize key findings, identify conflicting claims, and flag gaps."
```

Save the output to a timestamped research log:

```bash
cat > /tmp/researcher-workflow/<mission-slug>/layer-3-detailed/01-gather-pass-1.md << 'EOF'
# Gather Pass 1: <date>

## Sources Consulted
- <list URLs and what each provided>

## Key Findings
- <findings organized by research question>

## Conflicting Claims
- <where sources disagree>

## Potential Gaps
- <what seems missing or thin>
EOF
```

### 4. Fill Specific Gaps (Targeted Follow-ups)

For each identified gap, use the appropriate groktocrawl command:

- **Light gap** (need a quick fact): `groktocrawl search "<specific query>" --limit 3`
- **Medium gap** (need a single article): `groktocrawl scrape <url>`
- **Deep gap** (need synthesis): `groktocrawl agent "<focused prompt>"`
- **JS-rendered content**: groktocrawl browser suite

### 5. Evaluate Source Quality

For each source, apply the CRAAP test (from source-evaluation.md):
- **Currency:** Is this timely for the research question?
- **Relevance:** Does it actually address the question?
- **Authority:** Who wrote it and what are their credentials?
- **Accuracy:** Is the evidence sound and verifiable?
- **Purpose:** Why does this source exist? Any bias?

Flag low-quality sources in the research log. Do not discard them — note their limitations so the synthesis can account for them.

## Transition Signals

Move to Phase 3 (Evaluate Gaps) when:
- Initial pass is complete and saved to the artifact directory
- At least one round of targeted follow-ups has been done
- Gaps are documented in the research log
- Source quality has been assessed

You may also transition if the initial pass clearly saturated the topic (no significant gaps remain).

## What to Save

Each research pass should produce a dated file in `/tmp/researcher-workflow/<mission-slug>/layer-3-detailed/`. This builds the bottom layer of the pyramid — detailed dossiers of raw findings.
