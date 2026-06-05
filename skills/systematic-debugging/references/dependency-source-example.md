# Worked Example: Detecting an Editable Dev Fork

Demonstrates the "Check Dependency Source" pattern (Phase 1, step 5d).

## The Symptom

A background worker crashed on every invocation:

```
Traceback ...
  File "core/session.py", line 456, in _create_node
    cursor.execute("""INSERT INTO thought_nodes
    (id, content, node_type, timestamp, confidence, source_file, ...)
sqlite3.OperationalError: table thought_nodes has no column named confidence
```

## The Investigation Path

1. **Read the traceback** — the error is in `core/session.py` (a third-party library), line 456. It's trying to insert a `confidence` column that doesn't exist in the database.

2. **Check the schema** — `sqlite3 brain.db ".schema thought_nodes"` confirmed no `confidence` column in the actual table. The schema had `id, content, node_type, timestamp, source_file, decayed, ...` but no `confidence`.

3. **Check the source** — `python3 -c "import core.session; print(core.session.__file__)"` revealed the library was loading from `/private/tmp/some-fork/core/session.py` — not from site-packages.

4. **Check dependency source** — `pip show cashew-brain` revealed:
   - `Editable project location: /private/tmp/some-fork`
   - `Version: 1.0.0`
   - This is a `pip install -e` dev copy in a temp directory

5. **Compare to upstream** — `pip index versions <package>` showed a newer version on PyPI. The installed dev copy was behind and had un-merged changes.

## The Fix

The initial instinct was to patch the migration code in the dev copy — treating it as a bug in the code. The correct answer was: the dev copy shouldn't be there. The fix was:

```bash
pip uninstall <package> -y
pip install <package>          # install from PyPI
python3 -c "import <module>; print(<module>.__file__)"
# → site-packages/<module>/  ✓ production path
```

After switching to production, the INSERT no longer referenced `confidence` at all — the dev fork's schema drift was gone.

## Key Lesson

The `confidence` column had been added to INSERT statements in the dev fork, but the corresponding `ALTER TABLE ADD COLUMN` migration was never written. This is classic schema drift from an unmaintained fork. The symptom looked like a code bug, but the root cause was dependency management — running the wrong version of the library.

## Verification Commands

```bash
# Check install source
pip show <package>

# Check import path
python3 -c "import <module>; print(<module>.__file__)"

# Check PyPI for comparison
pip index versions <package>

# Check DB schema for drift
sqlite3 <db_path> ".schema <table_name>"
```
