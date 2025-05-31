#!/bin/zsh
# check_current_snapshots.sh
# Ověří, že ve workspace existují aktuální snapshoty a a11y reporty pro dnešní datum
# Používej před commitem, review, archivací nebo sdílením

DNES=$(date +%Y-%m-%d)
SNAPSHOT_DIR="snapshot_html_$DNES"
A11Y_DIR="pa11y_a11y_reports_$DNES"
SNAPSHOT_ZIP="snapshot_html_$DNES.zip"
A11Y_ZIP="pa11y_a11y_reports_$DNES.zip"

echo "\n--- Kontrola aktuálních snapshotů a a11y reportů pro $DNES ---"

if [[ -d "$SNAPSHOT_DIR" ]]; then
  echo "[OK] Složka $SNAPSHOT_DIR existuje."
else
  echo "[!] Složka $SNAPSHOT_DIR chybí! Vygeneruj aktuální snapshoty."
fi

if [[ -d "$A11Y_DIR" ]]; then
  echo "[OK] Složka $A11Y_DIR existuje."
else
  echo "[!] Složka $A11Y_DIR chybí! Spusť pa11y_batch.sh pro aktuální reporty."
fi

if [[ -f "$SNAPSHOT_ZIP" ]]; then
  echo "[OK] Archiv $SNAPSHOT_ZIP existuje."
else
  echo "[!] Archiv $SNAPSHOT_ZIP chybí! Archivuj aktuální snapshoty."
fi

if [[ -f "$A11Y_ZIP" ]]; then
  echo "[OK] Archiv $A11Y_ZIP existuje."
else
  echo "[!] Archiv $A11Y_ZIP chybí! Archivuj aktuální a11y reporty."
fi

echo "\n--- Doporučení ---"
echo "Pokud některá aktuální data chybí, spusť příslušné skripty pro jejich vygenerování a archivaci."
echo "  ./pa11y_batch.sh && ./cleanup_workspace.sh"
echo "  zip -r $SNAPSHOT_ZIP $SNAPSHOT_DIR"
echo "  zip -r $A11Y_ZIP $A11Y_DIR"
