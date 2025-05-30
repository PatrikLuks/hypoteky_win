#!/bin/zsh
# run_all_checks.sh
# Spustí všechny důležité testy a úklid workspace v jednom kroku
# Používej před commitem, nasazením nebo při onboardingu nového vývojáře

# Aktivace virtuálního prostředí
if [ -d "venv" ]; then
  source venv/bin/activate
elif [ -d ".venv" ]; then
  source .venv/bin/activate
else
  echo "[!] Virtuální prostředí nebylo nalezeno. Vytvoř ho příkazem: python3 -m venv venv"
  exit 1
fi

echo "\n--- Spouštím unit/integration testy (pytest) ---"
pytest || { echo "[!] Některé testy selhaly!"; }

echo "\n--- Spouštím edge-case testy import/export, API, bezpečnost ---"
pytest klienti/tests_import_csv.py klienti/tests_import_xlsx.py klienti/tests_api.py klienti/tests_bezpecnost.py klienti/tests_reporting_export.py || { echo "[!] Některé edge-case testy selhaly!"; }

echo "\n--- Spouštím a11y testy (pa11y_batch.sh) ---"
chmod +x ./pa11y_batch.sh
./pa11y_batch.sh || { echo "[!] Některé a11y testy selhaly!"; }

echo "\n--- Spouštím e2e testy (Playwright) ---"
python tests_e2e_playwright.py || { echo "[!] Některé e2e testy selhaly!"; }

echo "\n--- Úklid workspace ---"
chmod +x ./cleanup_workspace.sh
./cleanup_workspace.sh

echo "\n--- Vše hotovo! ---"
echo "Pokud některé testy selhaly, zkontroluj výstup výše nebo použij troubleshooting checklist v tests/!"
