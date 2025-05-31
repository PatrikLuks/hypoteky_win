#!/bin/zsh
# cleanup_duplicates_and_empty.sh
# Skript pro nalezení a bezpečný úklid duplicitních a prázdných souborů ve workspace.
# Optimalizováno pro MacBook Air, bezpečné, bez automatického mazání.
# Použití: ./cleanup_duplicates_and_empty.sh [--delete-duplicates] [--delete-empty]
# Autor: GitHub Copilot, 2025

set -euo pipefail

# Funkce pro nalezení duplicitních souborů (podle obsahu)
find_duplicates() {
  echo "\n--- Hledání duplicitních souborů ---"
  fdupes -r . || echo "(Nástroj fdupes není nainstalován, použijte 'brew install fdupes')"
}

# Funkce pro nalezení prázdných souborů (kromě .gitkeep apod.)
find_empty() {
  echo "\n--- Hledání prázdných souborů ---"
  find . -type f -empty ! -name ".gitkeep" ! -path "*/.venv/*"
}

# Bezpečné mazání duplicit (pouze pokud je zadán parametr)
delete_duplicates() {
  echo "\n--- MAZÁNÍ DUPLIKÁTŮ (nutné potvrzení) ---"
  echo "Tato funkce není ve výchozím stavu aktivní. Pro ruční mazání použijte fdupes -d."
}

# Bezpečné mazání prázdných souborů (pouze pokud je zadán parametr)
delete_empty() {
  echo "\n--- MAZÁNÍ PRÁZDNÝCH SOUBORŮ ---"
  find . -type f -empty ! -name ".gitkeep" ! -path "*/.venv/*" -exec rm -i {} +
}

# Hlavní logika
case "${1:-}" in
  --delete-duplicates)
    find_duplicates
    delete_duplicates
    ;;
  --delete-empty)
    find_empty
    delete_empty
    ;;
  *)
    find_duplicates
    find_empty
    echo "\nPro smazání duplicitních souborů spusťte: $0 --delete-duplicates"
    echo "Pro smazání prázdných souborů spusťte: $0 --delete-empty"
    ;;
esac

# Konec skriptu
