#!/bin/bash
# Graph diagnostics for the Magnus v2 Obsidian vault
# Run: bash assets/graph-diagnostics.sh

VAULT="/Users/magnus/Obsidian/Magnus v2"
echo "=== Vault Graph Diagnostics ===
"

# 1. Total notes
total=$(find "$VAULT/1 - Atoms" "$VAULT/2 - Molecules" "$VAULT/3 - Alloys" \
  "$VAULT/5 - People" "$VAULT/7 - Companies" "$VAULT/8 - Topics" \
  -name "*.md" ! -name "_Topic Tree.md" 2>/dev/null | wc -l | tr -d ' ')
echo "Structural notes: $total"

# 2. Orphan check — notes with zero incoming wikilinks
echo "
--- Orphans (zero incoming links) ---"
for dir in "1 - Atoms" "2 - Molecules" "3 - Alloys" "5 - People" "7 - Companies"; do
  find "$VAULT/$dir" -name "*.md" | while read note; do
    title=$(basename "$note" .md)
    # Escape special chars for grep
    pattern=$(echo "$title" | sed 's/\[/\\[/g; s/\]/\\]/g')
    count=$(grep -rl "$pattern" "$VAULT/1 - Atoms" "$VAULT/2 - Molecules" \
      "$VAULT/3 - Alloys" "$VAULT/5 - People" "$VAULT/8 - Topics" \
      --include="*.md" 2>/dev/null | grep -v "$note" | wc -l | tr -d ' ')
    if [ "$count" -eq 0 ]; then
      echo "  $dir/$(basename "$note")"
    fi
  done
done

# 3. Dead-end check — notes with zero outgoing wikilinks
echo "
--- Dead ends (zero outgoing links) ---"
for dir in "1 - Atoms" "2 - Molecules" "3 - Alloys" "5 - People"; do
  find "$VAULT/$dir" -name "*.md" | while read note; do
    links=$(grep -c '\[\[.*\]\]' "$note" 2>/dev/null || echo 0)
    if [ "$links" -eq 0 ]; then
      echo "  $dir/$(basename "$note")"
    fi
  done
done

# 4. Topic density — topics with most backlinks
echo "
--- Topic density (backlinks per topic) ---"
find "$VAULT/8 - Topics" -name "*.md" ! -name "_Topic Tree.md" | while read topic; do
  title=$(basename "$topic" .md)
  pattern=$(echo "$title" | sed 's/\[/\\[/g; s/\]/\\]/g')
  count=$(grep -rl "$pattern" "$VAULT/1 - Atoms" "$VAULT/2 - Molecules" \
    "$VAULT/3 - Alloys" "$VAULT/5 - People" \
    --include="*.md" 2>/dev/null | wc -l | tr -d ' ')
  echo "  $count  $title"
done | sort -rn | head -15

echo "
=== Done ==="
