# The Artifact Pyramid: Framework & Symmetry

## The Core Insight

Progressive disclosure governs how we feed AI agents context: start with metadata (~100 tokens), expand to instructions on activation (<5000 tokens), and load resources on demand. **The Artifact Pyramid applies the same principle to what agents produce.**

The same constraint — finite context windows and nonlinear quality degradation from overload — applies whether an agent is reading a skill description or reading a research artifact. The same solution — progressive disclosure via layered, linked, on-demand-loadable units — applies whether the agent is loading procedural knowledge or receiving declarative findings.

## The Asymmetry Problem

In current AI agent workflows:

| | Input Side | Output Side |
|---|---|---|
| Structure | Progressive disclosure (3 tiers) | Single flat document |
| Consumption | Load only what's needed | Everything bundled together |
| Cost | ~2500 tokens overhead for 50 skills | Full context window per consumer |

Every agent in a multi-agent pipeline inherits context from upstream agents. Without the pyramid, context accumulates across stages until every downstream agent operates in a window polluted by material irrelevant to its specific role.

## The Symmetry

| Input Tier (Skill Loading) | Output Tier (Artifact Pyramid) |
|---|---|
| **Metadata:** name + description (~100 tokens) | **L1 Summary:** key findings, implications (entry point) |
| **Instructions:** full skill body on activation | **L2 Analysis Collection:** per-dimension files |
| **Resources:** reference files loaded on demand | **L3 Detailed Dossiers:** source excerpts, transcripts |

The symmetry is the core architectural insight: the same three-tier model, the same context economy discipline, applied to what agents write rather than what they read.

## Relationship to Other Frameworks

### DIKW Pyramid (Ackoff 1989)

| DIKW | Artifact Pyramid |
|---|---|
| Wisdom | L1 Summary (actionable insights, decisions) |
| Knowledge | L2 Analysis Collection (connected understanding) |
| Information | L3 Detailed Dossiers (extracted data points) |
| Data | Raw primary sources (unprocessed captures) |

### Agent Skills (agentskills.io)

The Artifact Pyramid is the Agent Skills model reflected outward:

```
Skill File:     SKILL.md (metadata) → SKILL.md body (instructions) → references/ (resources)
     ↓ mirror
Artifact:       L1 Summary (metadata) → L2 Analysis (instructions) → L3 Dossiers (resources)
```

## Multi-Agent Routing

The pyramid gives an orchestrator the precision to deliver only what each downstream profile requires:

| Agent Profile | Receives |
|---|---|
| Product Manager Agent | L1 Summary only |
| Market Analyst Agent | Specific L2 analysis files |
| Data Architect Agent | L3 Dossiers |
| Validator Agent | L3 Dossiers + L2 files |

This prevents the context accumulation problem: each agent gets exactly what it needs, nothing more.

## When the Pyramid Breaks

1. **Ephemeral output**: A one-off calculation doesn't need three layers.
2. **Source IS the output**: Collecting data without synthesizing collapses the pyramid.
3. **Single consumer only**: If the same agent consumes and produces, the overhead of structured handoffs may not justify itself.
4. **Tiny output**: A three-sentence answer doesn't need three layers.

Use the pyramid when: research depth > 5 sources, multi-agent handoffs are involved, or outputs need to be auditable and reusable.
