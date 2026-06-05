# Reproduction Checklist

## Before Reporting a Fix

- [ ] Can you reproduce the issue consistently? (If not, mark as intermittent)
- [ ] What are the exact steps to reproduce? (Write them down)
- [ ] Does it reproduce across environments? (Dev/staging/prod)
- [ ] Does it reproduce with different data? (Is it data-dependent?)
- [ ] Can you reproduce with a minimal test case? (Eliminate unrelated factors)

## Reproduction Discipline

- **One variable at a time.** Change only one thing between reproduction attempts.
- **Log everything.** Capture timestamps, request IDs, error messages, stack traces.
- **The first reproduction is the most valuable.** Before making any changes, capture the failing state completely (logs, metrics, screenshots, core dumps).
- **Time matters.** Note whether the issue is time-sensitive (occurs at specific intervals, after specific durations, under specific loads).

## Environment Reproduction

| Factor | Check |
|--------|-------|
| Platform/OS | Same OS version? Same patches? |
| Dependencies | Same library versions? |
| Configuration | Same config files? Feature flags? |
| Data | Same data volume? Same data patterns? |
| Load | Same concurrent users? Same request rate? |
