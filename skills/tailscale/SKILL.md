---
name: tailscale
description: "WireGuard-based overlay networking — mesh VPN, ACL policies, subnet routing, exit nodes, and Headscale self-hosted control server."
author: Hermes Profiles
license: MIT
---

# Tailscale

## When to Load

Load this skill when the task involves setting up or managing a Tailscale tailnet — or a self-hosted Headscale instance — including ACL policies, subnet routing, exit nodes, DERP relay servers, and node lifecycle.

## Core Concepts

Tailscale builds an overlay mesh network on top of WireGuard. Each node gets a unique Tailscale IP (100.x.x.x range) and communicates peer-to-peer via NAT traversal. The control server coordinates key exchange and ACL policy; data flows directly between nodes.

### Node Lifecycle

- **Authentication:** Web auth (device opens browser), pre-auth keys (ephemeral or reusable, scoped to tags), OIDC (SSO via Google, GitHub, Microsoft, any OIDC provider)
- **Tags:** Device identity independent of user login — applied at auth time or via ACL. Used in ACL rules instead of user identity for servers, CI runners, infrastructure nodes
- **Expiry and cleanup:** Nodes expire after [N] days by default (configurable). Expired nodes are removed from tailnet. Pre-auth keys can be reusable or single-use, with expiry

### ACL Policy (huJSON)

- **Structure:** `{ "acls": [...], "groups": {...}, "tags": [...], "hosts": {...}, "derpMap": {...}, "ssh": [...], "nodeAttrs": [...] }`
- **ACL rules:** `{ "action": "accept", "src": ["group:dev"], "dst": ["tag:prod-server:*"] }` — src accepts connection to dst on given ports. Order independent; most specific policy wins.
- **Groups:** Named user groups — `"group:dev": ["alice@example.com", "bob@example.com"]`. Referenced in ACL src/dst.
- **Tags vs groups:** Tags identify devices (servers, CI runners). Groups identify users (developers, admins). ACL rules use both.
- **Deny rules:** Explicit `{ "action": "deny" }` rules with trailing `refuse` in dst — `"*:refuse"` blocks all ports. Deny overrides allow. Use for sensitive segments (prod-only database access, admin panels).
- **SSH:** Tailscale SSH replaces SSH key management — `{ "action": "check", "src": [...], "dst": [...], "users": [...] }` — ACL-enforced, logs all sessions, no keys to manage.

### Subnet Routing

- **Advertise routes:** `tailscale up --advertise-routes=10.0.1.0/24,192.168.0.0/16` — makes local subnets reachable via this node. Approved via ACL or admin console.
- **Use cases:** Connect on-prem networks, home lab subnets, cloud VPCs without peering, IoT device management
- **Performance:** Subnet router does not relay data through the control server — traffic flows directly through the subnet router node. Internet-bound traffic goes to the subnet router, then to its default gateway.

### Exit Nodes

- **Advertise:** `tailscale up --advertise-exit-node` — node becomes an exit to the internet for other tailnet members
- **Use:** Remote worker accessing public internet from office/home IP, geolocation bypass, outbound from a VPC for static IP
- **Limitations:** Single node bandwidth bottleneck. Not a replacement for a proper NAT gateway at scale.

### DERP Relay

- **Purpose:** Fallback relay when direct P2P connection fails (symmetric NAT, firewall). Auto-selected by Tailscale client.
- **Custom DERP:** Run your own DERP server for regions not covered, or to keep traffic off public relays. Requires TLS cert, STUN listener, and configuration in ACLs (`derpMap`)
- **Performance:** DERP-relayed traffic hits the server, so bandwidth is limited to server's capacity. Direct connection is always preferred.

### Headscale (Self-Hosted Control Server)

- **Role:** Open-source Tailscale control server replacement. When you don't want to use Tailscale's SaaS — run your own coordination server.
- **Deployment:** Single binary, SQLite or PostgreSQL backend, CLI management (`headscale users create`, `headscale nodes list`, `headscale routes enable`)
- **Integration:** OIDC for auth, DERP relay server bundled, `tailscale login --login-server https://headscale.example.com` on clients
- **Limitations:** No Funnel, no Serve (Tailscale SaaS features), admin UI is community-driven, API is less polished than Tailscale's

## Pitfalls

- **ACL ordering is NOT ordering.** All ACL rules of the same action are evaluated as a set — the most specific policy applies. Deny always overrides allow regardless of position.
- **Subnet routes must be approved.** Advertising doesn't make routes active. Admin must approve via console or pre-authorize via ACL.
- **Key expiry on headless nodes.** A server without interactive login will fail to re-authenticate after key expiry if no pre-auth key mechanism is set up. Use pre-auth keys with appropriate expiry for CI/CD and servers.
- **Tagged nodes cannot be logged into interactively.** Once a device is tagged, it loses user-based auth. ACLs applying to the tag govern access. If SSH access is needed, pair with Tailscale SSH ACL.
- **WireGuard overhead is minimal but not zero.** ~4% throughput impact on fast (1Gbps+) links. Encryption happens in kernel WireGuard module, so CPU impact is much lower than userspace VPNs.
