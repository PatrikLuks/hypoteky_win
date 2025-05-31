#!/bin/zsh
# Záloha celého workspace do časově označené složky
# Autor: GitHub Copilot, 2025

BACKUP_DIR="backup_workspace_$(date +%Y%m%d_%H%M%S)"
echo "Vytvářím zálohu do složky $BACKUP_DIR ..."

mkdir "$BACKUP_DIR"

# Zálohuj snapshoty
cp *.html "$BACKUP_DIR" 2>/dev/null
# Zálohuj reporty
cp pa11y_*.html "$BACKUP_DIR" 2>/dev/null
cp *.zip "$BACKUP_DIR" 2>/dev/null
# Zálohuj testy a skripty
cp *.py "$BACKUP_DIR" 2>/dev/null
cp *.sh "$BACKUP_DIR" 2>/dev/null
# Zálohuj checklisty a README
cp *.md "$BACKUP_DIR" 2>/dev/null
# Zálohuj důležité složky (testy, snapshoty, zálohy)
cp -r snapshot_backups_* "$BACKUP_DIR" 2>/dev/null
cp -r snapshot_html_* "$BACKUP_DIR" 2>/dev/null
cp -r pa11y_a11y_reports_* "$BACKUP_DIR" 2>/dev/null
cp -r test-results "$BACKUP_DIR" 2>/dev/null
cp -r tests "$BACKUP_DIR" 2>/dev/null

# Výpis obsahu zálohy
if [ -d "$BACKUP_DIR" ]; then
  echo "\nObsah zálohy $BACKUP_DIR:"
  ls -lh "$BACKUP_DIR"
  echo "\n✅ Záloha workspace dokončena."
else
  echo "Chyba při vytváření zálohy!"
fi
