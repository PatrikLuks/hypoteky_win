#!/bin/zsh
# check_duplicate_files.sh
# Najde soubory se stejným názvem (bez ohledu na příponu) v celém workspace
# Používej před refaktoringem, sdílením nebo troubleshootingem

ERROR=0

echo "\n--- Kontrola duplicitních souborů ve workspace ---"

# Najdi všechny soubory, extrahuj basename bez přípony, spočítej výskyty
find . -type f \
  ! -path "*/.venv/*" ! -path "*/venv/*" ! -path "*/__pycache__/*" ! -path "*/migrations/*" \
  | awk -F/ '{print $NF}' | sed 's/\.[^.]*$//' | sort | uniq -d | while read name; do
    echo "[!] Duplicitní název: $name"
    find . -type f -name "$name.*" \
      ! -path "*/.venv/*" ! -path "*/venv/*" ! -path "*/__pycache__/*" ! -path "*/migrations/*"
    ERROR=1
  done

if [[ $ERROR -eq 0 ]]; then
  echo "\n✓ Ve workspace nejsou žádné duplicitní názvy souborů."
else
  echo "\n[!] Některé soubory mají duplicitní názvy! Zkontroluj je a zvaž sloučení nebo odstranění duplicit."
fi
