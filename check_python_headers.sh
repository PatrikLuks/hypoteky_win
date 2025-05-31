#!/bin/zsh
# check_python_headers.sh
# Ověří, že všechny .py soubory mají správné kódování UTF-8 a spustitelné skripty správný shebang
# Používej před commitem, nasazením nebo při onboardingu

ERROR=0

echo "\n--- Kontrola kódování a shebangu v Python souborech ---"

PYFILES=$(find . \( -path "*/__pycache__/*" -o -path "*/migrations/*" -o -path "*/.venv/*" -o -path "*/venv/*" \) -prune -false -o -name "*.py" -type f)

for file in $PYFILES; do
  # Kontrola deklarace kódování UTF-8
  if ! head -n 2 "$file" | grep -q "coding[:=] *utf-8"; then
    echo "[!] $file nemá deklaraci kódování UTF-8 (doporučeno pro multiplatformní projekty)"
    ERROR=1
  fi
  # Kontrola shebangu pro spustitelné skripty (v kořeni, scripts, management/commands)
  if [[ "$file" =~ ^\./(create_userprofiles|sample_data|manage|check_db_integrity|test_all_scripts|.*management/commands/.*)\.py$ ]]; then
    FIRSTLINE=$(head -n 1 "$file")
    if [[ "$FIRSTLINE" != "#!/usr/bin/env python3" ]]; then
      echo "[!] $file nemá správný shebang (#!/usr/bin/env python3)"
      ERROR=1
    fi
  fi
done

if [[ $ERROR -eq 0 ]]; then
  echo "\n✓ Všechny .py soubory mají správné hlavičky."
else
  echo "\n[!] Některé soubory nemají správné hlavičky. Oprav je před commitem nebo nasazením!"
fi
