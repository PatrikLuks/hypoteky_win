#!/bin/zsh
# shrink_workspace_for_vscode.sh
# Skript pro minimalizaci workspace pro rychlý vývoj na MacBook Air a ve VS Code.
# Skryje snapshoty, zálohy, archivy a reporty, ponechá pouze klíčové soubory a složky.
# Autor: GitHub Copilot, 2025

set -euo pipefail

# Složky a soubory, které budou přesunuty do archivu mimo workspace
ARCHIVE_DIR="../_workspace_archive_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$ARCHIVE_DIR"

# Seznam vzorů k přesunu
PATTERNS=(
  "snapshot_html_*"
  "snapshot_html_backup_*"
  "snapshot_backups_*"
  "pa11y_a11y_reports_*"
  "*.zip"
  "*.gz"
  "*.bak*"
  "backup_workspace_*"
  "test-results"
)

for pattern in "${PATTERNS[@]}"; do
  for item in $pattern; do
    if [[ -e "$item" ]]; then
      echo "Přesouvám $item do $ARCHIVE_DIR"
      mv "$item" "$ARCHIVE_DIR/"
    fi
  done
done

echo "Workspace byl zmenšen. Archiv najdeš v $ARCHIVE_DIR. Pro běžný vývoj používej pouze klíčové složky a soubory."
