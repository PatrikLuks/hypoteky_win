#!/bin/zsh
# find_todos.sh
# Rychlé vyhledání všech TODO, FIXME a poznámek v kódu workspace
# Používej pro správu technického dluhu, plánování a review

# Hledané klíčové slova
KEYWORDS="TODO|FIXME|# POZNÁMKA|# NOTE|# ÚKOL|# NÁVRH|# IDEA"

# Prohledání workspace

echo "\n--- Výskyt TODO, FIXME a poznámek ve workspace ---"
grep -rnEI "$KEYWORDS" . --exclude-dir=.venv --exclude-dir=__pycache__ --exclude=*.pyc --exclude=*.log --exclude=*.zip --exclude=*.gz --color=always

if [[ $? -ne 0 ]]; then
  echo "Žádné TODO, FIXME ani poznámky nebyly nalezeny."
fi

echo "\n--- Doporučení ---"
echo "Pravidelně procházej TODO/FIXME poznámky a plánuj jejich řešení. Pro větší úkoly vytvoř issue na GitHubu."
