#!/bin/zsh
# cleanup_bak_files.sh
# Skript pro bezpečné nalezení a mazání všech *.bak* souborů ve workspace i zálohách.
# Optimalizováno pro MacBook Air, bezpečné, bez automatického mazání.
# Použití: ./cleanup_bak_files.sh [--delete]
# Autor: GitHub Copilot, 2025

set -euo pipefail

# Najdi všechny .bak* soubory (včetně záloh)
find_bak_files() {
  echo "\n--- Hledání *.bak* souborů ve workspace a zálohách ---"
  find . -type f -name "*.bak*"
}

# Bezpečné mazání .bak* souborů (s potvrzením)
delete_bak_files() {
  echo "\n--- MAZÁNÍ .bak* SOUBORŮ (nutné potvrzení) ---"
  find . -type f -name "*.bak*" -exec rm -i {} +
  echo "Hotovo. .bak* soubory byly odstraněny."
}

# Hlavní logika
case "${1:-}" in
  --delete)
    find_bak_files
    delete_bak_files
    ;;
  *)
    find_bak_files
    echo "\nPro smazání všech .bak* souborů spusťte: $0 --delete"
    ;;
esac

# Konec skriptu
