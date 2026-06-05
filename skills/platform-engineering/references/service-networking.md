# Service Networking — Reference

## Reverse Proxy

### Traefik

- **Core model:** Dynamic routing — auto-discovers services via providers (Docker, Kubernetes, Consul, file), hot-reloads config
- **Key concepts:** Routers (HTTP/HTTPS/TCP/UDP), middlewares (rate limiting, auth, headers, retries, circuit breakers, compression, redirect), services (load balancing), entrypoints (ports), TLS automation via Let's Encrypt
- **Providers:** Docker provider (labels on containers), Kubernetes provider (IngressRoute CRD, or standard Ingress), file provider (static/dynamic YAML/TOML), Consul, etcd, Redis, ZooKeeper
- **Middleware chains:** Order matters — rate limit → auth → headers → retry; custom middleware via plugins (WebAssembly, Go), pass through ForwardAuth to external services
- **Observability:** Metrics (Prometheus, OpenTelemetry, Datadog, InfluxDB), access logs (in JSON), tracing (Jaeger, Zipkin, OpenTelemetry), dashboard UI

### nginx

- **Core model:** Static config (reload on change), high-concurrency event loop, reverse proxy, load balancer, TLS termination, caching
- **Key patterns:** `upstream` blocks for load balancing, `proxy_pass` for forwarding, `location` blocks for path routing, `map` for conditional logic, `limit_req`/`limit_conn` for rate limiting
- **Config management:** Templating (Jinja, envsubst), include directories for modular config, nginx -t for validation, reload via SIGHUP

### Caddy

- **Core model:** Automatic HTTPS (ZeroSSL/Lets Encrypt by default), simple `Caddyfile` syntax, JSON API for dynamic config
- **Key features:** HTTP/3 (QUIC) by default, on-demand TLS, HTTP->HTTPS redirects, reverse proxy with health checking, match blocks, matchers
- **Best for:** Simple deployments where Traefik's dynamic service discovery is overkill; excellent developer experience

## Mesh Networking

### Tailscale / Headscale

- **Core model:** WireGuard-based overlay network — nodes get unique Tailscale IP, communicate directly (NAT traversal), ACLs control access
- **ACL policy (huJSON):** `acls` (src/dest/proto/port), `groups` (user groupings), `tags` (device identity), `hosts` (alias mapping), `derpMap` relay configuration, `ssh` for Tailscale SSH
- **Key features:** Subnet routing (advertise routes), exit nodes (traffic to internet), ACL deny rules (refuse trailing), Funnel (allow internet traffic to local), Serve (host services on tailnet), MagicDNS
- **Headscale specifics:** Self-hosted control server, open-source, PostgreSQL/ SQLite backend, OIDC integration, CLI (`headscale users`, `headscale nodes`, `headscale routes`), DERP relay server setup
- **Lifecycle:** Node registration (pre-auth keys, web auth), expiry/node cleanup, key rotation (node keys, auth keys), multi-tailnet federation (Headscale sharing)

### WireGuard

- **Core model:** Layer 3 secure tunnel — single UDP port, kernel-level (fast), peer-to-peer, pre-shared or public-key auth
- **Config basics:** Interface (private key, address, listen port, DNS), Peer (public key, allowed IPs, endpoint, persistent keepalive)
- **Topology patterns:** Point-to-point (simple site-to-site), hub-and-spoke (central node routes), mesh (direct peer-to-peer), routed subnet (wg-quick tables, policy routing)

## Service Mesh

### Istio

- **Core model:** Sidecar proxy (Envoy) injected into pods — intercepts all traffic, applies mesh policies
- **Key concepts:** VirtualService (traffic routing, retries, timeouts, mirroring), DestinationRule (load balancing, connection pool, mTLS, circuit breaker), Gateway (ingress/egress), ServiceEntry (external services), PeerAuthentication (mTLS mode), AuthorizationPolicy (RBAC for services)
- **Observability:** Telemetry via Envoy — HTTP/gRPC metrics (Prometheus), distributed tracing (Jaeger/Zipkin/OpenTelemetry), access logs, Kiali for topology visualization

### Cilium

- **Core model:** eBPF-based — no sidecar injection, kernel-level networking and security
- **Key capabilities:** NetworkPolicy (identity-based, FQDN-based), Service Mesh (L7 policies, ingress/gateway API, L7 load balancing), Encryption (WireGuard in-kernel), Observability (Hubble: flow logs, metrics, UI, OpenTelemetry), ClusterMesh (multi-cluster networking)
- **Advantage over Istio:** No sidecar overhead, native eBPF performance, integrated with Tetragon for runtime security
