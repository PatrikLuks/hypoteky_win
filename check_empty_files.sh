#!/bin/zsh
# check_empty_files.sh
# Najde všechny klíčové soubory (.sh, .py, .md, .html, .ini, .csv, .yml, .json) s nulovou velikostí
# Používej před commitem, archivací, sdílením nebo troubleshootingem

ERROR=0

echo "\n--- Kontrola prázdných souborů ve workspace ---"

find . \( -name "*.sh" -o -name "*.py" -o -name "*.md" -o -name "*.html" -o -name "*.ini" -o -name "*.csv" -o -name "*.yml" -o -name "*.json" \) -type f -size 0c | while read file; do
  echo "[!] Prázdný soubor: $file"
  ERROR=1
  done

if [[ $ERROR -eq 0 ]]; then
  echo "\n✓ Ve workspace nejsou žádné prázdné klíčové soubory."
else
  echo "\n[!] Některé soubory jsou prázdné! Zkontroluj je a případně obnov ze zálohy nebo znovu vygeneruj."
fi
