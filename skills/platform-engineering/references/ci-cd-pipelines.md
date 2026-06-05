# CI/CD Pipelines — Reference

## Pipeline Platforms

### GitHub Actions

- **Workflow structure:** `.github/workflows/*.yml` — triggers, jobs, steps, matrix builds
- **Key patterns:** reusable workflows (`uses:` with `{owner}/{repo}/.github/workflows/{name}@{ref}`), composite actions, OIDC for cloud auth, artifacts/pages for delivery
- **Secrets:** GitHub Actions secrets, environment-level secrets, OIDC as an alternative to static keys
- **Matrix builds:** `strategy.matrix` for cross-platform/testing, `fail-fast` for early exit
- **Self-hosted runners:** scale sets, labels, network isolation, ephemeral runners

### GitLab CI

- **Pipeline structure:** `.gitlab-ci.yml` — stages, jobs, needs (DAG), artifacts, cache
- **Key patterns:** multi-project pipelines, parent-child pipelines, merge request pipelines, scheduled pipelines
- **Runners:** shared vs specific, Docker executor, Kubernetes executor, tags, concurrency limits
- **Registry:** GitLab Container Registry integration, dependency proxy

### Forgejo CI / Gitea Actions

- **Structure:** `.forgejo/workflows/*.yml` or `.gitea/workflows/*.yml` — compatible with GitHub Actions syntax
- **Runners:** Forgejo Runner (act-based), self-hosted, labels for platform targeting
- **Key differences from GitHub Actions:** Lighter ecosystem, smaller action marketplace, often need to self-host runners
- **Secrets:** Forgejo repository/organization secrets, no OIDC built-in (use manual token exchange)

### Jenkins

- **Pipeline structure:** `Jenkinsfile` — declarative (`pipeline { }`) vs scripted (`node { }`)
- **Key concepts:** agents, stages, steps, post-build actions, shared libraries, Blue Ocean
- **Cloud integration:** Jenkins X for Kubernetes, plugin ecosystem, custom agents via Docker

### CircleCI

- **Pipeline structure:** `.circleci/config.yml` — orbs, executors, jobs, workflows (DAG)
- **Key concepts:** contexts (env sharing), workspaces/persist-to-workspace, parallelism, test splitting
- **Orbs:** reusable config packages (official and community orbs for AWS, Slack, browsers, etc.)

## GitOps

### Argo CD

- **Core model:** Declarative GitOps — desired state in Git repository, Argo CD syncs to cluster
- **Key concepts:** Applications, Projects, Sync strategies (auto/manual), sync waves, prune policies, health checks
- **Multi-cluster:** Hub-and-spoke, cluster registration, RBAC per cluster
- **Progressive delivery:** Rollouts, canary deployments, blue-green, traffic mirroring (Argo Rollouts add-on)
- **Patterns:** App-of-apps, Kustomize/Helm integration, config management plugins (CMP), ApplicationSets for multi-env/deployment

### Flux

- **Core model:** GitOps toolkit — source → kustomize/helm → sync to cluster
- **Key components:** Source Controller, Kustomize Controller, Helm Controller, Notification Controller, Image Automation
- **Key concepts:** GitRepository/Bucket sources, Kustomization/HelmRelease, OCIRepository, ImagePolicy
- **Multi-tenancy:** Namespace isolation, cross-namespace references, access controls

## Release Automation

- **Semantic versioning:** `MAJOR.MINOR.PATCH` — breaking changes, features, fixes; pre-release suffixes, build metadata
- **Changelog generation:** Conventional Commits → automated changelog (git-cliff, standard-version, semantic-release)
- **Artifact provenance:** SLSA levels, attestation (in-toto), SBOM generation (Syft, Trivy), signing (Cosign)
- **Release gates:** Manual approvals (GitHub Environments, GitLab Deployments), automatic rollback on health check failure
- **Artifact registries:** Container registries (Docker Hub, GHCR, GitLab Registry, ECR, GAR), package registries (NPM, PyPI, Maven)
