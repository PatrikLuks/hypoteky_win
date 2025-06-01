#!/bin/zsh
# check_md_utf8.sh – skript pro ověření, že všechny .md checklisty a dokumentace jsou validní UTF-8
# Používej před review, sdílením nebo archivací
# Kontroluje kódování všech .md souborů
# Autor: automatická optimalizace Copilot

ERROR=0

echo "\n--- Kontrola kódování .md checklistů a dokumentace (UTF-8) ---"

for file in *.md tests/*.md; do
  if [[ -f "$file" ]]; then
    ENCODING=$(file -b --mime-encoding "$file")
    if [[ "$ENCODING" != "utf-8" ]]; then
      echo "[!] $file není validní UTF-8 ($ENCODING)"
      ERROR=1
    else
      echo "[OK] $file je validní UTF-8"
    fi
  fi
done

if [[ $ERROR -eq 0 ]]; then
  echo "\n✓ Všechny .md checklisty a dokumentace jsou validní UTF-8."
else
  echo "\n[!] Některé .md soubory nejsou validní UTF-8! Oprav je před sdílením nebo archivací."
fi
