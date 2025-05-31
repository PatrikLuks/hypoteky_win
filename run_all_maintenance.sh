#!/bin/zsh
# run_all_maintenance.sh
# Spustí všechny údržbové skripty (check_*, cleanup_*, fix_*) ve workspace v bezpečném režimu (pouze výpis, bez mazání).
# Vhodné pro rychlou kontrolu stavu workspace a onboarding.
# Autor: GitHub Copilot, 2025

set -euo pipefail

# Barvy pro zvýraznění
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Najdi všechny skripty podle vzoru (bez nebezpečných variant)
scripts=(
  check_*.sh
  fix_*.sh
  cleanup_*.sh
)

# Filtruj skripty, které by mohly mazat bez potvrzení
exclude=(cleanup_bak_files.sh cleanup_backups.sh cleanup_duplicates_and_empty.sh cleanup_snapshot_backups.sh cleanup_old_archives.sh cleanup_workspace.sh)

# Spusť skripty postupně
for script in ${(f)"$(ls -1 ${scripts[@]} 2>/dev/null)"}; do
  skip=false
  for ex in $exclude; do
    if [[ "$script" == "$ex" ]]; then
      skip=true
      break
    fi
  done
  if $skip; then
    echo "${YELLOW}Přeskakuji potenciálně nebezpečný skript: $script${NC}"
    continue
  fi
  if [[ -x "$script" ]]; then
    echo "\n${GREEN}--- Spouštím: $script ---${NC}"
    ./$script || echo "${RED}Chyba při běhu $script${NC}"
  else
    echo "${YELLOW}Skript není spustitelný: $script${NC}"
  fi
  echo "${GREEN}--- Konec: $script ---${NC}\n"
done

echo "${GREEN}Všechny bezpečné údržbové skripty byly spuštěny.${NC}"
echo "Zkontrolujte výstup výše a případné chyby řešte podle doporučení v ONBOARDING.md."

# Konec skriptu
