#!/bin/zsh
# fix_file_permissions.sh
# Nastaví správná práva pro skripty, testy, checklisty a šablony ve workspace
# Používej po klonování, migraci nebo před CI/CD

# Spustitelné skripty
find . -type f -name "*.sh" -exec chmod 755 {} \;
echo "Nastaveno chmod 755 pro všechny .sh skripty."

# Běžné soubory (čtení/zápis pro uživatele)
find . \( -name "*.py" -o -name "*.md" -o -name "*.html" -o -name "*.txt" -o -name "*.ini" -o -name "*.csv" -o -name "*.yml" -o -name "*.json" \) -type f -exec chmod 644 {} \;
echo "Nastaveno chmod 644 pro .py, .md, .html, .txt, .ini, .csv, .yml, .json soubory."

# Výpis změn
find . -type f \( -perm 755 -o -perm 644 \) -print | grep -E '\.sh$|\.py$|\.md$|\.html$|\.txt$|\.ini$|\.csv$|\.yml$|\.json$'

echo "\nHotovo! Práva souborů jsou nastavena pro bezpečné sdílení a provoz."
