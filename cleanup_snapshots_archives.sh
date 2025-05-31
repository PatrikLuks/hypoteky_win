# Automatizované mazání snapshotů, záloh, archivů a reportů pro čistý workspace
# Spouštěj pravidelně pro udržení svižného vývoje na MacBook Air

rm -rf snapshot_html_* snapshot_html_backup_* snapshot_backups_* pa11y_a11y_reports_* *.zip *.bak *.backup *.report.html

echo "Workspace byl vyčištěn od snapshotů, záloh, archivů a reportů."
