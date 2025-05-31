#!/bin/zsh
# check_templates_validity.sh
# Rychlá kontrola HTML šablon v klienti/templates/ na základní chyby
# Používej před nasazením, refaktoringem nebo při onboardingu

TEMPLATEDIR="klienti/templates"
HTMLFILES=$(find "$TEMPLATEDIR" -type f -name "*.html")

if [[ -z "$HTMLFILES" ]]; then
  echo "Žádné .html šablony nebyly nalezeny v $TEMPLATEDIR."
  exit 0
fi

ERROR=0
echo "\n--- Kontrola HTML šablon v $TEMPLATEDIR ---"
for file in $HTMLFILES; do
  echo "\n>>> Kontroluji $file"
  # Kontrola neuzavřených tagů (základní heuristika)
  grep -E '<[^/!][^>]*$' "$file" | grep -v '/>' && { echo "[!] Pravděpodobně neuzavřený tag v $file"; ERROR=1; }
  # Kontrola bloků Django templatingu
  BLOCKS=$(grep -o '{% block [^ %]* %}' "$file" | wc -l)
  ENDBLOCKS=$(grep -o '{% endblock %}' "$file" | wc -l)
  if [[ $BLOCKS -ne $ENDBLOCKS ]]; then
    echo "[!] Nesouhlasí počet {% block %} a {% endblock %} v $file ($BLOCKS vs $ENDBLOCKS)"
    ERROR=1
  fi
  # Kontrola překlepů v blocích
  grep -E '{% blok ' "$file" && { echo "[!] Překlep 'blok' místo 'block' v $file"; ERROR=1; }
done

if [[ $ERROR -eq 0 ]]; then
  echo "\n✓ Všechny HTML šablony prošly základní kontrolou."
else
  echo "\n[!] Některé šablony obsahují chyby. Oprav je před nasazením!"
fi
