# Regulatory Analysis — GDPR, CCPA, AI Act

## General Data Protection Regulation (GDPR)

### Scope & Applicability

| Aspect | Detail |
|--------|--------|
| **Enforcement** | May 25, 2018 |
| **Territorial scope** | EU establishment; OR targeting/monitoring data subjects in the EU (Article 3) |
| **Material scope** | Personal data processed wholly or partly by automated means (Article 2) |
| **Penalties** | Up to €20M or 4% of global annual turnover, whichever is higher |

### Key Principles (Article 5)

1. **Lawfulness, fairness, transparency** — Must have a lawful basis; be clear about how data is used
2. **Purpose limitation** — Collect for specified, explicit, legitimate purposes; don't repurpose
3. **Data minimization** — Collect only what's necessary for the stated purpose
4. **Accuracy** — Keep data accurate and up to date; rectify inaccuracies
5. **Storage limitation** — Keep only as long as necessary for the purpose
6. **Integrity and confidentiality** — Appropriate security measures
7. **Accountability** — Must be able to demonstrate compliance with all principles

### Lawful Bases for Processing (Article 6)

| Basis | Description | Best for |
|-------|-------------|----------|
| **Consent** | Freely given, specific, informed, unambiguous | Marketing, non-essential cookies |
| **Contract** | Necessary to fulfill a contract with the data subject | Order processing, account management |
| **Legal obligation** | Required by law | Tax reporting, fraud prevention |
| **Vital interests** | Necessary to protect someone's life | Emergency medical data |
| **Public interest** | Official authority or public task | Government services |
| **Legitimate interests** | Balanced against data subject's rights | Analytics, security (not public authorities) |

### Data Subject Rights

| Right | Description | Response timeline |
|-------|-------------|------------------|
| **Right to be informed** | Privacy notice at collection point | At time of collection |
| **Right of access** | Copy of personal data and processing info | 1 month (extendable to 2) |
| **Right to rectification** | Correct inaccurate data | 1 month |
| **Right to erasure** ("Right to be forgotten") | Delete personal data | 1 month (with exceptions) |
| **Right to restrict processing** | Limit how data is used | 1 month |
| **Right to data portability** | Receive data in machine-readable format | 1 month |
| **Right to object** | Object to processing (including profiling/marketing) | Without undue delay |
| **Rights related to automated decision-making** | Not be subject to solely automated decisions with legal effects | N/A |

## California Consumer Privacy Act (CCPA / CPRA)

### Scope

Applies to for-profit businesses that:
- Gross annual revenue >$25M; OR
- Buy, sell, or share personal data of 100,000+ California residents/year; OR
- Derive 50%+ of revenue from selling/sharing personal data

### Consumer Rights

- **Right to know** — Categories and specific pieces of personal data collected, sources, purpose, third parties
- **Right to delete** — Subject to exceptions (complete transaction, security, legal compliance)
- **Right to opt out** — Of sale or sharing of personal data (includes cross-context behavioral advertising)
- **Right to correct** — Inaccurate personal data
- **Right to limit** — Use of sensitive personal data
- **Right to non-discrimination** — No retaliation for exercising rights

## EU AI Act

### Risk Categories

| Category | Examples | Requirements |
|----------|----------|--------------|
| **Unacceptable risk** (banned) | Social scoring, real-time biometric surveillance, manipulative AI | Prohibited entirely |
| **High risk** | Critical infrastructure, education, employment, law enforcement, migration, justice | Conformity assessment, risk management, human oversight, transparency, accuracy, cybersecurity |
| **Limited risk** | Chatbots, AI-generated content | Transparency obligations (disclose AI interaction) |
| **Minimal risk** | AI-enabled video games, spam filters | No additional obligations (voluntary codes of conduct) |

### High-Risk System Requirements

1. **Risk management system** — Continuous, iterative process throughout lifecycle
2. **Data governance** — Training, validation, and testing data must be relevant, representative, and free from biases
3. **Technical documentation** — Design specifications, development methodology, accuracy/robustness benchmarks
4. **Record-keeping** — Automatic logging of events during operation
5. **Transparency** — Clear disclosure to users
6. **Human oversight** — Appropriate for the risk level
7. **Accuracy, robustness, cybersecurity** — Appropriate levels of each

### Penalties

| Violation | Penalty |
|-----------|---------|
| Unacceptable risk practices | €35M or 7% of global annual turnover |
| Non-compliance with high-risk obligations | €15M or 3% of global annual turnover |
| Providing incorrect information | €7.5M or 1% of global annual turnover |

## Sector-Specific Regulations

### Healthcare (US — HIPAA)

- Protected Health Information (PHI) — 18 identifiers
- Privacy Rule — Use/disclosure limits
- Security Rule — Administrative, physical, technical safeguards
- Breach Notification Rule — 60-day notification requirement

### Financial Services (US — SOX, GLBA)

- **SOX** — Internal controls over financial reporting, records retention (7 years), CEO/CFO certification
- **GLBA** — Financial Privacy Rule, Safeguards Rule, Pretexting Protection
- **PCI DSS** — Payment card data security (not law, but contractual requirement)

### Children's Privacy

- **COPPA (US)** — Under 13: verifiable parental consent, privacy policy, data minimization
- **GDPR Art. 8** — Under 16 (varies by member state down to 13): parental consent

## Cross-Border Data Transfers

| Mechanism | GDPR | Notes |
|-----------|------|-------|
| Adequacy decision | EU deems country's protections adequate | UK, Japan, South Korea, others |
| Standard Contractual Clauses (SCCs) | EU Commission-approved contracts | Most common mechanism |
| Binding Corporate Rules (BCRs) | Multi-national group policies | Complex to implement |
| Derogations | Specific situations (consent, contract necessity) | Limited use — not a long-term solution |
