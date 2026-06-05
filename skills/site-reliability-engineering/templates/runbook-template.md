# Runbook: [Service Name]

> **Version:** [1.0.0]
> **Last Updated:** [YYYY-MM-DD]
> **Owner:** [Team Name / Individual]
> **Review Cadence:** [Quarterly / Bi-annual / Annual]

---

## Table of Contents

1. [Service Overview](#service-overview)
2. [SLOs & Error Budget](#slos--error-budget)
3. [On-Call Quick Reference](#on-call-quick-reference)
4. [Monitoring & Alerting](#monitoring--alerting)
5. [Common Failure Modes](#common-failure-modes)
6. [Detailed Troubleshooting Procedures](#detailed-troubleshooting-procedures)
7. [Escalation Paths](#escalation-paths)
8. [Recovery Procedures](#recovery-procedures)

---

## Service Overview

### Description

[Briefly describe what this service does, its purpose, and the critical function it serves in the broader system architecture.]

### Architecture

[High-level description of the service architecture — key components, dependencies, data flow, upstream/downstream services.]

### Owner

| Field | Value |
|-------|-------|
| **Engineering Team** | [Team Name] |
| **Team Channel** | [#slack-channel] |
| **Primary DRI** | [Name / Role] |
| **Service Catalog URL** | [https://link-to-service-catalog] |
| **Code Repository** | [https://github.com/org/repo] |

### Links

| Resource | URL |
|----------|-----|
| **Grafana Dashboard** | [https://grafana.example.com/d/...] |
| **Datadog Dashboard** | [https://app.datadoghq.com/dashboard/...] |
| **CloudWatch Dashboard** | [https://console.aws.amazon.com/cloudwatch/...] |
| **Kibana / Logs** | [https://kibana.example.com/app/discover#...] |
| **Jaeger / Tempo Traces** | [https://tracing.example.com/...] |
| **PagerDuty Schedule** | [https://pagerduty.com/schedules/...] |
| **Status Page** | [https://status.example.com/] |
| **Runbook (this doc)** | [link] |

### Dependencies

| Dependency | Criticality | Notes |
|------------|-------------|-------|
| [Database e.g. PostgreSQL] | Critical | [connection details, failover info] |
| [Cache e.g. Redis] | High | [cluster info, eviction policy] |
| [Queue e.g. Kafka] | High | [topic names, consumer groups] |
| [External API] | Medium | [rate limits, quota info] |
| [Auth provider] | Critical | [token expiry, rotation schedule] |

### Key Metrics

| Metric | Target | Description |
|--------|--------|-------------|
| `[p99_latency_ms]` | < [500ms] | End-to-end request latency |
| `[requests_per_second]` | [N] | Throughput |
| `[error_rate]` | < [0.1%] | Ratio of 5xx responses |
| `[cpu_utilization]` | < [80%] | Instance CPU usage |
| `[memory_utilization]` | < [80%] | Instance memory usage |

---

## SLOs & Error Budget

### Service Level Objectives

| SLO | Target | Window | Measurement Method |
|-----|--------|--------|--------------------|
| **Latency** | [99% of requests < 500ms] | [28 days] | [Histogram buckets / Prometheus] |
| **Availability** | [99.9%] | [28 days] | [Ratio of successful requests] |
| **Throughput** | [Handle N req/s] | [1 hour] | [Max RPS measured] |
| **Freshness** | [Data < 5min old] | [1 hour] | [Lag monitoring] |

### Error Budget

| Period | Budget | Remaining | Burn Rate |
|--------|--------|-----------|-----------|
| **28 days** | [0.1% = 43m 12s] | [XX.X% remaining] | [Alert if > 2x target] |

### Burn Rate Alerts

| Severity | Burn Rate | Duration | Action |
|----------|-----------|----------|--------|
| **Warning** | [2x] | [1 hour] | Investigate |
| **Critical** | [10x] | [6 minutes] | Page on-call |
| **Critical** | [2x] | [6 hours] | Page on-call |

---

## On-Call Quick Reference

### How to Access

```bash
# SSH to production instances
ssh [user]@[bastion-host]
ssh [instance-name].[region].internal

# Kubernetes access
kubectl config use-context [cluster-name]
kubectl get pods -n [namespace]

# Database access
psql -h [host] -U [user] -d [database]
```

### How to Restart

```bash
# Restart application service
sudo systemctl restart [service-name]

# Roll restart Kubernetes deployment
kubectl rollout restart deployment/[deployment-name] -n [namespace]
kubectl rollout status deployment/[deployment-name] -n [namespace]

# Safe restart with traffic drain
./scripts/safe-restart.sh [service-name]
```

### Common Commands

```bash
# Check service health
curl -s http://localhost:[port]/health | jq .

# View recent logs
journalctl -u [service-name] --since "1 hour ago" -n 100

# Check current version
[service-name] --version
curl -s http://localhost:[port]/version | jq .

# Check active connections
netstat -anp | grep [port] | wc -l

# Check disk space
df -h /data
```

### Common Issues at a Glance

| Symptom | Try First |
|---------|-----------|
| Service returning 5xx | Check `/health` endpoint, restart service |
| High latency on p99 | Check CPU/memory, database query times |
| Alerts firing after deploy | Rollback to last known good version |
| Database connection errors | Check connection pool, restart app |
| Out of memory | Increase resources, rollback recent change |
| TLS / certificate errors | Check cert expiry, restart with reload |

---

## Monitoring & Alerting

### Key Dashboards

1. **[Service Overview Dashboard](https://grafana.example.com/d/service-overview)** — Primary dashboard for latency, error rate, throughput, saturation (the Four Golden Signals).
2. **[Infrastructure Dashboard](https://grafana.example.com/d/infra)** — CPU, memory, disk, network I/O per instance/container.
3. **[Database Dashboard](https://grafana.example.com/d/db)** — Connections, query latency, replication lag, cache hit ratio.
4. **[Dependency Dashboard](https://grafana.example.com/d/deps)** — Upstream/downstream health, queue depths, API latency.
5. **[Business Metrics Dashboard](https://grafana.example.com/d/biz)** — User-facing metrics: signups, active users, conversion.

### Logging

- **Log Aggregator:** [Kibana / Loki / CloudWatch Logs]
- **Log Level:** [INFO in production, DEBUG on-demand]
- **Structured Log Format:** [JSON]
- **Log Retention:** [30 days hot, 90 days cold]
- **Log Query:** [`{service="[service-name]"} | json`]

**Useful Log Queries:**

```kql
# All errors in last hour
{service="[service-name]"} | json | level = "error"

# Requests for a specific user
{service="[service-name]"} | json | user_id = "[user-id]"

# Trace a single request ID
{service="[service-name]"} | json | trace_id = "[trace-id]"
```

### Tracing

- **Tracing Backend:** [Jaeger / Tempo / X-Ray]
- **Sampling Rate:** [1% head-based, 100% for errors]
- **Trace Query by Service:** [`service.name="[service-name]"`]

### Alert Rules

| Alert Name | Condition | Severity | Auto-Close |
|------------|-----------|----------|------------|
| `[HighErrorRate]` | error_rate > [1%] for [5min] | Critical | [15min after recovery] |
| `[HighLatency]` | p99_latency > [1s] for [5min] | Warning | [30min after recovery] |
| `[LowDiskSpace]` | disk_usage > [90%] | Warning | [Disabled] |
| `[ServiceDown]` | up{job="[service]"} == 0 for [1min] | Critical | [10min after recovery] |

---

## Common Failure Modes

> Each failure mode is self-contained. Follow the resolution steps sequentially.

### FM-01: Service Unreachable / High Error Rate

| Field | Value |
|-------|-------|
| **Symptom** | `5xx` responses > [N]%, health check failing, pager alert firing |
| **Likely Cause** | Recent deployment, resource exhaustion, upstream dependency failure |
| **Diagnosis** | 1. Check `/health` and `/metrics` endpoints<br>2. Review recent deployments (`kubectl rollout history` or equivalent)<br>3. Check CPU/memory on instance<br>4. Check upstream dependencies (database, cache, external APIs)<br>5. Review recent logs for panic/OOM/panic |
| **Resolution** | 1. **If caused by recent deploy:** Rollback immediately: `kubectl rollout undo deployment/[deploy]`<br>2. **If resource exhaustion:** Scale up: `kubectl scale deployment/[deploy] --replicas=[N]`<br>3. **If upstream failure:** Check dependency runbook, pager dependency owner<br>4. **Last resort:** Restart the service<br>5. If none of the above work, [escalate](#escalation-paths) |

---

### FM-02: High Latency

| Field | Value |
|-------|-------|
| **Symptom** | p99/p95 latency exceeds SLO threshold, users report slowness |
| **Likely Cause** | Traffic spike, database query degradation, slow upstream, GC pressure |
| **Diagnosis** | 1. Check traffic volume vs baseline (is this a spike?)<br>2. Check database slow query log — `SELECT * FROM pg_stat_activity WHERE state = 'active'`<br>3. Check GC metrics (if JVM: `jstat -gcutil`, if Go: `go_memstats_gc_cpu_fraction`)<br>4. Check upstream dependency latencies<br>5. Review tracing dashboard for slow spans |
| **Resolution** | 1. **Traffic spike:** Auto-scale groups should handle; manually increase replicas if needed<br>2. **Slow queries:** Kill runaway queries: `SELECT pg_terminate_backend(pid) WHERE ...`; add missing index<br>3. **GC pressure:** Increase heap/memory, tune GC parameters<br>4. **Upstream slow:** Circuit-breaker should trip; verify upstream health<br>5. **Temporary fix:** Rate-limit or shed non-critical traffic |

---

### FM-03: Out of Memory / OOM Killed

| Field | Value |
|-------|-------|
| **Symptom** | Container/process killed, OOM in kernel logs, instance becomes unresponsive |
| **Likely Cause** | Memory leak in code, traffic surge, insufficient resource limits |
| **Diagnosis** | 1. Check `dmesg | grep -i oom` for kernel OOM killer messages<br>2. Check memory metrics via dashboard (heap vs non-heap if JVM)<br>3. Review recent code changes for potential memory leaks<br>4. Check if memory limit was recently reduced<br>5. Heap dump analysis (if available): `jmap -dump:live,format=b,file=heap.hprof <pid>` |
| **Resolution** | 1. **Immediate:** Restart the service to reclaim memory<br>2. **Increase limits:** Edit resource `limits.memory` for the container/Pod<br>3. If caused by code change: rollback the release<br>4. Schedule memory leak investigation with engineering team<br>5. Consider enabling memory request-based autoscaling |

---

### FM-04: Database Connection Pool Exhaustion

| Field | Value |
|-------|-------|
| **Symptom** | Application logs show `connection refused`, `too many connections`, or `connection timeout` |
| **Likely Cause** | Connection leak in application, insufficient pool size, DB restart |
| **Diagnosis** | 1. Check active connections on DB: `SELECT count(*) FROM pg_stat_activity`<br>2. Check max connections: `SHOW max_connections`<br>3. Identify connections by application: `SELECT application_name, count(*) FROM pg_stat_activity GROUP BY 1`<br>4. Check if connections are idle-in-transaction: `SELECT * FROM pg_stat_activity WHERE state = 'idle in transaction'`<br>5. Review application connection pool metrics (hikariCP, etc.) |
| **Resolution** | 1. **Emergency:** Kill idle connections: `SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE state = 'idle'`<br>2. **Kill idle-in-transaction:** Same as above with `state = 'idle in transaction'`<br>3. Restart the application to reset its connection pool<br>4. If leak persists, increase `max_connections` temporarily on DB<br>5. Schedule fix for connection leak (usually unclosed `Connection` / `Session` objects) |

---

### FM-05: Disk Space Full

| Field | Value |
|-------|-------|
| **Symptom** | Disk usage alert firing, application unable to write logs/data, `no space left on device` |
| **Likely Cause** | Logs not rotated, data not cleaned up, unexpected large files (core dumps, heap dumps) |
| **Diagnosis** | 1. `df -h` to identify full partition<br>2. `du -sh /* 2>/dev/null` to find large directories<br>3. `du -sh /var/log/* | sort -rh | head -10` for log sizes<br>4. `find / -type f -size +1G -exec ls -lh {} \;` for large files<br>5. Check logrotate status: `logrotate -d /etc/logrotate.d/[app]` |
| **Resolution** | 1. **Immediate:** `sudo journalctl --vacuum-size=500M` or `truncate -s0 /var/log/[app].log`<br>2. Clean old logs: `find /var/log -name "*.log.*" -mtime +7 -delete`<br>3. Clean temp files: `sudo rm -rf /tmp/*`<br>4. Verify logrotate is working: `sudo logrotate -f /etc/logrotate.conf`<br>5. If persistent, add disk monitoring alarm at 80% |

---

### FM-06: TLS / Certificate Expiry

| Field | Value |
|-------|-------|
| **Symptom** | Clients receive `certificate expired` or `x509: certificate has expired` errors |
| **Likely Cause** | Auto-renewal failed, cert-manager/ACME issues, manual cert not replaced |
| **Diagnosis** | 1. Check cert expiry: `echo | openssl s_client -servername [domain] -connect [domain]:443 2>/dev/null | openssl x509 -noout -dates`<br>2. Check cert-manager logs (if Kubernetes): `kubectl logs -n cert-manager -l app=cert-manager`<br>3. Check certificate resource status: `kubectl get certificate -A`<br>4. Verify DNS resolution for ACME challenge domain |
| **Resolution** | 1. **Manual renewal:** If cert-manager: `kubectl delete certificate [name]` to trigger re-issue, or fix the ACME challenge<br>2. **Manual cert replacement:** Upload new cert to LB/Ingress<br>3. Restart ingress controller / LB after cert update<br>4. If auto-renewal is broken, create a ticket for the platform team |

---

### FM-07: Upstream API Degraded / Down

| Field | Value |
|-------|-------|
| **Symptom** | Our service returns errors for operations that depend on [upstream], upstream latency spikes |
| **Likely Cause** | Upstream outage, rate limiting, network partition |
| **Diagnosis** | 1. Check upstream status page<br>2. Test upstream directly: `curl -v https://upstream.example.com/health`<br>3. Check our circuit breaker metrics<br>4. Check for recent upstream API changes<br>5. Check network connectivity: `ping`, `traceroute`, `nslookup` |
| **Resolution** | 1. **If circuit breaker open:** Wait for half-open / reset, or manually reset if safe<br>2. **If rate limited:** Throttle requests, request quota increase<br>3. **If upstream outage:** Enable fallback/graceful degradation (serve stale data, queue requests)<br>4. Page upstream PagerDuty escalation<br>5. Consider feature flags to disable upstream-dependent features temporarily |

---

### FM-08: Slow Consumer / Queue Backlog

| Field | Value |
|-------|-------|
| **Symptom** | Queue depth growing, consumer lag increasing, messages not processed in time |
| **Likely Cause** | Consumer crashed or stuck, processing logic regression, queue partition imbalance |
| **Diagnosis** | 1. Check consumer group lag (Kafka: `kafka-consumer-groups --bootstrap-server ... --group [group] --describe`)<br>2. Check consumer process health and logs<br>3. Check if messages are stuck on poison-pill messages (deserialization errors)<br>4. Check partition assignment and rebalance events<br>5. Check downstream that the consumer writes to |
| **Resolution** | 1. **Restart consumers:** `kubectl rollout restart deployment/[consumer]`<br>2. **Skip poison-pill messages:** Seek consumer offset past bad message<br>3. **Scale consumers:** Increase partitions + consumer replicas<br>4. **If DB is bottleneck:** Investigate and resolve DB performance first<br>5. If backlog is critical, consider replaying messages from an earlier offset after fix |

---

### FM-09: DNS Resolution Failures

| Field | Value |
|-------|-------|
| **Symptom** | `lookup [hostname]` failures, `connection refused`, intermittent timeouts |
| **Likely Cause** | DNS resolver outage, cached stale records, DNS propagation delay, /etc/resolv.conf misconfiguration |
| **Diagnosis** | 1. Test resolution: `dig [hostname] @[dns-server]`<br>2. Check `/etc/resolv.conf`<br>3. Check `nslookup [hostname]` and `host [hostname]`<br>4. Check DNS server reachability: `nc -zv [dns-server] 53`<br>5. Compare results across different resolvers (e.g., `8.8.8.8`) |
| **Resolution** | 1. **Flush DNS cache:** `sudo systemd-resolve --flush-caches` or restart `nscd`<br>2. **Update resolv.conf:** Ensure valid nameservers listed<br>3. **Restart DNS-sidecar** (if Kubernetes with CoreDNS/node-local-dns)<br>4. **Override in /etc/hosts** as temporary measure<br>5. If using Kubernetes, check CoreDNS pods and service: `kubectl -n kube-system get pods -l k8s-app=kube-dns` |

---

### FM-10: Pod CrashLoopBackOff (Kubernetes)

| Field | Value |
|-------|-------|
| **Symptom** | Pod repeatedly restarting, `CrashLoopBackOff` status, zero ready replicas |
| **Likely Cause** | Startup failure (config error, missing secret, dependency unavailable), OOM, liveness probe failing |
| **Diagnosis** | 1. Describe pod: `kubectl describe pod [pod-name] -n [namespace]`<br>2. Check pod logs: `kubectl logs [pod-name] -n [namespace] --previous`<br>3. Check events: `kubectl get events -n [namespace] --sort-by='.lastTimestamp'`<br>4. Verify configmaps/secrets are mounted: `kubectl exec -it [pod] -- cat /path/to/config`<br>5. Check liveness/readiness probe configuration |
| **Resolution** | 1. **Fix config/secrets:** Correct the ConfigMap or Secret and re-deploy<br>2. **Fix missing dependency:** Start the dependency or fix the connection string<br>3. **Increase resources:** If OOM-killed, increase `limits.memory`<br>4. **Fix probe:** Correct the probe endpoint/timeout/period<br>5. Rollback to last known good version if config doesn't help |

---

## Detailed Troubleshooting Procedures

### T-01: Initial Incident Triage

```
                   ┌──────────────────────┐
                   │  Alert Fires / User   │
                   │  Reports Issue        │
                   └──────────┬───────────┘
                              │
                   ┌──────────▼───────────┐
                   │  1. ACKNOWLEDGE      │
                   │  Ack the alert in    │
                   │  PagerDuty/OpsGenie  │
                   └──────────┬───────────┘
                              │
                   ┌──────────▼───────────┐
                   │  2. TRIAGE           │
                   │  - What's affected?  │
                   │  - How many users?   │
                   │  - Is it critical?   │
                   │  - Create incident   │
                   └──────────┬───────────┘
                              │
                   ┌──────────▼───────────┐
                   │  3. INITIAL COMMS    │
                   │  - Post in #incidents│
                   │  - Ping team channel │
                   │  - Update status page│
                   └──────────┬───────────┘
                              │
                   ┌──────────▼───────────┐
                   │  4. DIAGNOSE         │
                   │  Check dashboards,   │
                   │  logs, traces, use   │
                   │  Common Failure Modes│
                   └──────────┬───────────┘
                              │
                   ┌──────────▼───────────┐
                   │  5. MITIGATE         │
                   │  Rollback, restart,  │
                   │  scale up, etc.      │
                   └──────────┬───────────┘
                              │
                   ┌──────────▼───────────┐
                   │  6. VERIFY           │
                   │  Check dashboards    │
                   │  confirm recovery    │
                   └──────────┬───────────┘
                              │
                   ┌──────────▼───────────┐
                   │  7. RESOLVE          │
                   │  Close alert, update │
                   │  incident, post-mor- │
                   │  tem if needed       │
                   └──────────────────────┘
```

### T-02: Reading Health Check Endpoints

```bash
# Standard health check
curl -s http://localhost:[port]/health | jq .

# Verbose health check (includes dependency status)
curl -s http://localhost:[port]/healthz | jq .

# Readiness check (Kubernetes)
curl -s http://localhost:[port]/readyz | jq .

# Expected output for healthy service:
# {"status":"ok","version":"1.2.3","uptime":"72h14m","dependencies":{"database":"ok","cache":"ok","queue":"degraded"}}
```

### T-03: Capturing Diagnostic Data

```bash
# Collect a diagnostics bundle
./scripts/diagnostics.sh > /tmp/diag-$(date +%s).txt

# Capture thread dump (Java)
jstack <pid> > /tmp/thread-dump-$(date +%s).txt

# Capture heap histogram (Java)
jmap -histo:live <pid> > /tmp/heap-hist-$(date +%s).txt

# Capture goroutine dump (Go)
curl -s http://localhost:[debug-port]/debug/pprof/goroutine?debug=2 > /tmp/goroutines.txt

# Capture metrics snapshot
curl -s http://localhost:[port]/metrics > /tmp/metrics-$(date +%s).txt
```

### T-04: Safe Rollback Procedure

```bash
# Step 1: Identify last known good version
kubectl rollout history deployment/[deployment] -n [namespace]

# Step 2: Rollback to previous revision
kubectl rollout undo deployment/[deployment] -n [namespace]

# Step 3: Monitor rollout status
kubectl rollout status deployment/[deployment] -n [namespace]

# Step 4: Verify recovery
curl -s http://[service-url]/health | jq .

# Step 5: Announce in incident channel
echo "Rolled back [deployment] from v[X] to v[Y]. Health check passing."
```

---

## Escalation Paths

### Primary Escalation

| Level | Contact | Method | Response Time |
|-------|---------|--------|---------------|
| **L1** | On-call Engineer | PagerDuty / Phone | [15min] |
| **L2** | [Team Name] Senior Engineer | PagerDuty / Slack | [30min] |
| **L3** | [Team Name] Tech Lead | Phone / Slack @mention | [1hr] |
| **L4** | Engineering Manager | Phone / Slack @mention | [2hr] |

### Dependency Escalation

| Dependency | Team | PagerDuty Schedule |
|------------|------|--------------------|
| [Database Cluster] | [Data Platfom Team] | [link] |
| [Kubernetes Cluster] | [Infra Team] | [link] |
| [Network / DNS] | [Networking Team] | [link] |
| [External API] | [Vendor Support] | [vendor-ticket-link] |

### Escalation Procedure

1. **5 minutes:** If not resolved, page L1.
2. **15 minutes:** If L1 cannot resolve, escalate to L2 (Senior Engineer).
3. **30 minutes:** If L2 needs additional context, involve L3 (Tech Lead).
4. **60 minutes:** If incident is customer-facing or SEV-1, notify L4 (Engineering Manager).
5. **SEV-1 criteria:** Service down for > 5min, data loss, security breach, revenue impact.
6. **Declare SEV-1:** Post in #severe-incidents, create incident channel, invite relevant teams.

### Communication Template

```
INCIDENT: #[incident-number]
STATUS: [Investigating / Mitigating / Resolved]
SERVICE: [service-name]
IMPACT: [Describe user/business impact]
TIMELINE:
  [HH:MM UTC] - Alert fired
  [HH:MM UTC] - On-call acknowledged
  [HH:MM UTC] - Rollback initiated
NEXT STEPS: [What's being done]
```

---

## Recovery Procedures

### R-01: Post-Incident Steps

1. **Verify full recovery** — All health checks pass, error rates and latencies returned to baseline, alerting silenced.
2. **Update status page** — Mark incident as resolved if used.
3. **Resolve alert** — Close PagerDuty / OpsGenie alert.
4. **Tag and annotate** — Add incident severity, team, and service tags.
5. **Notify stakeholders** — Send summary to team channel and affected users.

### R-02: Data / State Recovery

> **Warning:** Data recovery procedures should only be attempted by engineers with database admin access.

```bash
# Step 1: Identify the recovery point (RPO)
# Step 2: Restore from backup to a staging environment first
# Step 3: Verify data integrity in staging
# Step 4: Schedule maintenance window
# Step 5: Perform database restore in production
# Step 6: Verify application works against restored data
```

**Backup Locations:**

| Resource | Backup Frequency | Retention | Restore Process |
|----------|-----------------|-----------|-----------------|
| [Database] | [Hourly WAL + Daily full] | [30 days] | [link to restore doc] |
| [Object storage] | [Cross-region replication] | [N/A] | [link to restore doc] |
| [Configuration] | [Git-controlled] | [Permanent] | Terraform apply |

### R-03: Incident Report Template

```markdown
## Post-Mortem: [Title]

**Date:** [YYYY-MM-DD]
**Duration:** [Start] — [End] ([X] minutes)
**Severity:** [SEV-1 / SEV-2 / SEV-3]
**Team:** [Team Name]

### Summary
[2-3 sentence executive summary]

### Timeline
- [HH:MM UTC] — [Event]
- [HH:MM UTC] — [Action taken]
- [HH:MM UTC] — [Recovery verified]

### Root Cause
[What actually caused the incident]

### Impact
- [N] requests failed
- [N] users affected
- [N] minutes of downtime

### Action Items
| Action | Owner | Ticket |
|--------|-------|--------|
| [Fix root cause] | [Name] | [Jira/GH link] |
| [Improve monitoring] | [Name] | [Jira/GH link] |
| [Update runbook] | [Name] | [PR link] |

### Lessons Learned
- What went well:
- What went wrong:
- What we'll do differently:
```

### R-04: Runbook Update Checklist

After any incident, update this runbook:

- [ ] Add any new failure modes discovered
- [ ] Update diagnosis steps that were incorrect or incomplete
- [ ] Update resolution steps that worked
- [ ] Update escalation paths if contacts have changed
- [ ] Update links that were broken
- [ ] Update SLOs / error budget if thresholds have changed
- [ ] Increment version number
- [ ] Update "Last Updated" date

---

## Appendix

### A — Useful Scripts & Aliases

```bash
# Quick health check
alias svc-health='curl -s http://localhost:[port]/health | jq .'

# Check recent deploys
alias svc-history='kubectl rollout history deployment/[deployment] -n [namespace]'

# Tail logs
alias svc-logs='kubectl logs -f deployment/[deployment] -n [namespace]'

# Shell into a running pod
alias svc-shell='kubectl exec -it deployment/[deployment] -n [namespace] -- /bin/bash'
```

### B — Environment Information

| Environment | URL / Access | Replicas | Instance Type |
|-------------|-------------|----------|---------------|
| **Production** | [prod-url] | [N] | [e.g. m5.xlarge] |
| **Staging** | [staging-url] | [N] | [e.g. t3.large] |
| **Development** | [dev-url] | [N] | [e.g. t3.medium] |

### C — Configuration Reference

| Config Key | Description | Default | Production Value |
|------------|-------------|---------|------------------|
| `[DATABASE_URL]` | Primary DB connection string | — | [redacted] |
| `[REDIS_URL]` | Redis connection string | — | [redacted] |
| `[LOG_LEVEL]` | Logging verbosity | `info` | `info` |
| `[MAX_CONNECTIONS]` | DB pool size | `10` | `[N]` |
| `[REQUEST_TIMEOUT]` | Upstream request timeout | `30s` | `10s` |

### D — Related Runbooks

| Runbook | Service | Link |
|---------|---------|------|
| [Database Runbook] | [Database] | [link] |
| [Cache Runbook] | [Redis/Memcached] | [link] |
| [Infrastructure Runbook] | [Kubernetes/AWS] | [link] |
| [Auth Runbook] | [Auth Service] | [link] |

---

> **Document Status:** This runbook is a living document. If you find errors, omissions, or out-of-date information during an incident, fix it immediately and submit a PR.
>
> **Template Attribution:** Based on the [Site Reliability Engineering](https://sre.google/) principles and Google's SRE books.
