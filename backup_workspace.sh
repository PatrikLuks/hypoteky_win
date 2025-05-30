#!/bin/zsh
# backup_workspace.sh
# Rychlá záloha klíčových souborů workspace do datovaného ZIP archivu
# Používej před většími změnami, sdílením nebo migrací projektu

BACKUP_NAME="hypoteky_backup_$(date +%Y-%m-%d).zip"

if [[ -f "$BACKUP_NAME" ]]; then
  echo "[!] Archiv $BACKUP_NAME již existuje. Přepiš nebo přejmenuj starý archiv."
  exit 1
fi

zip -r "$BACKUP_NAME" \
  README.md \
  requirements.txt \
  cleanup_workspace.sh \
  run_all_checks.sh \
  restore_archives.sh \
  klienti/tests_*.py \
  klienti/utils.py \
  klienti/models.py \
  klienti/serializers.py \
  klienti/permissions.py \
  klienti/views.py \
  klienti/api_views.py \
  klienti/api_urls.py \
  klienti/tests/ \
  snapshot_html_*/ \
  pa11y_a11y_reports_*/ \
  tests/ \
  *.md \
  *.sh \
  DB_SETUP_MYSQL.md \
  sample_data.py \
  create_userprofiles.py \
  pytest.ini \
  hypoteky/ \
  --exclude=*.pyc --exclude=__pycache__ --exclude=*.log

if [[ $? -eq 0 ]]; then
  echo "\nZáloha úspěšně vytvořena: $BACKUP_NAME"
  echo "Archiv obsahuje snapshoty, reporty, testy, checklisty, skripty a klíčové soubory projektu."
else
  echo "[!] Chyba při vytváření zálohy. Zkontroluj práva a volné místo na disku."
fi
