#!/bin/zsh
# check_requirements_security.sh
# Popis: Bezpečnostní kontrola závislostí v requirements.txt pomocí safety.
# Autor: Patrik Luks, 2025
# Tento skript spustí safety check a vypíše případné zranitelnosti.
# Kontrola zastaralých a potenciálně zranitelných balíčků v requirements.txt
# Používej pravidelně, před nasazením nebo při auditu

# Aktivace virtuálního prostředí
if [ -d "venv" ]; then
  source venv/bin/activate
elif [ -d ".venv" ]; then
  source .venv/bin/activate
else
  echo "[!] Virtuální prostředí nebylo nalezeno. Vytvoř ho příkazem: python3 -m venv venv"
  exit 1
fi

echo "\n--- Kontrola zastaralých balíčků (pip list --outdated) ---"
pip list --outdated

echo "\n--- Kontrola bezpečnostních zranitelností (safety) ---"
if ! command -v safety &> /dev/null; then
  echo "[!] Nástroj safety není nainstalován. Instaluj ho: pip install safety"
else
  # Moderní příkaz (od června 2024):
  safety scan -r requirements.txt || echo "[!] Některé balíčky mají známé zranitelnosti!"
fi

echo "\n--- Doporučení ---"
echo "Pravidelně aktualizuj závislosti a řeš bezpečnostní varování. Pro update použij: pip install -U <balíček>"
