#!/bin/zsh
# Skript pro úklid záložních snapshotů (bak, bak2, bak_fix, bak_autofix_*)
# Všechny zálohy přesune do složky snapshot_backups_YYYYMMDD/
# Použití: ./cleanup_snapshot_backups.sh

BACKUP_DIR="snapshot_backups_$(date +%Y%m%d)"
mkdir -p "$BACKUP_DIR"

# Přesun všech záložních snapshotů
for f in *_snapshot.html.bak*; do
  if [[ -f "$f" ]]; then
    mv "$f" "$BACKUP_DIR/"
    echo "Přesunuto: $f -> $BACKUP_DIR/"
  fi
done

echo "Hotovo! Všechny záložní snapshoty jsou nyní ve složce $BACKUP_DIR."
