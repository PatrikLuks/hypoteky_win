#!/bin/zsh
# fix_file_ownership.sh – skript pro nastavení správného vlastníka a skupiny pro všechny soubory ve workspace
# Používej po přesunu projektu, změně uživatele nebo při řešení problémů s přístupem
# Nastaví vlastnictví pro všechny soubory a složky v aktuálním workspace
# Autor: automatická optimalizace Copilot

USER=$(whoami)
GROUP=$(id -gn)

# Nastavení vlastnictví pro všechny soubory a složky v aktuálním workspace
sudo chown -R "$USER":"$GROUP" .

echo "\nHotovo! Všechny soubory a složky nyní patří uživateli $USER a skupině $GROUP."
echo "Pokud používáš více uživatelů nebo sdílíš workspace, zkontroluj práva i pro ostatní členy týmu."
