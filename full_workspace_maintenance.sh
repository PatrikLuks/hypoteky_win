#!/bin/zsh
# full_workspace_maintenance.sh
# Kompletní údržba a rekapitulace stavu workspace v jednom kroku
# Spustí úklid, zálohu, statistiku, kontrolu integrity, TODO a checklisty

set -e

# Úklid workspace
echo "\n==================== ÚKLID WORKSPACE ===================="
chmod +x ./cleanup_workspace.sh
./cleanup_workspace.sh

# Záloha workspace
echo "\n==================== ZÁLOHA WORKSPACE ===================="
chmod +x ./backup_workspace.sh
./backup_workspace.sh || echo "[!] Záloha nebyla vytvořena (možná již existuje archiv pro dnešní datum)."

# Statistika workspace
echo "\n==================== STATISTIKA WORKSPACE ===================="
chmod +x ./workspace_stats.sh
./workspace_stats.sh

# Kontrola integrity DB
echo "\n==================== KONTROLA INTEGRITY DB ===================="
source venv/bin/activate && python check_db_integrity.py || echo "[!] Kontrola integrity DB selhala. Zkontroluj prostředí."

# Vyhledání TODO/FIXME
echo "\n==================== TODO / FIXME / POZNÁMKY ===================="
chmod +x ./find_todos.sh
./find_todos.sh

# Zobrazení checklistů
echo "\n==================== CHECKLISTY ===================="
chmod +x ./show_all_checklists.sh
./show_all_checklists.sh

echo "\n==================== HOTOVO! ===================="
echo "Kompletní údržba a rekapitulace workspace dokončena. Zkontroluj výstup výše a případné chyby oprav dle checklistů."
