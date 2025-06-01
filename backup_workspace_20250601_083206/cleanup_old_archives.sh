#!/bin/zsh
# Skript pro úklid starých záloh snapshotů a reportů (starších než 14 dní)
# Přesune je do složky archive/ nebo nabídne k bezpečnému smazání
# Použití: ./cleanup_old_archives.sh

ARCHIVE_DIR="archive"
mkdir -p "$ARCHIVE_DIR"

# Najdi a přesun složky/soubory starší než 14 dní
find . -maxdepth 1 \
  \( -name 'snapshot_backups_*' -o -name 'snapshot_html_*' -o -name 'pa11y_a11y_reports_*' \) \
  -type d -mtime +14 \
  -exec mv {} "$ARCHIVE_DIR/" \; -print

find . -maxdepth 1 \
  \( -name 'snapshot_html_*.zip' -o -name 'pa11y_a11y_reports_*.zip' \) \
  -type f -mtime +14 \
  -exec mv {} "$ARCHIVE_DIR/" \; -print

echo "Hotovo! Staré zálohy a reporty byly přesunuty do složky $ARCHIVE_DIR. Zkontroluj ji a případně smaž, co už nepotřebuješ."
