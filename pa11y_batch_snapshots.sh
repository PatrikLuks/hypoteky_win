#!/bin/zsh
# pa11y_batch_snapshots.sh
# Hromadná kontrola přístupnosti pro statické HTML snapshoty
# Výsledky ukládá do HTML reportů v aktuálním adresáři

SNAPSHOTS=(
  dashboard_snapshot.html
  home_snapshot.html
  klient_detail_snapshot.html
  klient_confirm_delete_snapshot.html
  kalkulacka_snapshot.html
  login_snapshot.html
  reporting_snapshot.html
)

for file in $SNAPSHOTS; do
  if [[ -f "$file" ]]; then
    outfile="pa11y_${file%.html}_report.html"
    echo "Testuji $file ..."
    pa11y "file://$PWD/$file" --reporter html > "$outfile"
    echo "Výsledek uložen do $outfile"
  else
    echo "[!] Soubor $file neexistuje, přeskočeno."
  fi

done

echo "Hotovo! Všechny reporty jsou v aktuálním adresáři."
