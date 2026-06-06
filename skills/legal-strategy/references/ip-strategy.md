# IP Strategy — Patents, Trademarks, Trade Secrets, and Open Source Licensing

## Patent Strategy

### Types of Patents

| Type | Duration | Subject matter | Example |
|------|----------|----------------|---------|
| **Utility patent** | 20 years from filing | Processes, machines, articles of manufacture, compositions of matter | Software algorithm, hardware device |
| **Design patent** | 15 years (US) | Ornamental design of a functional item | Icon design, product shape |
| **Provisional patent** | 12 months (placeholder) | Establishes priority date, doesn't become a patent automatically | "Patent pending" status |

### Patent Filing Strategy

| Strategy | When to use | Example |
|----------|-------------|---------|
| **Defensive filing** | Core technology you want to protect | Foundational algorithm |
| **Offensive filing** | Blocking competitors in key areas | Patent thicket around a technology domain |
| **Landscape filling** | Identify gaps in competitor portfolios and file there | Adjacent use cases competitors haven't claimed |
| **Standard-essential** | Technology required by an industry standard | 5G, Wi-Fi, video codecs |

### The Patent Process

```
Disclosure → Prior art search → Drafting → Filing → Examination → Grant/Maintenance
                                                                         ↓
                                                                Patent pools / licensing / enforcement
```

**Key decision:** Trade secret vs patent. Patents require public disclosure; trade secrets can last indefinitely. If the technology can be reverse-engineered with moderate effort, patent. If the secret can be kept (Coca-Cola formula, Google PageRank algorithm), consider trade secret.

## Trademark Strategy

### Trademark Types

| Type | Examples | Protection |
|------|----------|------------|
| **Word mark** | "Google," "Apple" | The word itself, in any stylization |
| **Design mark** | Nike swoosh, Apple logo | The visual design |
| **Sound mark** | Intel jingle, MGM lion roar | Sonic brand identity |
| **Trade dress** | Coca-Cola bottle shape, Tiffany blue | Product appearance or packaging |

### Trademark Clearance

Before adopting a mark, conduct:

1. **Screening search** — Internal database, general web search
2. **Full availability search** — USPTO / EUIPO trademark database
3. **Common law search** — Business registries, domain names, social media handles
4. **International search** — Madrid Protocol if filing in multiple jurisdictions

**Risk levels:**
| Finding | Risk | Action |
|---------|------|--------|
| No conflicting marks | Low | Proceed |
| Conflicting mark in different class/geography | Medium | File with careful monitoring |
| Direct conflict with active mark in same class | High | Abandon or acquire |

## Trade Secret Management

### Legal Requirements (US — DTSA / State Law)

A trade secret must:
1. Have **independent economic value** from not being generally known
2. Be subject to **reasonable measures** to maintain secrecy

### Reasonable Secrecy Measures

| Measure | Implementation |
|---------|----------------|
| **Access controls** | Need-to-know basis, role-based permissions, physical locks |
| **NDAs** | Employee, contractor, and partner non-disclosure agreements |
| **Exit procedures** | Return of materials, reminder of ongoing obligations, access revocation |
| **Labeling** | Clearly mark "CONFIDENTIAL — Trade Secret" on documents |
| **Training** | Annual training on trade secret handling |
| **Segmentation** | Compartmentalize — no one person knows the whole secret |
| **Audit trails** | Log access to trade secret repositories |

### Litigation Risks

- **Inevitable disclosure doctrine** — Former employee's new role inevitably requires disclosing trade secrets (injunction available in some jurisdictions)
- **Reverse engineering** — Legal unless prohibited by contract; cannot protect against it with trade secret law alone

## Open Source Licensing

### License Categories

| Category | Examples | Requirements | Commercial implications |
|----------|----------|-------------|------------------------|
| **Permissive** | MIT, Apache 2.0, BSD | Attribution only | Can use in proprietary products |
| **Weak copyleft** | LGPL, MPL, EPL | Modifications to the library itself must be open-sourced | Can link from proprietary code |
| **Strong copyleft** | GPL 2.0/3.0, AGPL | Derivative works must be open-sourced under same license | Usually incompatible with proprietary products |
| **Network copyleft** | AGPL | Software accessed over a network must be distributed with source | Affects SaaS companies |

### Strategic Decisions

| Decision | Consideration |
|----------|--------------|
| **Why open source?** | Community adoption, talent attraction, commoditize complement, standards setting |
| **License choice** | Permissive for maximum adoption; copyleft to prevent proprietary forks |
| **CLA (Contributor License Agreement)** | Required for corporate projects to relicense later |
| **Dual licensing** | Open source (GPL) + commercial license for proprietary users (Qt, MySQL model) |
| **Trademark policy** | Prevent confusion: who can use the project name/logo |

### Open Source Compliance

| Process | Description |
|---------|-------------|
| **SBOM generation** | Software Bill of Materials — list every dependency and its license |
| **License scanning** | Automated tools (FOSSA, Black Duck, Snyk) to detect license obligations |
| **Policy creation** | Approved licenses list, obligation matrix, approval workflow for exceptions |
| **Distribution compliance** | Include license notices, provide source code on request (GPL) |
| **Audit readiness** | Maintain a compliance artifact: notices file, source code archive, obligation log |

## IP Portfolio Management

### The IP Lifecycle

```
Creation → Protection → Maintenance → Monetization
                                      ↓
                                 Licensing / Sale / Enforcement
```

### IP Budget Allocation

| % of Budget | Category | Activity |
|-------------|----------|----------|
| 40-50% | **Defensive core** | Patent filing for core technology, trademark registration |
| 20-30% | **Offensive/IP landscape** | Competitive blocking, freedom-to-operate analysis |
| 15-20% | **Maintenance** | Renewal fees, trademark renewal, portfolio pruning |
| 10-15% | **Enforcement** | Cease-and-desist, licensing negotiations, litigation |
