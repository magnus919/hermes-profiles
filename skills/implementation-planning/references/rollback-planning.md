# Rollback Planning

## The Rule

Any deployment that cannot be rolled back is not ready to deploy.

## Rollback Strategies

| Strategy | Best For | How It Works |
|----------|----------|-------------|
| **Blue-green** | Services behind a load balancer | Deploy new version alongside old, switch traffic |
| **Canary** | High traffic, graduated risk | Deploy to 1% → 10% → 100%, abort at any stage |
| **Feature flag** | New behavior behind a toggle | Deploy the code with the feature off, toggle when ready |
| **Database migration** | Schema changes | Always make migrations backward-compatible first, clean up later |
| **Immutable deployment** | Containerized services | Deploy new containers, delete old ones, keep last known good image |

## Rollback Checklist

Before deploying:
- [ ] What's the rollback procedure? (Exact commands, not "we'll figure it out")
- [ ] How long will the rollback take? (Must be < acceptable downtime window)
- [ ] What data is affected? Can data changes be rolled back?
- [ ] Who is authorized to trigger the rollback?
- [ ] Has the rollback procedure been tested in the target environment?
- [ ] Will the rollback affect users? (How? Duration? Impact?)
