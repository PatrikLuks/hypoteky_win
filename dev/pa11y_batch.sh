#!/bin/zsh
# Skript pro hromadné spuštění pa11y na klíčových stránkách projektu
# Výsledky ukládá do HTML reportů v aktuálním adresáři

URLS=(
  "http://localhost:8000/"
  "http://localhost:8000/login/"
  "http://localhost:8000/klienti/"
  "http://localhost:8000/admin/"
  "http://localhost:8000/klient/1/"
)

for url in $URLS; do
  # Vytvoř název souboru podle URL
  name=$(echo $url | sed 's|http://localhost:8000/||;s|/|_|g;s|^$|home|;s|_$||')
  if [[ "$name" == "" ]]; then name="home"; fi
  outfile="pa11y_${name}_report.html"
  echo "Testuji $url ..."
  pa11y "$url" --reporter html > "$outfile"
  echo "Výsledek uložen do $outfile"
done

echo "Hotovo! Všechny reporty jsou v aktuálním adresáři."
