#!/bin/zsh
# check_html_utf8.sh – skript pro ověření, že všechny HTML snapshoty a reporty jsou validní UTF-8
# Používej před review, sdílením nebo archivací
# Kontroluje kódování HTML snapshotů a reportů po dekompresi
# Autor: automatická optimalizace Copilot

TMPDIR=$(mktemp -d)
ERROR=0

echo "\n--- Kontrola kódování HTML snapshotů a reportů (UTF-8) ---"

for file in snapshot_html_*/**/*.html.gz pa11y_a11y_reports_*/**/*.html.gz; do
  if [[ -f "$file" ]]; then
    BASENAME=$(basename "$file" .gz)
    OUTFILE="$TMPDIR/$BASENAME"
    gunzip -c "$file" > "$OUTFILE"
    # Kontrola kódování pomocí file
    ENCODING=$(file -b --mime-encoding "$OUTFILE")
    if [[ "$ENCODING" != "utf-8" ]]; then
      echo "[!] $file → $OUTFILE není validní UTF-8 ($ENCODING)"
      ERROR=1
    else
      echo "[OK] $file → $OUTFILE je validní UTF-8"
    fi
  fi
done

if [[ $ERROR -eq 0 ]]; then
  echo "\n✓ Všechny HTML snapshoty a reporty jsou validní UTF-8."
else
  echo "\n[!] Některé soubory nejsou validní UTF-8! Oprav je před sdílením nebo archivací."
fi

echo "\nDočasné soubory jsou v $TMPDIR (můžeš je smazat: rm -r $TMPDIR)"
