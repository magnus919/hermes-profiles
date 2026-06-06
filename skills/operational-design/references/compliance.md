# Compliance and Audit Frameworks

Compliance is a system, not a project. It requires embedded controls, continuous monitoring, and periodic testing. The frameworks below cover the most common compliance regimes for SaaS and technology companies.

## SOC 2

SOC 2 (System and Organization Controls 2) is the most common compliance framework for SaaS companies. It reports on controls related to security, availability, processing integrity, confidentiality, and privacy.

### Trust Services Criteria (TSC)

| Category | Criteria | What It Covers |
|----------|----------|---------------|
| **Security** | CC1-CC9 | The system is protected against unauthorized access. The foundational criteria that everyone must meet. |
| **Availability** | A1 | The system is available for operation and use as committed or agreed. |
| **Processing Integrity** | PI1 | System processing is complete, valid, accurate, timely, and authorized. |
| **Confidentiality** | C1 | Information designated as confidential is protected. |
| **Privacy** | P1-P4 | Personal information is collected, used, retained, disclosed, and disposed in conformity with commitments. |

### SOC 2 Report Types

| Type | Description | When to Get It |
|------|-------------|----------------|
| **Type I** | Controls are designed properly at a point in time | First audit, getting started |
| **Type II** | Controls operated effectively over a period (typically 6-12 months) | Customer demands, vendor due diligence |

### Key Controls by Domain

**Security (CC1-CC9):**
- Access control policy and enforcement
- Logical access reviews (quarterly)
- Change management process
- Incident response plan and testing
- Vendor risk management
- Encryption at rest and in transit
- Physical security (office/data center)
- Monitoring and alerting
- Background checks
- Security awareness training

**Availability (A1):**
- Uptime SLAs and monitoring
- Business continuity / disaster recovery plan
- Backup and restore testing
- Capacity planning

**Processing Integrity (PI1):**
- Input validation controls
- Error handling and corrective action
- Batch job monitoring

**Confidentiality (C1):**
- Data classification policy
- Access restrictions on confidential data
- Data retention and disposal

### SOC 2 Readiness Checklist

| Phase | Activities | Timeline |
|-------|-----------|----------|
| **Scoping** | Define system boundaries, identify in-scope services and data | 2-4 weeks |
| **Risk Assessment** | Identify risks to TSC criteria, document control objectives | 2-4 weeks |
| **Control Design** | Document existing controls, design new controls for gaps | 4-8 weeks |
| **Control Implementation** | Build and deploy controls, update policies | 4-12 weeks |
| **Evidence Collection** | Run controls, collect audit evidence | 3-6 months (Type II) |
| **Audit** | External auditor reviews controls and evidence | 4-8 weeks |

---

## ISO 27001

An international standard for Information Security Management Systems (ISMS). Broader than SOC 2 — requires a management system, not just controls.

### The ISO 27001 Approach

| Component | Description |
|-----------|-------------|
| **ISMS** | A systematic approach to managing sensitive information |
| **Annex A Controls** | 93 controls across 4 domains (organizational, people, physical, technological) |
| **PDCA Cycle** | Plan-Do-Check-Act continuous improvement |
| **Risk Assessment** | Risk-based approach — controls are selected based on risk, not checklist |
| **Statement of Applicability** | Which Annex A controls apply and why |

### ISO 27001 vs SOC 2

| Dimension | SOC 2 | ISO 27001 |
|-----------|-------|-----------|
| Focus | Controls effectiveness | Management system |
| Flexibility | Fixed TSC criteria | Risk-based, choose your controls |
| Certification | Auditor's opinion letter | Certificate issued |
| Recognition | US-focused | International |
| Renewal | Annual | Three-year certification + surveillance audits |

### Key Requirements

1. **ISMS Scope** — What's included and excluded, with justification
2. **Information Security Policy** — Top-level policy, reviewed annually
3. **Risk Assessment** — Systematic risk assessment methodology
4. **Risk Treatment Plan** — How risks will be addressed
5. **Internal Audit** — Regular internal audits of the ISMS
6. **Management Review** — Top management reviews ISMS performance
7. **Continuous Improvement** — Non-conformities are tracked and resolved

---

## GDPR Readiness

The General Data Protection Regulation governs how personal data of EU residents is handled, regardless of where the company is based.

### Key Principles

| Principle | Requirement |
|-----------|-------------|
| **Lawfulness, fairness, transparency** | Legal basis for processing, clear privacy notices |
| **Purpose limitation** | Data collected for specified, explicit purposes only |
| **Data minimization** | Collect only what's necessary |
| **Accuracy** | Keep data accurate and up to date |
| **Storage limitation** | Delete data when no longer needed |
| **Integrity and confidentiality** | Appropriate security measures |
| **Accountability** | Demonstrate compliance (documentation, DPO, records) |

### Data Subject Rights

| Right | Description | Response Time |
|-------|-------------|---------------|
| **Right to be informed** | Privacy notice at collection point | At collection |
| **Right of access** | Individuals can request their data | 30 days |
| **Right to rectification** | Correct inaccurate data | 30 days |
| **Right to erasure** ("Right to be forgotten") | Delete personal data | 30 days |
| **Right to restrict processing** | Limit how data is used | 30 days |
| **Right to data portability** | Export data in machine-readable format | 30 days |
| **Right to object** | Opt out of processing (including marketing) | At any time |
| **Rights related to automated decision-making** | Explanation of algo-based decisions | Upon request |

### GDPR Compliance Roadmap

| Phase | Activities | Timeline |
|-------|-----------|----------|
| **Discovery** | Data mapping, identify all personal data processing | 4-8 weeks |
| **Gap Analysis** | Current state vs GDPR requirements | 2-4 weeks |
| **Remediation** | Update policies, implement controls, update contracts | 8-16 weeks |
| **Implementation** | DPO appointment, privacy notices, consent management | 4-8 weeks |
| **Ongoing** | DSAR handling process, breach notification procedure, annual review | Continuous |

### GDPR Breach Notification

```
Under GDPR, a breach must be reported to the supervisory authority
within 72 hours of becoming aware of it.

If the breach is likely to result in high risk to individuals,
they must also be informed without undue delay.
```

---

## Common Compliance Pitfalls

| Pitfall | Symptom | Fix |
|---------|---------|-----|
| **Compliance once, not continuous** | Controls atrophy between audits | Build continuous monitoring, automate evidence collection |
| **Documentation but not implementation** | Policies exist but aren't followed | Test controls, not just documentation |
| **Scope creep** | Trying to cover everything at once | Start narrow, expand scope over time |
| **No executive ownership** | Compliance is delegated to IT without business support | Assign executive sponsor, report compliance at board level |
| **Vendor blind spot** | Vendors have access to your data but no compliance validation | Vendor risk management program, contract reviews |
| **Over-relying on automation** | Tools replace thinking | Automation supports controls, doesn't replace judgment |

### Evidence Collection Strategy

| Evidence Type | Examples | Collection Method |
|---------------|----------|-------------------|
| **System logs** | Access logs, change logs, audit trails | Automated log aggregation |
| **Configuration** | IAM policies, encryption settings | Infrastructure-as-code, CI/CD |
| **Process artifacts** | Signed forms, approved change requests | Document management system |
| **Training records** | Completed security training | LMS reports |
| **Review evidence** | Access review sign-offs | Quarterly automated workflow |
| **Testing results** | Penetration test reports, DR test results | Scheduled external testing |
