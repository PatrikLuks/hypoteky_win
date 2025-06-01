#!/bin/zsh
# check_git_conflicts.sh – skript pro kontrolu nevyřešených git konfliktů ve workspace
# Používej před commitem, review, sdílením nebo troubleshootingem
# Najde všechny klíčové soubory s konflikty (<<<<<<<, =======, >>>>>>>)
# Autor: automatická optimalizace Copilot

ERROR=0

echo "\n--- Kontrola git konfliktů ve workspace ---"

find . \( -name "*.sh" -o -name "*.py" -o -name "*.md" -o -name "*.html" -o -name "*.ini" -o -name "*.csv" -o -name "*.yml" -o -name "*.json" \) -type f | while read file; do
  if grep -qE '<<<<<<< |=======|>>>>>>> ' "$file"; then
    echo "[!] Konflikt v souboru: $file"
    grep -nE '<<<<<<< |=======|>>>>>>> ' "$file"
    ERROR=1
  fi
done

if [[ $ERROR -eq 0 ]]; then
  echo "\n✓ Ve workspace nejsou žádné nevyřešené git konflikty."
else
  echo "\n[!] Některé soubory obsahují nevyřešené konflikty! Oprav je ručně před commitem nebo sdílením."
fi
