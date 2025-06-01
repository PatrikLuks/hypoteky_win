#!/bin/zsh
# check_pytest_env.sh – skript pro ověření, že pytest je nainstalován a testy jsou spustitelné
# Používej před commitem, nasazením nebo při onboardingu
# Kontroluje testovací soubory v klienti/ a tests/
# Autor: automatická optimalizace Copilot

# Ověření pytestu
if ! command -v pytest &> /dev/null; then
  echo "[!] pytest není nainstalován. Instaluj ho: pip install pytest"
  exit 1
fi

echo "\n--- Kontrola testovacích souborů v klienti/ a tests/ ---"

ERROR=0
for file in klienti/test*.py klienti/tests_*.py tests/test*.py; do
  if [[ -f "$file" ]]; then
    echo "\n>>> pytest $file"
    pytest "$file" --maxfail=1 --disable-warnings
    if [[ $? -ne 0 ]]; then
      echo "[!] Chyba při spouštění testu: $file"
      ERROR=1
    fi
  fi
done

if [[ $ERROR -eq 0 ]]; then
  echo "\n✓ Všechny testy jsou spustitelné a prostředí je připravené."
else
  echo "\n[!] Některé testy selhaly nebo nejsou spustitelné. Oprav je před commitem nebo nasazením!"
fi
