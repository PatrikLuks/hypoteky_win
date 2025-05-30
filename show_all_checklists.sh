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

echo "\nHotovo! Pro detailní práci otevři konkrétní checklist v editoru."
