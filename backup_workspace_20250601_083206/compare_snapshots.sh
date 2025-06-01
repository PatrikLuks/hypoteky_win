#!/bin/zsh
# compare_snapshots.sh
# Porovná dva snapshoty nebo a11y reporty (ZIP archivy) a vypíše rozdíly v HTML souborech
# Ideální pro review, troubleshooting nebo vizuální kontrolu změn

# Výběr archivů
ls -1 snapshot_html_*.zip pa11y_a11y_reports_*.zip 2>/dev/null

echo "\nZadej název prvního archivu k porovnání (včetně .zip):"
read archiv1
if [[ ! -f "$archiv1" ]]; then
  echo "[!] Archiv $archiv1 nebyl nalezen."
  exit 1
fi

echo "Zadej název druhého archivu k porovnání (včetně .zip):"
read archiv2
if [[ ! -f "$archiv2" ]]; then
  echo "[!] Archiv $archiv2 nebyl nalezen."
  exit 1
fi

# Rozbalení do dočasných složek
tmp1=$(mktemp -d)
tmp2=$(mktemp -d)
unzip -q "$archiv1" -d "$tmp1"
unzip -q "$archiv2" -d "$tmp2"

echo "\nPorovnávám HTML soubory v $archiv1 a $archiv2..."

# Porovnání všech HTML(.gz) souborů podle jména
for file in $(find "$tmp1" -name '*.html.gz' -exec basename {} \; | sort | uniq); do
  f1=$(find "$tmp1" -name "$file" | head -n1)
  f2=$(find "$tmp2" -name "$file" | head -n1)
  if [[ -f "$f1" && -f "$f2" ]]; then
    gunzip -c "$f1" > "$tmp1/$file.html"
    gunzip -c "$f2" > "$tmp2/$file.html"
    diffout=$(diff -q "$tmp1/$file.html" "$tmp2/$file.html")
    if [[ -n "$diffout" ]]; then
      echo "Rozdíl v $file:"
      diff -u "$tmp1/$file.html" "$tmp2/$file.html" | head -n 20
      echo "... (použij vimdiff $tmp1/$file.html $tmp2/$file.html pro detailní porovnání)"
    fi
  fi
done

echo "\nPorovnání dokončeno. Dočasné složky: $tmp1 $tmp2"
echo "Pro detailní diff použij např.: vimdiff $tmp1/klient_list_snapshot.html $tmp2/klient_list_snapshot.html"
echo "Po kontrole můžeš složky smazat: rm -r $tmp1 $tmp2"
