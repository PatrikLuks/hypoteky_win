#!/bin/zsh
# Popis: Kontrola syntaxe všech Python souborů ve workspace.
# Autor: Patrik Luks, 2025
# Tento skript projde všechny .py soubory a ověří jejich syntaxi pomocí python -m py_compile.
# Rychlá kontrola syntaxe všech .py souborů ve workspace pomocí py_compile
# Používej před commitem, nasazením nebo při onboardingu

# Najdi všechny .py soubory mimo __pycache__, migrace a venv
PYFILES=$(find . \( -path "*/__pycache__/*" -o -path "*/migrations/*" -o -path "*/.venv/*" -o -path "*/venv/*" \) -prune -false -o -name "*.py" -type f)

if [[ -z "$PYFILES" ]]; then
  echo "Žádné .py soubory nebyly nalezeny."
  exit 0
fi

ERROR=0
echo "\n--- Kontrola syntaxe všech .py souborů ---"
for file in $PYFILES; do
  python3 -m py_compile "$file" 2>err.log
  if [[ $? -ne 0 ]]; then
    echo "[!] Syntax error: $file"
    cat err.log
    ERROR=1
  fi
done
rm -f err.log

if [[ $ERROR -eq 0 ]]; then
  echo "\n✓ Všechny .py soubory jsou bez syntax chyb."
else
  echo "\n[!] Některé soubory obsahují syntax chyby. Oprav je před commitem nebo nasazením!"
fi
