#!/bin/zsh
# Popis: Úklid workspace – odstranění dočasných, zálohovacích a nepotřebných souborů.
# Autor: Patrik Luks, 2025
# Tento skript smaže soubory typu *.pyc, *~, zálohy a další nečistoty.
# cleanup_workspace.sh
# Automatizovaný úklid workspace pro projekt hypoteky (macOS, zsh)
# Smaže dočasné a nepotřebné soubory, zkomprimuje nové reporty a snapshoty
# Spouštěj ručně nebo nastav jako cron úlohu

# Smazání dočasných a nepotřebných souborů
echo "Mazání .bak, .log, .pyc, __pycache__, PNG..."
find . -name '*.bak' -delete
find . -name '*.log' -delete
find . -name '*.pyc' -delete
find . -name '__pycache__' -type d -exec rm -r {} +
find . -name '*.png' -delete

# Smazání starých snapshotů a reportů (starších než 14 dní)
echo "Mazání starých snapshotů a reportů (starších než 14 dní)..."
find . -type f -name '*snapshot*.gz' -mtime +14 -delete
find . -type f -name '*report*.gz' -mtime +14 -delete

# Komprese nových snapshotů a reportů (pokud existují nové složky)
SNAPSHOT_DIR="snapshot_html_$(date +%Y-%m-%d)"
A11Y_DIR="pa11y_a11y_reports_$(date +%Y-%m-%d)"

if [ -d "$SNAPSHOT_DIR" ]; then
  echo "Archivace snapshotů do $SNAPSHOT_DIR.zip..."
  zip -r "$SNAPSHOT_DIR.zip" "$SNAPSHOT_DIR" 2>/dev/null
fi
if [ -d "$A11Y_DIR" ]; then
  echo "Archivace a11y reportů do $A11Y_DIR.zip..."
  zip -r "$A11Y_DIR.zip" "$A11Y_DIR" 2>/dev/null
fi

echo "Úklid dokončen."

# Poznámka: Skript spouštěj z kořenového adresáře projektu.
# Pro automatizaci přidej do crontab: crontab -e
# 0 1 * * * /Users/patrikluks/Applications/hypoteky/cleanup_workspace.sh
