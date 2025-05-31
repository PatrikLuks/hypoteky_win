#!/bin/zsh
# Obnova workspace ze zvolené zálohy backup_workspace_YYYYMMDD_HHMMSS/
# Autor: GitHub Copilot, 2025

# Najdi dostupné zálohy
BACKUPS=(backup_workspace_20*)

if [ ${#BACKUPS[@]} -eq 0 ]; then
  echo "[!] Nebyla nalezena žádná záloha backup_workspace_YYYYMMDD_HHMMSS/"
  exit 1
fi

echo "Dostupné zálohy:"
select BACKUP in "${BACKUPS[@]}"; do
  if [ -n "$BACKUP" ]; then
    echo "Vybraná záloha: $BACKUP"
    break
  fi
done

read "?Opravdu chceš obnovit workspace ze zálohy $BACKUP? (přepíše aktuální soubory) [y/N]: " CONFIRM
if [[ ! "$CONFIRM" =~ ^[Yy]$ ]]; then
  echo "Obnova zrušena."
  exit 0
fi

# Obnova souborů (bez mazání nových souborů, pouze přepis existujících)
cp -iv "$BACKUP"/* .

# Obnova složek (pouze pokud existují v záloze)
for DIR in snapshot_backups_* snapshot_html_* pa11y_a11y_reports_* test-results tests; do
  if [ -d "$BACKUP/$DIR" ]; then
    cp -Riv "$BACKUP/$DIR" .
  fi
done

echo "\n✅ Obnova workspace ze zálohy $BACKUP dokončena. Zkontroluj stav a spusť testy!"
