# Engineering Metrics

Frameworks for measuring engineering effectiveness, developer productivity, and delivery health. The goal is insight, not judgment — metrics should inform improvement, not evaluate individuals.

## DORA Metrics

DORA (DevOps Research and Assessment) defines four key metrics that predict organizational performance. They are the most widely adopted benchmark for software delivery capability.

### The Four Metrics

| Metric | Definition | Elite | High | Medium | Low |
|--------|-----------|-------|------|--------|-----|
| **Deployment Frequency** | How often code is deployed to production | On demand (multiple/day) | Between once/day and once/week | Between once/week and once/month | Between once/month and once/6 months |
| **Lead Time for Changes** | Time from commit to production | < 1 hour | < 1 day | < 1 week | > 6 months |
| **Mean Time to Recover (MTTR)** | Time to restore service after incident | < 1 hour | < 1 day | < 1 day | > 1 week |
| **Change Failure Rate** | % of deployments causing a failure | 0-5% | 5-10% | 10-15% | 15%+ |

### Benchmarking

Use these benchmarks to understand where your organization falls, but don't chase elite performance if your context doesn't require it.

| Industry | Typical Performance |
|----------|-------------------|
| SaaS (consumer) | High to Elite |
| SaaS (enterprise) | Medium to High |
| Fintech/Healthcare | Low to Medium (regulatory constraints) |
| Hardware/Firmware | Low to Medium |
| Internal tools | Varies widely |

### Improving DORA Metrics

| Metric | Lever | Intervention |
|--------|-------|-------------|
| Deployment frequency | Trunk-based development, CI/CD automation | Adopt feature flags, automate testing, reduce batch size |
| Lead time | Review speed, CI pipeline, deploy automation | Small PRs, auto-merge on passing CI, deploy previews |
| MTTR | Observability, incident response, rollback capability | Monitoring investment, incident playbooks, canary deployments |
| Change failure rate | Testing, code review, gradual rollout | Automated testing pyramid, load testing, feature flags |

### DORA Pitfalls

- **Measuring without context.** A low change failure rate might mean "good engineering" or "never deploying." Always interpret metrics together.
- **Comparing teams directly.** Teams doing different work will have different DORA profiles. Compare a team to its own trend, not to other teams.
- **Chasing elite on all four.** Some contexts (regulatory, safety-critical) cannot achieve elite change failure rate or lead time. Optimize for your constraints.

---

## SPACE Framework

DORA measures delivery. SPACE measures the human side of productivity — developer satisfaction and the quality of their work experience.

### The Dimensions

| Dimension | What It Measures | Sample Metrics |
|-----------|-----------------|----------------|
| **S**atisfaction & Well-being | How developers feel about their work, tools, and environment | eNPS, burnout survey, tool satisfaction score |
| **P**erformance | Outcomes and value delivered | Deploy frequency, feature adoption, MTTR |
| **A**ctivity | Quantity of output (use with caution) | PRs created, code reviews completed, commits |
| **C**ommunication & Collaboration | How effectively developers work together | Review cycle time, cross-team PRs, docs contributions |
| **E**fficiency & Flow | How easily developers can stay in flow state | Time in IDE, context switches, wait time for reviews |

### Using SPACE

- **Don't track all five equally.** Pick 2-3 dimensions that matter for your current challenges. If burnout is the issue, focus on Satisfaction. If bottlenecks are the issue, focus on Flow.
- **Pair SPACE with DORA.** DORA measures the system. SPACE measures the people. Both are needed for a complete picture.
- **Survey quarterly, not weekly.** Satisfaction and well-being don't change fast enough for frequent measurement. Quarterly surveys + monthly pulse checks.
- **Avoid activity myopia.** "PRs per developer" alone drives bad behavior (tiny PRs). Always pair activity metrics with outcome metrics.

### Common SPACE Anti-Patterns

- **Treating satisfaction as a metric.** It's a dimension. The metric within it should be specific (e.g., "I have adequate time for focused work" scored 1-5).
- **Survey fatigue.** If you survey developers about satisfaction too often, they stop giving honest answers.
- **Ignoring the results.** Asking developers about their experience and then doing nothing is worse than not asking at all. Close the feedback loop publicly.

---

## DevEx (Developer Experience)

Developer Experience focuses on the friction developers encounter in their daily work. Reducing friction is a force multiplier — minutes saved per developer translate to significant organizational throughput.

### The DevEx Framework

| Layer | What It Covers | Friction Signals |
|-------|---------------|-----------------|
| **Local Development** | IDE, dev environment, local testing | Long build times, complex setup, "it works on my machine" |
| **Inner Loop** | Code, build, test, debug cycle | Slow feedback, flaky tests, context switching |
| **Outer Loop** | CI/CD, review, deploy, monitor | Long CI, slow reviews, complex deployment |
| **Cognitive Load** | How much a developer needs to know | Complexity of architecture, number of tools, documentation quality |

### Measuring DevEx

| Method | What It Captures | Frequency |
|--------|-----------------|-----------|
| **Developer survey (Dx or SPACE)** | Subjective experience, satisfaction | Quarterly |
| **Time-to-first-commit** | Onboarding friction | Tracked per new hire |
| **IDE time in flow** | Focused work time | Weekly (via tool telemetry) |
| **Build/CI wait times** | Infrastructure bottlenecks | Weekly |
| **Context switch count** | Fragmentation of work | Monthly via calendar analysis |

### DevEx Improvement Levers

| Lever | Impact | Effort |
|-------|--------|--------|
| Standardized development environment (DevContainer, Nix) | High | Medium |
| Local development with production-like data | High | Medium-High |
| CI/CD pipeline optimization | Medium-High | Medium |
| Documentation-as-code for architecture decisions | Medium | Low |
| Automated dev environment setup (single command) | High | Medium |
| Flaky test remediation | High | Medium |

### DevEx Pitfalls

- **Building internal tools that don't solve real friction.** Survey developers about their top 3 pains before building anything.
- **Measuring the wrong thing.** Time in IDE could mean "in flow" or "stuck and trying to figure things out." Combine tool data with qualitative feedback.
- **One-size-fits-all solutions.** Different teams have different friction points. Let teams opt into platform improvements rather than mandating them.
- **Ignoring cognitive load.** The most expensive friction is mental — having to keep too many details in your head to be productive. Invest in abstractions and documentation.
