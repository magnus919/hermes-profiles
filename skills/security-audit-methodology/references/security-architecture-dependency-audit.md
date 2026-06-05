# Security Architecture Review & Dependency Audit Methodology Reference

> A practical reference for security engineers evaluating authentication, authorization,
> secrets management, and software supply chain security in modern systems.
>
> Compiled June 2026.

---

## Table of Contents

1. [Authentication Architecture](#1-authentication-architecture)
   - [OAuth 2.0 & OAuth 2.1 Flows](#11-oauth-20--oauth-21-flows)
   - [OpenID Connect (OIDC)](#12-openid-connect-oidc)
   - [SAML 2.0](#13-saml-20)
   - [API Keys](#14-api-keys)
   - [Mutual TLS (mTLS)](#15-mutual-tls-mtls)
   - [Authentication Review Checklist](#16-authentication-review-checklist)
2. [Session Management](#2-session-management)
   - [Server-Side Sessions](#21-server-side-sessions)
   - [JWT-Based Sessions](#22-jwt-based-sessions)
   - [Session Security Patterns](#23-session-security-patterns)
3. [Authorization Models](#3-authorization-models)
   - [RBAC (Role-Based Access Control)](#31-rbac-role-based-access-control)
   - [ABAC (Attribute-Based Access Control)](#32-abac-attribute-based-access-control)
   - [ReBAC (Relationship-Based Access Control)](#33-rebac-relationship-based-access-control)
   - [Authorization Comparison & Review](#34-authorization-comparison--review)
4. [Secrets Management Architecture](#4-secrets-management-architecture)
   - [Centralized Secrets Stores](#41-centralized-secrets-stores)
   - [Secret Types & Lifecycle](#42-secret-types--lifecycle)
   - [Secrets Management Review Patterns](#43-secrets-management-review-patterns)
5. [Dependency Audit & Supply Chain Security](#5-dependency-audit--supply-chain-security)
   - [SBOM Generation (CycloneDX & SPDX)](#51-sbom-generation-cyclonedx--spdx)
   - [CVE Matching & Severity Triage](#52-cve-matching--severity-triage)
   - [License Compatibility Analysis](#53-license-compatibility-analysis)
   - [Supply Chain Attack Patterns](#54-supply-chain-attack-patterns)
   - [SLSA Framework](#55-slsa-framework)
   - [Dependency Audit Review Checklist](#56-dependency-audit-review-checklist)

---

## 1. Authentication Architecture

Authentication is the process of verifying identity. A security review must examine
each authentication mechanism present in the system, its configuration, and its
integration points.

### 1.1 OAuth 2.0 & OAuth 2.1 Flows

OAuth 2.0 (RFC 6749) is the industry-standard delegation protocol. OAuth 2.1
consolidates years of security best practices into a single specification.

**Core Flows & Review Considerations:**

| Flow | Use Case | Security Profile | Review Focus |
|------|----------|-----------------|--------------|
| **Authorization Code** | Web apps, server-side | Best; token never in browser | Must use PKCE; verify `redirect_uri` exact match; confirm authorization code is single-use, short-lived (<10 min) |
| **Authorization Code + PKCE** | Mobile, SPAs, all apps | Strongest public-client flow | Mandatory in OAuth 2.1. Verify `code_challenge_method` = S256 (not `plain`); replay protection on code verifier |
| **Client Credentials** | Machine-to-machine | No user context; server-side only | Verify client secret rotation; scope least-privilege; no human UI interaction |
| **Device Authorization** | CLI tools, IoT, smart TVs | High phishing surface | Watch for polling abuse (min 5s interval); verify user_code entropy; confirm user_code expiration |
| **Resource Owner Password** | Legacy / high-trust only | Deprecated in OAuth 2.1. | Avoid unless migration path exists; requires direct credential exposure |
| **Implicit (deprecated)** | — | Removed in OAuth 2.1. | Migrate to Authorization Code + PKCE |

**OAuth 2.1 Key Changes (security-driven):**
- Eliminates the Implicit flow entirely.
- Mandates PKCE for all Authorization Code exchanges.
- Requires exact redirect URI matching (no pattern matching).
- Removes the Resource Owner Password Credentials grant.
- Requires refresh token rotation and sender-constrained access tokens.

**IETF OAuth Security Best Current Practice (draft):**
- JWT-Secured Authorization Request (JAR): Signs/encrypts the authorization request
  to prevent tampering.
- JWT-Secured Authorization Response Mode (JARM): Encrypts the authorization response.
- Token binding / DPoP (Demonstration of Proof-of-Possession) binds tokens to client
  key pairs, preventing replay by intermediates.
- Authorization server MUST validate all inputs; MUST enforce TLS 1.2+ exclusively.

**Review Checklist for OAuth 2.0:**
- [ ] Is PKCE enforced for all public clients?
- [ ] Are redirect URIs validated as exact strings (not patterns)?
- [ ] Are authorization codes single-use and short-lived (< 10 minutes)?
- [ ] Are access tokens and refresh tokens sender-constrained or rotated?
- [ ] Is the Client Credentials grant scoped to the minimum necessary?
- [ ] Is the Resource Owner Password grant absent or in documented legacy-only use?
- [ ] Is TLS 1.2+ mandatory at all endpoints?
- [ ] Are client secrets stored as hashed values (not plaintext) in the auth server?
- [ ] Is the Implicit flow absent?
- [ ] Is there rate-limiting on token endpoints?

### 1.2 OpenID Connect (OIDC)

OIDC adds an identity/authentication layer on top of OAuth 2.0. OIDC is the
recommended SSO protocol for modern applications.

**Core Concepts:**

| Element | Description | Review Notes |
|---------|-------------|--------------|
| **ID Token** | JWT that proves authentication | Validate the `iss`, `aud`, `azp`, `exp`, `iat`, `nonce` |
| **UserInfo Endpoint** | Claims endpoint behind access token | Must be TLS; verify scope authorization |
| **Discovery URL** | `/.well-known/openid-configuration` | Verify against known provider metadata |
| **Claims** | `sub`, `email`, `name`, etc. | Define required claims; avoid over-scoping `openid` scope |
| **Prompt Parameter** | `login`, `consent`, `select_account`, `none` | Abuse of `prompt=none` enables session probing |

**Security Review for OIDC Implementations:**

**ID Token Validation Rules (per OIDC Core Spec):**
1. MUST validate the `iss` (issuer) matches the expected provider.
2. MUST validate the `aud` (audience) includes this client's `client_id`.
3. MUST validate `exp` (expiration) is in the past relative to current time.
4. MUST validate `iat` (issued-at) is reasonable (not future-dated).
5. MUST validate `nonce` matches the one sent in the authentication request
   (prevents replay).
6. `azp` (authorized party) must be checked when the token is issued to multiple
   audiences.
7. If using `alg=RS256` (recommended), verify the signature against the provider's
   JWKS endpoint.
8. Reject `alg=none` or `alg=HS256` (symmetric) unless the client controls the
   symmetric key.

**OIDC Logout (RP-Initiated):**
- Verify `id_token_hint` parameter is validated.
- Post-logout redirect URIs must be pre-registered.
- Session management (session management / iframe-based) should use `sid` claim.

**OIDC Threat Vectors to Review:**
- **Malicious Relying Party:** A rogue client intercepting authorization codes.
- **Cross-Site Request Forgery (CSRF):** Mitigated by `nonce` and `state` parameters.
- **Token Substitution:** Swapping an ID token from one client to another (mitigated
  by `aud` and `azp` checks).
- **Mix-Up Attack:** Attacker redirects a victim's browser to a different client's
  redirect URI (mitigated by `redirect_uri` exact validation).

### 1.3 SAML 2.0

Security Assertion Markup Language (SAML) 2.0 is the XML-based SSO protocol
predominantly used in enterprise environments (Okta, Azure AD, ADFS, Ping).

**Core Artifacts:**

| Component | Description | Review Focus |
|-----------|-------------|--------------|
| **Identity Provider (IdP)** | Authenticates user; issues assertions | Verify signature validation; clock skew tolerance |
| **Service Provider (SP)** | Consumes assertions to grant access | Confirm Assertion Consumer Service (ACS) URL whitelist |
| **Assertion** | XML token containing `Subject`, `Conditions`, `AuthnStatement`, `AttributeStatement` | Validate `NotBefore`, `NotOnOrAfter`, `AudienceRestriction` |
| **Metadata XML** | Exchange of certificates, endpoints, bindings | Verify XML signature; watch for unsigned metadata |

**Bindings:**
- **HTTP Redirect:** Assertion in URL query; must be signed (default, but verify).
- **HTTP POST:** Assertion in POST body; most common; must be encrypted+ signed.
- **Artifact Resolution:** IdP returns short artifact; SP resolves to full assertion;
  good for large assertions but adds a network round-trip.

**SAML Security Pitfalls to Review:**
1. **XML Signature Wrapping (XSW):** Attackers modify the SAML message structure
   while keeping the signature valid. Verify the signed element matches the
   consumed element.
2. **Missing `AudienceRestriction`:** Without it, an assertion for one SP can be
   replayed to another SP.
3. **Long `NotOnOrAfter`:** Permits replay attacks hours after issue.
4. **Unencrypted Assertions:** Sensitive attributes (SSN, roles) should be encrypted.
5. **Improper Assertion Consumer Service (ACS) Validation:** Only pre-registered
   ACS URLs should be accepted.

**SAML vs OIDC — When to Use Each:**
- Choose OIDC for: mobile apps, SPAs, APIs, cloud-native, consumer-facing, modern stacks.
- Choose SAML for: enterprise federation, legacy systems, government/certification
  requirements, complex attribute exchange.

### 1.4 API Keys

API keys are static bearer tokens used for programmatic access. They are the
weakest form of authentication and require compensating controls.

**Security Concerns:**
- **Long-lived by nature:** Keys often have no expiration.
- **Hard-coded in code:** Frequently committed to version control.
- **No identity binding:** Any bearer of the key is treated as the authentic entity.
- **Difficult to rotate:** Clients must update configurations.
- **No granular scoping:** Often grant blanket access.

**API Key Review Checklist:**
- [ ] Are keys unique per client/application (not shared across clients)?
- [ ] Do keys have an expiration / rotation policy (90 days max recommended)?
- [ ] Are keys stored as hashes (bcrypt/argon2) in the database, not plaintext?
- [ ] Is there a revocation mechanism that takes effect in < 5 minutes?
- [ ] Is key usage logged and monitored for anomalous patterns?
- [ ] Is the key exposed only via TLS 1.2+ (never in URL query strings)?
- [ ] Are keys scoped to the minimum set of resources/actions?
- [ ] Is there a rate-limit per key?
- [ ] Are keys excluded from source code (via `.env`, secrets manager, or vault)?
- [ ] Is there a "show once on creation" UX pattern?

**Better alternatives:** OAuth 2.0 Client Credentials (machine-to-machine) with
short-lived JWTs rotated via refresh.

### 1.5 Mutual TLS (mTLS)

mTLS extends TLS to authenticate both sides of the connection using X.509
certificates. It is foundational in zero-trust and service-mesh architectures.

**Architecture Patterns:**

| Pattern | Description | When to Use |
|---------|-------------|-------------|
| **Strict mTLS** | Both client and server present certs; mutual validation. | East-west service communication; API gateways. |
| **Permissive mTLS** | Server requests but does not require client cert. | Gradual mTLS adoption; monitoring path. |
| **mTLS + SPIFFE** | SPIFFE IDs embedded in X.509 SAN as workload identity. | Service mesh (Istio, Linkerd, Consul Connect, Cilium). |

**Implementation Review Points:**
- **Certificate Authority (CA) trust model:** Which CAs are trusted? Are there
  private CAs with dedicated PKI?
- **Certificate lifecycle:** Rotation interval (recommended: 24h-72h for short-lived
  SPIFFE certs; 30-90 days for traditional); revocation via CRL or OCSP.
- **Certificate validation depth:** Verify hostname matching against SAN, not CN.
- **Client certificate subject identity:** Use a unique identity (SPIFFE ID or
  service account name) in the Subject or SAN.
- **mTLS termination:** At ingress gateway? Sidecar proxy? Application layer?
- **mTLS passthrough vs re-encryption:** Passthrough preserves end-to-end identity;
  re-encryption loses client identity at the proxy.

**mTLS Security Review Checklist:**
- [ ] Are client certificates bound to workload/service identities (not human users)?
- [ ] Is there a documented PKI with CA hierarchy?
- [ ] Is certificate revocation testing performed?
- [ ] Are short-lived certificates used (< 72h for service mesh)?
- [ ] Is the mTLS handshake logged for audit?
- [ ] Are fallback (non-mTLS) paths explicitly disabled in production?
- [ ] Is client certificate verification enforced at the application level (not just
      the proxy)?

### 1.6 Authentication Review Checklist (Aggregate)

- [ ] All authentication mechanisms require TLS 1.2+.
- [ ] No deprecated/broken algorithms (SHA-1 signings, `alg=none`) in use.
- [ ] All secrets (keys, passwords, tokens) are hashed at rest (bcrypt/argon2/scrypt).
- [ ] Rate-limiting on authentication endpoints (login, token, password reset).
- [ ] Account lockout or progressive delay on failed attempts.
- [ ] Multi-factor authentication available (ideally enforced) for human users.
- [ ] Authentication failure logging with correlation IDs.
- [ ] No vertical privilege escalation through modified authentication claims.
- [ ] Credential stuffing protections (CAPTCHA, device fingerprint, risk scoring).

---

## 2. Session Management

Session management controls how an authenticated user's state is maintained across
requests. The two dominant patterns are server-side sessions (opaque session IDs)
and JWT-based sessions (self-contained tokens).

### 2.1 Server-Side Sessions

Identity stored server-side; client holds a random opaque session ID (typically
a cookie).

**Review Checklist:**
- [ ] Session IDs are cryptographically random (>= 128 bits of entropy, CSPRNG-generated).
- [ ] Session IDs are single-use (reissued on login, privilege escalation).
- [ ] Session ID is never in URLs (secure cookie with `HttpOnly`, `Secure`, `SameSite`,
      and `Path` attributes set).
- [ ] Session expiration: absolute timeout (e.g., 8 hours) + idle timeout (e.g., 30 min).
- [ ] Session data stored securely (encrypted at rest in Redis/DB/database).
- [ ] Logout invalidates the server-side session immediately.
- [ ] Password changes invalidate all existing sessions.
- [ ] Session fixation protection (regenerate ID on authentication).
- [ ] Binding session ID to a client fingerprint (IP, User-Agent, TLS session) as
      a secondary check.

### 2.2 JWT-Based Sessions

Identity and claims encoded in a signed/encrypted JWT, stored client-side (cookie
or Authorization header).

**Review Checklist:**
- [ ] JWT is signed with a strong algorithm (RS256, ES256, EdDSA — never `none`
      or HS256 with a leaked public key).
- [ ] `exp` claim is set and validated (short-lived: 5-15 min for access tokens).
- [ ] `nbf` claim (not-before) validated to reject prematurely valid tokens.
- [ ] Signature validated using a trusted JWKS endpoint.
- [ ] Access tokens are NOT stored in browser `localStorage` (prefer `httpOnly`
      cookies + CSRF tokens, or in-memory for SPAs).
- [ ] Refresh tokens are stored separately, rotated with each use, and have
      additional validation (binding to client ID or TLS fingerprint).
- [ ] Refresh token rotation with revocation of the previous refresh token
      (prevents refresh token theft persistence).
- [ ] JWT does NOT contain sensitive PII in the header or payload (JWT payloads
      are base64-encoded, not encrypted, unless JWE is used).
- [ ] JWT `jti` (JWT ID) claim used for single-use detection.
- [ ] Server-side allowlist/blocklist for high-value operations.

**Common JWT Attacks to Review For:**
- **alg=none injection:** Server must reject tokens with `"alg":"none"`.
- **Key confusion (RS256 -> HS256):** If public key is leaked, attacker signs with
  HS256 and public key as secret. Mitigation: strict algorithm validation.
- **JWK injection:** Token supplies its own public key. Mitigation: validate JWK
  against trusted JWKS, or reject JWK in header.
- **Token replay:** Short TTL, DPoP binding, or token binding.
- **Timing attacks on signature verification:** Use constant-time comparison.

### 2.3 Session Security Patterns

| Pattern | Purpose | Implementation Concern |
|---------|---------|----------------------|
| **Short-lived access tokens + refresh tokens** | Balance security with UX | Refresh token rotation must be atomic |
| **Refresh token rotation** | Prevent replay of stolen refresh tokens | Concurrent requests can invalidate legitimate tokens (use family-based rotation) |
| **Refresh token reuse detection** | Detect theft | On reuse of a rotated refresh token, invalidate entire refresh token family |
| **Session binding** | Tie session to client attributes | Avoid excessive IP binding (mobile users change networks) |
| **Concurrent session limits** | Restrict session proliferation | Must be configurable per user/role |
| **Idle timeout** | Auto-expire inactive sessions | Match to sensitivity of accessed data |
| **Absolute session timeout** | Force periodic re-authentication | 8-24 hours typical for web apps |
| **Session revocation** | Admin/forced logout | Must propagate to all active sessions instantly |

---

## 3. Authorization Models

Authorization determines what an authenticated identity can do. The three primary
models — RBAC, ABAC, and ReBAC — each have different complexity, scalability, and
security characteristics.

### 3.1 RBAC (Role-Based Access Control)

Users are assigned roles; roles are granted permissions.

**Structure:** `User -> Role(s) -> Permission(s)`

**When RBAC Works Well:**
- Organizations with stable, well-defined job functions.
- Systems with coarse-grained permission needs (standard employee, manager, admin).
- Auditing and compliance environments (SOX, HIPAA).

**RBAC Review Checklist:**
- [ ] Roles follow the principle of least privilege (no users with unnecessary roles).
- [ ] No role explosion: if there are more roles than users, the model is broken.
- [ ] Role hierarchy is documented and restricted (no deep inheritance chains).
- [ ] Separation of duties enforced (e.g., same user cannot be both "approver" and
      "requester").
- [ ] Role assignments are approved, audited, and time-bound where possible.
- [ ] Default "deny" — no implicit permissions through role absence.
- [ ] Static vs. dynamic roles documented.

**Common RBAC Anti-Patterns:**
- **Super-admin role assigned to everyone:** Defeats RBAC entirely.
- **Role creep:** Accumulated roles across user transfers never removed.
- **Hundreds of roles:** Leads to configuration errors; consider ABAC if this occurs.
- **Permission duplication across roles:** Indicates missing abstract role.

### 3.2 ABAC (Attribute-Based Access Control)

Access decisions use policies that evaluate attributes of the user, resource,
action, and environment.

**Structure:** `Policy(user.attr, resource.attr, action, context) -> Permit/Deny`

**Attribute Sources:**
- **Subject attributes:** department, clearance level, location, employment type.
- **Resource attributes:** classification, owner, sensitivity, project.
- **Action attributes:** read, write, delete, share, export.
- **Environment attributes:** time of day, IP range, device compliance, risk score.

**ABAC Review Checklist:**
- [ ] Policy engine is externalized (e.g., OPA, OpenFGA, Cedar, Oso) — not
      hard-coded in application business logic.
- [ ] Policies are version-controlled and tested.
- [ ] Attribute values are trusted (validated at ingestion, not from user input).
- [ ] Policy evaluation is performant (< 10ms per decision).
- [ ] Caching strategy does not permit stale/cached decisions after attribute changes.
- [ ] Deny overrides: explicit deny always overrides allow.
- [ ] Attribute aggregation across multiple sources is deterministic (if sources
      disagree, which wins?).
- [ ] Policies use Rego (OPA), Cedar, or similar declarative language with formal
      semantics.

**Common ABAC Pitfalls:**
- **Policy complexity explosion:** Too many policies become un-auditable.
- **Attribute sprawl:** Every microservice adds its own attributes.
- **Latency:** Attribute retrieval from multiple backends at request time.
- **Implicit consent:** Using attributes the user never explicitly provided.

### 3.3 ReBAC (Relationship-Based Access Control)

Access is determined by the relationships between entities in a graph. Popularized
by Google Zanzibar and implemented in OpenFGA, SpiceDB, and Keto.

**Structure:** `User --[relation]--> Object` e.g., `alice --[member]--> org:acme`

**Key Concepts:**
- **Objects** (resources) arranged in a hierarchy (e.g., Org > Workspace > Doc).
- **Relations** define how objects connect (owner, editor, viewer, parent).
- **Usersets** represent all users with a given relation on an object.
- **Direct and indirect relationships** (transitive closure through the graph).

**When ReBAC Excels:**
- Multi-tenant systems with hierarchical resources (Google Drive, GitHub, Notion).
- Systems where sharing and collaboration are core features.
- Organizational hierarchies with inherited permissions.

**ReBAC Review Checklist:**
- [ ] Relationship graph is stored in a dedicated system (not application database).
- [ ] Tuples are checked, not computed: "check" is a graph traversal, not a role lookup.
- [ ] Consistency model is documented (Zanzibar uses eventual consistency with
      "caveats" for critical paths).
- [ ] Maximum graph traversal depth is bounded (prevent infinite loops).
- [ ] Relation tuples are immutable/append-only to enable audit trails.
- [ ] Public access (unauthenticated) is explicitly modeled as `*` userset.
- [ ] Negative relationships (block, revoke) override positive paths.
- [ ] Cross-object relationship references are validated at write time.

**Zanzibar-Inspired Implementation Patterns:**
- **Check:** "Is user X allowed relation Y on object Z?" — graph traversal.
- **Expand:** "Who has relation Y on object Z?" — return all users/usersets.
- **Read:** "What relations does user X have on object Z?"
- **Write:** Tuple mutations with transaction support.
- **Watch:** Change data capture for relationship events.

### 3.4 Authorization Comparison & Review

| Criterion | RBAC | ABAC | ReBAC |
|-----------|------|------|-------|
| **Conceptual complexity** | Low | High | Medium |
| **Policy granularity** | Coarse (role-level) | Fine (any attribute) | Fine (relationship paths) |
| **Change overhead** | Role reassignment needed | Policy update only | Tuple mutation only |
| **Audit trail** | Role assignment history | Policy + attribute history | Relationship tuple history |
| **Performance** | Fast (lookup table) | Variable (policy evaluation) | Variable (graph traversal depth) |
| **Best for** | Stable org structures | Dynamic, context-sensitive | Hierarchical, shared resources |
| **Worst for** | Fine-grained, orgs with role explosion | Simple CRUD apps | Non-relational flat resources |

**Authorization Security Review — Cross-Cutting:**
- [ ] Every access request goes through a central policy decision point (PDP).
- [ ] Default deny — any request not explicitly permitted is denied.
- [ ] Authorization failures log: user ID, resource, action, deny reason, timestamp.
- [ ] No authorization bypass paths (direct database access, admin interfaces
      without PDP).
- [ ] Policy as code: policies stored in VCS, reviewed, tested.
- [ ] Functional testing of authorization logic (positive and negative cases).
- [ ] Performance / load testing of PDP under realistic request volume.
- [ ] If multiple authorization models coexist (RBAC + ABAC), the resolution order
      is documented (e.g., ABAC overrides RBAC, or union/intersection semantics).

---

## 4. Secrets Management Architecture

Secrets management covers the storage, access, rotation, and auditing of
non-human credentials (API keys, database passwords, TLS certificates, service
tokens, encryption keys).

### 4.1 Centralized Secrets Stores

| Solution | Model | Key Features | Review Considerations |
|----------|-------|--------------|----------------------|
| **HashiCorp Vault** | Self-hosted or HCP | Dynamic secrets, PKI, transit encryption, leasing, wrapping | Configure audit device; seal/unseal procedures; replication for HA |
| **AWS Secrets Manager** | Managed | Automatic rotation, cross-account access, fine-grained IAM policies | CloudWatch monitoring; rotation schedules; KMS integration |
| **AWS Systems Manager Parameter Store** | Managed | Tiered pricing (Standard/Advanced); free for non-sensitive | No automatic rotation for Standard tier; audit trail requires CloudTrail |
| **Azure Key Vault** | Managed | Soft-delete, purge protection, RBAC integration, managed HSM tiers | Key rotation policies; firewall + VNET integration; logging to Log Analytics |
| **GCP Secret Manager** | Managed | IAM integration, versioning, replication across regions | IAM policies per secret; audit logs via Cloud Audit Logs |
| **Doppler / Infisical** | Cloud/SaaS | Developer-first, environment management, secrets sync | Third-party SaaS risk; RBAC for workspace access; backup/export capability |

### 4.2 Secret Types & Lifecycle

**Secret Types:**
1. **Static secrets** — Pre-existing credentials stored in the vault (e.g., legacy
   database passwords, third-party API keys).
2. **Dynamic secrets** — Generated on-demand, short-lived, automatically revoked
   (e.g., Vault's database credential engine creates a unique SQL user for each
   lease).
3. **Encryption keys** — Key Encryption Keys (KEKs) and Data Encryption Keys (DEKs)
   used for envelope encryption.
4. **Certificates** — TLS/SSH certificates issued by an internal PKI.

**Secret Lifecycle:**
1. **Creation** — Store with metadata (owner, purpose, rotation period).
2. **Rotation** — Replace with new value; schedule (90 days static, hours/days dynamic).
3. **Access** — Authenticate and authorize the client; audit every access.
4. **Revocation** — Immediately on compromise; scheduled for end-of-life.
5. **Destruction** — Permanently delete; ensure no backups contain old versions.

### 4.3 Secrets Management Review Patterns

**Architecture Review Checklist:**
- [ ] Is there a single, centralized secrets store (no secrets scattered in
      config files, .env, source code)?
- [ ] Are dynamic secrets preferred over static secrets?
- [ ] Are secrets encrypted in transit AND at rest?
- [ ] Is the secrets store itself authenticated and authorized (no anonymous access)?
- [ ] Is access to the secrets store logged (who accessed which secret, when)?
- [ ] Is there a trusted identity system (e.g., Vault Kubernetes auth, AWS IAM,
      SPIFFE) for workloads to authenticate to the vault without human-accessible
      credentials?

**The "Secret Zero" Problem:**
The initial credential a workload uses to authenticate to the secrets store must
itself be managed. Solutions:
- Cloud-native: AWS IAM roles (instance profiles, ECS task roles, IRSA),
  GCP service accounts, Azure managed identities.
- Kubernetes: ServiceAccount token volume projection + OIDC federation for Vault.
- SPIFFE: Workload identity via X.509 SVIDs in service mesh.

**Common Secrets Misconfigurations:**
- Secrets in environment variables at rest (e.g., Docker Compose `.env` planted into
  the container image).
- Secrets in Git history (use `git secrets`, `truffleHog`, `Gitleaks` for scanning).
- Overly permissive vault policies (any app can read any secret).
- No rotation or manual-only rotation.
- Shared secrets across environments (dev credentials for production).
- Secrets exposed in logs, error messages, or stack traces.

**Secrets Scanning Tools (for code review):**
- `truffleHog` — scans Git history for high-entropy strings.
- `Gitleaks` — regex-based Git scanning.
- `GitGuardian` — cloud-managed; can detect 600+ secret types.

---

## 5. Dependency Audit & Supply Chain Security

### 5.1 SBOM Generation (CycloneDX & SPDX)

An SBOM (Software Bill of Materials) is a machine-readable inventory of all
components in a software artifact. The two dominant formats are **CycloneDX** and
**SPDX**. Both are ISO/IEC standards.

**Format Comparison:**

| Criterion | CycloneDX | SPDX |
|-----------|-----------|------|
| **Standard body** | OWASP | SPDX / Linux Foundation |
| **ISO/IEC** | 23587:2024 | 5962:2021 |
| **Focus** | Security-first (vulnerabilities, licensing, pedigree) | Legal-first (licensing, copyrights, provenance) |
| **Component identification** | PURL + CPE | PURL + CPE (SPDX 2.3+) |
| **Vulnerability mapping** | Native `vulnerabilities` array | External refs / advisory fields |
| **License expressiveness** | Good | Excellent (detailed license info, concluded and declared) |
| **Tooling ecosystem** | Mature (many generators) | Mature (Linux toolchain) |
| **Package manager support** | npm, pip, Maven, Gradle, Go, Cargo, NuGet, etc. | npm, pip, Maven, RPM, deb, etc. |

**Recommended Approach:** Use CycloneDX as your primary format for security
workflows; use SPDX as a supplement for legal/compliance workflows. Most mature
pipelines generate both.

**SBOM Generation Tools:**
- **`cdxgen`** (AppSec team OWASP): Generates CycloneDX SBOMs for all major
  ecosystems. Integrates with CI/CD.
- **`syft`** (Anchore): Fast SBOM generation in CycloneDX, SPDX, and Syft format.
- **`trivy`** (Aqua Security): Scans for vulnerabilities AND generates SBOMs.
- **`cyclonedx-bom`** (npm): Node.js-specific BOM generation.
- **`pip-audit` + `cyclonedx-python`**: Python ecosystem.
- **`gradle-sbom`**: Gradle plugin for CycloneDX.
- **GitHub Dependency Graph**: Auto-generated for GitHub-hosted repos.

**SBOM Generation Review Checklist:**
- [ ] SBOM generated at build time (not after deployment).
- [ ] SBOM includes direct AND transitive dependencies.
- [ ] SBOM is signed or attested (cosign, in-toto attestation).
- [ ] SBOM is stored alongside the artifact or in an SBOM management platform.
- [ ] SBOM regenerated and rescanned on every build.
- [ ] All components have identifiable PURLs (Package URL) or CPEs (Common
      Platform Enumeration).
- [ ] SBOMs are verified for completeness (dependency trees resolved correctly).
- [ ] Components with unknown versions are flagged for investigation.

### 5.2 CVE Matching & Severity Triage

CVE (Common Vulnerabilities and Exposures) matching involves correlating SBOM
components against vulnerability databases.

**Vulnerability Databases:**
| Database | Description | Review Consideration |
|----------|-------------|----------------------|
| **NVD (NIST)** | US govt CVE database with CVSS scores | NIST changed enrichment policy April 2026; ~80% of CVEs now lack CVSS/CPE/CWE enrichments |
| **GitHub Advisory Database** | Curated, OSV-formatted advisories | Used by Dependabot; good coverage for GHSA IDs |
| **OSV.dev** (Open Source Vulnerabilities) | Aggregated from multiple sources; uses OSV schema | Fast, schema-driven; best for automated tooling |
| **GitLab Advisory Database** | Curated for GitLab dependency scanning | Integrated with GitLab pipeline |
| **Snyk / WhiteSource / Sonatype** | Commercial vulnerability intelligence with proprietary research | Broader coverage but requires licensing |
| **Reachability** (e.g., Sonatype Nexus IQ, Snyk) | Filters CVEs based on reachability in code paths | Reduces noise dramatically — prioritizes actual exploitable paths |

**CVSS v3.1 Severity Triage:**

| Severity | Score Range | Response SLA |
|----------|-------------|--------------|
| Critical | 9.0 - 10.0 | Immediate (< 24 hours) |
| High | 7.0 - 8.9 | Urgent (< 72 hours) |
| Medium | 4.0 - 6.9 | Standard (within sprint) |
| Low | 0.1 - 3.9 | Informational (plan next cycle) |
| None | 0.0 | No action |

**Triage Enrichment Factors (beyond CVSS base score):**
- **EPSS (Exploit Prediction Scoring System):** Predicts likelihood of exploitation
  in the wild (0-100%). Use EPSS >= 0.05 (5%) as actionable threshold.
- **Known Exploited Vulnerabilities (KEV) Catalog:** CISA-maintained list of
  vulnerabilities actively exploited. Treat KEV-listed CVEs as immediate priority
  regardless of CVSS score.
- **Reachability:** Is the vulnerable function actually called in your code?
- **Attack vector:** Network vs. adjacent vs. local — network-exploitable CVEs
  have higher priority.
- **Component usage:** Runtime dependency (higher priority) vs. build-time/dev
  dependency (lower priority).
- **Compensating controls:** WAF rules, network segmentation, or other controls
  that block the attack path.

**CVE Matching Review Checklist:**
- [ ] Dependency scanning tool configured with multiple CVE data sources.
- [ ] Scans run on every build and on a recurring schedule (daily).
- [ ] False positive handling process documented (formal suppression with
      justification + re-review date).
- [ ] Severity overrides documented (e.g., CVSS 7.0 high in our context because
      it's a reachable network-facing dependency).
- [ ] KEV catalog checked for flagged CVEs.
- [ ] EPSS scores used for prioritization (not only CVSS).
- [ ] Critical/high CVEs have documented dependency update timelines.
- [ ] Autofix / automated PRs enabled for transitive dependency updates.
- [ ] Delay/block thresholds set in CI/CD for critical/high CVEs in
      production dependencies.

### 5.3 License Compatibility Analysis

Open-source software licenses impose obligations and restrictions on derivative
works. An audit must verify that every dependency's license is compatible with the
project's distribution model.

**License Categories:**

| Category | Examples | Restrictions |
|----------|----------|--------------|
| **Permissive** | MIT, Apache 2.0, BSD-2/3, ISC, Unlicense | Minimal: attribution required |
| **Weak Copyleft** | LGPL v2.1/v3, MPL 2.0, EPL 2.0 | Modified library files must be shared; linking permitted |
| **Strong Copyleft** | GPL v2/v3 | Derivative works must be distributed under the same license |
| **Network Copyleft** | AGPL v3 | SaaS/source-sharing triggers GPL obligations |
| **Proprietary / Non-commercial** | Commons Clause, BSL, custom | Must be avoided unless explicitly approved |

**Critical Compatibility Rules:**
- ❌ **Apache 2.0** project CANNOT include **GPL v2** code (incompatible).
- ✅ **Apache 2.0** CAN include **GPL v3** code (one-way compatibility — GPL v3
  accepts Apache 2.0).
- ❌ **GPL v2** (without "or later" clause) is incompatible with **Apache 2.0**,
  **GPL v3**, and **AGPL v3**.
- ✅ **GPL v3** and **AGPL v3** are compatible with each other.
- ✅ **MIT** code can be included in almost any project.
- ❌ **AGPL v3** in a commercial SaaS product creates sharing obligations (careful
  review required).
- ⚠️ **MPL 2.0** files must remain MPL 2.0, but the containing project can be
  any license.

**License Audit Tools:**
- **FOSSA:** Automated license scanning, policy management, compliance reports.
- **Snyk:** License checking alongside vulnerability scanning.
- **Scancode Toolkit:** Open-source license and copyright scanner.
- **licensed (GitHub):** Cache and verify dependency licenses.
- **ORT (OSS Review Toolkit):** Automated license compliance for CI/CD.
- **`trivy`:** Can detect license information alongside CVEs.

**License Review Checklist:**
- [ ] Every dependency has a declared, identifiable license.
- [ ] No "NOASSERTION" or "LICENSE UNKNOWN" entries without manual review.
- [ ] Copyleft dependencies are documented and their obligations understood.
- [ ] Multi-licensed dependencies are reviewed for the applicable license.
- [ ] License header requirements documented (MIT, Apache 2.0 require attribution).
- [ ] Dual-license projects (e.g., Terraform, MongoDB) are flagged for commercial
      use restrictions.
- [ ] License compliance is gated in CI/CD.
- [ ] Third-party code audits performed for contract/copyright year accuracy.

### 5.4 Supply Chain Attack Patterns

Supply chain attacks target the trust relationships in the software development
and distribution pipeline.

**Attack Taxonomy:**

| Attack Type | Description | Real Example | Mitigation |
|-------------|-------------|--------------|------------|
| **Typosquatting** | Package name similar to popular package (e.g., `requrests` vs `requests`) | `coa` (npm), `crossenv` (PyPI) | Pin exact package names; use lock files; enable namespace scopes |
| **Dependency Confusion** | Attacker uploads to public repo a package with same name as internal package; dependency resolver picks public (higher version) | 2021: generic npm/PyPI confusion attacks | Verify package sources; scope namespaced packages (e.g., `@org/pkg`); use private registries with priority |
| **Malicious Maintainer / Account Takeover** | Compromised maintainer account pushes malicious version (SAP, stargazers download trick) | `event-stream` (npm, 2018), `colors` + `faker` (2022) | 2FA for package maintainers; code review of dependency updates; signing commits |
| **Brandjack "Piggybacking"** | Legitimate-looking package stealing auth tokens or personal info — like typosquatting but with real looking name/icon | Various malicious PyPI packages | Verify package author/commits; signature verification |
| **Compromised CI/CD Pipeline** | Attacker gains access to CI/CD credentials to inject code into build artifacts | SolarWinds Orion (2020), Codecov breach (2021) | SLSA framework; artifact attestation; signed artifacts; hardened CI/CD |
| **Direct Dependency Hijack** | NPM/Python maintainer intentionally ships malware after building trust | Various from `node-ipc` protestware to actual credential stealers | Vendor review; code freeze on updates; verify publisher identity |
| **Malicious Upstream Compromise** | Attacker compromises an upstream dependency that your dependencies pull | Many via compromised dev dependencies | Pin exact dependency versions; verify lock file hashes; regular dependency audits |
| **Build/Artifact Tampering** | Attack on build infrastructure to inject malicious code | SolarWinds | SLSA level 3+; reproducible builds; signed artifacts |

**Key Mitigation Layers:**

1. **Prevention:**
   - Use lock files (`package-lock.json`, `yarn.lock`, `Cargo.lock`,
     `go.sum`, `poetry.lock`, `requirements.txt` pinned).
   - Enable namespace scoping (e.g., `@scope/package` style prevents confusion).
   - Use private registries (e.g., GitHub Packages, Artifactory, Verdaccio)
     with verified upstream proxying.
   - Enable signed commits (maintainer PGP signatures) for releases where available.
   - Use `--ignore-platform-reqs` sparingly; verify platform-specific packages.

2. **Detection:**
   - CI/CD pipeline scanning for malicious packages (Snyk, Checkmarx, trivy,
     socket.dev, GuardDog).
   - Behavioral scanning: does the package access the file system, network,
     environment variables? (e.g., `socket.dev` analyzes package behavior).
   - Runtime monitoring: unexpected network connections from dependencies.
   - Lock file auditing: track hash changes.

3. **Response:**
   - Immediate revert to last known-good version.
   - Force repository re-scan (all affected pipelines).
   - Rotate all secrets that may have been exposed.
   - Publish advisory internally.
   - Contribute to CVE / OSV database.

**Supply Chain Hygiene Levels (from SLSA):**

| Level | Trust Criteria | Practical Implication |
|-------|----------------|----------------------|
| L0 | No guarantees | Default for most open-source |
| L1 | Build process is documented and run | Some automation in place |
| L2 | Build is fully automated; provenance exists | Trustworthy CI/CD pipeline |
| L3 | Provenance is non-forgeable; artifact integrity verified | Hardened CI; artifact attestation |
| L4+ | Two-party review; hermetic builds; reproducible | Top-tier (few orgs achieve this) |

### 5.5 SLSA Framework

Supply-chain Levels for Software Artifacts (SLSA, pronounced "salsa") provides
an end-to-end framework for ensuring software artifact integrity.

**SLSA Build Levels (v1.0+):**
- **SLSA 1:** Build process documented; provenance generated.
- **SLSA 2:** Build fully automated (no manual steps); provenance authentic
  (signed).
- **SLSA 3:** Hardened build platform with strong isolation; provenance
  non-forgeable.
- **SLSA 4:** Two-person review for the build; hermetic, reproducible builds.

**SLSA Requirements per Track:**

| Requirement | L1 | L2 | L3 | L4 |
|-------------|----|----|----|----|
| Provenance exists | ✅ | ✅ | ✅ | ✅ |
| Provenance is authenticated | | ✅ | ✅ | ✅ |
| Provenance is non-forgeable | | | ✅ | ✅ |
| Dependencies are complete | | | ✅ | ✅ |
| Build service is isolated | | | | ✅ |
| Build is hermetic | | | | ✅ |
| Provenance covers all sources | | | | ✅ |
| Two-person review | | | | ✅ |

**Attestation Format (in-toto):**
- Predicate types include `SLSAProvenance`, `SPDX`, `CycloneDX`, `VSA`
  (Verification Summary Attestation).
- Statements are signed by the build platform.
- Verification step uses the attestation to verify artifact integrity.

**SLSA Review Checklist:**
- [ ] What SLSA level does the supply chain target?
- [ ] Are provenance attestations generated for every build?
- [ ] Are attestations signed by a trusted build platform?
- [ ] Are attestations stored alongside artifacts?
- [ ] Is the build process documented and audited?
- [ ] Are all external dependencies captured in the provenance?
- [ ] Is there a policy for rejecting artifacts without valid attestations?

### 5.6 Dependency Audit Review Checklist (Aggregate)

- [ ] Lock files are committed and audited (package-lock.json, yarn.lock, Cargo.lock,
      go.sum, poetry.lock, requirements.txt).
- [ ] SBOMs generated in CycloneDX format (at minimum) for every build artifact.
- [ ] SBOMs are signed/attested.
- [ ] Dependency scanning runs on every commit and scheduled (daily).
- [ ] CVE triage process documented: CVSS + EPSS + reachability + KEV enrichment.
- [ ] Critical CVEs in production dependencies trigger CI/CD block.
- [ ] License scanning is automated and gated in CI/CD.
- [ ] Copyleft dependencies are documented; AGPL/GPL obligations understood.
- [ ] Lock files are audited for unexpected dependency changes.
- [ ] Typosquatting and dependency confusion scans run in CI/CD.
- [ ] Private registry with verified proxying used (not direct public registry access).
- [ ] All packages pinned to exact versions (no `^` or `~` ranges in production).
- [ ] Dependency update PRs are automatically created and reviewed.
- [ ] All CI/CD pipelines run in ephemeral, isolated environments.
- [ ] SLSA framework adopted at level >= 1, targeting level >= 2.

---

## References & Further Reading

### Standards & Specifications
- OAuth 2.0 — RFC 6749, RFC 6750
- OAuth 2.1 — draft-ietf-oauth-v2-1
- OAuth 2.0 Security BCP — draft-ietf-oauth-security-topics
- PKCE — RFC 7636
- OpenID Connect Core 1.0
- SAML 2.0 — OASIS Standard
- CycloneDX — OWASP, ISO/IEC 23587:2024
- SPDX — Linux Foundation, ISO/IEC 5962:2021
- SLSA v1.0 — SLSA.dev
- CVSS v3.1 — FIRST.org
- EPSS — FIRST.org (epss.cyentia.com)
- CISA KEV Catalog — cisa.gov/known-exploited-vulnerabilities
- Google Zanzibar — "Zanzibar: Google's Consistent, Global Authorization System" (USENIX 2019)

### Tools (Open Source)
- **SBOM:** `cdxgen`, `syft`, `trivy`, `cyclonedx-bom`
- **Dependency scanning:** `trivy`, `pip-audit`, `npm audit`, `osv-scanner`,
  `Dependabot`, `Renovate`
- **SAST / Secrets:** `truffleHog`, `Gitleaks`, `semgrep`
- **Policy engines:** `OPA` (Rego), `OpenFGA`, `SpiceDB`, `Cedar`,
  `Oso`, `Keto`
- **License auditing:** `FOSSA`, `scancode-toolkit`, `ORT`, `licensed`
- **Supply chain:** `cosign`, `slsa-verifier`, `in-toto`, `Grafeas`

### Commercial Vendors (ECosystem)
- **Dependency/Vulnerability:** Snyk, Sonatype Nexus Lifecycle, Checkmarx SCA,
  Mend (formerly WhiteSource), Black Duck, Socket.dev
- **Secrets Management:** HashiCorp Vault, AWS Secrets Manager, Azure Key Vault,
  GCP Secret Manager, Doppler, Infisical
- **Authorization:** Auth0, Okta, Oso Cloud, Aserto, Styra (OPA), Permit.io

---

> This document is intended as a practical reference for security engineers
> conducting architecture reviews and dependency audits. It focuses on
> actionable patterns, checklists, and common pitfalls rather than exhaustive
> specification coverage.
