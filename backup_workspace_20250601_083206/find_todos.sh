#!/bin/zsh
# find_todos.sh
# Rychlé vyhledání všech TODO, FIXME a poznámek v kódu workspace
# Používej pro správu technického dluhu, plánování a review

# Hledané klíčové slova
# Rozšíření hledaných klíčových slov o NOTE, HACK, XXX
KEYWORDS="TODO|FIXME|NOTE|HACK|XXX|# POZNÁMKA|# ÚKOL|# NÁVRH|# IDEA"

# Prohledání workspace

echo "\n--- Výskyt TODO, FIXME a poznámek ve workspace ---"
grep -rnEI "$KEYWORDS" . --exclude-dir=.venv --exclude-dir=__pycache__ --exclude=*.pyc --exclude=*.log --exclude=*.zip --exclude=*.gz --color=always

if [[ $? -ne 0 ]]; then
  echo "Žádné TODO, FIXME ani poznámky nebyly nalezeny."
fi

echo "\n--- Doporučení ---"
echo "Pravidelně procházej TODO/FIXME poznámky a plánuj jejich řešení. Pro větší úkoly vytvoř issue na GitHubu."
# Doplnění doporučení
echo "Pokud najdeš poznámku, která už není aktuální, odstraň ji nebo ji nahraď konkrétním issue v repozitáři."
echo "Pro onboarding nových vývojářů doporučujeme projít tento výpis a zaměřit se na klíčové TODO/FIXME."
