# SRE Ecosystem Guide: A Curator's Map of Google SRE Learning Resources

> **Purpose:** Synthesize and analyze every resource at sre.google beyond the core SRE book and the two major articles (Embracing Risk / Eliminating Toil). This document is a **curator's guide** — it explains what each resource adds, how it connects to the others, and what level of practitioner it serves.
>
> **Audience:** SRE practitioners building the `site-reliability-engineering` Hermes skill profile. Use this to decide what to study, reference, or incorporate into your own SRE practice.

---

## Table of Contents

1. [The Site Reliability Workbook — Templates, Case Studies, and Org Change](#1-the-site-reliability-workbook)
2. [Building Secure & Reliable Systems — Security Meets Reliability](#2-building-secure--reliable-systems)
3. [SRE Classroom — Workshops That Build Systems Thinking](#3-sre-classroom--workshops)
4. [SRE Prodcast — The Audio Companion](#4-sre-prodcast)
5. [SRE Video Gallery — Curated Learning Paths](#5-sre-video-gallery)
6. [STPA — System Theoretic Process Analysis](#6-stpa-system-theoretic-process-analysis)
7. [Why Heroism is Bad](#7-why-heroism-is-bad)
8. [SRE Fundamentals Course](#8-sre-fundamentals-course)
9. [Measuring Reliability](#9-measuring-reliability)
10. [AI Engineering Reliable Operations](#10-ai-engineering-reliable-operations)
11. [SRE Milestones & History](#11-sre-milestones--history)
12. [Mobaa — Museum of Borgmon Abstract Art](#12-mobaa--museum-of-borgmon-abstract-art)
13. [SRE Local Events](#13-sre-local-events)

---

## 1. The Site Reliability Workbook

**URL:** https://sre.google/workbook/table-of-contents/

The Workbook is not a second SRE book — it's a **field manual** designed to be dog-eared and coffee-stained. Where the original SRE book describes *why* Google does SRE, the Workbook describes *how* to implement it in your own organization.

### Structure and Contents

| Part | Section | What It Adds |
|------|---------|-------------|
| **I. Foundations** | Implementing SLOs, SLO Case Studies, Monitoring, Alerting on SLOs, Eliminating Toil, Simplicity | Practical templates and worked examples for the core SRE disciplines |
| **II. Practices** | On-Call, Incident Response, Postmortem, Managing Load, NALSD, Data Pipelines, Config Design, Config Specifics, Canarying | Step-by-step operational playbooks |
| **III. Processes** | Identifying Overload, SRE Engagement Model, Reaching Beyond Your Walls, Team Lifecycles, Org Change Management | The people and organizational side of reliability |
| **Appendices** | Example SLO Document, Error Budget Policy, Postmortem Analysis Results | Ready-to-adapt templates |
| **Case Studies** | Evernote, Home Depot, New York Times | Real-world implementations outside Google |

### Critical Additions Over the Original Book

**1. The NALSD (Non-Abstract Large System Design) Chapter**
The original book mentions systems design briefly. The Workbook devotes a full chapter to NALSD — the structured process Google SREs use to reason about planet-scale systems. This is arguably the most transferable skill in the entire SRE canon. The chapter walks through: defining the problem scope, sketching architecture, evaluating tradeoffs (consistency vs. availability, latency vs. throughput), and stress-testing the design against failure modes. It's the same framework used in Google's SRE interview loop.

**2. The SRE Engagement Model**
The original book implies that SRE teams interact with product teams, but the Workbook makes the model explicit with three tiers:
- **Hands-off (consultative):** SRE provides advice, product teams own operations
- **Limited engagement (embedded):** SRE co-owns parts of the service
- **Full engagement (service ownership):** SRE operates the service end-to-end

Each tier comes with clear entry criteria — error budgets, monitoring maturity, on-call readiness — that the product team must meet before SRE commits deeper engagement. This is fundamentally an *org design* pattern, not a technical one.

**3. Org Change Management**
The chapter on organizational change management is unique in the SRE literature. It addresses the human dynamics of adopting reliability practices: how to build coalitions, how to handle resistance, how to measure cultural adoption alongside technical SLIs. The original SRE book is almost silent on this, yet it's the single biggest obstacle most organizations face.

**4. Practical Templates**
The appendices include:
- An SLO document template with all the fields an SLO should capture (service definition, SLI specification, measurement methodology, target, window, policy)
- An error budget policy template covering governance, exceptions, and quarterly reviews
- A postmortem action-item tracking format with owner, deadline, and evidence-of-completion fields

These alone make the Workbook worth its weight. For teams adopting SRE, copying these templates and filling them in is faster and more reliable than inventing them from scratch.

**5. Case Studies from Non-Google Companies**
Evernote, Home Depot, and the New York Times are not Google-scale but face Google-class reliability problems with far fewer resources. Their case studies demonstrate how SRE principles adapt when you don't have a Borg cluster or a dedicated monitoring team. The New York Times case study on migrating from a monolithic CMS to microservices while maintaining 99.9%+ availability is particularly instructive.

**How to Use It:** If the SRE book is for *understanding*, the Workbook is for *doing*. Read a Workbook chapter, then immediately implement its template or process with your team. The NALSD and Engagement Model chapters should be on the syllabus for any SRE candidate's first 90 days.

---

## 2. Building Secure & Reliable Systems

**URL:** https://google.github.io/building-secure-and-reliable-systems/

This is a full-length book published collaboratively by Google's SRE and Security teams. It is available freely online and was published in 2020 — newer than the original SRE book (2016) and the Workbook (2018).

### How Security and SRE Converge

The foundational insight of this book is that **reliability and security are the same class of problem**: both are emergent properties of a system that cannot be added after the fact, both are eroded by complexity, both require cultural investment, and both fail catastrophically when treated as an afterthought.

| Dimension | Pure Reliability View | Pure Security View | Converged View |
|-----------|----------------------|--------------------|----------------|
| Failure mode | Service degradation | Breach | Both cause trust erosion |
| Measurement | Error budget burn | Time-to-patch / MTTR for incidents | Integrated risk scorecard |
| Response | Incident commander | Incident commander + forensics | Unified crisis response |
| Design principle | Redundancy, graceful degradation | Least privilege, defense in depth | Both, with explicit tradeoff awareness |

### Key Chapters and Their SRE Relevance

**Part II: Designing Systems (Proxies, Tradeoffs, Least Privilege)**

The Design Tradeoffs chapter (Chapter 7) is a must-read for SREs. It introduces a framework for reasoning about nonfunctional requirements (NFRs) — the properties a system must have but which aren't captured in feature specifications. It distinguishes between *feature properties* (what the system does) and *emergent properties* (how the system behaves — reliability, security, performance, operability). The key move is recognizing that emergent properties **compete**: improving security often hurts performance; improving performance often hurts reliability (redundancy adds latency). The chapter provides a structured way to make these tradeoffs explicit rather than implicit.

The Least Privilege chapter (Chapter 9) extends the SRE concept of "simplicity" into access control. The principle of least privilege — granting only the permissions a component or person needs to function — is directly analogous to the SRE principle of minimizing surface area. The chapter also covers **breakglass mechanisms**: emergency access systems that bypass normal controls during outages. Any SRE who has been locked out of a production system during an incident should study this chapter.

**Part IV: Maintaining Systems (Operations, Crisis Response, Recovery)**

The Crisis Response chapter (Chapter 17) is SRE incident management seen through a security lens. It introduces:
- **Purple teaming:** combining red (adversarial) and blue (defensive) teams to test both reliability and security posture simultaneously
- **Adversarial incident response:** treating every incident as potentially malicious until proven otherwise, while avoiding the paralysis that assumption can cause
- **Recovery with forensic preservation:** the tension between restoring service quickly and preserving evidence for post-incident analysis

**Part V: Organizing for Reliability and Security**

The Culture and Community chapters (19-20) address something the SRE book touches but doesn't fully explore: **blameless culture in a security context**. Security incidents often involve intent, negligence, or policy violations — the blameless model breaks down when malice is involved. The book offers a nuanced framework for distinguishing between honest mistakes, reckless behavior, and malicious actions, and handling each differently.

**Synthesis:** This book extends the SRE profile into adversarial thinking. Every SRE should read at least Chapters 7 (Design Tradeoffs), 9 (Least Privilege), and 17 (Crisis Response). For teams running ML models or public APIs, Chapter 14 (Testing) covers adversarial testing techniques (fuzzing, chaos engineering with malicious inputs) that are directly applicable.

| Comparison | SRE Book | Building Secure & Reliable Systems |
|-----------|----------|-----------------------------------|
| Focus | Operational reliability | Reliability at the intersection of ops and security |
| Target audience | Aspiring/practicing SREs | SREs + Security engineers + Architects |
| Unique contribution | Error budgets, toil, monitoring philosophy | Breakglass, least privilege, adversarial thinking |
| Age | 2016 | 2020 |
| Best consumed | Cover-to-cover | Selected chapters + reference |

---

## 3. SRE Classroom — Workshops

SRE Classroom is Google's most underappreciated resource. These are structured, multi-hour workshops designed to be run with teams. They develop the **systems thinking muscle** that distinguishes senior SREs from junior ones.

### Workshop 1: Distributed PubSub

**URL:** https://sre.google/classroom/distributed-pubsub/

This workshop asks participants to design a planet-scale pub-sub messaging system. It is explicitly a **NALSD (Non-Abstract Large System Design)** exercise.

**What it covers:**
- Correctness: At-least-once vs. exactly-once delivery, ordering guarantees, deduplication
- Reliability: How to survive server failures, network partitions, and leader election
- Performance: Throughput scaling, batching strategies, backpressure
- Communication styles: Synchronous vs. asynchronous, push vs. pull

**Why it matters for SRE thinking:**
The workshop forces participants to make explicit tradeoffs that in production are often implicit. By reasoning through the design on paper, you develop the mental habit of asking "what happens when this component fails?" before you build it — rather than discovering failure modes during an outage.

The workshop also teaches **structured communication of architectural decisions**. The output is not a UML diagram but a written design document organized by requirements, assumptions, architecture, tradeoffs, and failure modes — exactly the format used in Google SRE design reviews.

### Workshop 2: Distributed Image Server

**URL:** https://sre.google/classroom/imageserver/

A more concrete workshop focusing on the design of a photo storage and serving system. Key concepts:

| Concept | Workshop Exercise | SRE Relevance |
|---------|------------------|---------------|
| Sharding | Partitioning images across servers | Horizontal scaling patterns |
| Replication | K-replication with quorum reads/writes | Consistency vs. availability tradeoffs |
| Latency | Edge caching, CDN offloading | SLO design for user-facing latency |
| Load balancing | Consistent hashing, hot-spot mitigation | Capacity planning and traffic management |

### Workshop 3: The Art of SLOs

**URL:** https://sre.google/resources/practices-and-processes/art-of-slos/

A workshop that guides participants through defining SLIs, SLOs, and error budgets for a fictional mobile game (Quest Squad). This is the most practical SLO workshop available publicly.

**What it teaches:**
- How to decompose a user-facing service into critical user journeys (CUJs)
- How to define SLIs that actually measure user experience, not system internals
- How to set SLO targets that balance reliability investment with feature velocity
- How to use error budgets to make deployment decisions

**Synthesis:** The three workshops together form a **capstone curriculum**: NALSD reasoning (PubSub), system architecture design (Image Server), and reliability measurement (Art of SLOs). A team that completes all three workshops has internalized the core SRE skill set at a depth that reading alone cannot provide.

| Workshop | Duration | Pre-read Skills | Best For |
|----------|----------|-----------------|----------|
| Distributed PubSub | 3-4 hours | Basic distributed systems concepts | Senior ICs, design interview prep |
| Image Server | 2-3 hours | Web architecture, caching | Mid-level SREs, backend engineers |
| Art of SLOs | 2-3 hours | Familiarity with SRE concepts | New SRE team members, product teams adopting SRE |

---

## 4. SRE Prodcast

**Available on:** YouTube, Spotify, Apple Podcasts, RSS

Six seasons of Google SREs talking about their work. The Prodcast is not a course — it's a **cultural artifact**. It captures the voice and thinking of SREs in a way that formal writing cannot.

### Season-by-Season Guide

| Season | Theme | Best Episodes for... |
|--------|-------|---------------------|
| 1 | SRE Fundamentals | **New SREs** — explains the basics: what is SRE, how it differs from DevOps, the birth of the discipline at Google |
| 2 | SLOs Deep Dive | **Teams adopting SLOs** — practical discussions of SLI design, error budget policies, and the human side of setting targets |
| 3 | Prodcast Live! | **Experienced SREs** — live Q&A sessions where audience questions drive the conversation. Unpredictable and illuminating |
| 4 | On-Call | **On-call practitioners** — the psychology of pager duty, sustainable rotations, incident escalation, the "Ops-Exhausted" problem |
| 5 | SRE Careers | **Aspiring SREs and managers** — how to grow as an SRE, what distinguishes staff/principal SREs, the non-linear career path |
| 6 | Modern SRE | **Everyone** — reliability in ML systems, platform engineering, SRE in regulated industries, the future of the discipline |

### How to Use the Prodcast for Onboarding

Design a 6-week "listening curriculum" for new SRE team members:

- **Week 1:** Season 1, Episodes 1-3 (What is SRE, Birth of SRE, The CRE Model) — establishes foundational context
- **Week 2:** Season 2, Episodes 1-2 (SLOs in Practice, Error Budget Conversations) — complements reading the SLO chapters
- **Week 3:** Season 4, Episodes 1-3 (On-Call Psychology, Incident Management, Postmortems) — prepares new team members for their first on-call rotation
- **Week 4:** Season 3, Live episodes (any 2) — exposes them to unscripted SRE thinking
- **Week 5:** Season 5, Episodes 1-2 (Career Growth, Technical Leadership) — sets expectations for growth
- **Week 6:** Season 6, Episodes covering ML reliability and platform engineering — connects SRE to their likely future work

---

## 5. SRE Video Gallery

**URL:** https://sre.google/ (Video Gallery section)

90+ videos spanning SREcon conferences (2014-2025), GOTO conferences, and Google Technical Learning sessions. Filterable by: AI/ML, SLOs, Observability, Systems, Security.

### Curated Learning Path by Topic Area

| Topic | Must-Watch Talk | Speaker / Event | Why |
|-------|----------------|-----------------|-----|
| **SLOs** | "The Art of SLOs" workshop recording | SREcon | The workshop in action — watch before running it with your team |
| **Observability** | "Monitoring Distributed Systems" | Google Tech Learning | Foundational talk on the difference between monitoring and observability |
| **Incident Response** | "Incident Management at Google" | SREcon Americas | How Google runs incidents — command structure, communication, handoffs |
| **Postmortems** | "Blameless Postmortems" | SREcon EMEA | The cultural prerequisites for effective postmortems |
| **Capacity Planning** | "Managing Load" | SREcon Americas | Google's approach to load shedding, rate limiting, and capacity |
| **AI/ML Reliability** | "Reliability for ML Systems" | SREcon 2023-2024 | The latest thinking on non-deterministic system reliability |
| **Security** | "Building Secure & Reliable Systems" talk | GOTO Chicago | Overview talk by the book's authors — great starting point |
| **Cultural** | "Why Heroism is Bad" | SREcon | The definitive version of this argument (see section 7) |

### Strategic Use

The video gallery is best used as a **just-in-time learning resource**. When preparing for a specific initiative (adopting SLOs, redesigning on-call, running a postmortem), watch the related talks 2-3 days before the event. The talks from 2022-2025 are most relevant for modern practice; the 2014-2018 talks are valuable for historical context but some specific advice (e.g., about specific tools) is outdated.

---

## 6. STPA — System Theoretic Process Analysis

**URL:** https://sre.google/resources/practices-and-processes/stpa/

STPA is a hazard analysis technique developed by Nancy Leveson at MIT. Google has adopted it for analyzing complex system failures. It is fundamentally different from the postmortem and root-cause analysis (RCA) approaches most SREs know.

### How STPA Differs from Traditional RCA

| Dimension | 5 Whys / RCA | STPA |
|-----------|-------------|------|
| Unit of analysis | Linear chain of events | Control loops and constraints |
| Causal model | Root cause (single failure) | Emergent from interactions |
| Scope | Individual incident | System design |
| Output | Corrective actions on specific components | Design changes to control structure |
| Best for | Simple, well-understood failures | Complex, socio-technical failures |

### Control Loops as the Unit of Analysis

STPA treats every system as a set of **control loops**: a controller (human or automated) that sends control actions to a process, and receives feedback from sensors. Failures occur when:

1. Control actions are missing (the controller doesn't act when it should)
2. Control actions are provided incorrectly (wrong action)
3. Control actions are provided at the wrong time (too early, too late, or out of order)
4. Control actions stop too soon or continue too long

This framing is powerful for SRE because it encompasses **both technical and human failures** in a single model. An on-call engineer who doesn't respond to an alert (a missing control action) can be analyzed using the same framework as a load balancer that fails to route traffic away from a degraded backend.

### When to Use STPA vs. 5 Whys vs. Fault Tree Analysis

| Scenario | Recommended Method | Why |
|----------|-------------------|-----|
| Simple, isolated failure (e.g., single server crash) | 5 Whys | Fast, cheap, sufficient |
| Known failure mode with clear path (e.g., disk full) | Fault Tree Analysis | Systematic, covers combinatorics |
| Complex socio-technical failure (e.g., cascading outage across teams) | STPA | Captures control loop dynamics |
| Safety-critical or ML system failure | STPA | Handles non-deterministic behavior |
| Postmortem after a major incident | 5 Whys + STPA | Whys for immediate actions, STPA for systemic redesign |

### Value for ML and Safety-Critical Systems

Traditional RCA assumes a **deterministic causal chain**: A caused B which caused C. This breaks down for ML systems where the same input can produce different outputs (model drift, non-deterministic inference) and for safety-critical systems where the cost of failure is so high that you need to prevent it before it occurs.

STPA is **proactive**: it analyzes the design of the control structure and identifies unsafe control actions before they cause failures. For ML systems, this means analyzing the feedback loop between training data quality, model deployment, and production monitoring — a control structure that traditional RCA is ill-equipped to model.

**Synthesis:** STPA is an advanced technique, not a replacement for postmortems. Every SRE should be proficient in 5 Whys. Senior SREs should add STPA to their analysis toolkit for complex, non-deterministic, and safety-critical systems.

---

## 7. Why Heroism is Bad

This is one of the most cited pieces of SRE cultural writing at Google. It exists as a talk (in the Video Gallery) and as a principle woven throughout the SRE book and Workbook.

### The Hero Culture Anti-Pattern

The "hero" is the engineer who stays up all night fighting a fire, who has access to systems no one else understands, who carries the pager for their entire team. In most organizations, heroism is rewarded — promotions, praise, the adrenaline of being "the one who saved the day."

**Why it's bad for reliability:**

| Hero Behavior | Systemic Cost |
|--------------|---------------|
| Fixing incidents solo without documentation | Knowledge silo — only one person can fix it next time |
| Working off-hours to "save" a service | Burnout, turnover, and expertise loss |
| Accumulating niche knowledge without sharing | Bus factor of 1 |
| Being the "go-to" person for every problem | Overload, bottleneck, no time for proactive work |
| Working around systemic problems | Masks the need for engineering investment |

### Connection to Blameless Culture and Toil Elimination

The heroism argument connects directly to two pillars of SRE:

1. **Blameless culture:** Hero narratives assign blame by inversion — the hero is celebrated, which implies everyone else (who didn't stay up all night) is at fault. This creates a culture where failures are hidden unless someone heroes their way through them.

2. **Toil elimination:** Heroic firefighting is the purest form of toil — manual, repetitive, non-durable work that could be automated. An organization that rewards heroism is incentivizing its engineers to *not* reduce toil, because reducing toil reduces opportunities for heroism.

**The antidote:** The SRE model argues that reliability should be achieved through engineering, not heroism. If a service fails the same way twice, the correct response is not to train better heroes — it's to build better systems. Error budgets, monitoring, SLOs, and blameless postmortems are all structural anti-heroism measures.

**Synthesis:** This is the most important cultural concept for new SRE teams to internalize. It's also the hardest to implement because it requires changing what "good work" looks like in an organization. Use the talk for team discussions; use the SRE book's toil framework for implementation.

---

## 8. SRE Fundamentals Course

A structured course that maps directly to the SRE book's chapter structure. It is Google's internal onboarding curriculum for new SREs, made public.

### How It Maps to the SRE Book

| Module | SRE Book Chapter(s) | Topic |
|--------|---------------------|-------|
| 1 | 1-2 | Introduction, The Environment (why SRE exists) |
| 2 | 3-4 | Embracing Risk, SLOs |
| 3 | 5-6 | Eliminating Toil, Monitoring |
| 4 | 7-8 | Automation, Release Engineering |
| 5 | 9-10 | Simplicity, Practical Maturation |
| 6 | 11-13 | On-Call, Incident Response, Postmortems |
| 7 | 14-15 | Managing Load, Capacity Planning |
| 8 | 16-18 | Emergency Response, Data Pipelines, Prod Meetings |
| 9 | 19-21 | SRE Org Models, CRE, the Future |

### Using It for Onboarding

The course provides:
- **Slides** that can be adapted for internal training
- **Discussion questions** for each module
- **Exercises** that test comprehension

This is the **ideal onboarding structure** for new SRE team members. A recommended 9-week cadence:

- Week N: Read the corresponding SRE book chapters
- Week N+1: Watch the Fundamentals course module
- Week N+1 follow-up: Team discussion of the discussion questions and exercises

This pairs reading (individual, deep) with discussion (team, social) — reinforcing learning through both modes.

The course does **not** cover the Workbook's practical templates or the organizational change content. It is purely an introduction to the concepts. Use it as the first pass, then layer on the Workbook for implementation.

---

## 9. Measuring Reliability

**URL:** https://sre.google/resources/practices-and-processes/measuring-reliability/

A focused resource that addresses the practical mechanics of defining and measuring reliability. It fills a gap between the SRE book's conceptual framework ("you need SLOs") and the actual work of implementing them.

### What It Covers

- **Service boundaries:** Where does "your service" end? Shared infrastructure, APIs, client-side code — what's included in your reliability measurement?
- **SLI selection:** Practical criteria for choosing which metrics to use as SLIs, with worked examples for different service types (CRUD APIs, batch processing, streaming, storage)
- **Measurement windows:** Rolling windows vs. calendar windows, sliding vs. fixed windows, and the implications for error budget interpretation
- **Counting failures:** How to count events (request-level, user-level, time-based) and the impact of each counting methodology on perceived reliability
- **Target setting:** How to set SLO targets that are achievable but meaningful, with guidance on distinguishing aspirational targets from contractual ones

### How It Complements the SLO/SLI Framework Reference

The SLO/SLI framework in the SRE book tells you *what* to build. Measuring Reliability tells you *how to build it correctly*. It covers edge cases the book glosses over:

- What happens when your measurement pipeline is itself unreliable? (The "who measures the measurer" problem)
- How to handle services with heterogeneous request types (reads vs. writes, small vs. large payloads)
- How to aggregate reliability across service tiers (critical vs. best-effort)

**Synthesis:** Read this *after* the SRE book's SLO chapters and *before* implementing your first SLO. It will save you from common measurement mistakes that produce misleading reliability numbers.

---

## 10. AI Engineering Reliable Operations

**Marked "New!" on sre.google**

This is Google's most recent SRE content, reflecting the growing importance of ML systems in production. It addresses the unique challenges of maintaining reliability in non-deterministic systems.

### Why ML Reliability is Different

| Dimension | Traditional Software | ML Systems |
|-----------|---------------------|------------|
| Correctness | Deterministic — same input, same output | Statistical — same input, different output |
| Failure mode | Crash, exception, error code | Silent degradation, model drift, concept drift |
| Debugging | Reproduce with fixed input | Reproduce in expectation (requires data distribution analysis) |
| Rollback | Revert to previous version | Revert model + data + features (all must be consistent) |
| Monitoring | Latency, error rate, throughput | Latency, error rate + prediction distribution, feature distribution, data quality |

### How This Extends SRE into Non-Deterministic Systems

The core SRE framework (SLOs, error budgets, monitoring, incident response) still applies to ML systems, but every technique needs adaptation:

- **SLIs for ML:** Must include data quality metrics (feature freshness, null rates, distribution shifts) alongside traditional performance metrics. A model may have 99.9% uptime but produce useless predictions because input features have drifted out of distribution.
- **Error budgets for ML:** Need to account for model staleness. An error budget that only tracks API failures misses the more common failure mode: a model that's still running but producing degraded predictions because it hasn't been retrained on recent data.
- **Monitoring for ML:** Requires multiple "verification layers": service health, pipeline health, model health, and business outcome health. Each layer can fail independently.
- **Incident response for ML:** Cannot just "restart" a model. Fixing a degraded model may require: rolling back training data, retraining with corrected labels, adjusting inference parameters, or even redesigning the feature pipeline.

**Synthesis:** This is essential reading for any SRE working with ML-powered systems. It should be paired with the STPA resource (section 6) — STPA provides the analysis methodology for understanding control loop failures in these complex, non-deterministic systems.

---

## 11. SRE Milestones & History

### Twentieth Anniversary (https://sre.google/20/)

20+ video testimonials from SREs across Google, from the founders of the discipline to current practitioners.

**What it reveals:**
- **The origin story:** Ben Treynor Sloss formalized SRE in 2003 when Google was already running at planetary scale. The early years were about survival; SRE emerged as a response to the failure of traditional ops models.
- **The inflection points:** The introduction of error budgets (c. 2010) was the theoretical breakthrough that made SRE scalable. Before error budgets, reliability was a theological argument; after, it became an engineering tradeoff.
- **The cultural evolution:** Early SRE was a startup within Google — small, elite, and somewhat adversarial with product teams. Modern SRE is more collaborative, with clearer engagement models and less "us vs. them" dynamics.

### Ask an SRE at Next '26 (https://sre.google/next26/)

A recent Q&A session (2025/2026) that reveals current SRE thinking at Google.

**Key takeaways:**
- **Platform engineering is SRE's evolution:** The line between SRE and platform engineering is blurring. SREs increasingly build internal platforms that product teams use to self-serve reliability.
- **AI as both tool and challenge:** SREs use AI for incident classification, anomaly detection, and runbook automation — but also struggle with the reliability of AI-powered systems themselves.
- **The diversity problem:** Google SRE remains less diverse than they'd like. The session includes honest discussion of what's being done to change this.

### Why History Matters

SRE is a young discipline (est. 2003). Its practices evolved in response to specific failures and constraints at Google. Understanding that history helps practitioners:

1. **Recognize which practices are universal** (error budgets, toil elimination, blameless culture) vs. **which are Google-specific** (Borg, specific monitoring architectures, engagement models that assume massive scale)
2. **Understand why practices are the way they are** — not just *what* to do, but *why* it worked at Google and why it might need adaptation elsewhere
3. **Avoid repeating the same mistakes** — most SRE practices are formalized scar tissue from specific failures

---

## 12. Mobaa — Museum of Borgmon Abstract Art

> *"Borgmon was a beautiful monster."* — Google SRE

Mobaa is a collection of **monitoring data visualizations turned into art**. Borgmon was Google's internal monitoring system — a powerful but famously idiosyncratic tool with its own query language, visualization format, and idiosyncrasies. As Borgmon was phased out (replaced by Monarch and other systems), some SREs created abstract art from old monitoring data.

### What Mobaa Reveals About SRE Culture

1. **Affection for the tool:** SREs form deep attachments to their tools. Borgmon was ugly, hard to configure, and opaque — but it *worked* at a scale no other tool could handle. The art is a form of appreciation.

2. **Operational folklore:** Monitoring data captures the history of a service's life — every spike is an outage, every dip is a deployment. The art preserves that history in a way that dashboards don't.

3. **Team-building through shared experience:** Mobaa started as an internal exhibit. SREs submitted pieces, voted on favorites, and held "gallery openings." This is SRE culture expressing itself through creativity rather than postmortems and runbooks.

4. **Healthy detachment from production:** Creating art from monitoring data transforms the relationship to production — from anxiety ("my pager might fire") to reflection ("this is what our service looked like"). This is psychologically healthy for engineers whose entire job is to worry about failure.

### Value for the SRE Profile

Mobaa is not a learning resource in the traditional sense. Its value is **cultural**: it demonstrates that SRE teams function best when they have outlets beyond pure operations. The best SRE teams are not the ones that never have outages — they're the ones that have rituals for processing and learning from outages. Mobaa is one such ritual.

**Synthesis:** Include Mobaa in the SRE profile's recommended "cultural immersion" materials alongside the Prodcast and the Milestones videos. It won't teach anyone to run better systems, but it will help them understand the community they're joining.

---

## 13. SRE Local Events

**Meetups in:** Munich, NYC, Pittsburgh, Sunnyvale

Google hosts regular SRE meetups in these cities. These are community events, not corporate communications.

### What They Offer

- **Presentations from local practitioners** (not just Googlers) sharing their SRE implementations
- **Workshop sessions** where attendees work through problems together
- **Networking** with other SREs facing similar challenges
- **Recruiting** for Google SRE roles (for those interested)

### Community Knowledge-Sharing Value

Local meetups serve a function that documentation cannot: they provide **context**. Every SRE implementation is different — understanding how other organizations adapted SRE practices to their specific constraints is invaluable. The meetup format also allows for questions and conversations that documentation and talks don't accommodate.

**For the SRE profile:** Include the meetup URLs and mention that these are the most reliable source of "SRE in the real world" case studies outside of formal case study publications. For teams without a local meetup, the YouTube recordings of past meetup talks are a good substitute.

---

## Cross-Reference: A Learning Path Matrix

The table below maps each resource to learning goals and experience levels.

| Resource | Deep Theory | Practical Application | Culture | Beginner | Intermediate | Advanced |
|----------|-------------|----------------------|---------|----------|-------------|----------|
| SRE Book | ★★★ | ★★ | ★★★ | ★ | ★★★ | ★★★ |
| SRE Workbook | ★★ | ★★★ | ★★ | ★★ | ★★★ | ★★★ |
| Building Secure & Reliable Systems | ★★★ | ★★ | ★★ | ★ | ★★ | ★★★ |
| SRE Classroom Workshops | ★★ | ★★★ | ★ | ★ | ★★★ | ★★★ |
| SRE Prodcast | ★ | ★ | ★★★ | ★★★ | ★★★ | ★★ |
| Video Gallery | ★★ | ★★ | ★★★ | ★★ | ★★★ | ★★★ |
| STPA | ★★★ | ★ | ★ | ★ | ★★ | ★★★ |
| Why Heroism is Bad | ★ | ★ | ★★★ | ★★★ | ★★★ | ★★ |
| Fundamentals Course | ★★ | ★ | ★★ | ★★★ | ★★ | ★ |
| Measuring Reliability | ★★ | ★★★ | ★ | ★★★ | ★★ | ★★ |
| AI Engineering | ★★★ | ★★ | ★ | ★ | ★★ | ★★★ |
| Milestones & History | ★ | ★ | ★★★ | ★★ | ★★★ | ★★ |
| Mobaa | ★ | ★ | ★★★ | ★ | ★★ | ★★★ |
| Local Events | ★ | ★★ | ★★★ | ★★ | ★★★ | ★★★ |

**Key:** ★ = Limited value, ★★ = Moderate value, ★★★ = High value

---

## Summary: The SRE Learning Ecosystem at a Glance

```
SRE ECOSYSTEM MAP
=================

                             [Foundations]
         ┌────────────────────────────────────────────┐
         │  SRE Book (original)                       │
         │  SRE Fundamentals Course (onboarding)      │
         │  Measuring Reliability (practical SLOs)    │
         └────────────────────────────────────────────┘
                              │
         ┌────────────────────┴────────────────────┐
         │                                         │
  [Implementation]                         [Advanced Topics]
  SRE Workbook                          Building Secure & Reliable
  - Templates, case studies             - Adversarial thinking
  - NALSD, engagement model             - Breakglass mechanisms
  - Org change management               - Design tradeoffs
  - Postmortem analysis                          │
         │                                         │
         ├──────────────────┬──────────────────────┤
         │                  │                      │
  [Hands-On Skills]   [Analysis Methods]    [New Frontiers]
  SRE Classroom       STPA                  AI Engineering
  - PubSub workshop   - Control loops       - ML reliability
  - Image server      - Safety-critical     - Non-deterministic
  - Art of SLOs       - ML systems          - Verification layers
         │                  │                      │
         └──────────────────┴──────────────────────┤
                                                   │
                              ┌────────────────────┘
                              │
                    [Culture & Community]
                    - SRE Prodcast (6 seasons)
                    - Video Gallery (90+ talks)
                    - Why Heroism is Bad
                    - Milestones & History
                    - Mobaa (monitoring art)
                    - Local Events (meetups)
```

---

## Recommended Reading Order by Role

### For a New SRE (first 90 days)
1. SRE Fundamentals Course (weeks 1-3)
2. SRE Book, Chapters 1-6 (weeks 1-2)
3. Measuring Reliability (week 3)
4. SRE Prodcast, Season 1 (weeks 2-4, for commuting)
5. Why Heroism is Bad (week 4 — cultural context)
6. SRE Workbook, Parts I-II (weeks 5-8)
7. SRE Classroom: Art of SLOs (week 8, run with team)
8. Milestones & History videos (week 9 — inspiration)

### For an Experienced SRE Expanding into Security
1. Building Secure & Reliable Systems, Chapters 1, 7, 9, 17 (read in order)
2. STPA overview (control loops as analysis tool)
3. Video Gallery: Security track talks
4. SRE Classroom: Distributed PubSub workshop (applies NALSD to a security-relevant system)

### For an SRE Team Adopting SLOs
1. SRE Book, Chapters 3-4 (Embracing Risk, SLOs)
2. Measuring Reliability (practical pitfalls)
3. SRE Workbook, Chapter on Implementing SLOs + appendices
4. SRE Classroom: Art of SLOs (team workshop)
5. SRE Prodcast, Season 2 (listening while implementing)
6. SRE Workbook, SLO Case Studies (Home Depot, New York Times)

### For an SRE Working with ML Systems
1. AI Engineering Reliable Operations (latest guidance)
2. STPA (control loop analysis for non-deterministic systems)
3. Building Secure & Reliable Systems, Chapter 14 (Testing)
4. Video Gallery: AI/ML track
5. SRE Prodcast, Season 6 (Modern SRE, ML episodes)

---

*This guide was synthesized from the resources at https://sre.google/ and related Google publications. It is a living document — the SRE ecosystem evolves as Google publishes new content. Revisit the source sites periodically for updates.*
