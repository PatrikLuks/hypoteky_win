#!/bin/zsh
# Skript pro kontrolu validity všech hlavních HTML snapshotů pomocí nástroje 'tidy'
# Vyžaduje: tidy (nainstaluj např. 'brew install tidy-html5')

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

EXITCODE=0

echo "Kontroluji validitu HTML snapshotů..."
for file in $SNAPSHOTS; do
  if [[ -f "$file" ]]; then
    echo "\n--- $file ---"
    tidy -errors -quiet "$file"
    if [[ $? -ne 0 ]]; then
      echo "Chyby ve $file!"
      EXITCODE=1
    else
      echo "OK: $file je validní HTML."
    fi
  else
    echo "Soubor $file neexistuje."
  fi
done

if [[ $EXITCODE -eq 0 ]]; then
  echo "\nVšechny snapshoty jsou validní HTML!"
else
  echo "\nNěkteré snapshoty obsahují chyby. Oprav je podle výpisu výše."
fi

exit $EXITCODE
