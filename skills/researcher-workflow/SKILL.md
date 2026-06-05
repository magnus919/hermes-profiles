---
name: researcher-workflow
description: >-
  Non-interactive deep research pipeline for specialist subagents.
  Use when the orchestrator, product-manager, or another profile assigns a
  research mission that requires systematic investigation with progressive
  disclosure. The researcher receives a brief, interpolates scope, executes
  multi-pass research via groktocrawl, evaluates gaps for recursion, and
  produces a layered artifact pyramid in /tmp/.
compatibility: Hermes Agent — designed for non-interactive subagent operation
metadata:
  tags: [workflow, bundle, research, subagent, pipeline, progressive-disclosure]
  spec-version: "1.0"
---

# Researcher Workflow

A 5-phase workflow for systematic deep research with progressive disclosure artifact output. Designed for the researcher specialist subagent profile when dispatched by an orchestrator.

```
RECEIVE MISSION → GATHER → EVALUATE GAPS → [RECURSE] → BUILD PYRAMID → DELIVER
```

## Sub-Skills

| Phase | Skill | Trigger |
|-------|-------|---------|
| Receive Mission | `researcher-workflow/receive-mission` | Orchestrator assigns a research brief — reformulate into explicit scope |
| Gather | `researcher-workflow/research-gather` | Execute research using groktocrawl suite exclusively |
| Evaluate Gaps | `researcher-workflow/evaluate-gaps` | Assess gathered material, decide on recursion depth |
| Build Pyramid | `researcher-workflow/build-pyramid` | Assemble progressive disclosure artifact files |
| Deliver | `researcher-workflow/deliver-findings` | Report back with absolute path references and layer descriptions |

## Navigation

When this umbrella is loaded (by the researcher profile), identify which phase you're in, load the corresponding sub-skill via `skill_view()`, and follow its instructions. Each sub-skill documents its transition signals.

## Pipeline Heuristics

- **Entry:** Always starts at Phase 1 (Receive Mission). The other phases cannot be entered directly.
- **Recursion:** Phase 3 (Evaluate Gaps) can loop back to Phase 2 (Gather) for targeted follow-up. This is the only non-linear path.
- **Tool discipline:** ALL web research goes through groktocrawl. The built-in web_search and web_extract tools are explicitly prohibited — they are insufficient and often broken. See references/tool-governance.md for the full fallback chain and rationale. Load with skill_view(name="researcher-workflow", file_path="references/tool-governance.md").
- **Artifacts:** Output is written to /tmp/researcher-workflow/<mission-slug>/ as layered markdown files. Each layer links downward with descriptions so consuming agents can choose their depth.
- **State:** No persistent state between phases. Each sub-skill reads the mission brief and artifact directory to determine context.

## Pitfalls

### delegate_task timeout recovery

The Gather phase uses delegate_task to spawn subagents for parallel research. These subagents have a 600-second hard timeout. When a single monolithic research task times out, split into parallel sub-tasks (up to 3) each covering a distinct methodology, source, or angle. This succeeded for two of three parallel tasks in one real session; the third still timed out.

Second-line fallback when parallel sub-tasks also timeout: use direct groktocrawl scrape on known canonical URLs for the remaining sources. Note that `groktocrawl agent` and `groktocrawl search` may return empty results even when the server is functioning — `agent` sometimes returns "unable to find any relevant web pages" and `search` may be unconfigured. The reliable fallback is `groktocrawl scrape <url>` on each known canonical URL individually. Known URLs for common architecture-methodology sources:
- https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions — Michael Nygard's original ADR post
- https://docs.arc42.org/ — arc42 template docs with all 12 sections listed
- https://arc42.org/canvas — arc42 Canvas (zip-version of full template)
- https://www.cs.ubc.ca/~gregor/teaching/papers/4+1view-architecture.pdf — Kruchten's original 1995 paper
- https://c4model.com — Simon Brown's C4 Model

Key recovery principle: When the subagent times out, the research question is still valid. Recover by reducing each subagent's scope (fewer sources per agent) and filling the gap with direct groktocrawl scrapes on specific URLs rather than re-delegating the same bundle.
