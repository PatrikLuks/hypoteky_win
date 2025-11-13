#!/bin/zsh
# Popis: Kontrola, zda je git workspace čistý (žádné necommitnuté změny).
# Autor: Patrik Luks, 2025
# Tento skript ověří stav git repozitáře a vypíše případné neuložené změny.
# check_git_clean.sh
# Rychlá kontrola, zda je workspace čistý a všechny důležité soubory jsou verzované v Gitu
# Používej před commitem, pushem, zálohou nebo nasazením

echo "\n--- Stav workspace (git status) ---"
git status --short

if [[ $(git status --porcelain | wc -l) -eq 0 ]]; then
  echo "\n✓ Workspace je čistý – všechny změny jsou commitnuté."
else
  echo "\n[!] Ve workspace jsou necommitnuté změny! Zvaž commit a push před dalším krokem."
  echo "Pro detailní diff použij: git diff nebo ./git_status_review.sh"
fi

echo "\n--- Přehled změn ---"
git diff --stat

echo "\n--- Doporučení ---"
echo "Před nasazením, zálohou nebo sdílením vždy commitni a pushni všechny důležité změny."
