# CI Pipeline Templates for Architecture Documentation

Platform-specific CI/CD pipeline templates for automating Structurizr-based architecture documentation — validation, diagram export, static site generation, and deployment.

All templates use the **Docker image** `structurizr/cli:latest` to avoid Java runtime dependencies on CI runners.

## Pipeline Stages (Common Across Platforms)

Every pipeline follows the same logical sequence:

```
1. validate  →  structurizr-cli validate -w docs/arch/model/system.dsl
2. inspect   →  structurizr-cli inspect -w docs/arch/model/system.dsl
3. export    →  structurizr-cli export -w docs/arch/model/system.dsl -format mermaid -output site/diagrams
4. site      →  structurizr-cli export -w docs/arch/model/system.dsl -format static -output site
5. deploy    →  Platform-specific Pages or artifact publishing
```

Not all stages run on every trigger. PRs typically run only stages 1-2 (validation). Merges to main run the full pipeline.

---

## 1. GitHub Actions

### Pipeline A: PR Validation (Stages 1-2 Only)

Path: `.github/workflows/validate-architecture.yml`

```yaml
name: Validate Architecture Docs
on:
  pull_request:
    paths:
      - 'docs/arch/**'

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Validate Structurizr DSL
        uses: docker://structurizr/cli:latest
        with:
          args: validate -w docs/arch/model/system.dsl

      - name: Inspect for architectural drift
        uses: docker://structurizr/cli:latest
        with:
          args: inspect -w docs/arch/model/system.dsl
```

### Pipeline B: Full Deploy to GitHub Pages (Stages 1-5)

Path: `.github/workflows/deploy-architecture-site.yml`

```yaml
name: Deploy Architecture Documentation
on:
  push:
    branches: [main]
    paths:
      - 'docs/arch/**'

permissions:
  contents: read
  pages: write
  id-token: write

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Validate Structurizr DSL
        uses: docker://structurizr/cli:latest
        with:
          args: validate -w docs/arch/model/system.dsl

      - name: Inspect for architectural drift
        uses: docker://structurizr/cli:latest
        with:
          args: inspect -w docs/arch/model/system.dsl

      - name: Export Mermaid diagrams
        uses: docker://structurizr/cli:latest
        with:
          args: export -w docs/arch/model/system.dsl -format mermaid -output site/diagrams

      - name: Export static site
        uses: docker://structurizr/cli:latest
        with:
          args: export -w docs/arch/model/system.dsl -format static -output site

      - name: Upload Pages artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: site

  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

### Alternative: Marketplace Action

A community action `structurizr/structurizr-cli-action` wraps the CLI as a dedicated action step:

```yaml
- name: Validate with marketplace action
  uses: structurizr/structurizr-cli-action@v1
  with:
    args: validate -w docs/arch/model/system.dsl
```

The Docker-based approach above is more portable and works identically on ForgeJo.

---

## 2. GitLab CI

Path: `.gitlab-ci.yml`

```yaml
stages:
  - validate
  - export
  - pages

validate-architecture:
  stage: validate
  image:
    name: structurizr/cli:latest
    entrypoint: [""]
  script:
    - /usr/local/structurizr-cli/structurizr.sh validate -w docs/arch/model/system.dsl
    - /usr/local/structurizr-cli/structurizr.sh inspect -w docs/arch/model/system.dsl
  only:
    changes:
      - docs/arch/**/*
  except:
    - main

export-diagrams:
  stage: export
  image:
    name: structurizr/cli:latest
    entrypoint: [""]
  script:
    - /usr/local/structurizr-cli/structurizr.sh export -w docs/arch/model/system.dsl -format mermaid -output public/diagrams
    - /usr/local/structurizr-cli/structurizr.sh export -w docs/arch/model/system.dsl -format static -output public
  artifacts:
    paths:
      - public
  only:
    - main

pages:
  stage: pages
  script:
    - echo "Publishing architecture documentation to GitLab Pages"
  artifacts:
    paths:
      - public
  only:
    - main
  environment: production
```

**Notes:**
- The `entrypoint: [""]` override is required to use the Structurizr CLI as a command rather than a long-running process
- GitLab Pages serves from the `public/` directory — the export step targets `public/` directly
- The `except: main` on validate ensures it runs on feature branches but not on the main branch (redundant with `only: changes` but explicit)

---

## 3. ForgeJo (Gitea Actions)

ForgeJo is a fork of Gitea. Gitea 1.19+ ships **Gitea Actions** as a built-in CI/CD solution — a GitHub Actions compatible runner using `act`. Workflows go in `.gitea/workflows/` and use the same syntax as GitHub Actions.

### Pipeline A: PR Validation

Path: `.gitea/workflows/validate-architecture.yml`

```yaml
name: Validate Architecture Docs
on:
  pull_request:
    paths:
      - 'docs/arch/**'

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Validate Structurizr DSL
        uses: docker://structurizr/cli:latest
        with:
          args: validate -w docs/arch/model/system.dsl

      - name: Inspect for architectural drift
        uses: docker://structurizr/cli:latest
        with:
          args: inspect -w docs/arch/model/system.dsl
