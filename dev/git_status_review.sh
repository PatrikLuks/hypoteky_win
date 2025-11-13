#!/bin/zsh
# git_status_review.sh
# Rychlý přehled posledních změn v git repozitáři a diff workspace
# Používej před commitem, při review nebo troubleshooting

# Výpis posledních 5 commitů

echo "\n--- Posledních 5 commitů ---"
git log -5 --pretty=format:"%C(yellow)%h%Creset %Cgreen%ad%Creset %C(bold blue)%an%Creset %Creset- %s" --date=short

echo "\n--- Stav workspace (git status) ---"
git status

echo "\n--- Diff necommitnutých změn (unstaged) ---"
git diff | head -n 40
if [[ $(git diff | wc -l) -gt 40 ]]; then
  echo "... (další změny skryty, použij git diff pro celý výpis)"
fi

echo "\n--- Diff připravených změn (staged) ---"
git diff --cached | head -n 40
if [[ $(git diff --cached | wc -l) -gt 40 ]]; then
  echo "... (další změny skryty, použij git diff --cached pro celý výpis)"
fi

echo "\n--- Doporučení ---"
echo "Pokud vidíš nechtěné změny, uprav je před commitem. Pro detailní diff použij git diff nebo git difftool."
echo "Pro zobrazení změn v konkrétním souboru: git diff <soubor>"
