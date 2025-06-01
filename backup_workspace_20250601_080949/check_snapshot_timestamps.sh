#!/bin/zsh
# check_snapshot_timestamps.sh – skript pro ověření časových razítek snapshotů a reportů
# Používej před commitem, review, archivací nebo sdílením
# Kontroluje, že všechny .html.gz snapshoty a reporty mají dnešní časové razítko
# Autor: automatická optimalizace Copilot

DNES=$(date +%Y-%m-%d)
ERROR=0

echo "\n--- Kontrola časových razítek .html.gz snapshotů a reportů pro $DNES ---"

for file in snapshot_html_$DNES/*.html.gz pa11y_a11y_reports_$DNES/*.html.gz; do
  if [[ -f "$file" ]]; then
    MTIME=$(stat -f "%Sm" -t "%Y-%m-%d" "$file")
    if [[ "$MTIME" != "$DNES" ]]; then
      echo "[!] $file má časové razítko $MTIME (není dnešní!)"
      ERROR=1
    else
      echo "[OK] $file ($MTIME)"
    fi
  fi
done

if [[ $ERROR -eq 0 ]]; then
  echo "\n✓ Všechny snapshoty a reporty mají dnešní časové razítko."
else
  echo "\n[!] Některé soubory nejsou z dnešního dne! Přegeneruj je nebo zkontroluj workflow."
fi

echo "\n--- Doporučení ---"
echo "Pokud některá data nejsou aktuální, spusť příslušné skripty pro jejich vygenerování."
echo "  ./pa11y_batch.sh && ./cleanup_workspace.sh"