```

### Pipeline B: Full Deploy (Artifact-based)

Path: `.gitea/workflows/deploy-architecture.yml`

```yaml
name: Build Architecture Documentation
on:
  push:
    branches: [main]
    paths:
      - 'docs/arch/**'

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Validate Structurizr DSL
        uses: docker://structurizr/cli:latest
        with:
          args: validate -w docs/arch/model/system.dsl

      - name: Export Mermaid diagrams
        uses: docker://structurizr/cli:latest
        with:
          args: export -w docs/arch/model/system.dsl -format mermaid -output site/diagrams

      - name: Export static site
        uses: docker://structurizr/cli:latest
        with:
          args: export -w docs/arch/model/system.dsl -format static -output site

      - name: Upload artifact
        uses: actions/upload-artifact@v4
        with:
          name: architecture-docs
          path: site
```

**Deploy note:** Gitea/ForgeJo does not have a built-in Pages deployment in all versions (unlike GitHub Pages or GitLab Pages). Options for hosting the generated static site:

1. **Download artifact manually** — developers download from the Actions run page
2. **External hosting** — add a step to rsync/scp to a web server:
   ```yaml
   - name: Deploy to web server
     run: |
       rsync -avz --delete site/ user@server:/var/www/architecture/
   ```
3. **Woodpecker CI** — if your ForgeJo instance uses Woodpecker instead of Gitea Actions, see the note below

### Woodpecker CI Alternative

If the ForgeJo instance uses Woodpecker CI (not Gitea Actions), the schema is different:

```yaml
# .woodpecker.yml
pipeline:
  validate:
    image: structurizr/cli:latest
    commands:
      - /usr/local/structurizr-cli/structurizr.sh validate -w docs/arch/model/system.dsl
      - /usr/local/structurizr-cli/structurizr.sh inspect -w docs/arch/model/system.dsl
    when:
      path:
        include: [docs/arch/**]

  export:
    image: structurizr/cli:latest
    commands:
      - /usr/local/structurizr-cli/structurizr.sh export -w docs/arch/model/system.dsl -format mermaid -output site/diagrams
      - /usr/local/structurizr-cli/structurizr.sh export -w docs/arch/model/system.dsl -format static -output site
    when:
      branch: main

  deploy:
    image: alpine:latest
    commands:
      - echo "Site generated in ./site — deploy via rsync, S3, or artifact download"
    when:
      branch: main
```

---

## 4. Pipeline Selection Guide

| Situation | Trigger | Stages | Pipeline |
|---|---|---|---|
| PR changes architecture docs | `pull_request` | 1-2 (validate + inspect) | Short validation |
| Merge to main | `push main` | 1-5 (full pipeline) | Full deploy |
| Ad-hoc manual run | `workflow_dispatch` | 1-5 (full pipeline) | Full deploy |

---

## 5. Customization Notes

### Path Scoping

All templates use `docs/arch/**` as the path filter. Adjust to match your actual architecture directory:

| Directory Convention | Path Pattern |
|---|---|
| AaC standard (`docs/arch/`) | `docs/arch/**` |
| ADR + docs (`docs/adr/`, `docs/`) | Add multiple paths: `['docs/adr/**', 'docs/model/**']` |
| Root-level (`model.dsl` at project root) | `*.dsl` |
| Monorepo with multiple systems | `services/*/docs/arch/**` |

### PNG/SVG Export Limitation

The Structurizr CLI can only export Mermaid, PlantUML, DOT, and static HTML. For PNG/SVG rendering, you need headless Chrome + Puppeteer. Scripts are available at:

https://github.com/structurizr/puppeteer

This adds significant CI complexity (Chrome installation, rendering time). For most CI pipelines, the static HTML site with interactive diagrams (Mermaid) is sufficient.

### vNext Migration

The Structurizr CLI is deprecated in favor of new vNext commands. When vNext stabilizes:
- The binary name may change (`structurizr.sh` → `structurizr`)
- Flag syntax may change (`-workspace` → `--workspace`)
- The pipeline structure (validate → export → deploy) and Docker image (`structurizr/cli`) will remain the same

Monitor https://docs.structurizr.com/commands for updates.

### Trigger on Specific File Types

To only run when the DSL or ADR files change (not images or unrelated docs):

```yaml
paths:
  - 'docs/arch/model/**/*.dsl'
  - 'docs/arch/adr/**/*.md'
  - 'docs/arch/src/**/*.adoc'
```

---

## 6. Further Reading

- Structurizr CLI installation: https://docs.structurizr.com/cli/installation
- Structurizr CLI export: https://docs.structurizr.com/cli/export
- Structurizr static site: https://docs.structurizr.com/static
- GitHub Actions marketplace (Structurizr): https://github.com/marketplace/actions/structurizr-cli-action
- Gitea Actions overview: https://docs.gitea.com/usage/actions/overview
- Woodpecker CI: https://woodpecker-ci.org/
