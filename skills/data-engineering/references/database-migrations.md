# Database Migrations

## Migration Types

| Type | Risk | Rollback | Example |
|------|------|----------|---------|
| Add column (nullable) | Low | Trivial | `ALTER TABLE ADD COLUMN x TEXT` |
| Add column (NOT NULL) | Medium | Trivial if default provided | `ALTER TABLE ADD COLUMN x INT NOT NULL DEFAULT 0` |
| Rename column | High | Requires migration | Two-phase: add new, dual-write, backfill, drop old |
| Drop column | High | Requires restore | Verify no readers first, soft-delete before hard-drop |
| Create table | Low | Trivial | `CREATE TABLE` |
| Drop table | Critical | Requires restore | Verify no readers, triply confirm |
| Data migration | High | Requires rollback script | Transform values, update references |

## Migration Checklist

- [ ] Migration reviewed by another engineer
- [ ] Rollback script exists and is tested
- [ ] Downtime window confirmed (if required)
- [ ] Read replicas considered (replication lag)
- [ ] Foreign key constraints handled
- [ ] Indexes created after data load (not before)
- [ ] Migration tested against copy of production data
- [ ] Query performance verified post-migration
