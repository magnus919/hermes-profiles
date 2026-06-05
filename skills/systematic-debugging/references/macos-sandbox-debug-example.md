# Worked Example: Apple Books.app Import Pipeline (macOS)

Demonstrates the "macOS App Troubleshooting" and "Research Before Guessing" patterns (Phase 1 steps 6a/6b).

## The Symptom

Importing EPUBs into Apple Books fails silently. Three failure modes:
1. **Silent drag-and-drop** — file lands in app, nothing happens
2. **Double-click in Finder** — focus shifts to Books, but import never starts
3. **File → Open dialog** — selecting a file does nothing

No error dialogs. No crash reports. Books stays open and responsive.

## Investigation Path

### Phase 1 — Evidence Gathering

**1. Check the database (BKLibrary)**

The main library database is at:
```
~/Library/Containers/com.apple.iBooksX/Data/Documents/BKLibrary/BKLibrary-1-091020131601.sqlite
```

The `ZBKLIBRARYASSET` table tracks all books. Key columns:
- `ZSTATE` — 3=local file exists, 5=cloud-only
- `ZCONTENTTYPE` — 1=ebook, 5=book store, 6=audiobook/other
- `ZPATH` — full path to local file in BKAgentService container
- `ZASSETID` / `ZSTOREID` — Apple Store identifiers

**2. Check the XPC service (BKAgentService)**

File storage lives in:
```
~/Library/Containers/com.apple.BKAgentService/Data/Documents/iBooks/Books/
```

Books are stored as **unzipped directory bundles** (`.epub` extension on a directory, containing `META-INF/`, `OEBPS/`, and `mimetype`). Apple's Books app unzips EPUBs on import and stores the raw directory structure. This means standard EPUB tools (Calibre, etc.) cannot directly read from this storage — the files must be re-zipped with `mimetype` as the first entry.

**3. Check the import queue**

```
~/Library/Containers/com.apple.iBooksX/Data/Library/Caches/Inbox/
```

Files that have been draggged or opened but not yet processed appear here. Files can get stuck indefinitely.

**4. Read the system logs**

```bash
log show --predicate 'process == "Books"' --last 30m --style compact
```

The critical error:
```
BKResolveAssetForImportOperation: Unable to access url
BKResolveAssetForImportOperation: User cancelled import of cloud asset.
importBookFromURL: BKResolveAssetForImportOperation failed.
```

The "User cancelled" message is misleading — it's the app's internal interpretation of an NSFileCoordinator claim failure (Code=3072 "The operation was cancelled"), likely caused by a sandbox permission issue or XPC service state corruption.

**5. Check for container migration artifacts**

A `Data.old/` directory inside the BKAgentService container indicates a failed sandbox container migration during a macOS update:
```
~/Library/Containers/com.apple.BKAgentService/Data.old/
```

This can contain old book files and plists from a previous container version, creating orphaned state.

### The Root Cause

The user had deleted EPUB files from the Books local storage folder to free disk space. This broke the concordance between the CoreData database (which tracks book metadata) and the actual file store. Two layers of corruption resulted:

1. **Database inconsistency** — entries had `ZSTATE=3` (local file exists) but the file was gone
2. **Container migration ghost** — `Data.old/` from an OS update left orphaned files
3. **XPC service degradation** — BKAgentService would process exactly one import after restart, then silently stop

### Solutions Tested

**What worked (partially):**
- Container deletion (`rm -rf ~/Library/Containers/com.apple.iBooksX/` and `BKAgentService/`) — books re-downloaded from iCloud, but import pipeline remained fragile
- Full process kill (Books + BKAgentService + BooksThumbnail) — one successful import, then degradation

**What didn't work:**
- SQL-level database fixes (CoreData cached state and overwrote changes)
- TCC permission reset (`tccutil reset All com.apple.iBooksX`) — removed file access prompts
- BKAgentService selective kill — XPC respawns with broken state

**Confirmed workaround:**
- **iPhone iCloud Drive workaround** — upload EPUB to iCloud Drive, open on iPhone/iPad in Files app, share to Books. Syncs to Mac via iCloud, bypassing local import pipeline entirely.
- **iCloud Books data reset** — System Settings → Apple ID → iCloud → Manage Storage → Books → Delete All Data (forces full iCloud sync state reset)

## Books.app Import Pipeline

```
User drags EPUB → Powerbox creates security-scoped bookmark
  → Books.app receives URL via AppleEvent
  → BKResolveAssetForImportOperation copies file to Caches/Inbox
  → BKAgentService XPC picks it up from Inbox
  → BKAgentService unzips EPUB into bundle directory under Books/
  → BKAgentService updates Books.plist with metadata
  → BKLibrary CoreData store records the asset
  → iCloud sync pushes to other devices
```

### Where It Breaks

1. Sandbox security-scoped bookmarks fail → "Unable to access url" (TCC issue)
2. BKAgentService XPC degrades over time → silent import failures
3. Database/file concordance breaks → Books thinks it has files it doesn't
4. iCloud sync state corrupts → phantom entries, cross-device sync fails

### Diagnostic Quick-Reference

| Check | Command |
|-------|---------|
| App log | `log show --predicate 'process == "Books"' --last 10m` |
| XPC log | `log show --predicate 'process == "com.apple.BKAgentService"' --last 10m` |
| Database state | `sqlite3 .../BKLibrary-*.sqlite "SELECT ZSTATE,COUNT(*) FROM ZBKLIBRARYASSET GROUP BY ZSTATE;"` |
| Container size | `du -sh ~/Library/Containers/com.apple.iBooksX/` |
| Import queue | `ls ~/Library/Containers/com.apple.iBooksX/Data/Library/Caches/Inbox/` |
| Book files | `ls ~/Library/Containers/com.apple.BKAgentService/Data/Documents/iBooks/Books/` |
| Migration ghosts | `ls -d ~/Library/Containers/com.apple.BKAgentService/Data.old 2>/dev/null` |
