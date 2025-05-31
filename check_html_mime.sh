#!/bin/zsh
# check_html_mime.sh
# Ověří, že všechny HTML snapshoty a a11y reporty mají MIME typ text/html po dekompresi
# Používej před review, sdílením nebo troubleshooting

TMPDIR=$(mktemp -d)
ERROR=0

echo "\n--- Kontrola MIME typu HTML snapshotů a reportů (text/html) ---"

for file in snapshot_html_*/**/*.html.gz pa11y_a11y_reports_*/**/*.html.gz; do
  if [[ -f "$file" ]]; then
    BASENAME=$(basename "$file" .gz)
    OUTFILE="$TMPDIR/$BASENAME"
    gunzip -c "$file" > "$OUTFILE"
    # Kontrola MIME typu
    MIME=$(file -b --mime-type "$OUTFILE")
    if [[ "$MIME" != "text/html" ]]; then
      echo "[!] $file → $OUTFILE má špatný MIME typ: $MIME"
      ERROR=1
    else
      echo "[OK] $file → $OUTFILE je text/html"
    fi
  fi
done

if [[ $ERROR -eq 0 ]]; then
  echo "\n✓ Všechny HTML snapshoty a reporty mají správný MIME typ text/html."
else
  echo "\n[!] Některé soubory nemají správný MIME typ! Oprav je před sdílením nebo review."
fi

echo "\nDočasné soubory jsou v $TMPDIR (můžeš je smazat: rm -r $TMPDIR)"
