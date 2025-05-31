#!/bin/zsh
# Skript pro automatickou opravu nejčastějších HTML chyb ve snapshot souborech
# - escapuje neescapované & na &amp;
# - odstraní neplatné znaky (kód 141, 153, 155, 128, 147, 140, 154)
# - upozorní na neznámé tagy (nav, canvas)
#
# Použití: ./fix_html_snapshot_issues.sh

SNAPSHOTS=(
  home_snapshot.html
  klient_detail_snapshot.html
  klient_confirm_delete_snapshot.html
  klient_form_snapshot.html
  klient_list_snapshot.html
  dashboard_snapshot.html
  kalkulacka_snapshot.html
  login_snapshot.html
  reporting_snapshot.html
)

for file in $SNAPSHOTS; do
  if [[ -f "$file" ]]; then
    echo "\n--- Opravuji $file ---"
    # Záloha
    cp "$file" "$file.bak_fix"
    # Escapování &display, &family, &subset atd. (nejčastější v Google Fonts)
    sed -i '' -E 's/&(display|family|subset|text|effect|amp;)/\&amp;\1/g' "$file"
    # Odstranění neplatných znaků (kód 128, 140, 141, 147, 153, 154, 155)
    perl -CSD -i -pe 's/[\x80\x8C\x8D\x93\x99\x9A\x9B]//g' "$file"
    # Upozornění na neznámé tagy (jen výpis)
    grep -Eo '<(/?)(nav|canvas)[^>]*>' "$file" | sort | uniq | while read tag; do
      echo "  Upozornění: nalezen tag $tag (ověř, zda je v pořádku podle HTML5)"
    done
    echo "  Opraveno: $file (záloha v $file.bak_fix)"
  else
    echo "Soubor $file neexistuje."
  fi
done

echo "\nHotovo! Pro kontrolu spusť znovu ./check_html_validity.sh."
