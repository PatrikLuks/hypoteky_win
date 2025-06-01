#!/bin/zsh
# check_empty_dirs.sh
# Zkontroluje, že klíčové složky (snapshoty, reporty, testy, checklisty, skripty) nejsou prázdné
# Používej před commitem, archivací, sdílením nebo troubleshootingem

ERROR=0

# Seznam klíčových složek
DIRS=(snapshot_html_* pa11y_a11y_reports_* tests klienti/scripts)

echo "\n--- Kontrola prázdných složek ve workspace ---"

for dir in $DIRS; do
  if [[ -d "$dir" ]]; then
    COUNT=$(find "$dir" -type f | wc -l | tr -d ' ')
    if [[ "$COUNT" -eq 0 ]]; then
      echo "[!] Prázdná složka: $dir"
      ERROR=1
    else
      echo "[OK] $dir obsahuje $COUNT souborů."
    fi
  else
    echo "[!] Složka $dir neexistuje!"
    ERROR=1
  fi
done

if [[ $ERROR -eq 0 ]]; then
  echo "\n✓ Všechny klíčové složky obsahují soubory."
else
  echo "\n[!] Některé složky jsou prázdné nebo chybí! Zkontroluj workflow, obnov data nebo vygeneruj znovu."
fi
