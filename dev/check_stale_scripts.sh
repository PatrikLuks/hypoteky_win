#!/bin/zsh
# check_stale_scripts.sh
# Najde shellové skripty, Python utility a testy starší než 30 dní (lze upravit)
# Používej pro pravidelnou údržbu, refaktoring nebo audit

DAYS=30

# Najdi všechny .sh a .py soubory v kořeni, klienti/, hypoteky/, scripts/, tests/
FILES=$(find . \( -path "*/__pycache__/*" -o -path "*/migrations/*" -o -path "*/.venv/*" -o -path "*/venv/*" \) -prune -false -o \( -name "*.sh" -o -name "*.py" \) -type f)

STALE=0
echo "\n--- Soubory starší než $DAYS dní ---"
for file in $FILES; do
  if [[ $(find "$file" -mtime +$DAYS) ]]; then
    echo "[!] $file ("$(stat -f "%Sm" -t "%Y-%m-%d" "$file")")"
    STALE=1
  fi
done

if [[ $STALE -eq 0 ]]; then
  echo "\n✓ Všechny skripty a testy byly upraveny v posledních $DAYS dnech."
else
  echo "\n[!] Některé skripty nebo testy jsou starší než $DAYS dní. Zvaž jejich kontrolu, aktualizaci nebo archivaci."
fi

echo "\n--- Doporučení ---"
echo "Pravidelně kontroluj a aktualizuj starší skripty a testy, aby workspace zůstal bezpečný a aktuální."
