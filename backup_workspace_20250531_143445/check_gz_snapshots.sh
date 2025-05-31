#!/bin/zsh
# check_gz_snapshots.sh
# Rychlá kontrola, že všechny .html.gz snapshoty a a11y reporty lze bez chyby dekomprimovat
# Používej před archivací, review nebo troubleshooting

ERROR=0

echo "\n--- Kontrola integrity .html.gz snapshotů a reportů ---"

for file in snapshot_html_*/**/*.html.gz pa11y_a11y_reports_*/**/*.html.gz; do
  if [[ -f "$file" ]]; then
    gunzip -t "$file" 2>/dev/null
    if [[ $? -ne 0 ]]; then
      echo "[!] Poškozený nebo nečitelný soubor: $file"
      ERROR=1
    else
      echo "[OK] $file"
    fi
  fi
done

if [[ $ERROR -eq 0 ]]; then
  echo "\n✓ Všechny .html.gz snapshoty a reporty lze bez chyby dekomprimovat."
else
  echo "\n[!] Některé snapshoty nebo reporty jsou poškozené! Oprav je nebo znovu vygeneruj před archivací."
fi
