#!/bin/zsh
# Skript pro automatickou aktualizaci HTML snapshotů po běhu testů (macOS/zsh)
# 1. Zálohuje aktuální snapshoty
# 2. Přepíše je aktuálními verzemi ze snapshot_html_<dnesni datum>/, pokud existují
# 3. Vypíše změny

set -e

SNAPSHOT_DIR="snapshot_html_$(date +%Y-%m-%d)"
BACKUP_DIR="snapshot_html_backup_$(date +%Y-%m-%d)"

# Záloha aktuálních snapshotů
echo "[INFO] Zálohuji snapshoty do $BACKUP_DIR"
mkdir -p "$BACKUP_DIR"
cp *_snapshot.html "$BACKUP_DIR" 2>/dev/null || echo "[INFO] Žádné snapshoty k zálohování."

# Pokud existuje adresář s aktuálními snapshoty, přepiš je
echo "[INFO] Aktualizuji snapshoty ze složky $SNAPSHOT_DIR (pokud existuje)"
if [[ -d "$SNAPSHOT_DIR" ]]; then
  for f in $SNAPSHOT_DIR/*_snapshot.html(.N); do
    if [[ -f "$f" ]]; then
      cp -v "$f" .
    fi
  done
else
  echo "[INFO] Složka $SNAPSHOT_DIR neexistuje, snapshoty nebyly přepsány."
fi

echo "[INFO] Hotovo. Pokud chceš, spusť znovu testy: python manage.py test klienti.tests_ui --keepdb"
