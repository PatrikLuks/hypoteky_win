#!/bin/zsh
# fix_shebangs.sh
# Zkontroluje a případně opraví shebang (#!/bin/zsh) ve všech .sh skriptech ve workspace
# Používej po klonování, při onboardingu nebo před CI/CD

SCRIPTS=$(find . -type f -name "*.sh")

if [[ -z "$SCRIPTS" ]]; then
  echo "Žádné .sh skripty nebyly nalezeny."
  exit 0
fi

CHANGED=0
for script in $SCRIPTS; do
  FIRSTLINE=$(head -n 1 "$script")
  if [[ "$FIRSTLINE" != "#!/bin/zsh" ]]; then
    echo "[!] $script má špatný nebo chybějící shebang: $FIRSTLINE"
    # Oprava shebangu
    TMPFILE=$(mktemp)
    echo "#!/bin/zsh" > "$TMPFILE"
    tail -n +2 "$script" >> "$TMPFILE"
    mv "$TMPFILE" "$script"
    chmod +x "$script"
    echo "    → Opraveno na #!/bin/zsh"
    CHANGED=1
  fi
done

if [[ $CHANGED -eq 0 ]]; then
  echo "\n✓ Všechny .sh skripty mají správný shebang."
else
  echo "\nHotovo! Všechny shellové skripty nyní začínají #!/bin/zsh."
fi
