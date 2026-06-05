# Data Architecture Anti-Patterns Catalog

A catalog of named anti-patterns with symptoms, root causes, and remediations.
Sources: Sunil Prakash (Enterprise Data Architecture), Kengie Ho (Common Enterprise Architectural Pitfalls), DataForest, and industry experience.

## 1. Silver Bullet Thinking

**Symptom:** Adopting Data Mesh, Data Fabric, or another pattern because it's trendy, without organizational readiness.

**Root cause:** Believing an architectural pattern alone solves what are fundamentally organizational problems (ownership, trust, skills).

**Remediation:** Before adopting Data Mesh, verify you have: domain teams willing to own data products, a platform team to build self-serve infra, and executive sponsorship for federated governance. If any is missing, start smaller.

## 2. SoR vs SSoT Confusion

**Symptom:** Business leaders point to a legacy 20-year-old billing system and say "That's our Single Source of Truth." Modern apps are forced to dumb down their data to fit the legacy system's narrow schema.

**Root cause:** Confusing a transactional System of Record (SoR) — where data is originally authored — with a Single Source of Truth (SSoT) — an aggregated, reconciled, governed view across the enterprise.

**Remediation:** Decouple the two domains. Let operational systems be localized SoRs for their domain. Build a dedicated layer (MDM platform, data lakehouse, or data mesh) above them that ingests from every SoR, resolves conflicts, applies quality rules, and serves as the true SSoT.

## 3. High-Fidelity / Lossy Sync Destruction

**Symptom:** A modern CRM with rich, structured data is synced bidirectionally with a legacy ERP. The ERP truncates names, flattens addresses, drops extra fields — then syncs that flattened data back to the CRM, permanently overwriting the high-fidelity records.

**Root cause:** Allowing a low-fidelity system to blindly update a high-fidelity system through lossy synchronization. Known formally as semantic heterogeneity, information loss in schema mapping, and destructive overwrites.

**Remediation:** Place an integration middleware or MDM platform at the system boundary with **metadata-driven field-level survivorship**. Apply hierarchical rules: "The ERP always wins financial fields, but the CRM always wins customer contact info." Build an Anti-Corruption Layer (from Domain-Driven Design) to protect modern systems from legacy constraints.

## 4. Fragmented Identity / "Customer 720"

**Symptom:** Customer logs in with email (System A), calls support as "Jane Doe" (System B). Without a shared primary key, the integration layer creates a duplicate record. Instead of Customer 360, you get "Customer 720."

**Root cause:** Relying on simple SQL JOINs or exact-match keys for entity resolution across systems that have no common identifier.

**Remediation:** Introduce an Identity Resolution Engine at the data ingestion layer. Use two-stage matching:
- **Deterministic:** exact matches on hashed email, SSN, phone
- **Probabilistic:** ML-based matching (Levenshtein distance, shared device IPs, behavioral patterns) with confidence scoring

Treat identity resolution as a foundational requirement, not a downstream analytics problem.

## 5. Schema Evolution Mismatch

**Symptom:** A modern microservices team splits `FullName` into `FirstName`/`LastName`. A downstream legacy app consuming the data stream crashes because it expects the old schema.

**Root cause:** Speed mismatch between agile schema evolution and rigid legacy consumers. Tightly coupled interfaces without mediation.

**Remediation:** Introduce an Anti-Corruption Layer (ACL) between modern and legacy systems. The ACL translates schemas at the boundary — the modern system evolves freely, the ACL provides backward-compatible views to legacy consumers.

## 6. The Ivory Tower

**Symptom:** Architecture team produces standards, roadmaps, and reference architectures in isolation, without engaging delivery teams or business stakeholders. Artifacts are technically correct but irrelevant to actual problems.

**Root cause:** Architecture practiced as a detached design discipline rather than an embedded consulting function.

**Remediation:** Embed architects with delivery teams. Architecture decisions should emerge from concrete problems, not abstract frameworks. The architect who writes a standard without understanding the team's actual constraints is building shelfware.

## 7. Tool-First Architecture

**Symptom:** Organization picks Snowflake (or Databricks, or Kafka) and then goes looking for problems to solve with it.

**Root cause:** Technology selection driven by vendor marketing, hiring availability, or executive preference rather than requirements analysis.

**Remediation:** Start with business requirements, data profiles, and consumer needs. Let the architecture drive the tool selection, not the other way around. Run POCs against real workloads before committing.

## 8. Governance as an Afterthought

**Symptom:** "We'll add governance later." Data proliferates uncontrolled for 18 months. When governance finally arrives, it requires a multi-quarter cleanup effort and meets resistance from teams accustomed to full autonomy.

**Root cause:** Treating governance as a phase rather than a design constraint.

**Remediation:** Establish minimum viable governance from day one: data classification, ownership tagging, basic lineage. Add rigor incrementally as the platform matures. Governance that grows with the system is adopted; governance imposed after the fact is rejected.

## 9. Premature Petabyte

**Symptom:** Designing for "petabyte scale" when the organization has 2TB of data. Complex, expensive architecture that delivers no marginal benefit for years.

**Root cause:** Architects designing for resumes rather than actual problems. Future-proofing without understanding the cost of complexity.

**Remediation:** Design for 10x growth, not 1000x. Use architectures that scale horizontally without requiring upfront complexity. The cloud warehouse patterns (Snowflake, BigQuery) handle growth without premature optimization.

## 10. Streaming Everything

**Symptom:** Kafka for every data movement, even daily batch reports. Streaming infrastructure cost exceeds the value of real-time data.

**Root cause:** Assuming "real-time is better" without quantifying the latency requirement. Conflating event-driven architecture with streaming infrastructure.

**Remediation:** Require a concrete latency SLA before introducing streaming. If the business can tolerate 15-minute latency, micro-batch is sufficient. If it can tolerate hourly, batch is fine. Keep streaming infrastructure for the subset of pipelines that genuinely need sub-second delivery.

## 11. Copy-Paste FAANG Architecture

**Symptom:** Replicating the data infrastructure patterns of Google, Netflix, or Uber without accounting for your organization's actual scale, budget, team capability, or problem complexity.

**Root cause:** Assuming that what works at hyperscale is optimal at any scale. FAANG patterns evolved to solve FAANG-scale problems — not general problems.

**Remediation:** Choose the simplest architecture that meets your actual requirements. Managed services (Snowflake, BigQuery, Fivetran, dbt Cloud) are often the right choice for teams of 5-50, even if they wouldn't scale to FAANG levels. Complexity should be earned, not inherited.

## 12. Design by Committee

**Symptom:** Architecture that tries to accommodate every stakeholder's preference and ends up satisfying no one. Compromised designs that mix incompatible patterns.

**Root cause:** Architecture by consensus rather than by clear ownership and decision rights.

**Remediation:** Assign clear decision authority for architecture decisions. Solicit input from stakeholders, but the architect makes the final call with documented rationale. ADRs (Architecture Decision Records) make this explicit: "We considered X, Y, Z. We chose X because... The tradeoffs are..."

## 13. Neglecting the Team

**Symptom:** Designing a technically elegant system that the team cannot operate, troubleshoot, or extend. High "bus factor" on the architecture itself.

**Root cause:** Designing for technical purity rather than organizational reality.

**Remediation:** Factor in team size, skill level, and operational maturity. A simple architecture operated well is better than a clever architecture nobody understands. Build runbooks, invest in training, and design for debuggability.
