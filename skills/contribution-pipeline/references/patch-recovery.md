# Patch Recovery — When the `patch` Tool Corrupts a File

The `patch` tool is the preferred editing mechanism, but it can corrupt files when:
- Match context is insufficient (multiple similar blocks)
- The file was read with offset/limit pagination (partial view)
- Line numbers shifted between reading and patching (concurrent edits)
- The `old_string` matches partially but the replacement breaks syntax

## Detection

Run the linter after every patch. If lint fails and the error is in the patched area, the file is corrupted.

If the skill has `skill_view()` output that warns "was last read with offset/limit pagination (partial view)", re-read the full file before applying further patches.

## Recovery Strategies

### Strategy A: Rewrite small files (<200 lines)

Read the current (corrupted) file, then write it from scratch using `write_file` with the correct content. This is the fastest path for small files.

### Strategy B: Git restore + re-patch (any size)

1. Restore the file: `git checkout <path>` (works if changes weren't committed)
2. Re-read the restored file to get fresh line numbers and context
3. Apply the edit with more surrounding context (include 3-5 lines before and after the change point)
4. Verify with lint after the re-apply

### Strategy C: Escalate (files >500 lines with heavy modification)

If the file is large, heavily modified, and the patch keeps failing:
1. Stop trying to patch
2. Report the situation: which file, what was being changed, why the patch keeps failing
3. Ask the user whether to rewrite the file entirely or use a different editing strategy

## Prevention

- Always include 3-5 lines of surrounding context in `old_string`, not just the exact line being changed
- After reading a file with offset/limit, do a follow-up `read_file` of the full file before editing
- For Python files, run a syntax check after every patch: `python3 -c "import ast; ast.parse(open('<path>').read())"`
- When the file structure is complex (nested try/except, deeply indented blocks, long dicts), prefer `write_file` over `patch`
