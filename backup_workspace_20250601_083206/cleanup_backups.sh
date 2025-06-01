#!/bin/zsh
# cleanup_backups.sh
# Skript pro bezpečné nalezení a přesun/mazání záložních složek (backup_workspace_*) z hlavního workspace.
# Optimalizováno pro MacBook Air, bezpečné, bez automatického mazání.
# Použití: ./cleanup_backups.sh [--move <cesta>] [--delete]
# Autor: GitHub Copilot, 2025

set -euo pipefail

# Najdi všechny záložní složky v aktuálním workspace
find_backups() {
  echo "\n--- Hledání záložních složek (backup_workspace_*) ---"
  find . -maxdepth 1 -type d -name "backup_workspace_*"
}

# Bezpečný přesun záloh do zadané složky
move_backups() {
  local target="$1"
  echo "\n--- Přesouvání záloh do $target ---"
  mkdir -p "$target"
  for dir in $(find . -maxdepth 1 -type d -name "backup_workspace_*"); do
    mv -i "$dir" "$target/"
  done
  echo "Hotovo. Zálohy byly přesunuty."
}

# Bezpečné mazání záloh (s potvrzením)
delete_backups() {
  echo "\n--- MAZÁNÍ ZÁLOH (nutné potvrzení) ---"
  for dir in $(find . -maxdepth 1 -type d -name "backup_workspace_*"); do
    rm -ri "$dir"
  done
  echo "Hotovo. Zálohy byly odstraněny."
}

# Hlavní logika
case "${1:-}" in
  --move)
    if [ -z "${2:-}" ]; then
      echo "Chybí cílová složka pro přesun!"
      exit 1
    fi
    find_backups
    move_backups "$2"
    ;;
  --delete)
    find_backups
    delete_backups
    ;;
  *)
    find_backups
    echo "\nPro přesun záloh spusťte: $0 --move /cesta/k/archivu"
    echo "Pro smazání záloh spusťte: $0 --delete"
    ;;
esac

# Konec skriptu
