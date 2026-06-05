# Compliance by Framework — Data Architecture Implications

What major regulatory frameworks require from a data architecture perspective.
This is not legal advice — it's a guide to the **design implications** each framework creates.

## GDPR (General Data Protection Regulation) — EU

**Scope:** Personal data of EU residents, regardless of where the organization operates.

**Key architectural implications:**

- **Data inventory and mapping** — you must know what personal data you hold, where it came from, and who you share it with. Requires: automated data discovery and classification, data lineage tracking, data catalog
- **Right to erasure (Article 17)** — you must be able to delete an individual's data across all systems, including backups. Requires: cascading delete patterns, purging from archives, backup retention hygiene
- **Data minimization (Article 5)** — collect only what you need. Requires: schema design discipline, separate PII from analytics data, column-level access controls
- **Consent management** — track what data subjects consented to, and when. Requires: consent flag as metadata on customer records, integration between data platform and consent system
- **Data Protection Impact Assessment (Article 35)** — document high-risk processing. Requires: process metadata, data flow documentation, classification lineage
- **72-hour breach notification** — you must detect and report breaches. Requires: data access auditing, anomaly detection, automated alerting

**Design patterns:**
- PII/PHI tagging at column level in the data catalog
- Separate PII store from analytical data warehouse
- Data masking at query time (not at rest) for analytics access
- Immutable audit logs with retention policies
- Pseudonymization as a transformation step (replace PII with tokens before analytics)

## HIPAA (Health Insurance Portability and Accountability Act) — US Healthcare

**Scope:** Protected Health Information (PHI) of US patients.

**Key architectural implications:**

- **PHI must be encrypted at rest and in transit** — applies to databases, backups, data lakes, and data warehouse
- **Access controls (minimum necessary rule)** — RBAC at row and column level. Not just who can access a table, but who can see which rows and columns within it
- **Audit trails** — who accessed what PHI, when, and from where. Requires: access logging, immutable audit storage
- **Business Associate Agreements (BAAs)** — all vendors handling PHI must sign a BAA. Requires: vetting every tool in the data pipeline (warehouse, ETL tool, BI tool, catalog)
- **Data retention** — PHI must be retained per state and federal requirements, then securely destroyed
- **Breach notification** — 60 days to report breaches affecting 500+ individuals

