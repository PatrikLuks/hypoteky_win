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

# --- Záloha snapshotů před testy ---
if [ -f cleanup_snapshot_backups.sh ]; then
  echo "\n--- Zálohuji snapshoty ---"
  chmod +x ./cleanup_snapshot_backups.sh
  ./cleanup_snapshot_backups.sh
else
  echo "\n--- Skript cleanup_snapshot_backups.sh nenalezen, záloha snapshotů přeskočena ---"
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

# --- Validace HTML snapshotů po testech ---
if [ -f check_html_validity.sh ]; then
  echo "\n--- Kontroluji validitu HTML snapshotů ---"
  chmod +x ./check_html_validity.sh
  ./check_html_validity.sh || { echo "[!] Chyba v HTML snapshotu!"; }
else
  echo "\n--- Skript check_html_validity.sh nenalezen, validace HTML přeskočena ---"
fi

echo "\n--- Úklid workspace ---"
chmod +x ./cleanup_workspace.sh
./cleanup_workspace.sh

# --- Úklid starých záloh a archivů ---
if [ -f cleanup_old_archives.sh ]; then
  echo "\n--- Mažu staré zálohy a archivy ---"
  chmod +x ./cleanup_old_archives.sh
  ./cleanup_old_archives.sh
else
  echo "\n--- Skript cleanup_old_archives.sh nenalezen, úklid archivů přeskočen ---"
fi

echo "\n--- Vše hotovo! ---"
echo "Pokud některé testy selhaly, zkontroluj výstup výše nebo použij troubleshooting checklist v tests/!"
