# Remote Docker Verification — P3 Clean-Room Pattern

When the build target is a remote Docker host (not local Docker), use this sequence to verify changes in isolation.

## Sequence

```
1. Sync code             rsync changed files to Docker host
2. Build images          docker compose build <service>
3. Recreate services     docker compose up -d --force-recreate <service>
4. Verify health         curl /health on recreated service
5. Run tests             Execute test suite against running stack
```

## Step Details

### 1. Code Sync

```bash
# From the repo root:
rsync -av --relative \
  path/to/changed/file.py \
  path/to/another/file.py \
  docker-host:~/docker-compose/project/
```

Sync only the files that changed, not the entire repo. Track which files you've synced so you don't miss any.

### 2. Build

```bash
ssh docker-host 'cd ~/docker-compose/project && docker compose build <service>'
```

Build only the affected services. `docker compose build` uses Docker's layer cache — if only source files changed, the build is fast.

### 3. Recreate

```bash
ssh docker-host 'cd ~/docker-compose/project && docker compose up -d --force-recreate <service>'
```

`--force-recreate` ensures the container starts fresh with the new image, even if config hasn't changed.

### 4. Health Check

```bash
ssh docker-host 'sleep 3 && curl -s http://localhost:PORT/health'
```

Services that don't publish ports to the host require health checks through the Docker network:

```bash
ssh docker-host 'docker compose exec <service> curl -s http://localhost:PORT/health'
```

### 5. Test

Run relevant tests against the running stack. Tests that require specific fixtures (test-site, mock services) need those fixtures to be started first.

## Pitfalls

- **Cache ordering** — If your change adds metadata/results to pipeline outputs that go through a cache, verify the enrichment happens BEFORE the cache write, not after. See the "Enrich pipeline results before caching" pitfall in the contribution-pipeline SKILL.md.
- **Stale cache entries** — Previously cached results from before the code change may lack new fields. Either flush the cache, wait for TTL expiry, or enrich on cache read.
- **Partial rebuilds** — If you changed models or schemas shared between services, rebuild ALL affected services, not just the one whose code changed.
- **Logs confirm the fix** — After recreating, check `docker compose logs <service> --tail 10` to confirm the new code loaded without errors.
