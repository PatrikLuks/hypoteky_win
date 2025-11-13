#!/bin/zsh
# fix_line_endings.sh
# Zkontroluje a opraví ukončení řádků (LF) ve všech .sh skriptech ve workspace
# Používej po úpravách na Windows, při onboardingu nebo před CI/CD

SCRIPTS=$(find . -type f -name "*.sh")

if [[ -z "$SCRIPTS" ]]; then
  echo "Žádné .sh skripty nebyly nalezeny."
  exit 0
fi

CHANGED=0
for script in $SCRIPTS; do
  if file "$script" | grep -q CRLF; then
    echo "[!] $script má CRLF ukončení řádků – opravuji na LF."
    if command -v dos2unix &> /dev/null; then
      dos2unix "$script" &>/dev/null
    else
      awk '{ sub("\r$", ""); print }' "$script" > "$script.tmp" && mv "$script.tmp" "$script"
    fi
    CHANGED=1
  fi
done

if [[ $CHANGED -eq 0 ]]; then
  echo "\n✓ Všechny .sh skripty mají správné LF ukončení řádků."
else
  echo "\nHotovo! Všechny shellové skripty nyní používají LF ukončení řádků."
fi
