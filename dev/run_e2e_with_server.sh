#!/bin/zsh
# Skript: run_e2e_with_server.sh
# Popis: Spustí Django server na pozadí a následně E2E/UI testy Playwright (pytest). Po dokončení testů server ukončí.
# Autor: GitHub Copilot, 2025

set -e

# Aktivace virtuálního prostředí
source .venv/bin/activate

# Spuštění Django serveru na pozadí
python manage.py runserver 0.0.0.0:8000 &
DJANGO_PID=$!

# Počkej, než server naběhne
sleep 5

# Ověření dostupnosti serveru
for i in {1..10}; do
  if curl -s http://localhost:8000/login/ | grep -q '<form'; then
    echo "[OK] Django server je dostupný."
    break
  fi
  echo "[WAIT] Čekám na spuštění serveru... ($i/10)"
  sleep 1
done

# Spuštění E2E/UI testů
pytest tests_e2e_playwright.py -v
TEST_RESULT=$?

# Ukončení serveru
kill $DJANGO_PID
wait $DJANGO_PID 2>/dev/null || true

exit $TEST_RESULT
