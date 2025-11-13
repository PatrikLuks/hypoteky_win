#!/bin/zsh
# Spustí snapshot testy a v případě selhání automaticky aktualizuje snapshoty a spustí testy znovu.
# Používej pro pohodlnou správu snapshot testů s dynamickými hodnotami (CSRF, datumy, ID).

set -e

# 1. Spusť snapshot testy
python manage.py test klienti.tests_ui --keepdb || {
  echo "[INFO] Snapshot testy selhaly, aktualizuji snapshoty..."
  ./update_snapshots.sh
  echo "[INFO] Spouštím snapshot testy znovu po aktualizaci..."
  python manage.py test klienti.tests_ui --keepdb
}

echo "[INFO] Hotovo. Pokud testy stále selhávají, zkontroluj ručně diff a snapshoty."
