---
name: docker-management
description: "Container lifecycle management: Dockerfiles, multi-stage builds, Compose stacks, registries, container networking, and production container patterns."
author: Hermes Profiles
license: MIT
---

# Docker Management

## When to Load

Load this skill when the task involves Dockerfile authoring, Compose stack design, container registry operations, multi-stage build optimization, production container patterns, or troubleshooting container runtimes.

## Core Concepts

### Dockerfiles

- **Multi-stage builds:** Separate build-time dependencies from runtime image — `FROM ... AS builder` for compilation, final `FROM` for minimal runtime. Drastically reduces image size
- **Layer optimization:** Each `RUN`, `COPY`, `ADD` creates a layer. Order from least-to-most frequently changing (system deps first, app code last). Combine `RUN apt-get update && apt-get install -y ... && rm -rf /var/lib/apt/lists/*` in one RUN to avoid caching stale package lists
- **Best practices:** Use specific base image tags (not `:latest`), `COPY --chown` for non-root user, `HEALTHCHECK` instruction, `LABEL` for metadata, `EXPOSE` for documentation, `ENTRYPOINT` + `CMD` pattern for flexible default commands, `.dockerignore` for build context size

### Docker Compose

- **Service definition:** `image` (build locally or pull), `build` (context + Dockerfile + args), `ports`, `volumes`, `environment`, `depends_on`, `healthcheck`, `restart`, `networks`
- **Production concerns:** Named volumes (not bind mounts for persistent data), network isolation (separate frontend/backend/db networks), restart policies (`unless-stopped`), CPU/memory limits (`deploy.resources`), logging driver (`json-file` with rotation, or `journald`)
- **Multi-file compose:** `docker-compose -f docker-compose.yml -f docker-compose.prod.yml config` for override layers, `docker-compose.yml` (base) + `docker-compose.override.yml` (dev, gitignored) by convention

### Container Registries

- **Registry operations:** `docker tag`, `docker push`, `docker pull`, authentication via `docker login` or credential helpers
- **Platforms:** Docker Hub, GitHub Container Registry (GHCR), GitLab Container Registry, Amazon ECR, Google Artifact Registry, Azure Container Registry, self-hosted (Harbor, distribution)
- **Tagging strategies:** `git-sha` for traceability, `semver` for releases, `latest` as convenience pointer only; avoid `:prod`, `:staging` — use environment-specific `values.yaml` orchestration instead

### Container Networking

- **Network drivers:** `bridge` (default, per-host), `host` (no network isolation, best performance), `overlay` (swarm/multi-host), `macvlan` (physical IP per container), `none` (loopback only)
- **DNS resolution:** Docker's embedded DNS (service name resolution for Compose, container name for custom networks), `--dns` and `--dns-search` overrides
- **Common issues:** DNS caching, port conflicts on host, container-to-container vs external access, published port binding to all interfaces by default (use `127.0.0.1:PORT:PORT` to restrict)

## Pitfalls

- **Build context bloating:** `.dockerignore` is easy to forget. A node_modules-heavy context can send hundreds of MB to the Docker daemon every build. Always add `.dockerignore`.
- **Cache invalidation:** A `COPY . .` after adding one file invalidates every subsequent layer. Structure Dockerfiles so the most volatile content comes last.
- **Zombie processes without init:** Containers run PID 1 by default. Signals don't propagate. Use `tini` or `--init` flag for proper signal handling and zombie reaping.
- **Permission mismatches with bind mounts:** Host UID/GID may not match container user. Use `Dockerfile` USER directive consistently and consider `--user` flag for one-off debug containers.
- **Unpinned base images:** `FROM node:latest` breaks tomorrow. Pin to SHA256 digest or specific semver: `FROM node:20-slim@sha256:...`
