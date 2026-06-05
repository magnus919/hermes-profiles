---
name: traefik
description: "Reverse proxy, load balancer, and ingress controller — dynamic routing, TLS automation, middleware chains, and integration with Docker, Kubernetes, and file-based providers."
author: Hermes Profiles
license: MIT
---

# Traefik

## When to Load

Load this skill when the task involves configuring Traefik as a reverse proxy or ingress controller — setting up routers, middlewares, TLS certificates, service discovery via Docker labels or Kubernetes CRDs, or debugging traffic routing.

## Core Concepts

### Architecture

Traefik uses dynamic routing: **entrypoints** (ports) → **routers** (URL rules + middleware chains) → **services** (backend load balancing). Configuration comes from **providers** (Docker, Kubernetes, file, Consul, etc.) and can change without a restart.

### Key Objects

- **Entrypoints:** Network listeners — `web` (HTTP :80), `websecure` (HTTPS :443), `traefik` (dashboard :8080). Can define additional for specific services (metrics, TCP, UDP)
- **Routers:** Match rules (`Host(\`example.com\`) && PathPrefix(\`/api\`)`), protocol (HTTP, HTTPS, TCP, UDP), set `tls:` for HTTPS, attach middleware chain, reference backend service
- **Middlewares:** Processing pipeline — `redirectScheme` (HTTP → HTTPS), `rateLimit`, `basicAuth`/`digestAuth`/`forwardAuth`, `addPrefix`/`stripPrefix`, `headers` (CORS, security headers), `retry`, `circuitBreaker`, `compress`, `replacePath`, `ipWhiteList`, `errorPage`
- **Services:** Load balancer config — servers with URLs/ports, health checks (interval, timeout, path), sticky sessions, circuit breakers, mirroring (traffic shadow for testing)

### Provider Patterns

- **Docker provider:** Labels on containers — `traefik.enable=true`, `traefik.http.routers.app.rule=Host(\`app.example.com\`)`, `traefik.http.services.app.loadbalancer.server.port=8080`. Hot-reloaded on container start/stop automatically
- **Kubernetes provider:** Standard Ingress (limited) or `IngressRoute` CRD (full Traefik features), CRD for Middleware, TLS options, ServersTransport resources
- **File provider:** YAML/TOML/JSON config file, useful for static services and dynamic config not covered by other providers. TOML deprecated in v3 in favor of YAML
- **Consul / etcd / Redis / ZooKeeper providers:** Key-value stores for config — less common but useful for distributed environments without K8s

### TLS Automation

- Let's Encrypt via ACME — `certificatesResolvers.myresolver.acme` with `httpChallenge` or `dnsChallenge` (for wildcards, behind load balancers, private networks)
- `dnsChallenge` requires provider credentials (AWS Route53, Cloudflare, GCP Cloud DNS, etc.) — more setup but more flexible
- Certificate storage (local file or KV store), SAN tracking, wildcard cert renewal

## Dashboard

- Exposed on Traefik entrypoint — `api.dashboard=true`, secured via `basicAuth` or `forwardAuth` middleware. Shows routers, services, middlewares, providers, health.
- Metrics: Prometheus (`metrics.prometheus`), OpenTelemetry, Datadog, InfluxDB, StatsD

## Pitfalls

- **Middleware ordering matters:** Middleware chain executes left to right. Put `rateLimit` before auth to avoid auth-d DoS. Put `redirectScheme` first to redirect before processing headers.
- **Docker provider scoping:** By default Traefik sees all containers on the same network. Use `--providers.docker.exposedByDefault=false` and explicit `traefik.enable=true` labels.
- **TCP vs HTTP routers:** TCP routers cannot use HTTP middlewares (headers, redirect). For TCP services with TLS, configure TLS termination at the router level.
- **Host rule vs TLS:** `Host(\`app.example.com\`)` in router matches the Host header. If the request goes to the IP, the Host header may not match — access via configured domain only.
- **Dashboard not accessible without auth:** `api.insecure=true` is for dev only. Always pair dashboard with `basicAuth` or `forwardAuth` middleware on the `api@internal` service.
