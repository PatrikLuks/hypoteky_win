#!/bin/zsh
# restore_archives.sh
# Rychlá obnova snapshotů nebo a11y reportů ze ZIP archivů do workspace
# Používej při review, onboardingu nebo troubleshooting

# Výběr archivu
echo "Vyber archiv k rozbalení:"
echo "1) Snapshoty UI (snapshot_html_YYYY-MM-DD.zip)"
echo "2) a11y reporty (pa11y_a11y_reports_YYYY-MM-DD.zip)"
read "choice?Zadej číslo (1/2): "

if [[ "$choice" == "1" ]]; then
  archive=$(ls snapshot_html_*.zip 2>/dev/null | tail -n 1)
  target_dir="snapshot_html_$(date +%Y-%m-%d)"
  typ="snapshoty UI"
elif [[ "$choice" == "2" ]]; then
  archive=$(ls pa11y_a11y_reports_*.zip 2>/dev/null | tail -n 1)
  target_dir="pa11y_a11y_reports_$(date +%Y-%m-%d)"
  typ="a11y reporty"
else
  echo "[!] Neplatná volba. Ukončuji."
  exit 1
fi

if [[ ! -f "$archive" ]]; then
  echo "[!] Archiv $archive nebyl nalezen. Ujisti se, že existuje v aktuálním adresáři."
  exit 1
fi

# Rozbalení archivu
unzip -n "$archive" -d "$target_dir"
echo "\nArchiv $archive byl rozbalen do složky $target_dir."
echo "Najdeš zde HTML snapshoty/reporty pro vizuální kontrolu."
echo "Například otevři v prohlížeči:"
echo "  open $target_dir/klient_list_snapshot.html.gz (nejprve gunzip)"
echo "  gunzip $target_dir/klient_list_snapshot.html.gz && open $target_dir/klient_list_snapshot.html"

echo "\nHotovo! Pro další použití uprav tento skript dle potřeby."
