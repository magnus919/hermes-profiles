# Plan: Implement platform-engineer Profile

## Goal

Create a general-purpose, reusable `platform-engineer` Hermes agent profile — open-sourced on magnus919/hermes-profiles — that owns the build-and-deploy lifecycle: CI/CD pipelines, infrastructure as code, container orchestration, service networking, and deployment infrastructure. Nothing customized for any personal deployment.

Closes #58.

## Ownership & Destination

| Field | Value |
|-------|-------|
| **Repo** | magnus919/hermes-profiles (public) |
| **License** | MIT (matches repo) |
| **Profile name** | `platform-engineer` |
| **Target branch** | `feat/platform-engineer` → PR → squash-merge to `main` |

## Current Context

- 20 existing profiles follow a consistent pattern: `SOUL.md` + `profile.yaml` + `README.md` + `AGENTS.md` + `skills/` symlink directory
- Shared skill pool at `skills/` contains 27 skills (artifact-pyramids, site-reliability-engineering, etc.)
- CI checks (`.github/workflows/profile-checks.yml`) validate: symlink resolution, required files, YAML syntax, README mirroring
- Parent profile: issue #58 defines scope with 9 core domains (container orchestration, IaC, CI/CD, service networking, observability, secret management, cloud, languages)
- Sister profile: `site-reliability-engineer` — closest structural analog (same pattern of SOUL.md→profile.yaml→README.md→AGENTS.md→skills/symlinks)
- **Skills in the shared pool that already exist and can be symlinked:** `artifact-pyramids`, `implementation-planning`, `mermaid-diagrams`
- **Skills that need to be created in the shared pool:** `docker-management`, `traefik`, `tailscale` — these exist as installed skills on the author's machine but are NOT in the open-source shared pool
- **Niche tools (recommended, not required):** `dokku`/`dokku-fn` — Dokku is a specific PaaS, not universal platform engineering. Documented in references within the platform-engineering methodology skill rather than as standalone pool skills.

## Content Sourcing

| Deliverable | Sourcing Approach |
|-------------|------------------|
| SOUL.md first principles | Derived from platform engineering literature (Team Topologies, Platform Engineering by Camille Fournier, K8s patterns, IaC conventions) |
| profile.yaml | From the issue spec |
| README.md | Pattern from site-reliability-engineer, generalized |
| AGENTS.md | Trigger patterns derived from platform engineer scope of work |
| `platform-engineering` skill SKILL.md | Thin index with trigger table, references listing |
| skill references/ | For each domain (IaC, K8s, CI/CD, observability, secret management, service networking): researched content against current tool docs |

## Confirmed Design Decisions

