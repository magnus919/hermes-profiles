# Release Engineering Reference

> **Domain:** Site Reliability Engineering
> **Purpose:** Comprehensive reference for designing, operating, and improving release pipelines in SRE-managed environments.
> **Audience:** SREs, Platform Engineers, DevOps practitioners, and Release Managers.

---

## Table of Contents

1. [The Self-Service Release Model](#1-the-self-service-release-model)
2. [Hermetic Builds](#2-hermetic-builds)
3. [Push-on-Green Deployment Model](#3-push-on-green-deployment-model)
4. [Release Branch Management and Cherry-Picking](#4-release-branch-management-and-cherry-picking)
5. [Build and Deployment Pipeline Design (CI/CD)](#5-build-and-deployment-pipeline-design-cicd)
6. [Configuration Management Strategies](#6-configuration-management-strategies)
7. [Progressive Delivery](#7-progressive-delivery)
8. [Rollback Strategies](#8-rollback-strategies)
9. [Audit Trails and Change Reporting](#9-audit-trails-and-change-reporting)
10. [Security and Access Control for Releases](#10-security-and-access-control-for-releases)
11. [Release Velocity Metrics](#11-release-velocity-metrics)
12. [SRE and Release Engineering: The Relationship](#12-sre-and-release-engineering-the-relationship)

---

## 1. The Self-Service Release Model

Traditional release engineering placed a central "release team" as a gatekeeper: every deploy required a ticket, a manual approval meeting, and a designated change window. This model does not scale beyond a handful of services.

### Core Principles

- **Developer autonomy.** Teams own their release pipeline end-to-end — they trigger builds, run tests, promote artifacts, and deploy without filing tickets.
- **Platform over process.** The platform encodes safety (gates, rollbacks, approvals) so humans do not need to remember a checklist.
- **Low-friction, high-safety.** Removing manual bottlenecks increases velocity; automated safety nets (canary analysis, metrics verification) reduce risk.

### Implementation Requirements

| Component | Purpose |
|---|---|
| CLI / API surface | Engineers trigger releases via `shipctl release --service payments --version v2.3.1` or a CI chat-ops command |
| Role-based delegation | Any engineer can promote to staging; only on-call or release managers can promote to production |
| Approval workflows | Optional manual approval step (via Slack button, Jira, or web UI) for compliance-sensitive services |
| Self-service dashboard | Real-time view of pipeline status, artifact provenance, and release history per service |
| Documentation | Every team's pipeline must be discoverable and repeatable without tribal knowledge |

> **SRE Rule:** If an engineer needs to ask "how do I release this service?", the self-service model has failed. The answer should be a documented command or CI trigger.

---

## 2. Hermetic Builds

A hermetic build produces a byte-for-byte reproducible artifact whose output depends only on the declared inputs — not on the state of the build machine, the time of day, or network-available packages.

### Why Hermeticity Matters

- **Determinism.** The same commit always produces the same artifact, eliminating "works on my machine" and "build broke because the repo was flaky."
- **Supply-chain integrity.** No surprise dependency pulled from an external registry at build time.
- **Cacheability.** Build outputs can be content-addressed and cached globally.
- **Auditability.** You know exactly what went into an artifact because the build environment is pinned.

### How to Achieve Hermetic Builds

1. **Pin all toolchains.** Use Docker images with pinned OS packages, compiler versions, and language runtimes. Store images in a registry you control.
2. **Vendor or mirror dependencies.** Commit lockfiles (`package-lock.json`, `Cargo.lock`, `go.sum`, `requirements.txt` with hashes). Mirror npm/PyPI/Maven repos behind an internal proxy (e.g., Artifactory, Nexus).
3. **Disable network access during build.** Use Docker's `--network none` or Bazel's sandbox. If a build needs a dependency, it must be declared and pre-fetched.
4. **Use content-addressable storage.** Bazel, Nix, and similar tools compute a hash of every input and store outputs by hash, making rebuilds of unchanged inputs instant.
5. **Pin base images.** Use digest references (`alpine@sha256:abc123...`) instead of tags (`alpine:3.19`), which can change under you.

### Trade-Offs

| Benefit | Cost |
|---|---|
| Reproducible, tamper-evident builds | Longer initial setup; dependency mirroring overhead |
| Global cache hits across teams | Requires investment in build infrastructure (Bazel, Nix, remote executors) |
| Strong supply-chain guarantees | Some language ecosystems (Python, Node) resist full hermeticity without extensive tooling |

---

## 3. Push-on-Green Deployment Model

"Push on green" means that if the automated pipeline gates all pass (unit tests, integration tests, security scans, performance benchmarks), the artifact is automatically promoted to the next environment — including production — with no human intervention required.

### Pipeline Stages

```
Commit -> Build -> Unit Tests -> Container Image -> Integration Tests
    -> Staging Deploy -> Smoke Tests -> Security Scan -> Canary Deploy
    -> Production Deploy -> Metrics Verification -> Done
```

Each stage gates the next. If any stage fails, promotion halts and the team is alerted.

### When Push-on-Green Works

- **Mature test suites** with high coverage and low flakiness.
- **Strong monitoring** that can detect regressions within minutes of deploy.
- **Fast rollbacks** (ideally automated via the pipeline or infrastructure-as-code).
- **Small batch sizes** — frequent, small releases reduce the blast radius of a bad deploy.

### When It Doesn't

- **Regulatory environments** requiring explicit sign-off per release.
- **Immature services** where tests are sparse or flaky.
- **Database migrations** that are incompatible with quick rollbacks (require manual reconciliation).

> **SRE Best Practice:** Start with manual approval gates between stages (staging and production) and remove them one by one as metrics and confidence improve. Push-on-green is a goal, not a starting point.

---

## 4. Release Branch Management and Cherry-Picking

### Branch Strategy Overview

| Model | Description | Use Case |
|---|---|---|
| Trunk-based development | All work lands on `main`. Releases are tags on `main`. | High-velocity teams, push-on-green, microservices |
| Release branches | Stable branches (`release/v2.3.x`) cut from `main` at a release point. Bug fixes cherry-picked from `main`. | Mobile apps, customer-managed software, regulated industries |
| GitFlow | Long-lived `develop` and `release` branches. | Large monoliths with scheduled releases; falling out of favor |

### Release Branch Lifecycle

1. **Branch cut.** At the release candidate point, create `release/v<major>.<minor>.x` from `main`.
2. **Stabilization.** Cherry-pick only critical bug fixes from `main` into the release branch.
3. **Release.** Tag the commit (e.g., `v2.3.0`) and build the artifact from the release branch.
4. **Patch releases.** Cherry-pick hotfixes into the same branch; tag as `v2.3.1`, `v2.3.2`, etc.
5. **End of life.** Archive the branch once all customers have migrated.

### Cherry-Picking Discipline

Cherry-picking is a necessary evil — every cherry-pick represents code that bypassed the integration testing done on `main`.

**Rules:**

- Require a tracking issue (bug ID or Jira ticket) for every cherry-pick.
- Limit cherry-picks to P0/P1 defects, security vulnerabilities, and customer-blocking issues.
- Enforce code review on the cherry-pick commit — same standards as any other change.
- Run the full CI suite on the release branch after each cherry-pick — do not assume the fix is isolated.
- Keep a changelog of cherry-picked commits (SHA + description) attached to the release notes.

**Automation pattern:** A bot monitors labels on GitHub issues; when a PR with label `cherrypick/release-v2.3` merges to `main`, the bot automatically opens a backport PR against the release branch.

---

## 5. Build and Deployment Pipeline Design (CI/CD)

### Pipeline Architecture

A well-designed CI/CD pipeline is composed of loosely coupled stages, each with a clear success/failure signal.

```
                         +-----------+
                         |  Trigger  |
                         +-----+-----+
                               |
                     +---------v---------+
                     |  Source Fetch &    |
                     |  Commit Metadata   |
                     +---------+---------+
                               |
                     +---------v---------+
                     |  Hermetic Build    |
                     |  & Artifact        |
                     |  Publishing        |
                     +---------+---------+
                               |
                     +---------v---------+
                     |  Unit & Static     |
                     |  Analysis Tests    |
                     +---------+---------+
                               |
                     +---------v---------+
                     |  Integration &     |
                     |  E2E Tests         |
                     +---------+---------+
                               |
                     +---------v---------+
                     |  Security &        |
                     |  Compliance Scan   |
                     +---------+---------+
                               |
          +--------------------+--------------------+
          |                                         |
  +-------v-------+                        +--------v-------+
  |  Staging       |                        |  Canary / Prod |
  |  Deploy +      |                        |  Deploy +      |
  |  Smoke Tests   |                        |  Verification  |
  +-------+-------+                        +--------+-------+
          |                                         |
          v                                         v
     Promoted if                             Promoted if
     green                                  green
```

### Key Design Decisions

| Decision | Recommendation |
|---|---|
| Monorepo vs. multi-repo | Monorepo with per-service CI scoping (affected-target detection) |
| CI runners | Ephemeral, containerized, no state between runs |
| Artifact storage | Content-addressable blob store (S3/GCS with immutable buckets) |
| Deployment tool | ArgoCD, Spinnaker, or in-house orchestrator with GitOps |
| Pipeline-as-code | YAML/Starlark pipeline definitions versioned in the source repo |

### Pipeline Observability

Every pipeline should emit structured events (CloudEvents format) covering:

- **Start timestamp** and **end timestamp** per stage.
- **Commit SHA**, **branch**, **author**, **PR number**.
- **Artifact digest** (SHA256 of the built artifact).
- **Stage result** (passed / failed / skipped / aborted).
- **Duration** and **resource utilization** (CPU, memory, network I/O).

This telemetry feeds dashboards, SLA/SLO tracking, and postmortem analysis.

---

## 6. Configuration Management Strategies

Configuration is the most common source of production incidents. How you manage it alongside your code artifacts is a critical design decision.

### Strategy Comparison

| Strategy | Description | Advantages | Disadvantages | Best For |
|---|---|---|---|---|
| **Mainline** | Config lives in the same repo as application code, deployed together as a single artifact | Atomic deploys, simple mental model, easy version correlation | Config change requires full rebuild; config cannot be toggled independently of code | Small services, early-stage products |
| **Bundled packages** | App artifact includes default config; runtime overrides stored separately | Separation of concerns; default config always matches the code version | Complexity of merging defaults + overrides at startup | Services with small per-environment differences |
| **Config-only packages** | Config is packaged as its own versioned artifact, deployed independently of the application binary | Config can be promoted/rolled back without redeploying code | Drift between config and code versions can cause incompatibilities | Large services where config changes are frequent (feature flags, routing rules) |
| **External stores** | Config lives in a centralized service (Consul, etcd, ZooKeeper, cloud parameter store), served at runtime | Real-time changes without any deploy; fine-grained access control; audit logging | Adds latency on startup/refresh; external dependency (must be highly available); can cause cascading failures if the store is misconfigured | Multi-service systems, dynamic routing, global feature flags |

### Recommended Approach

Use a **layered** strategy:

1. **Bundled defaults** inside the artifact (for safe-start without external dependencies).
2. **Environment overrides** in a config-only package or external store (per env: dev, staging, prod).
3. **Runtime overrides** in a feature-flag system (LaunchDarkly, Flagsmith, in-house) for progressive delivery.

---

## 7. Progressive Delivery

Progressive delivery exposes changes to a subset of users or traffic before rolling out to the full population, reducing the blast radius of defects.

### Techniques

| Technique | Mechanism | Detection Time | Risk Profile |
|---|---|---|---|
| **Canary deployments** | Route a small percentage of live traffic (e.g., 2%) to the new version | Seconds to minutes | Low — immediate detection of errors, latency spikes |
| **Traffic shifting** | Controlled percentage-based routing via service mesh (Istio, Linkerd) or load balancer | Minutes | Low — canaries and gradual shift |
| **Feature flags** | Toggle code paths at runtime without redeploying; per-user or per-group targeting | Real-time | Very low — instant kill switch without any deploy |
| **Blue-green deployments** | Maintain two full environments; switch traffic atomically from old (blue) to new (green) | Seconds (switch time) | Medium — full environment cost; rollback is just another switch |
| **A/B testing** | Execute A/B/n traffic split with instrumentation for business-metric comparison | Hours to days | Low — typically used for non-critical features alongside canary |
| **Shadow / mirroring** | Duplicate live traffic to the new version without serving it to users | Minutes to hours | Lowest — no user impact; but no real user feedback either |

### Deployment Safety Patterns

| Safety Pattern | Description | Implementation |
|---|---|---|
| **Metrics gate** | Pipeline pauses after canary deploy and verifies key SLOs (error rate < 0.1%, p99 latency < 500ms, CPU < 80%). | Prometheus + alerting rules evaluated by the pipeline |
| **Auto-abort** | If metrics degrade beyond a threshold, the pipeline aborts and optionally triggers a rollback. | Pipeline controller watches a metrics endpoint; CD tool (Argo Rollouts, Flagger) handles it natively |
| **Bake period** | Minimum observation window (e.g., 10 minutes) before progressing to the next rollout percentage. | Configurable `minBakeSeconds` in the pipeline YAML |
| **Manual pause** | Pipeline pauses at configurable checkpoints for human review. | Approval step in CI/CD tool + Slack/email notification |
| **Kill switch** | A single command or toggle that halts the rollout and returns to the previous stable version. | Feature flag system or CD tool rollback command |
| **Saturation gate** | Check that downstream dependencies (databases, queues, caches) are not saturated before allowing more traffic. | Customized metrics check or HPA feedback |
| **Drift detection** | Verify that the deployed configuration matches the desired state in version control. | GitOps tool (ArgoCD) reconciliation |

---

## 8. Rollback Strategies

Even with perfect progressive delivery, rollbacks are inevitable. A good rollback plan is fast, safe, and auditable.

### Rollback Types

| Type | Mechanism | Speed | Caveats |
|---|---|---|---|
| **Reversion** | Deploy the previous known-good artifact version | Fast (minutes) | Requires artifact immutability; previous version must still be available |
| **Forward fix** | Deploy a new version that fixes the regression (leaves the bad change in place, adds a correction on top) | Moderate (time to fix + pipeline) | Best long-term; does not revert unrelated changes |
| **Git revert + deploy** | `git revert <bad-commit>` and run the full pipeline | Same as forward fix | Can conflict if intervening commits touch the same code |
| **Blue-green flip** | Switch load balancer back to the old (still-running) environment | Seconds | Only works if blue-green is already deployed; doubles infrastructure cost |
| **Feature flag off** | Toggle the offending feature off at runtime | Seconds (or real-time with polling) | Feature must be behind a flag; the code stays deployed but dormant |

### Rollback Best Practices

1. **Test the rollback.** Every release should include a documented, tested rollback procedure. Schedule a "game day" to verify it works.
2. **Handle stateful rollbacks.** Stateless rollbacks (flip load balancer) are easy. Stateful rollbacks (database schema changes, queue migrations) require careful planning — schema changes should be backward-compatible for at least one deploy cycle.
3. **Roll forward as the default.** Reversion should be the exception, not the rule. Forward fixes preserve progress and avoid losing unrelated changes.
4. **Automate the decision.** If the pipeline detects a metrics regression during canary, it should automatically halt and optionally trigger a rollback — do not wait for a human to notice pager alerts.
5. **Audit every rollback.** Log the trigger (why), the action (what), the affected surface (which users/regions), and the outcome (was it successful?). Feed into incident reviews.

---

## 9. Audit Trails and Change Reporting

SRE requires a complete, immutable, and queryable history of every release and configuration change.

### What to Log

| Event | Fields |
|---|---|
| Build created | artifact digest, commit SHA, build trigger (manual / CI), builder identity, timestamp |
| Promotion decision | artifact version, source env, target env, pass/fail status per gate, verifier identity |
| Deployment | artifact version, target environment, rollout strategy (canary % / blue-green), operator identity |
| Rollback | artifact being reverted to, reason (metric regression / manual / auto-abort), operator identity |
| Config change | config version, diff from previous, deployer identity, approval if required |
| Approval gate | approver identity, timestamp, stage being approved, comments or evidence |

### Storage and Query

- **Immutable log store.** Append-only storage (cloud audit logs, immutable S3/GCS buckets, blockchain-based notary).
- **Searchable.** Index by service name, environment, artifact version, and operator identity.
- **Linkable to incidents.** Every production incident should be cross-referenced with the release that introduced it (via the deploy log SHA).
- **Retention.** Minimum 1 year for operational logs; 3–7 years for compliance-regulated environments.

### Reporting Cadence

| Report | Frequency | Audience |
|---|---|---|
| Release dashboard | Real-time | Engineering teams |
| Weekly release summary | Weekly | Engineering management |
| Deploy failure analysis | Per-incident | SRE + affected team |
| Compliance change report | Per release cycle or monthly | Audit / Compliance |
| Velocity and stability trends | Monthly | Platform / Eng leadership |

---

## 10. Security and Access Control for Releases

### Principles

- **Least privilege.** An engineer who can initiate a release should not necessarily be able to approve it or bypass gates.
- **Separation of duties.** Build, promote, and deploy stages should have distinct authorization.
- **Non-repudiation.** Every action is attributable to a specific identity (human or service account).
- **Artifact signing.** Every build artifact is cryptographically signed. The deployment pipeline verifies the signature before deploying.

### Access Control Model

| Role | Can Trigger Build | Can Promote to Staging | Can Promote to Prod | Can Approve Hotfix | Can Modify Pipeline Config |
|---|---|---|---|---|---|
| Developer | Yes | Yes (via CI) | No | No | No |
| Senior Engineer | Yes | Yes | Yes (with auto-gates) | Yes | No |
| SRE On-Call | Yes | Yes | Yes | Yes | Yes (with review) |
| Release Manager | Yes | Yes | Yes (override gates) | Yes | Yes |
| CI/CD Service Acct | Yes (on push) | Yes (on green) | Yes (on green) | No | No |

### Secret Management

- Never bake secrets into artifacts. Use a secrets manager (Vault, AWS Secrets Manager, GCP Secret Manager) injected at deploy time.
- Pipeline credentials should be short-lived (15-minute expiry) and scoped to the minimum required action.
- Audit all secret access — who read which secret, when, and from what context.

### Supply-Chain Security

- **SLSA framework.** Target SLSA Level 3+ for critical production services: signed builds, hardened build platform, provenance attestation.
- **Software Bill of Materials (SBOM).** Generate an SBOM per build (CycloneDX or SPDX format). Store alongside the artifact.
- **Vulnerability scanning.** Scan all base images and dependencies at build time. Fail the pipeline on CVSS >= 7.0 findings.
- **Image signing.** Use cosign (Sigstore) or similar to sign container images. Enforce signature verification in the deploy admission webhook.

---

## 11. Release Velocity Metrics

You cannot improve what you do not measure. These are the canonical metrics for release engineering.

### Core Metrics

| Metric | Definition | Target | Formula |
|---|---|---|---|
| **Deploy Frequency** | How often a service is deployed to production | High-velocity: multiple times per day; Medium: weekly; Low: monthly | # of production deploys / time period |
| **Lead Time for Changes** | Time from commit to production deploy | Elite: < 1 hour; High: < 1 day; Medium: < 1 week | median(time(deploy) - time(commit)) |
| **Change Failure Rate (CFR)** | Percentage of deploys that cause a degradation or incident | Elite: < 5%; High: < 10%; Medium: < 15% | # of failed deploys / total deploys |
| **Mean Time to Recovery (MTTR)** | Time from incident detection to full remediation (including rollback) | Elite: < 1 hour; High: < 1 day; Medium: < 1 week | median(time(resolved) - time(alerted)) |
| **Pipeline Success Rate** | Percentage of pipeline runs that complete all stages successfully | Target: > 95% | successful runs / total runs |
| **Artifact Age** | Time since the artifact in production was built | Target: < 24 hours | now - build_timestamp |
| **Gate Pass Rate** | Percentage of promotion attempts that pass automated gates | Baseline: > 90% | passed promotions / total promotions |

### Leading Indicators

These metrics predict future reliability problems:

- **Flaky test rate** — if > 5% of test reruns succeed, confidence in the gate is eroded.
- **Gate bypass requests** — if teams regularly bypass gates (e.g., hotfix override), the pipeline is too restrictive or the tests are too slow.
- **Cherry-pick density** — the ratio of cherry-picked commits to normal commits on a release branch. Rising density indicates poor mainline discipline.
- **Pipeline queue time** — if builds wait for CI runners for more than a few minutes, velocity will plateau.

---

## 12. SRE and Release Engineering: The Relationship

Release engineering and SRE share overlapping but distinct responsibilities.

### Common Misconceptions

- **"Release engineering is just CI/CD."** It is CI/CD plus artifact management, configuration strategy, progressive delivery, security, compliance, and the organizational model that enables self-service.
- **"SREs are release engineers."** SREs define the reliability requirements (SLOs, error budgets) that the release pipeline must enforce. They do not necessarily own the pipeline infrastructure itself, though in practice many SRE teams operate the deployment platform.

### Responsibility Matrix

| Activity | Release Engineering | SRE | Development Team |
|---|---|---|---|
| Pipeline design and maintenance | Lead | Consult | Feed requirements |
| Artifact signing and provenance | Lead | Review | N/A |
| Deployment tooling (CD platform) | Lead | Co-own reliability | Use |
| Rollback automation | Lead | Define recovery SLOs | Test |
| Canary analysis and metrics gates | Consult | Lead (define thresholds) | Review |
| Incident response for bad deploys | Support | Lead | Support |
| Release velocity metrics | Lead | Consume for error budget | Use |
| Security scanning and SBOM | Lead | Review compliance | Fix findings |
| Configuration management strategy | Lead | Review (reliability impact) | Implement |
| Release approval / change management | Facilitate | Gate for SLO risk | Request |

### How They Work Together

1. **Error budgets inform release velocity.** If a team has error budget remaining, they can release freely (push on green). If they have exhausted their error budget, the pipeline can enforce a cool-down period (gating further releases until reliability improves).
2. **Release pipelines enforce SLOs.** The metrics gate in the pipeline (Section 7) validates that the new version meets the service's SLOs before more traffic is shifted.
3. **SREs set the "pain threshold."** Release engineering implements the technical mechanism; SRE defines what "bad enough to abort" means (e.g., 0.1% error rate increase, p99 latency over 800ms).
4. **Postmortems drive pipeline improvements.** Every deploy-related incident feeds back into the release pipeline: add a new gate, harden an existing check, improve the rollback script.

### Organizational Models

| Model | Description | Best For |
|---|---|---|
| **Embedded** | Release engineers sit within the SRE org; dedicated platform team | Large organizations (> 200 engineers), multiple service teams |
| **SRE-as-platform** | SRE builds and maintains the release platform; teams self-serve | Mid-sized orgs (50–200 engineers) |
| **Federated** | Each team owns its release pipeline; SRE provides standards and consulting | Small orgs (< 50 engineers), strong DevOps culture |

---

## References and Further Reading

- *Accelerate: The Science of Lean Software and DevOps* by Nicole Forsgren, Jez Humble, Gene Kim
- *Site Reliability Engineering* (Beyer et al., O'Reilly) — Chapters on release engineering
- *The DevOps Handbook* by Gene Kim, Jez Humble, Patrick Debois, John Willis
- *Continuous Delivery* by Jez Humble and David Farley
- SLSA (Supply-chain Levels for Software Artifacts) — [slsa.dev](https://slsa.dev)
- Google CI/CD best-practices documentation
- Argo Rollouts — Progressive delivery for Kubernetes
- Flagger — Canary deployments with service mesh integration
- Sigstore / cosign — Container image signing
- OpenFeature — Standardized feature flagging

---

> **Revision 1.0** — Created for the Site Reliability Engineering skill profile. Maintained by the SRE Knowledge Base working group.
