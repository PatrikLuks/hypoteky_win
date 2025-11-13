#!/bin/zsh
# Popis: Kontrola kvality Python skriptů v kořeni a klienti/scripts/ (neprázdnost, shebang, hlavička s popisem a autorem)
# Autor: Patrik Luks, 2025

# Najdi všechny .py skripty v kořeni a klienti/scripts/
PYFILES=$(find . -maxdepth 1 -type f -name "*.py"; find klienti/scripts/ -type f -name "*.py" 2>/dev/null)

ALL_OK=1
for FILE in $PYFILES; do
  echo "\nKontroluji: $FILE"
  # Kontrola neprázdnosti
  if [[ ! -s "$FILE" ]]; then
    echo "[SELHÁNÍ] Soubor je prázdný."
    ALL_OK=0
  fi
  # Kontrola shebangu (jen pokud je spustitelný)
  if [[ -x "$FILE" ]]; then
    FIRST_LINE=$(head -n 1 "$FILE")
    if [[ "$FIRST_LINE" != '#!'* ]]; then
      echo "[SELHÁNÍ] Chybí shebang (#!) na prvním řádku."
      ALL_OK=0
    fi
  fi
  # Kontrola hlavičky (popis + autor v prvních 5 řádcích)
  HEADER=$(head -n 5 "$FILE")
  if [[ "$HEADER" != *Autor* || ( "$HEADER" !=x *popis* && "$HEADER" != *Popis* && "$HEADER" != *účel* ) ]]; then
    echo "[SELHÁNÍ] Chybí komentář s popisem a autorem v prvních 5 řádcích."
    ALL_OK=0
  fi
  echo "[OK] Kontrola dokončena pro $FILE"
done
if [[ $ALL_OK -eq 1 ]]; then
  echo "\n✓ Všechny Python skripty splňují požadavky!"
else
  echo "\n[!] Některé Python skripty nesplňují požadavky. Zkontroluj výstup výše."
fi
