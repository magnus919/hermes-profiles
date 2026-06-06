# C-Suite Council Template

Standard council composition for strategic-level debates. Assembles the full executive team
to stress-test proposals from different altitudes.

## Composition

| Profile | Role | Weight | Optimization Function |
|---|---|---|---|
| ceo | CEO | 1.2 | Long-term value, strategic coherence |
| cto | CTO | 1.0 | Technical leverage, velocity |
| cfo | CFO | 1.0 | Capital efficiency, risk management |
| coo | COO | 1.0 | Process reliability, scalability |
| cpo | CPO | 1.0 | User value, market differentiation |
| cmo | CMO | 1.0 | Market presence, brand coherence |
| clo | CLO | 0.8 | Legal risk, compliance |
| chro | CHRO | 0.8 | Organizational capability, talent |

## Sub-Templates

### Strategic Triad (CEO/CTO/CFO)
For resource allocation, major investments, build-vs-buy at company level.
Profiles: ceo, cto, cfo

### Product Strategy Quad (CEO/CPO/CTO/CMO)
For product direction, market entry, competitive positioning.
Profiles: ceo, cpo, cto, cmo

### Operational Review (CEO/COO/CFO/CHRO)
For scaling decisions, organizational design, process investment.
Profiles: ceo, coo, cfo, chro

### Risk Assessment (CEO/CFO/CLO/CTO)
For compliance exposure, IP strategy, regulatory response.
Profiles: ceo, cfo, clo, cto

## Council Dynamics

- **CEO breaks deadlocks** — when the council can't converge, the CEO makes the call
- **CFO stress-tests everything** — every proposal gets a financial viability check
- **CLO has veto power** on legal exposure with documented rationale
- **CHRO evaluates organizational readiness** — can we execute with current talent?

## Loading Order

```python
skill_view('executive-methodology')
skill_view('artifact-pyramids')
# Role-specific per profile:
skill_view('strategy-frameworks')      # CEO
skill_view('technology-radar')         # CTO
skill_view('financial-modeling')       # CFO
skill_view('operational-design')       # COO
skill_view('product-strategy')         # CPO
skill_view('go-to-market')             # CMO
skill_view('legal-strategy')           # CLO
skill_view('org-design')               # CHRO
```
