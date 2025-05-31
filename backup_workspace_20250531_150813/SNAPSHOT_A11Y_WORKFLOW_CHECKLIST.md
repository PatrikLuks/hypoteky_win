# Checklist a workflow pro správu snapshotů a a11y testů

Tento dokument slouží jako rychlý návod a checklist pro správu snapshotů UI a testů přístupnosti (a11y) v projektu hypoteky.

---

## 1. Před každou úpravou UI
- [ ] Zálohuj aktuální snapshoty (`cleanup_snapshot_backups.sh` nebo ručně zkopíruj snapshoty do záložní složky)
- [ ] Ověř, že všechny snapshot testy procházejí (`pytest klienti/tests_ui.py tests_ui.py`)

## 2. Po změně UI nebo šablon
- [ ] Spusť snapshot testy a zkontroluj případné rozdíly
- [ ] Pokud testy selžou kvůli neviditelným rozdílům (mezery, entity, dynamický obsah):
    - [ ] Použij utilitu `normalize_html` a `mask_dynamic_content` v testech
    - [ ] Spusť `fix_html_snapshot_issues.sh` pro automatickou opravu snapshotů
    - [ ] Pokud je potřeba, smaž a vygeneruj snapshoty znovu (`update_snapshots.sh`)
- [ ] Ověř, že všechny testy nyní procházejí

## 3. Testování přístupnosti (a11y)
- [ ] Spusť `pa11y_batch.sh` nebo `pa11y_batch_csv.sh` pro kontrolu hlavních stránek
- [ ] Projdi reporty v HTML (např. `pa11y_home_report.html`)
- [ ] Oprav případné chyby (role, aria-label, kontrast, ovládání klávesnicí)

## 4. Validace HTML snapshotů
- [ ] Spusť `check_html_validity.sh` pro ověření správnosti HTML5
- [ ] Oprav chyby ručně nebo pomocí `fix_html_snapshot_issues.sh`

## 5. Údržba a úklid
- [ ] Pravidelně spouštěj `cleanup_snapshot_backups.sh` a `cleanup_old_archives.sh` pro úklid starých záloh
- [ ] Udržuj workspace čistý a přehledný

---

## Tipy a best practices
- Vždy komentuj změny v snapshot souborech a testech.
- Při větších změnách UI zálohuj snapshoty předem.
- Pokud narazíš na opakované chyby, rozšiř tento checklist nebo README.
- Pro onboarding nových vývojářů odkaž na tento soubor a `README_snapshot_a11y_management.md`.

---

*Vytvořeno pro studenty a vývojáře, kteří chtějí udržet projekt spolehlivý, přístupný a snadno rozšiřitelný.*
