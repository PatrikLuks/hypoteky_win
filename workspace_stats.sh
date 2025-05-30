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

echo "\n--- Doporučení ---"
echo "Pokud některá složka nebo soubor zabírá neobvykle mnoho místa, zvaž úklid nebo archivaci."
echo "Pro úklid použij ./cleanup_workspace.sh, pro zálohu ./backup_workspace.sh."
