# Senior / Staff / Principal SRE — Role Blueprint

> **Audience:** SRE profile agent, engineering leadership, aspirants  
> **Last updated:** 2025-06-05  
> **Version:** 1.0

---

## Table of Contents

1. [Role Mission Statement](#1-role-mission-statement)
2. [Core Responsibilities by Category](#2-core-responsibilities-by-category)
3. [Key Performance Indicators](#3-key-performance-indicators)
4. [Required Technical Skills](#4-required-technical-skills)
5. [Soft Skills & Leadership Competencies](#5-soft-skills--leadership-competencies)
6. [Tools & Tech Stack](#6-tools--tech-stack)
7. [Career Progression](#7-career-progression)
8. [Senior vs. Mid-Level: The Distinction](#8-senior-vs-mid-level-the-distinction)

---

## 1. Role Mission Statement

> **"Maximize service reliability while enabling engineering velocity. Design, build, and operate distributed systems at scale — then teach others to do the same."**

The Senior/Staff/Principal SRE is the organizational authority on production excellence. This is not an operations escalation role. It is an **engineering leadership** role that blends deep systems knowledge, software engineering skill, and cross-functional influence to ensure the services customers depend on remain available, performant, and evolvable.

At each tier the scope expands:

| Level | Scope | Primary Lever |
|-------|-------|---------------|
| **Senior SRE** | A service family or platform area | Technical execution, incident command, runbook authorship |
| **Staff SRE** | Multiple teams across an organization | Reliability standards, architectural decisions, org-wide initiatives |
| **Principal SRE** | The entire engineering organization | Strategy, multi-year roadmap, industry influence |
| **SRE Manager** (parallel track) | A team of SREs | People development, hiring, org design, stakeholder management |

The common thread: **every SRE at this level ships code**, writes design docs, and carries a pager. The higher you go, the more of your leverage comes from *enabling others* rather than *doing it yourself*.

---

## 2. Core Responsibilities by Category

### 2.1 Strategic

| Responsibility | Description | Senior | Staff | Principal |
|---------------|-------------|--------|-------|-----------|
| **SLO / SLI Definition** | Work with product and engineering to define meaningful service-level objectives and indicators | Leads for own service | Defines framework org-wide | Sets org-wide methodology |
| **Error Budget Policy** | Design and enforce error budget policies that balance reliability vs. feature velocity | Applies policy | Designs policy | Audits and evolves policy |
| **Capacity Planning** | Forecast infrastructure needs 6–18 months out based on growth trends and product roadmap | Quarterly per service | Annual org-level | Multi-year / cross-org |
| **Reliability Roadmap** | Identify and prioritize reliability investments — observability gaps, architectural debt, toil | Quarter-ahead | Year-ahead | Multi-year strategy |
| **Cost Optimization** | Drive infrastructure efficiency without compromising SLOs | Per-team savings | Org-wide cost + performance | Unit-economics design |

### 2.2 Operational

| Responsibility | Description | Senior | Staff | Principal |
|---------------|-------------|--------|-------|-----------|
| **Incident Response** | Lead high-severity incidents, perform postmortems, track action items | Incident commander | Coach incident commanders | Design incident-response program |
| **On-Call Rotation** | Participate in rotations, improve runbooks, reduce alert fatigue | Active participant | Improve rotation design | Eliminate entire classes of pages |
| **Change Management** | Review and approve production changes, enforce safe deployment practices | Reviews changes | Defines change policy | Audits change outcomes |
| **Toil Reduction** | Identify and automate repetitive operational work | 50% toil reduction/quarter | Defines toil metrics org-wide | Eliminates structural toil sources |
| **Disaster Recovery** | Design, document, and regularly test DR plans and failover procedures | Owns per-service DR | Cross-service DR exercises | Multi-region / multi-cloud DR strategy |

### 2.3 Technical

| Responsibility | Description | Senior | Staff | Principal |
|---------------|-------------|--------|-------|-----------|
| **Architecture Review** | Review system designs for reliability, scalability, operability | Per-service | Cross-team | Org-wide standards |
| **Observability Pipelines** | Design metrics, logs, and traces infrastructure; build dashboards and alerts | Owns service observability | Designs platform approach | Defines telemetry strategy |
| **Automation & Tooling** | Build tools for deployment, configuration, self-healing, and incident remediation | Service-level tooling | Platform-level tooling | Open-source / industry-level tooling |
| **Performance Engineering** | Profile and optimize latency, throughput, and resource utilization | Application-level | System-level | Cross-system architecture |
| **Security & Compliance** | Implement security controls, access policies, and audit compliance in infrastructure | Applies controls | Defines controls for org | Partners with security on strategy |

### 2.4 Cross-Functional

| Responsibility | Description | Senior | Staff | Principal |
|---------------|-------------|--------|-------|-----------|
| **Onboarding & Training** | Ramp new SREs; teach reliability fundamentals to adjacent teams | Mentors 1–2 juniors | Runs internal training program | Builds reliability curriculum |
| **Embedded SRE / Consulting** | Work inside product teams as a reliability subject-matter expert | Embedded in one team | Rotates across teams | Consults org-wide |
| **Interviewing & Hiring** | Participate in the SRE hiring pipeline | Conducts interviews | Designs interview loops | Defines hiring bar |
| **Postmortem Culture** | Lead blameless postmortems and drive systemic improvements | Facilitates own | Improves postmortem process | Defines org culture |
| **Stakeholder Communication** | Translate reliability metrics into business impact for non-technical audiences | Per-incident | Quarterly reviews | Board-level reporting |

---

## 3. Key Performance Indicators

The following KPIs define what "good" looks like at the senior+ SRE level. Every metric should be tracked, trended, and reviewed quarterly.

### 3.1 Reliability & Availability

| KPI | Definition | Target | Why It Matters |
|-----|-----------|--------|----------------|
| **SLO Attainment** | % of rolling 28-day windows where the service meets its SLO | ≥ 99.9% (tier-1) | Direct customer experience measure |
| **Error Budget Burn Rate** | Rate at which error budget is consumed per week | < 1/3 of budget/week | Burn rate too fast → no room for deploys |
| **Compound SLO** | Multi-service SLO accounting for dependency chains | ≥ 99.5% (tier-1) | Real user experience across call chain |
| **Availability** | % of time service is fully functional (uptime) | ≥ 99.99% (tier-1) | Traditional availability metric |

### 3.2 Incident Response

| KPI | Definition | Target | Why It Matters |
|-----|-----------|--------|----------------|
| **MTTD** (Mean Time to Detect) | Time from fault introduction to detection | < 5 minutes (P0) | Shorter = less user impact |
| **MTTR** (Mean Time to Resolve) | Time from detection to mitigation | < 15 minutes (P0) | Shorter = faster recovery |
| **MTTR × Severity** | Weighted MTTR by incident severity | < 30 min weighted avg | Reflects actual user outage time |
| **Incident Frequency** | Number of P0/P1 incidents per month | Trending down | Indicates systemic improvement |
| **Change Failure Rate** | % of changes causing a degradation or incident | < 5% | DORA metric; high failure = process problem |

### 3.3 Operational Health

| KPI | Definition | Target | Why It Matters |
|-----|-----------|--------|----------------|
| **Alert Quality** | % of alerts that trigger a meaningful human response (precision) | ≥ 90% | High noise = burnout and missed real issues |
| **Alerts per Shift** | Number of pages per on-call shift | < 5 per week | DORA: < 2 ideal, < 5 acceptable |
| **Mean Alert Acknowledgment Time** | Time between page and acknowledge | < 2 minutes | Indicates alert noise and on-call readiness |
| **Toil %** | % of time spent on manually repeatable, automatable work | < 25% | > 50% is burnout territory |
| **Runbook Coverage** | % of known failure modes with validated runbooks | ≥ 95% | Reduces MTTR and cognitive load |

### 3.4 Postmortem & Learning

| KPI | Definition | Target | Why It Matters |
|-----|-----------|--------|----------------|
| **Postmortem Closure Rate** | % of postmortem action items closed within 30 days | ≥ 90% | Shows org commitment to learning |
| **Postmortem Completeness** | % of qualifying incidents with a published postmortem | 100% | Every incident is a learning opportunity |
| **Action Item Recurrence** | % of incidents caused by a previously identified root cause | < 5% | Indicates action items were meaningful |
| **Time to Postmortem** | Time from incident resolution to published postmortem | < 5 business days | Freshness matters for accuracy |

### 3.5 Engineering & Automation

| KPI | Definition | Target | Why It Matters |
|-----|-----------|--------|----------------|
| **Deployment Frequency** | Number of production deployments per week | ≥ 1/day (tier-1) | DORA high-performer metric |
| **Deployment Lead Time** | Time from commit to production | < 1 hour | DORA high-performer metric |
| **Automation Coverage** | % of repetitive operational tasks automated | ≥ 80% | Direct toil reduction measure |
| **Capacity Margin** | Headroom in critical infrastructure (CPU, memory, storage) | ≥ 30% | Prevents capacity-driven outages |

---

## 4. Required Technical Skills

### 4.1 Skills Matrix

| Skill Domain | Senior | Staff | Principal | Assessment Criteria |
|-------------|--------|-------|-----------|-------------------|
| **Linux / Systems** | Expert-level kernel tuning, namespaces, cgroups, systemd | Designs OS-level reliability patterns | Defines host-hardening and performance baselines org-wide | Can debug a kernel oops, tune sysctls, reason about page cache vs. OOM |
| **Cloud Infrastructure** | Deep expertise in 1–2 cloud providers (AWS/GCP/Azure) | Multi-cloud architecture, cost analysis, org-wide best practices | Defines cloud strategy, negotiates commitments, designs multi-region topology | Can design a multi-region active-active topology and cost-model it |
| **Observability** | Builds dashboards, writes PromQL, configures alert rules | Designs unified telemetry pipeline (metrics + logs + traces) | Defines observability strategy, selects vendors, sets standards | Can trace a P0 from dashboard to root cause < 10 min |
| **Incident Response** | Incident commander certified, runs postmortems | Designs incident-response playbooks and training | Designs org-wide incident command structure and major-incident program | Has commanded 10+ real P0 incidents |
| **Infrastructure as Code** | Terraform/Pulumi/CDK expert, module author | Designs IaC patterns and module registries | Defines IaC strategy, security policy as code, compliance automation | Can review a 1000+ line Terraform plan and spot the risk |
| **Kubernetes / Containers** | Cluster operations, custom controllers, Helm chart author | Platform design, multi-cluster federation, CNCF ecosystem selection | Defines container strategy, custom scheduler extensions or platform abstraction | Can debug a CrashLoopBackOff, tune HPA, explain pod lifecycle |
| **Programming (Python)** | Production-quality Python: async, testing, profiling | Writes tooling and libraries consumed by multiple teams | Authors and maintains critical automation frameworks | Can write a gRPC service, async worker, pytest suite, and CLI tool |
| **Programming (Go)** | Production-quality Go: concurrency, interfaces, profiling | Builds operators, controllers, sidecars, or service mesh components | Contributes to or leads open-source projects in the CNCF ecosystem | Can write a Kubernetes operator or custom Prometheus exporter |
| **Shell (Bash)** | Advanced scripting, awk/sed/jq mastery, pipeline composition | Writes robust, testable shell libraries | Defines shell scripting standards and patterns | Can write a safe, idempotent bootstrap script for a bare-metal host |
| **CI/CD** | Pipeline author (GitHub Actions, GitLab CI, ArgoCD) | Designs deployment strategies (blue/green, canary, feature flags) | Defines release engineering strategy and SLSA compliance | Can design a progressive delivery rollout with canary analysis |
| **Networking** | TCP/IP, DNS, HTTP, TLS, load balancers, service mesh | Designs network policies, mTLS mesh, multi-cluster networking | Defines network architecture and zero-trust networking strategy | Can diagnose a TCP retransmission storm or TLS handshake failure |
| **Databases** | Query optimization, replication, failover, backups | Designs data-layer reliability patterns (active/active, CQRS) | Defines data resiliency and consistency strategy | Can manually failover a PostgreSQL cluster and validate consistency |

### 4.2 Technology Depth Expectations

**Senior SRE** must be able to:
- Write a production-grade Kubernetes operator from scratch in Go
- Design and implement a complete observability stack (Prometheus + Loki/Tempo/Grafana or equivalent)
- Automate a multi-step incident runbook end-to-end with zero manual steps
- Debug a complex distributed-system failure across multiple services, data stores, and network hops
- Author and review architecture documents for reliability, scalability, and operability

**Staff SRE** additionally:
- Design a multi-cluster, multi-region Kubernetes platform serving 100+ microservices
- Lead the technical design and execution of a quarter-to-year-long reliability initiative
- Define org-wide coding standards, deployment practices, and reliability expectations
- Evaluate and select technologies (databases, observability tools, CI/CD platforms) at org scale

**Principal SRE** additionally:
- Define the technical reliability strategy for the entire engineering organization
- Influence industry standards through open-source contributions, conference talks, or publications
- Make build-vs-buy decisions that affect multi-million dollar infrastructure budgets
- Act as the final escalation for the hardest distributed-systems problems in the organization

---

## 5. Soft Skills & Leadership Competencies

### 5.1 Incident Leadership

- **Command presence**: Remain calm and directive during high-stress outages. Know when to delegate, when to escalate, and when to say "I don't know yet."
- **Communication discipline**: During incidents, communicate to stakeholders in structured updates (situation → impact → action → ETA). No speculation. No silence.
- **Systems triage**: Quickly identify the failure domain — network, storage, application, configuration, capacity — and route to the right expertise.

### 5.2 Influence Without Authority

- **Cross-team negotiation**: Convince product teams to invest in reliability work without a reporting-line mandate. Frame reliability investments in terms of user impact and business value.
- **Technical persuasion**: Write RFCs and design docs that survive rigorous review. Use data, not opinion. If you can't measure it, you can't argue for it.
- **Bias for written communication**: Async documentation scales better than meetings. Write clearly, concisely, and inclusively.

> **"The Senior SRE's most powerful tool is a well-written design document."**

### 5.3 Customer-Impact Orientation

- Translate every technical metric (p99 latency, error rate, saturation) into user-facing impact ("users in region X experience 3-second page loads").
- Prioritize reliability work based on the number of users affected and the severity of the impact, not technical interest.

### 5.4 Coaching & Mentorship

- **One-on-one coaching**: Regularly invest in the growth of junior and mid-level SREs. Teach debugging methodology, system design thinking, and operational judgment.
- **Code and design review**: Review with the intent to teach, not just to gatekeep. Leave comments that explain *why* something is a concern, not just *what* to change.
- **Shadow programs**: Run incident-shadow programs where junior engineers observe and gradually take on incident-command responsibilities.

### 5.5 Strategic Communication

| Audience | Message | Frequency | Format |
|----------|---------|-----------|--------|
| **Engineering team** | Reliability metrics, incident learnings, upcoming work | Weekly | Standup, Slack, dashboard |
| **Product / PM** | Error budget status, feature-velocity tradeoffs, reliability roadblocks | Bi-weekly | 1:1, shared dashboard |
| **Engineering leadership** | Reliability trends, major incidents, org-wide risks, investment needs | Monthly | Written report + walkthrough |
| **Executive / Board** | Business-level reliability posture, SLO compliance, top risks | Quarterly | Executive summary (1-pager) |

---

## 6. Tools & Tech Stack

### 6.1 Tooling Reference Table

| Category | Tools | Senior SRE Level | Staff+ SRE Level |
|----------|-------|------------------|------------------|
| **Container Orchestration** | Kubernetes (EKS/AKS/GKE), OpenShift, Nomad | Operators, Helm charts, cluster scaling | Multi-cluster federation, platform abstraction, CNI/service-mesh design |
| **Infrastructure as Code** | Terraform, Pulumi, AWS CDK, Crossplane, Ansible | Module author, backend state management, review | Pattern design, compliance-as-code, platform abstraction layers |
| **CI / CD** | GitHub Actions, GitLab CI, ArgoCD, Spinnaker, Jenkins X | Pipeline author, canary deployment configuration | Deployment strategy design, progressive delivery framework |
| **Observability — Metrics** | Prometheus, Thanos, VictoriaMetrics, M3DB, Grafana | PromQL, recording rules, dashboard design, alert thresholds | Unified metric strategy, long-term storage, cardinality management |
| **Observability — Logs** | Loki, Elasticsearch/OpenSearch, Datadog Logs, Splunk | Log parsing, structured logging, log-based alerting | Log pipeline design, cost optimization, sampling strategy |
| **Observability — Tracing** | Tempo, Jaeger, Honeycomb, Datadog APM | Trace analysis, span instrumentation | Distributed tracing strategy, tail-based sampling, root-cause automation |
| **Service Mesh** | Istio, Linkerd, Consul Connect, Cilium | mTLS, traffic shifting, circuit breaking | Mesh architecture for multi-cluster, zero-trust, observability injection |
| **Secrets Management** | Vault, AWS Secrets Manager, SOPS, External Secrets | Secret rotation, policy authoring | Secrets strategy, PKI management, identity-based access |
| **Configuration** | Helm, Kustomize, jsonnet, CUE, KCL | Chart author, environment overlays | Configuration-as-data patterns, policy enforcement |
| **Database / Storage** | PostgreSQL, MySQL, Cassandra, Redis, S3, Vitess, CockroachDB | Query optimization, backup/restore, replication config | Data-layer HA pattern design, DR strategy, consistency modeling |
| **Messaging / Streaming** | Kafka, RabbitMQ, NATS, Pulsar | Topic design, consumer group management, monitoring | Streaming platform architecture, data-loss prevention, schema registry |
| **CD / GitOps** | ArgoCD, Flux, Fleet | Application sync, health checks, secrets | Multi-tenant GitOps, cluster registration, drift detection |
| **Cost Management** | AWS Cost Explorer, Vantage, Kubecost, Infracost | Tagging, cost attribution, waste reduction | Unit cost modeling, RI/savings-plan strategy, chargeback |
| **Incident Management** | PagerDuty, OpsGenie, Incident.io, FireHydrant | On-call schedule, escalation policies | Incident-response program design, severity taxonomy, major-incident workflows |
| **Chaos Engineering** | Chaos Mesh, Litmus, Gremlin | Experiment design, blast-radius control | Chaos program strategy, steady-state hypothesis definition, gameday facilitation |
| **Security / Compliance** | Trivy, Falco, OPA/Gatekeeper, Kyverno, Cert-Manager | Policy authoring, vulnerability scanning, admission control | Security posture framework, compliance automation, audit readiness |

### 6.2 Platforms & Managed Services (by Cloud)

| Cloud | Core Services | SRE Focus |
|-------|---------------|-----------|
| **AWS** | EC2, EKS, RDS/Aurora, ElastiCache, S3, CloudFront, Route53, Lambda, Step Functions, DynamoDB, MSK, SQS/SNS | VPC design, IAM policy, cost optimization, multi-AZ/multi-region |
| **GCP** | GKE, Cloud SQL, Cloud Spanner, Cloud Storage, Cloud CDN, Cloud Run, Pub/Sub, BigQuery | GKE Autopilot, VPC-native clusters, Cloud Interconnect |
| **Azure** | AKS, Azure SQL, Cosmos DB, Blob Storage, Front Door, Traffic Manager, Functions, Service Bus | AKS networking (CNI/Azure CNI), managed identity, ExpressRoute |

---

## 7. Career Progression

### 7.1 Level Ladder

```
                    ┌─────────────────────────────────────┐
                    │       Principal SRE (L8/L9)          │
                    │  Org-wide strategy, industry impact   │
                    └─────────────────────────────────────┘
                                 │
                    ┌─────────────────────────────────────┐
                    │         Staff SRE (L7)               │
                    │  Cross-team reliability standards     │
                    └─────────────────────────────────────┘
                                 │
                    ┌─────────────────────────────────────┐
                    │        Senior SRE (L6)               │
                    │  Service reliability, technical lead  │
                    └─────────────────────────────────────┘
                                 │
                    ┌─────────────────────────────────────┐
                    │         SRE II (L5)                  │
                    │  Independent contributor, on-call     │
                    └─────────────────────────────────────┘
                                 │
                    ┌─────────────────────────────────────┐
                    │         SRE I (L4)                   │
                    │  Learning, paired with senior         │
                    └─────────────────────────────────────┘

    ─── Individual Contributor Track ───      ─── Management Track ───
```

### 7.2 Progression Criteria

| Transition | Timeframe (Typical) | Key Evidence |
|-----------|---------------------|--------------|
| **SRE I → SRE II** | 12–18 months | Owns service reliability; handles on-call independently; writes good runbooks |
| **SRE II → Senior SRE** | 2–3 years | Leads incident response; architects solutions; mentors juniors; automates toil across a service |
| **Senior SRE → Staff SRE** | 3–5 years | Drives org-wide reliability initiatives; defines standards; embedded across multiple teams |
| **Staff SRE → Principal SRE** | 3–5 years | Sets org-wide reliability strategy; industry presence; architectural authority |
| **Senior SRE → SRE Manager** | 2–3 years | Has managed projects and people; demonstrates hiring/org-building skills |

### 7.3 Management Track: SRE Manager

Not all senior SREs stay IC. The SRE Manager track runs parallel:

| Responsibility | SRE Manager | Senior SRE (IC) |
|---------------|-------------|------------------|
| **Primary focus** | Team health, hiring, career growth, stakeholder management | Technical execution, system design, production excellence |
| **On-call** | Backup / escalation | Primary participant |
| **Technical depth** | Maintains architectural review capability | Maintains hands-on depth |
| **Meetings / calendar** | Heavy (1:1s, planning, cross-team syncs) | Lighter (design review, incident coordination) |
| **Leverage** | Through the team | Through code, architecture, and teaching |

---

## 8. Senior vs. Mid-Level: The Distinction

### 8.1 What Makes a Senior SRE Different

| Dimension | Mid-Level SRE | Senior SRE |
|-----------|--------------|------------|
| **Scope** | Owns reliability for a specific service | Owns reliability for a service family or platform area |
| **Proactivity** | Responds to incidents; improves runbooks | Anticipates failure modes; builds defenses before incidents occur |
| **Architectural Authority** | Implements designs reviewed by seniors | Reviews and approves designs; writes RFCs that set direction |
| **Automation** | Automates repetitive tasks for own work | Builds tooling consumed by multiple teams |
| **Mentorship** | Occasionally helps new team members | Regularly coaches 1–3 junior SREs; runs knowledge-sharing sessions |
| **Incident Command** | Can command for own service | Commands for any service in the domain; coaches new ICs |
| **Systems Thinking** | Understands service internals | Understands end-to-end user journeys through multiple services |
| **Org Influence** | Influences within the team | Influences across teams without direct authority |
| **Postmortem Leadership** | Contributes action items | Leads the postmortem; identifies systemic patterns |
| **Time Horizon** | Days to weeks | Quarters to a year |

### 8.2 The Staff / Principal Multiplier

Staff and Principal SREs differentiate from Senior SREs through **leverage**:

> **"A Principal SRE's value is not in how many incidents they resolve, but in how many incidents never happen because they designed the system better."**

| Activity | Senior SRE | Staff SRE | Principal SRE |
|----------|-----------|-----------|---------------|
| Fix system A | Fixes it | Fixes it + writes playbook + teaches system B team the same pattern | Fixes system A AND identifies the org-wide pattern that caused the failure, then removes it for all systems |
| Reduce MTTR | Cuts MTTR for service from 30→10 min | Cuts MTTR for the entire org by 50% through better tooling and training | Eliminates whole incident classes through architectural changes |
| Influence | 5–20 engineers | 20–100 engineers | 100–1000+ engineers |
| Time horizon | Quarter | Year | 2–5 years |
| Failure mode | Burning out from carrying too much weight | Becoming a bottleneck for decision-making | Losing touch with operational reality |

### 8.3 Common Failure Modes by Level

| Level | Failure Mode | Prevention |
|-------|-------------|------------|
| **Senior SRE** | Hero mode — too much direct execution, not enough teaching or automation | Track "time spent teaching vs. doing"; enforce a 30% minimum on enabling work |
| **Senior SRE** | Perfectionism — refusing to ship good-enough solutions | Error budgets apply to operations too; shipping a 90% solution early beats 100% never |
| **Staff SRE** | Bottleneck — every design review and incident needs their input | Delegate authority; write decisions into standards so others can self-serve |
| **Staff SRE** | Ivory tower — too far from production, designs don't match reality | Carry a pager. Stay in rotation. Do gamedays. |
| **Principal SRE** | Loss of credibility — org stops listening because they haven't debugged a real incident in years | Stay technical. Write code that ships. Join critical incidents, even just as an observer. |
| **Principal SRE** | Scope creep — saying yes to everything, diluting impact | Ruthless prioritization. "No" is a strategic decision. |

---

## Appendix A: Interview Rubric for Senior+ SRE

| Criterion | Weight | Strong Signal | Weak Signal |
|-----------|--------|---------------|-------------|
| **Systems Design** | 30% | Designs a reliable, observable, evolvable distributed system with tradeoff analysis | Memoized solution; misses failure modes; can't explain tradeoffs |
| **Incident Response** | 20% | Structured, calm approach to troubleshooting; communicates clearly under pressure | Panics; goes dark; guesses instead of gathering data |
| **Automation & Coding** | 20% | Writes clean, idiomatic, well-tested code that solves an ops problem | Overly complex; ignores error handling; untestable |
| **Cultural Fit** | 15% | Blameless mindset; data-driven; empowers others | Blame-oriented; cargo-cults practices; must be right |
| **Communication** | 15% | Clear, concise written and verbal explanations; adapts to audience | Rambling; overly technical for non-technical; can't explain "why" |

---

## Appendix B: Books, Talks & References

| Resource | Author | Why |
|----------|--------|-----|
| *Site Reliability Engineering* | Beyer, Jones, Petoff, Murphy (Google) | The foundational SRE text |
| *The Site Reliability Workbook* | Google SRE Team | Practical implementation guidance |
| *Seeking SRE* | Jones, Beyer, Murphy, Rensin | Conversations with industry SRE leaders |
| *Chaos Engineering* | Rosenthal, Jones, et al. | Systematic failure-injection methodology |
| *The Phoenix Project* | Gene Kim | IT/DevOps transformation narrative (SRE cultural alignment) |
| *Accelerate* | Forsgren, Humble, Kim | DORA metrics and evidence-based DevOps/SRE |
| *Designing Data-Intensive Applications* | Martin Kleppmann | Distributed systems fundamentals for reliability design |
| *Google SRE YouTube Channel* | Various | SRE talks, postmortems, and training from Google |
| *"How Complex Systems Fail"* | Richard Cook | Foundational essay on failure in complex systems |
| *"My Philosophy on Alerting"* | Rob Ewaschuk (Google) | Landmark essay on alert design and on-call quality |

---

*This document is a living reference. Propose updates via PR or open an issue to suggest improvements. For the most current version, see the canonical source at `/references/senior-sre-blueprint.md`.*