(From issue #58 and conversation)
1. **Nothing deployment-specific** — all paths, examples, and content must use generic/synthetic data. No `/Users/magnus/`, no `phatalbert`, no `montcastle.bitches`, no `brandyapple.com`.
2. **General-purpose** — the profile must be useful for any platform engineer on any infrastructure, not tied to a homelab or specific cloud provider.
3. **Skill-based loading** — methodology depth lives in `references/` files loaded on demand (progressive disclosure), not in SKILL.md.
4. **Artifact-pyramid output contract** — the profile produces three-layer progressive disclosure artifacts. The response to any caller is the absolute path to `00-index.md`.
5. **Dokku** is a niche tool — listed as recommended, not required, and documented within the platform-engineering methodology skill references rather than as a standalone pool skill.
6. **Profile name**: `platform-engineer` (not `platform-engineering` which would be the methodology skill name).

## Proposed Approach

Build the profile in parallel with the shared-pool skills it needs. The core identity (SOUL.md, profile.yaml, AGENTS.md, README.md) is the primary deliverable. The supporting skills in `skills/` are scaffolded with SKILL.md and key references — not exhaustive encyclopedias, but enough to be useful.

Container skill pattern (same as site-reliability-engineering): a single `platform-engineering` methodology skill in the shared pool hosts the reference packs (IaC, K8s, CI/CD, observability, service networking, secret management, cloud patterns). This keeps the shared pool flat-ish and follows the existing pattern.

## Step-by-Step Plan

### Phase 1 — Prerequisite: sync repo and branch

1. `git pull origin main` in hermes-profiles repo
2. `git checkout -b feat/platform-engineer`

### Phase 2 — Create shared-pool skills

**2a. Create `skills/platform-engineering/`** — the core methodology skill

- `SKILL.md` — thin index with trigger conditions, domain reference table, loading instructions
- `references/ci-cd-pipelines.md` — GitHub Actions, GitLab CI, Forgejo CI, Jenkins, CircleCI pipeline patterns; GitOps with ArgoCD/Flux
- `references/container-orchestration.md` — K8s/k3s pod lifecycle, Helm chart conventions, Kustomize overlays, RBAC patterns, Docker Compose patterns
- `references/infrastructure-as-code.md` — Terraform/OpenTofu module patterns, state management, Pulumi project structure, Ansible role conventions, CloudFormation/CDK
- `references/service-networking.md` — Traefik/nginx/Caddy dynamic config, Tailscale/Headscale ACL patterns, WireGuard topology, service mesh fundamentals
- `references/observability.md` — Prometheus recording rules, Grafana dashboards-as-code, Loki log queries, OpenTelemetry tracing, health check patterns
- `references/secret-management.md` — Vault auth methods and policies, SOPS/age encryption in Git, External Secrets Operator patterns, Sealed Secrets
- `references/cloud-platforms.md` — AWS/GCP/Azure foundational patterns, multi-cloud design considerations, cost governance
- `references/automation-languages.md` — Go CLI tool patterns, Python SDK integration patterns, Bash bootstrap script conventions

**2b. Create `skills/docker-management/`** — container lifecycle and Compose

- `SKILL.md` — Docker fundamentals, multi-stage builds, layer optimization, Compose stacks, registries, health checks
- Standalone skill because Docker is a universal platform engineering tool — everyone needs it regardless of orchestrator choice

**2c. Create `skills/traefik/`** — reverse proxy and ingress

- `SKILL.md` — routers, middleware chains, TLS automation, dynamic config, metrics, dashboard
- Standalone skill because Traefik is a major ingress controller with specific configuration patterns

**2d. Create `skills/tailscale/`** — mesh networking

- `SKILL.md` — node lifecycle, ACL huJSON policy, subnet routing, exit nodes, DERP relay, Headscale self-hosting
- Standalone skill covering both Tailscale SaaS and Headscale self-hosted

### Phase 3 — Create profile directory

**3a. `profiles/platform-engineer/SOUL.md`**

Identity document with:
- First principles (the platform is a product, reduce cognitive load, everything as code, self-service over tickets, automation is the default, observability is infrastructure, security built-in, progressive delivery, API-first design)
- Output contract (artifact pyramid: path-as-handoff)
- Domain scope (container orchestration, IaC, CI/CD, service networking, observability, secret management, cloud, languages)
- Methodology mandate (which frameworks to load and when)
- Relationship with other profiles (especially sister profiles SRE, technical-architect)

**3b. `profiles/platform-engineer/profile.yaml`**

```yaml
description: >
  Platform engineer — owns the build-and-deploy lifecycle. Designs CI/CD
  pipelines, infrastructure as code (Terraform/OpenTofu/Pulumi/Ansible),
  container orchestration (K8s, Helm, Docker Compose), service networking
  (Tailscale, Traefik), and the deployment infrastructure that makes services
  reachable. Produces architecture assessments, pipeline designs,
  infrastructure plans, and deployment strategies as artifact pyramids.
skills:
  required:
    - artifact-pyramids
    - platform-engineering
    - docker-management
  recommended:
    - traefik
    - tailscale
    - implementation-planning
    - mermaid-diagrams
```

**3c. `profiles/platform-engineer/README.md`**

Usage guide with:
- What the profile provides
- Prerequisites
- Installation (clone + symlink + `hermes --profile platform-engineer`)
- Quick start prompts
- Skill dependency table
- Supporting references (from platform-engineering skill)
- Output format description
- Verification checklist

**3d. `profiles/platform-engineer/AGENTS.md`**

Agent guidance with:
- Trigger patterns table (user says X → load Y, produce Z)
- Loading order (platform-engineering → artifact-pyramids, then references per domain)
- Output contract (path to 00-index.md)
- Expected artifact pyramid structure
- Cross-reference rules
- Handoff protocol
- Related profiles

**3e. `profiles/platform-engineer/skills/`** — relative symlinks

```
skills/artifact-pyramids -> ../../../skills/artifact-pyramids
skills/platform-engineering -> ../../../skills/platform-engineering
skills/docker-management -> ../../../skills/docker-management
skills/traefik -> ../../../skills/traefik
skills/tailscale -> ../../../skills/tailscale
```

(All 3 levels deep from `profiles/platform-engineer/skills/<name>`, so `../../../skills/<name>` for each)

### Phase 4 — Update repo-level documentation

1. Add platform-engineer to repo `README.md` profile tree (alphabetically before product-manager)
2. Update `README.md` skills tree if new skills are added
3. Verify AGENTS.md symlink rules table covers 3-level depth

### Phase 5 — Verification

1. **Symlink check:** `find profiles/platform-engineer -type l | while read l; do test -e "$l" || echo "BROKEN: $l"; done` — all resolve
2. **Required files:** `SOUL.md`, `profile.yaml`, `README.md`, `AGENTS.md` present in `profiles/platform-engineer/`
3. **YAML:** `python3 -c "import yaml; yaml.safe_load(open('profiles/platform-engineer/profile.yaml'))"` — valid
4. **No absolute paths:** `grep -r '/' profiles/platform-engineer/skills/` — should show only relative symlinks
5. **No deployment-specific content:** `grep -r 'magnus\|montcastle\|phatalbert\|brandyapple\|\.hermes' profiles/platform-engineer/ skills/platform-engineering/` — zero matches
6. **README count:** Verify README.md profile count (expect 21) and skill count (expect 31)

### Phase 6 — PR and CI

1. `git add -A && git commit -m "feat: add platform-engineer profile"`
2. `git push -u origin feat/platform-engineer`
3. `gh pr create` with structured body:
   - Summary
   - Files changed (list)
   - Architecture: platform-engineering methodology skill with 7+ reference packs
   - QA results table (symlinks, required files, YAML, no personal data)
   - "Closes #58"
   - Agent disclosure
4. Wait for CI to turn green — all 4 checks must pass (symlinks, required files, YAML, README mirror)
5. If CI fails, fix and re-push
6. Present for review — do not merge without user approval

## Files Likely to Change

| File | Action |
|------|--------|
| `profiles/platform-engineer/SOUL.md` | Create |
| `profiles/platform-engineer/profile.yaml` | Create |
| `profiles/platform-engineer/README.md` | Create |
| `profiles/platform-engineer/AGENTS.md` | Create |
| `profiles/platform-engineer/skills/` (symlinks) | Create |
| `skills/platform-engineering/SKILL.md` | Create |
| `skills/platform-engineering/references/ci-cd-pipelines.md` | Create |
| `skills/platform-engineering/references/container-orchestration.md` | Create |
| `skills/platform-engineering/references/infrastructure-as-code.md` | Create |
| `skills/platform-engineering/references/service-networking.md` | Create |
| `skills/platform-engineering/references/observability.md` | Create |
| `skills/platform-engineering/references/secret-management.md` | Create |
| `skills/platform-engineering/references/cloud-platforms.md` | Create |
| `skills/platform-engineering/references/automation-languages.md` | Create |
| `skills/docker-management/SKILL.md` | Create |
| `skills/traefik/SKILL.md` | Create |
| `skills/tailscale/SKILL.md` | Create |
| `README.md` | Update — add platform-engineer to profile tree |

## Tests / Validation

- **Symlink resolution:** CI check + manual `find ... test -e` pass
- **Required files:** CI check passes with 4/4 files present
- **YAML syntax:** CI check passes
- **README mirroring:** CI check passes (21 profiles, 31 skills)
- **No personal data leak:** manual grep pass (proof before PR)
- **Profile loads in Hermes:** `hermes --profile platform-engineer` succeeds (manual, not part of CI)
- **Skill loads:** `skill_view('platform-engineering')` returns SKILL.md with correct linked_files

## Risks and Open Questions

1. **Skill granularity** — The `platform-engineering` container skill holds 7+ reference packs. This is a lot of content under one skill. Alternative: individual skills per domain (ci-cd, container-orchestration, etc.). Decided to follow the SRE pattern (one methodology skill with many references). Revisit if the skill becomes unwieldy.
2. **docker-management, traefik, tailscale** — These exist as skills on the author's machine. The versions created in the shared pool must be scrubbed of deployment-specific content and be generally useful. They don't need the full reference depth of platform-engineering — just enough to be useful (SKILL.md with methodology, a few key examples, and pitfalls).
3. **dokku/dokku-fn omitted from required** — Decided to include these in platform-engineering reference documentation rather than as standalone pool skills. Dokku is a specific PaaS; including it as required would make the profile less general. Revisit if there's demand.
4. **CI readiness** — CI runs `find profiles -type l` which covers the full tree including the new profile's symlinks. If any symlink is wrong, CI catches it. The README count check requires matching counts — if 21 profiles and 31 skills, README must reflect that.
5. **Proposed order discrepancy** — README.md lists profiles alphabetically. platform-engineer goes between "orchestrator" and "product-manager" in the current tree.
6. **Skill list discrepancy** — README.md lists skills alphabetically within each section. The new skills go in their alphabetical positions.
