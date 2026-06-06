---
name: go-to-market
description: >-
  CMO methodology — positioning and messaging frameworks (April Dunford's
  positioning, message hierarchy), customer acquisition strategy (paid, organic,
  PLG, SLG), brand architecture (brand house vs house of brands), growth modeling
  (CAC/LTV by channel, cohort analysis), market entry strategy (beachhead,
  land-and-expand), competitive response (pricing wars, feature races, brand defense).
version: 1.0.0
author: Hermes Agent community
license: MIT
metadata:
  hermes:
    tags: [go-to-market, cmo, marketing, positioning, messaging, acquisition, brand-architecture, growth-modeling, competitive-response, plg, slg]
---

# Go-to-Market — CMO Methodology

CMO-level methodology for go-to-market strategy, positioning, acquisition, brand, and growth modeling. This skill provides the frameworks and reference material for a chief marketing officer profile.

## When to Load

| Trigger | What's Needed |
|---------|---------------|
| Define positioning and messaging | `references/positioning-messaging.md` — Dunford framework, message hierarchy |
| Build acquisition channel strategy | `references/acquisition-strategy.md` — channel mix, PLG/SLG, funnel metrics |
| Design brand architecture | `references/acquisition-strategy.md` — brand systems, visual identity, brand health |
| Model growth economics | `references/growth-modeling.md` — CAC/LTV, cohort analysis, market entry |
| Develop competitive response | `references/acquisition-strategy.md` — pricing wars, feature races, brand defense |
| Plan market entry | `references/growth-modeling.md` — beachhead, land-and-expand, channel economics |

## Loading Order

```text
skill_view('go-to-market')
# Then domain-specific references:
skill_view('go-to-market', file_path='references/positioning-messaging.md')
skill_view('go-to-market', file_path='references/acquisition-strategy.md')
skill_view('go-to-market', file_path='references/growth-modeling.md')
```

## Reference Files

| Reference | Purpose |
|-----------|---------|
| `references/positioning-messaging.md` | April Dunford positioning, message hierarchy (elevator pitch → value prop → narrative), positioning diagnostic |
| `references/acquisition-strategy.md` | Channel taxonomy, PLG vs SLG playbooks, sales funnel ratios, competitive response playbook, brand architecture |
| `references/growth-modeling.md` | CAC/LTV deep dive, cohort analysis practical guide, NRR, market entry strategy (beachhead, land-and-expand) |

## Output Contract

The profile using this skill produces artifact pyramids. The response to any caller is the absolute path to `00-index.md`. See `artifact-pyramids` skill for the specification.

## Related Skills

- `artifact-pyramids` — output contract
- `product-strategy` — CPO methodology (product vision, PMF, market sizing)
- `brand-designer` — visual brand identity design
- `seo-content-optimization` — organic search and content strategy
