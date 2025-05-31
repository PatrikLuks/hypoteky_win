#!/bin/zsh
# fix_unwanted_executable.sh
# Odebere spustitelné právo všem .py, .md, .html, .ini, .csv, .yml, .json souborům (ponechá pouze .sh skripty spustitelné)
# Používej pro bezpečnost, čistotu repozitáře a správné chování v CI/CD

# Najdi všechny soubory s nevhodným +x
find . \( -name "*.py" -o -name "*.md" -o -name "*.html" -o -name "*.ini" -o -name "*.csv" -o -name "*.yml" -o -name "*.json" \) -type f -perm +111 | while read file; do
  chmod 644 "$file"
  echo "Odebráno +x: $file"
done

echo "\nHotovo! Všechny neskriptové soubory mají nyní správná práva. .sh skripty zůstávají spustitelné."
