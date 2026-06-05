# Security Review

Systematic approach to finding vulnerabilities in code before they reach production.

## The Security Review Mindset

Unlike a code review, a security review assumes the code is broken and looks for ways to prove it. The question is not "does this work correctly?" but "what would an attacker do with this?"

## Threat Modeling in Review

Before looking at individual code paths, sketch the threat model:

| Element | What to ask |
|---------|-------------|
| **Assets** | What is this code protecting? (Data, credentials, access, compute) |
| **Attackers** | Who would want to compromise it? (External attacker, malicious insider, dependencies) |
| **Attack surface** | What entry points can an attacker reach? (API endpoints, file inputs, user-supplied data) |
| **Trust boundaries** | Where does data cross from untrusted to trusted context? (Input parsing, deserialization, exec calls) |
| **Privilege levels** | What can the process do that it shouldn't be able to? (Root, database access, network) |

## Vulnerability Classes to Check

### Injection (Critical)
- **Shell injection**: User input concatenated into shell commands. Flag: `os.system()`, `subprocess.Popen()` with `shell=True`, f-strings in commands. Fix: `shlex.quote()` or `subprocess.run()` with argument list.
- **SQL injection**: User input in SQL strings. Flag: f-strings or `+` concatenation in SQL. Fix: parameterized queries.
- **Command injection**: User input in CLI flag values. Flag: untrusted data passed as `--flag value` without validation.

### Deserialization (Critical)
- **Pickle**: Can execute arbitrary code during deserialization. Flag: `pickle.loads()` from untrusted sources. Fix: use JSON or structured formats.
- **YAML**: `yaml.load()` with untrusted input can execute code. Fix: `yaml.safe_load()`.
- **JSON with eval**: `json.loads()` followed by `eval()` — treat as critical.

### Authentication & Authorization (Critical)
- **Hardcoded credentials**: API keys, tokens, passwords in source code. Flag: `API_KEY = "sk-..."` in Python files. Fix: environment variables or secret manager.
- **Missing auth checks**: Endpoints or functions that should require authentication but don't.
- **Privilege escalation**: User can access resources they shouldn't. Check: object IDs in URLs, role checks.

### Path Traversal (High)
- **Unvalidated file paths**: User input used to construct file paths. Flag: `open(user_input)`, `os.path.join()` with user input. Fix: `os.path.realpath()` and prefix checking.
- **Symlink attacks**: Code follows symlinks to access unintended files. Fix: `os.path.realpath()` before access control checks.

### Information Disclosure (High)
- **Stack traces in production**: Uncaught exceptions that leak internal state.
- **Verbose error messages**: "User not found" vs "Invalid password" — the former reveals valid usernames.
- **Logging secrets**: API keys, tokens, passwords in log output. Flag: any `logger.info(f"secret={token}")`.

### Supply Chain (Medium-High)
- **Pinned dependencies**: Check `requirements.txt`, `pyproject.toml`, `package.json` for unpinned versions.
- **Deprecated packages**: Check for known-vulnerable dependencies (`pip audit`, `npm audit`, `grype`).
- **Dev dependencies in production**: Flag: dev-only packages installed in production Docker images.

### Cryptographic (Medium)
- **Homegrown crypto**: Custom encryption, hashing, or random number generation. Flag: anything implementing AES, SHA, or RNG from scratch.
- **Weak algorithms**: MD5, SHA-1 for security contexts. Flag and suggest SHA-256+ or bcrypt/argon2.
- **Hardcoded IVs/keys**: Static initialization vectors or encryption keys.

## The Security Review Protocol

### Phase 1: Map the Attack Surface
1. List all entry points (API routes, file loads, network connections, user inputs)
2. List all trust boundaries (where unvalidated data is processed)
3. List all privilege contexts (what level of access does each component run at?)

### Phase 2: Scan for Vulnerability Classes
1. Run automated checks for the classes above (grep for dangerous patterns)
2. For each match, read the actual code around it — context separates signal from noise
3. Classify each finding: Confirmed (exploitable), Suspicious (needs deeper investigation), Benign (not exploitable in context)

### Phase 3: Assess Exploitability
For each confirmed finding:
- **Is it reachable from an untrusted input?** If yes, it's exploitable. If no, it's defense-in-depth.
- **What's the impact?** Data exposure, RCE, privilege escalation, denial of service?
- **Is there existing mitigation?** Rate limiting, sandboxing, WAF rules?

### Phase 4: Report
For each finding, provide:
1. File and line number
2. Vulnerability class
3. The dangerous code pattern (excerpt)
4. Why it's exploitable (or why it's not)
5. Remediation suggestion

## Severity for Security Findings

| Severity | Impact | Action |
|----------|--------|--------|
| 🔴 Critical | RCE, privilege escalation, credential exposure | Block — must fix before merge |
| 🟠 High | Data exposure, path traversal, auth bypass | Block — must fix before merge |
| 🟡 Medium | Hardening, missing best practices | Should fix, can discuss |
| 🔵 Low | Defensive depth, informational | Note for future improvement |
