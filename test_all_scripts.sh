#!/bin/zsh
# test_all_scripts.sh
# Rychlé spuštění všech Python skriptů v klienti/scripts/ a kontrola jejich funkčnosti
# Používej pro údržbu, před refaktoringem nebo při onboardingu

SCRIPTDIR="klienti/scripts"
PYFILES=$(find "$SCRIPTDIR" -type f -name "*.py")

if [[ -z "$PYFILES" ]]; then
  echo "Žádné .py skripty nebyly nalezeny v $SCRIPTDIR."
  exit 0
fi

ERROR=0
echo "\n--- Spouštím všechny skripty v $SCRIPTDIR ---"
for file in $PYFILES; do
  echo "\n>>> python3 $file"
  python3 "$file"
  if [[ $? -ne 0 ]]; then
    echo "[!] Chyba při spuštění: $file"
    ERROR=1
  else
    echo "[OK] $file"
  fi
done

if [[ $ERROR -eq 0 ]]; then
  echo "\n✓ Všechny skripty v $SCRIPTDIR proběhly bez chyb."
else
  echo "\n[!] Některé skripty obsahují chyby. Oprav je před refaktoringem nebo nasazením!"
fi
