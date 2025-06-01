#!/bin/zsh
# quick_check_onboarding.sh
# Rychlý onboarding test pro nové vývojáře (macOS/zsh)
# Autor: GitHub Copilot, 2025-05-31

set -e

print_header() {
  echo "\n\033[1;36m$1\033[0m"
}

print_header "1️⃣  Kontrola aktivace virtuálního prostředí (.venv) a verze Pythonu:"
if [[ -z "$VIRTUAL_ENV" ]]; then
  echo "\033[1;31m[CHYBA]\033[0m Virtuální prostředí není aktivní! Spusť: source .venv/bin/activate"
  exit 1
else
  echo "Virtuální prostředí aktivní: $VIRTUAL_ENV"
fi
python --version

print_header "2️⃣  Kontrola klíčových balíčků (django, pytest, playwright):"
for pkg in django pytest playwright; do
  python -c "import $pkg" 2>/dev/null && echo "$pkg OK" || { echo "\033[1;31m[CHYBA]\033[0m Balíček $pkg není nainstalován!"; exit 1; }
done

print_header "3️⃣  Kontrola připojení k databázi a migrací:"
python manage.py showmigrations || { echo "\033[1;31m[CHYBA]\033[0m Nelze zobrazit migrace! Zkontroluj DB a settings."; exit 1; }

print_header "4️⃣  Spuštění základních testů (unit/integration):"
python manage.py test klienti.tests_api || { echo "\033[1;31m[CHYBA]\033[0m Testy neprošly! Zkontroluj výstup výše."; exit 1; }

print_header "5️⃣  Vše OK! Prostředí je připraveno. 🎉"

print_header "6️⃣  Doporučení pro další kroky:"
echo "- Spusť ./run_all_maintenance.sh pro kompletní údržbu workspace."
echo "- Proveď ./cleanup_bak_files.sh a ./cleanup_backups.sh pro úklid záloh a .bak souborů."
echo "- Projdi ONBOARDING.md a ověř checklisty."
echo "- Zkontroluj výstup CI/CD a snapshoty."
echo "- Pokud narazíš na problém, hledej v README.md nebo se ptej v chatu."

# Konec skriptu
