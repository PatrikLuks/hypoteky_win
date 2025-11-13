#!/bin/zsh
# show_all_checklists.sh
# Rychlé zobrazení všech checklistů v adresáři tests/ v terminálu
# Používej při onboardingu, review, testování nebo plánování

CHECKLIST_DIR="tests"
echo "\n--- Výpis všech checklistů v $CHECKLIST_DIR/ ---"

for file in $CHECKLIST_DIR/*checklist.md; do
  if [[ -f "$file" ]]; then
    echo "\n==================== $(basename "$file") ===================="
    cat "$file"
    echo "\n-------------------------------------------------------------"
  fi
done

# --- Výpis hlavních checklistů a README z kořenového adresáře ---
MAIN_CHECKLISTS=(
  "README.md"
  "README_snapshot_a11y_management.md"
  "SNAPSHOT_A11Y_WORKFLOW_CHECKLIST.md"
  "E2E_TESTING_CHECKLIST.md"
)

for file in $MAIN_CHECKLISTS; do
  if [ -f "$file" ]; then
    echo "\n==================== $file ===================="
    cat "$file"
    echo "\n-------------------------------------------------------------"
  fi
done

# Nové sekce: onboarding, TODO, shell skripty, testy

# Najdi a vypiš všechny onboarding sekce a best practices
 echo "\n--- [ONBOARDING, BEST PRACTICES] ---"
grep -i -H -A 3 'onboard\|best practice' *.md README* *.txt 2>/dev/null || echo "[Žádné onboarding/best practices v .md/.txt nenalezeny]"

# Najdi a vypiš všechny TODO v kódu a skriptech
echo "\n--- [TODO v kódu a skriptech] ---"
grep -r -n --color=always 'TODO' . | grep -v '.venv/' || echo "[Žádné TODO nenalezeny]"

# Vypiš souhrn všech shell skriptů pro údržbu
echo "\n--- [SHELL SKRIPTY PRO ÚDRŽBU] ---"
ls -1 *.sh | grep -v '.venv/' || echo "[Žádné shell skripty nenalezeny]"

# Vypiš souhrn všech testovacích souborů
echo "\n--- [TESTOVACÍ SOUBORY] ---"
ls -1 klienti/tests_*.py tests/*.py 2>/dev/null || echo "[Žádné testovací soubory nenalezeny]"

echo "\nHotovo! Pro detailní práci otevři konkrétní checklist nebo README v editoru."
