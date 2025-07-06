#!/bin/bash
# Jednoduchý startovací skript pro vývojáře (macOS/Linux)
# Vytvoří venv, nainstaluje závislosti, provede migrace a spustí server

set -e

if [ ! -d ".venv" ]; then
  echo "[+] Vytvářím virtuální prostředí..."
  python3 -m venv .venv
fi

source .venv/bin/activate

echo "[+] Instalace závislostí..."
pip install -r requirements.txt

if [ ! -f ".env" ] && [ -f ".env.example" ]; then
  echo "[+] Kopíruji .env.example do .env (doporučujeme upravit)..."
  cp .env.example .env
fi

# Fallback na SQLite pokud není nastaveno DB v .env
if ! grep -q "DB_NAME" .env 2>/dev/null; then
  echo "[!] DB není nastavena, používám SQLite (pro testování)"
  export DJANGO_SETTINGS_MODULE=hypoteky.settings_sqlite
fi

echo "[+] Migrace DB..."
python manage.py migrate

if ! python manage.py showmigrations | grep "\[X\]" | grep admin > /dev/null; then
  echo "[+] Vytvářím superuživatele (admin:admin, změň si ho!)"
  echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@example.com', 'admin') if not User.objects.filter(username='admin').exists() else None" | python manage.py shell
fi

# Volitelně: python sample_data.py

echo "[+] Spouštím server na http://127.0.0.1:8000 ..."
python manage.py runserver
