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

# --- KONTROLA VŠECH SHELL SKRIPTŮ V PROJEKTU ---
# Ignoruj systémové a virtuální adresáře
IGNORE_DIRS=(.venv venv node_modules migrations __pycache__)
FIND_IGNORE=""
for DIR in "${IGNORE_DIRS[@]}"; do
  FIND_IGNORE+=" -path ./$DIR -prune -o"
done
# Najdi všechny .sh skripty mimo ignorované složky
SHELLSCRIPTS=$(eval find . $(for DIR in "${IGNORE_DIRS[@]}"; do echo -n " -path ./$DIR -prune -o"; done) -type f -name "*.sh" -print)
ALL_OK=1
for SCRIPT in $SHELLSCRIPTS; do
  echo "\nKontroluji shell skript: $SCRIPT"
  # Kontrola spustitelnosti
  if [[ ! -x "$SCRIPT" ]]; then
    echo "[SELHÁNÍ] Skript není spustitelný (chybí chmod +x)"
    ALL_OK=0
  fi
  # Kontrola shebangu
  FIRST_LINE=$(head -n 1 "$SCRIPT")
  if [[ "$FIRST_LINE" != '#!'* ]]; then
    echo "[SELHÁNÍ] Chybí shebang (#!) na prvním řádku."
    ALL_OK=0
  elif [[ "$FIRST_LINE" != *bash* && "$FIRST_LINE" != *zsh* ]]; then
    echo "[SELHÁNÍ] Shebang není bash/zsh: $FIRST_LINE"
    ALL_OK=0
  fi
  # Kontrola neprázdnosti
  if [[ ! -s "$SCRIPT" ]]; then
    echo "[SELHÁNÍ] Skript je prázdný."
    ALL_OK=0
  fi
  # Kontrola hlavičky (popis + autor v prvních 5 řádcích)
  HEADER=$(head -n 5 "$SCRIPT")
  if [[ "$HEADER" != *Autor* || ( "$HEADER" != *popis* && "$HEADER" != *Popis* && "$HEADER" != *účel* ) ]]; then
    echo "[SELHÁNÍ] Chybí komentář s popisem a autorem v prvních 5 řádcích."
    ALL_OK=0
  fi
  echo "[OK] Kontrola dokončena pro $SCRIPT"
done
if [[ $ALL_OK -eq 1 ]]; then
  echo "\n✓ Všechny shellové skripty splňují požadavky!"
else
  echo "\n[!] Některé shellové skripty nesplňují požadavky. Zkontroluj výstup výše."
fi