**Design patterns:**
- Column-level encryption for sensitive PHI fields (SSN, diagnosis codes)
- Row-level security filters in the data warehouse (analyst sees only their department's patients)
- Separate de-identified data marts for analytics (no PHI)
- Logging pipeline that captures all queries against PHI tables
- Automated PHI detection and classification at ingestion

## CCPA/CPRA (California Consumer Privacy Act) — US California

**Scope:** Personal information of California residents. Broader definition of "personal information" than GDPR.

**Key architectural implications:**

- **Right to know** — what data you've collected about a consumer. Requires: data inventory, consumer-level data mapping
- **Right to delete** — similar to GDPR, with exceptions. Requires: purging consumer data across systems
- **Right to opt out of sale/sharing** — treats "sharing for cross-context behavioral advertising" as a sale. Requires: data sharing classification, consent metadata propagation
- **Non-discrimination** — can't penalize consumers for exercising rights. Requires: separation of operational data from consent data

**Design patterns:** Similar to GDPR, with additional attention to data sharing classification. Any data shared with third parties (advertising, analytics vendors) needs opt-out tracking.

## SOX (Sarbanes-Oxley Act) — US Public Companies

**Scope:** Financial reporting accuracy and controls for publicly traded US companies.

**Key architectural implications:**

- **Internal controls over financial reporting** — every data transformation that touches financial reports must be auditable and verifiable. Requires: immutable data lineage, version-controlled transformations
- **Data retention** — financial records must be retained for 7+ years. Requires: archival data storage with retrieval capabilities
- **Segregation of duties** — the person who enters data shouldn't be the person who approves the report. Requires: role-based access control, separation of data producer and data consumer roles
- **Full audit trail** — every change to financial data must be logged with who, what, when

**Design patterns:**
- Data Vault 2.0 (hub-link-satellite with load dates and record sources for every row)
- Immutable data lake (write-once, never modify)
- Version-controlled transformation code (dbt with git, CI/CD for data pipelines)
- Reconciliation processes between source systems and reporting layer

## PCI DSS (Payment Card Industry Data Security Standard)

**Scope:** Any organization handling credit card data.

**Key architectural implications:**

- **Cardholder data must be encrypted at rest and in transit** — full encryption everywhere
- **Access must be on a need-to-know basis** — strict RBAC, no shared credentials
- **Tokenization** — replace PAN (Primary Account Number) with tokens in analytics environments
- **Logging and monitoring** — all access to cardholder data must be logged
- **Segmentation** — cardholder data environment must be network-separated from non-cardholder systems

**Design patterns:**
- Tokenization at ingestion (PCI data never enters the analytics warehouse as raw card numbers)
- Separate data environment for PCI data with stricter controls
- Query-level monitoring for any access to token vault
- Automated masking for any UI/reporting layer

## BCBS 239 (Basel Committee) — Banking

**Scope:** Risk data aggregation and reporting for global systemically important banks.

**Key architectural implications:**

- **Data lineage** — full traceability from source to regulatory report. Every field in a regulatory return must trace to a source system field.
- **Data quality** — accuracy, completeness, timeliness must be demonstrated. Requires: data quality dashboards with formal metrics, automated quality checking
- **Data dictionary** — common definitions across the organization. Requires: business glossary with formal definitions, data ownership
- **Audit trail** — all data transformations must be auditable. Requires: version-controlled transformation, change data capture, immutable logs
- **IT resilience** — data architecture must support stress testing and recovery scenarios

**Design patterns:**
- Data Vault 2.0 (provides built-in auditability, source tracking, and flexibility for regulatory change)
- Formal data quality framework with automated scorecards
- Enterprise data catalog acting as the single source of definitions
- Reconciliation processes between source data warehouse → data mart → regulatory report

## General Architecture Principles for Compliance

1. **Design for auditability from day one.** Retrofitting audit trails is 10x harder than building them in.
2. **Separate sensitive data from analytics data.** Use de-identified data marts for BI; keep raw PII/PHI behind strict access controls.
3. **Automate compliance where possible.** Manual compliance processes fail at scale. Automate PII detection, data classification, lineage capture, and quality monitoring.
4. **Data retention is an architecture concern, not just a policy.** If you can't enforce retention at the storage layer, it won't happen consistently.
5. **Access controls must be granular enough for minimum necessary access.** Table-level access is not sufficient for HIPAA or GDPR (need column and row level).
6. **Data catalogs are compliance infrastructure.** Without knowing what data you have and where it lives, you cannot comply with any framework's inventory requirements.

## Industry-to-Framework Quick Reference

Use this table when someone asks "what compliance frameworks apply to us?"

| Industry | Likely Frameworks | Primary Architectural Impact |
|---|---|---|
| Healthcare (US) | HIPAA, GDPR (if EU patients), CCPA (if CA patients) | PHI encryption, row/column-level access controls, BAAs with every vendor, de-identified analytics marts |
| Financial services (US public) | SOX, PCI DSS (if cards), BCBS 239 (if systemic bank) | Immutable audit trails, 7-year retention, Data Vault for lineage, segregation of duties |
| Financial services (EU) | GDPR, PSD2, BCBS 239 | Consent management, data minimization, lineage for regulatory reporting |
| E-commerce / retail | CCPA (if CA customers), GDPR (if EU customers), PCI DSS | PII classification, data sharing opt-out tracking, tokenization |
| SaaS / technology | GDPR, CCPA, SOC 2 (voluntary) | Data inventory, right to erasure, data processing agreements |
| Insurance | HIPAA (if health), SOX (if public), GDPR, CCPA | Multiple frameworks simultaneously — layered compliance architecture |
| Government / defense | FedRAMP, ITAR, GDPR (if EU citizens) | Data residency controls, classification markings, strict access segmentation |
| Any B2B (global) | GDPR (EU customer data applies extraterritorially) | PII discovery, data mapping, consent tracking — even if not EU-based |

**If the answer is "we're not sure":** Start with a data inventory and classification. You can't determine which frameworks apply until you know what data you hold, where it lives, and who your data subjects are. The data catalog isn't just compliance infrastructure — it's how you scope your compliance obligations.
