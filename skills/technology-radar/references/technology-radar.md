# Technology Radar

The technology radar is a structured approach to tracking, evaluating, and deciding on technologies. It categorizes technologies into four quadrants and two rings.

## The Radar Framework

### Quadrants (Technology Categories)

| Quadrant | What It Covers | Example |
|----------|---------------|---------|
| **Languages & Frameworks** | Programming languages, web frameworks, application frameworks | Python, React, Django, Go |
| **Platforms & Infrastructure** | Cloud providers, container orchestration, databases, message queues | Kubernetes, AWS, Postgres, Kafka |
| **Tools & Techniques** | CI/CD, monitoring, testing, security scanning, project management | GitHub Actions, Prometheus, Terraform |
| **Patterns & Practices** | Architectural patterns, development methodologies, operational practices | Microservices, event sourcing, GitOps |

### Rings (Maturity Levels)

| Ring | Meaning | Policy |
|------|---------|--------|
| **Adopt** | Proven in production, recommended for all relevant new projects | Actively promoted, documented standards exist |
| **Trial** | Worth pursuing, low-risk to experiment | Sandboxed POC allowed, must revisit decision within 6 months |
| **Assess** | Worth investigating, but not ready for commitment | Research and small experiments only, no production use |
| **Hold** | Not recommended for new projects, plan migration away | No new usage, existing usage must have migration plan |

### Transition Rules

| Transition | When | Process |
|------------|------|---------|
| Assess → Trial | Team assessed, sees potential, has a POC plan | Brief written recommendation, tech lead approval |
| Trial → Adopt | Successful in 2+ projects with documented results | Full review, standardization of patterns, documentation |
| Adopt → Hold | Newer better alternative, maintenance burden, strategic shift | Migration plan for existing systems, deprecation notice |
| Hold → (Retire) | No remaining users, migration complete | Archive docs, remove from supported list |
| Trial → Hold | Experiment failed the thesis | Document learnings, archive. Not a failure — it's data. |

### Radar Review Cadence

- **Full radar refresh:** Quarterly (review all quadrants and rings)
- **New technology intake:** Continuous (proposed via RFC or lightweight form)
- **Emergency promotion:** As needed (critical security update, strategic shift)
- **Hold review:** Annual (verify hold decisions are still valid)

---

## Tool Selection Criteria

When evaluating whether to Adopt, Trial, or Hold a technology, use this criteria framework.

### Evaluation Dimensions

| Dimension | Weight | Scoring (1-5) | Notes |
|-----------|--------|---------------|-------|
| **Fit for purpose** | 30% | Does it solve the actual problem? | Beware over-engineering. "Does it work?" is the first question. |
| **Community & ecosystem** | 20% | Active development, documentation, community support | GitHub stars, contributor count, release cadence, Stack Overflow activity |
| **Operational maturity** | 20% | Production readiness, monitoring, upgrade stability | Does the community have a track record of stable releases? |
| **Talent availability** | 15% | Can we hire/develop people who know this? | Market availability, learning curve, internal expertise |
| **Integration complexity** | 15% | How hard is it to integrate with our existing stack? | Migration cost, interoperability, dependency conflicts |

### Scoring Guide

| Score | Meaning |
|-------|---------|
| 5 | Excellent — best in class for our context |
| 4 | Good — strong fit with minor concerns |
| 3 | Adequate — works but not differentiated |
| 2 | Poor — significant concerns |
| 1 | Unacceptable — does not meet requirements |

### Red Flags (Automatic Hold)

Any of these flags should move a technology to Hold regardless of other scores:

- **Single point of failure.** Core dependency managed by a single person or company without redundancy.
- **No clear governance.** Unclear licensing, governance model, or contribution process.
- **Security concerns.** Known unpatched vulnerabilities, history of supply-chain attacks.
- **EOL or deprecated.** No active development, community migration away.
- **License incompatibility.** License conflicts with company policy or distribution model.

---

## Deprecation Policy

Removing technology is harder than adding it. A clear deprecation policy prevents the accumulation of zombie technologies.

### Deprecation Process

1. **Announce intent.** "We plan to deprecate Technology X. Here's why, and here's the migration path."
2. **Freeze new usage.** No new projects may adopt the deprecated technology.
3. **Provide migration window.** 3-12 months depending on complexity.
4. **Support during migration.** Documentation, office hours, migration tools.
5. **Sunset date.** After this date, no support, no security patches, no guarantees.
6. **Archive.** Final documentation archived. Technology removed from radar.

### Deprecation by Volume

| Scenario | Migration Window | Support Level |
|----------|-----------------|---------------|
| <5 consumers | 3 months | Documentation only |
| 5-20 consumers | 6 months | Dedicated migration guide + office hours |
| 20-100 consumers | 9-12 months | Migration tools, paired support, extended support |
| 100+ consumers | 12+ months | Automated migration, phased approach, extended support |

### Pitfalls

- **Deprecation without migration path.** You cannot remove a technology without showing people what to replace it with. "Don't use X anymore" without "use Y instead" creates chaos.
- **Too many holds without removal.** If technologies sit on Hold indefinitely, the Hold ring loses meaning. Set sunset dates for every Hold decision.
- **Ignoring the migration cost.** For deeply embedded technologies (e.g., a database, a framework), the migration cost may exceed the benefit of deprecation. Be honest about the economics.
