# Observability — Reference

## Metrics: Prometheus

- **Core model:** Pull-based timeseries — scrape targets, service discovery, metric exposition format (`/metrics` endpoint)
- **Metric types:** Counter (cumulative, only increases), Gauge (up/down), Histogram (bucketed durations/sizes), Summary (quantile-based)
- **Recording rules:** Compute new timeseries from existing ones — `rate(...)[5m]` for per-second averages, `histogram_quantile()` for latency percentiles, aggregation via `sum() by ()` / `topk()`. Stored as new metric in Prometheus, faster than ad-hoc query
- **Alerting rules:** Vector → alert — `for:` duration eliminates flapping, severity labels (critical/warning/info), routing via Alertmanager to PagerDuty, Slack, email, etc.
- **Service discovery:** Kubernetes (pod annotations, kubelet), file_sd (JSON/YAML files), Consul, EC2, DNS
- **Best practices:** Use `rate()` not `irate()`, prefer histograms over summaries (aggregatable), label hygiene (cardinality limits, structured label naming)

## Dashboards: Grafana

- **Core model:** Data source abstraction — panel types (time series, bar, stat, table, gauge, logs), variables (interval, datasource filter), dashboard-as-code via JSON provisioning
- **Provisional dashboards:** JSON files in `provisioning/dashboards/` — auto-imported on Grafana startup. YAML datasource config in `provisioning/datasources/`. Version-controlled in Git alongside application config
- **Key patterns:** Template variables for environment switching, repeat panels per label value, annotations from Prometheus alerts, mixed data sources per panel, transformations (merge, group by, rename)
- **Best practices:** Single dashboard per service, row per concern (traffic, errors, latency, saturation), no more than 15 panels per row, dashboard links for navigation, `$__interval` for adaptive time range

## Logs: Loki

- **Core model:** Label-based log aggregation — indexes labels (not full text), stores compressed chunks in object storage. Promtail/Alloy/Fluent Bit for log shipping
- **LogQL:** `{label=~"value"} |= "error" \| json` for label matchers + content filters + pipeline stages. `rate()` for log error rates, `count_over_time()` for volume monitoring
- **Best practices:** CRI-O/Docker log format handling, structured logging (JSON), label cardinality limits, retention per storage tier (hot/warm/cold), multi-tenancy via label enforcement

## Tracing: OpenTelemetry

- **Core model:** Spans (operation units) → Traces (span DAG) → context propagation via W3C TraceContext headers
- **Signals:** Traces (request flow), Metrics (OTLP), Logs (via OTLP or file export) — unified in OpenTelemetry Collector
- **Components:** SDK (instrumentation libraries for Go, Python, JS, Java, etc.), Collector (receiver → processor → exporter pipeline), sampling (head-based, tail-based for storage cost management)
- **Instrumentation:** Auto-instrumentation (agent injection for Java/Python/.NET/Node), manual instrumentation (create spans, add attributes/events), existing library instrumentation (HTTP, gRPC, DB clients, messaging)
