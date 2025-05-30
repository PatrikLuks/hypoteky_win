#!/bin/zsh
# fix_script_permissions.sh
# Rychlá kontrola a oprava spustitelných práv u všech .sh skriptů ve workspace
# Používej po klonování repozitáře, při onboardingu nebo před CI/CD

# Najdi všechny .sh skripty v kořeni a podadresářích
SCRIPTS=$(find . -type f -name "*.sh")

if [[ -z "$SCRIPTS" ]]; then
  echo "Žádné .sh skripty nebyly nalezeny."
  exit 0
fi

for script in $SCRIPTS; do
  chmod +x "$script"
  echo "Nastaveno spustitelné právo: $script"
done

echo "\nHotovo! Všechny shellové skripty mají správná práva."
