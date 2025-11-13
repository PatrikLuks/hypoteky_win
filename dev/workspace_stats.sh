#!/bin/zsh
# workspace_stats.sh
# Rychlý přehled o velikosti a počtu souborů ve snapshot, report a test složkách workspace
# Používej pro úklid, troubleshooting nebo před zálohou

# Výpis velikostí klíčových složek

echo "\n--- Velikost složek (du -sh) ---"
du -sh snapshot_html_*/ pa11y_a11y_reports_*/ tests/ *.zip 2>/dev/null

echo "\n--- Počet souborů ve snapshot a report složkách ---"
echo "Snapshoty:   $(find snapshot_html_*/ -type f 2>/dev/null | wc -l)"
echo "A11y reporty: $(find pa11y_a11y_reports_*/ -type f 2>/dev/null | wc -l)"
echo "Testy:       $(find tests/ -type f 2>/dev/null | wc -l)"
echo "Archivy:     $(ls *.zip 2>/dev/null | wc -l)"

echo "\n--- Největší soubory ve workspace (top 10) ---"
find . -type f -exec du -h {} + 2>/dev/null | sort -hr | head -n 10

# Počet snapshotů v kořenovém adresáři
SNAPSHOTS=$(ls *_snapshot.html 2>/dev/null | wc -l)
echo "\nPočet snapshotů v kořenovém adresáři: $SNAPSHOTS"

# Počet shell skriptů
SH_SCRIPTS=$(ls *.sh 2>/dev/null | wc -l)
echo "Počet shell skriptů: $SH_SCRIPTS"

# Počet TODO v kódu
TODO_COUNT=$(grep -r --exclude-dir=.venv --exclude-dir=backup_workspace_* 'TODO' . | wc -l)
echo "Počet TODO v kódu: $TODO_COUNT"

# Poslední záloha a její velikost
LATEST_BACKUP=$(ls -dt backup_workspace_* 2>/dev/null | head -n1)
if [ -n "$LATEST_BACKUP" ]; then
  echo "\nPoslední záloha: $LATEST_BACKUP"
  du -sh "$LATEST_BACKUP"
fi

# Git stav
if [ -d .git ]; then
  echo "\n--- Git stav ---"
  git status -s
  echo "\nPoslední commity:"
  git --no-pager log --oneline -5
fi

echo "\n--- Doporučení ---"
echo "Pokud některá složka nebo soubor zabírá neobvykle mnoho místa, zvaž úklid nebo archivaci."
echo "Pro úklid použij ./cleanup_workspace.sh, pro zálohu ./backup_workspace.sh."
