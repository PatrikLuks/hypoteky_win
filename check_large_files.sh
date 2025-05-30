#!/bin/zsh
# check_large_files.sh
# Najde všechny klíčové soubory (.sh, .py, .md, .html, .ini, .csv, .yml, .json) větší než 2 MB
# Používej před commitem, archivací, sdílením nebo troubleshootingem

LIMIT=2097152 # 2 MB v bajtech
ERROR=0

echo "\n--- Kontrola velkých souborů ve workspace (>2 MB) ---"

find . \( -name "*.sh" -o -name "*.py" -o -name "*.md" -o -name "*.html" -o -name "*.ini" -o -name "*.csv" -o -name "*.yml" -o -name "*.json" \) -type f -size +${LIMIT}c | while read file; do
  SIZE=$(stat -f "%z" "$file")
  echo "[!] Velký soubor: $file ($((SIZE/1024)) kB)"
  ERROR=1
  done

if [[ $ERROR -eq 0 ]]; then
  echo "\n✓ Ve workspace nejsou žádné klíčové soubory větší než 2 MB."
else
  echo "\n[!] Některé soubory jsou příliš velké! Zvaž jejich zmenšení, odstranění nebo přidání do .gitignore."
fi
