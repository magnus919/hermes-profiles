# Secret Management — Reference

## HashiCorp Vault

- **Core model:** Dynamic secrets — generated on-demand (database credentials, cloud access keys, PKI certificates), short TTL, automatic revocation
- **Auth methods:** Token, Kubernetes (service account JWT → vault token), LDAP, OIDC, AppRole (machine-to-machine), AWS/GCP/Azure, GitHub
- **Secret engines:** KV (static, versioned), Database (dynamic DB creds), AWS/GCP/Azure (dynamic cloud creds), PKI (leaf certs), Transit (encryption as a service, data never leaves client)
- **Policies:** Path-based access control (`path "secret/data/app/*" { capabilities = ["read", "list"] }`), templating (`{{identity.entity.name}}`), fine-grained CRUD + deny + sudo
- **Patterns:** Sidecar injector (auto-auth, auto-renew), Vault Agent for caching/templating, kubernetes secrets via CSI provider, Terraform Vault provider, ACL templating for per-app secrets

## SOPS / age

- **Core model:** Encrypted files in Git — `sops --encrypt` (age or PGP), `sops --decrypt`, encrypted file is valid YAML/JSON with encrypted fields as `ENC[AES256_GCM,...]`
- **Encryption backends:** age (modern, key-based), PGP (traditional), AWS KMS, GCP KMS, Azure Key Vault, HashiCorp Vault
- **Workflow:** `.sops.yaml` config — creation rules per file path, key list for multi-key encryption (dev team key + CI key). Secrets files committed alongside code, CI decrypts at deploy time
- **CI/CD integration:** `sops --decrypt` in pipeline (using CI system's key access), age key securely injected (not in repo), KMS-based for cloud-native CI
- **Limitations:** No secret rotation (re-encrypt manually), no access audit, suitable for static config secrets but not dynamic credentials

## External Secrets Operator (Kubernetes)

- **Core model:** CRD-based — ExternalSecret resource syncs from external API to Kubernetes Secret. One-time sync or polling
- **Backends:** AWS Secrets Manager, GCP Secret Manager, Azure Key Vault, HashiCorp Vault, Akeyless, GitLab, SOPS-encrypted files
- **Patterns:** `refreshInterval` for periodic sync, `target` to control created secret name/type, `data` for static key mapping, `dataFrom` for bulk (all keys from remote), `remoteRef` strategies (property, version)
- **Best practices:** Namespace-scoped `ClusterSecretStore` vs `SecretStore`, push secret reconciliation errors to monitoring, avoid over-polling (set realistic `refreshInterval`)

## Sealed Secrets

- **Core model:** Encrypt secrets client-side — `SealedSecret` CRD (controller decrypts, creates regular Secret in cluster)
- **Workflow:** Developer creates `SealedSecret` YAML with `kubeseal` using cluster's public cert. Committed to Git. Controller on cluster decrypts and materializes `Secret` when applied.
- **Best for:** GitOps workflows where secrets must be in Git but cannot be stored in plaintext
- **Limitations:** Static only (no rotation), cert management (backup cluster key), no external API integration, per-cluster certs (same sealed secret won't work across clusters)
