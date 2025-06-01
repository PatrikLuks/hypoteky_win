#!/bin/zsh
# cleanup_snapshots_archives.sh – skript pro automatizované mazání snapshotů, záloh, archivů a reportů
# Spouštěj pravidelně pro udržení svižného vývoje na MacBook Air
# Odstraňuje snapshoty, zálohy, archivy a reporty z workspace
# Autor: automatická optimalizace Copilot

rm -rf snapshot_html_* snapshot_html_backup_* snapshot_backups_* pa11y_a11y_reports_* *.zip *.bak *.backup *.report.html

echo "Workspace byl vyčištěn od snapshotů, záloh, archivů a reportů."
