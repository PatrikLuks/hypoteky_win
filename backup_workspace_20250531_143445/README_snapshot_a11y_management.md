# Kontrola snapshotů a a11y reportů v CI/CD

Tato sekce popisuje, jak je v projektu automatizována kontrola snapshotů UI a přístupnosti (a11y) pomocí GitHub Actions.

## Automatizace v CI/CD

- Při každém commitu nebo pull requestu na hlavní větev se automaticky spouští workflow `.github/workflows/ci.yml`.
- Workflow provádí:
  1. Spuštění všech testů (unit, integrační, edge-case, e2e)
  2. Automatizované generování a kontrolu a11y reportů pomocí `pa11y_batch.sh`
  3. Archivaci snapshotů a a11y reportů (HTML, CSV, ZIP) jako artefaktů buildu
  4. Úklid workspace (mazání dočasných souborů, logů, starých snapshotů)

## Jak spravovat snapshoty a reporty

- Všechny snapshoty a reporty jsou ukládány do složek `snapshot_html_YYYY-MM-DD/` a `pa11y_a11y_reports_YYYY-MM-DD/`.
- Po každém buildu jsou tyto složky a jejich ZIP archivy dostupné ke stažení v sekci artefaktů na GitHubu.
- Pro troubleshooting lze otevřít HTML reporty v prohlížeči a porovnat změny mezi snapshoty (viz skript `compare_snapshots.sh`).

## Rychlý workflow pro snapshot testy (macOS/zsh)

Pro pohodlnou správu snapshot testů použij:

1. Spusť testy a automatickou aktualizaci snapshotů:

   ```zsh
   ./run_and_update_snapshots.sh
   ```
   - Pokud testy selžou pouze kvůli dynamickým hodnotám (CSRF, datumy), snapshoty se automaticky přepíší a testy se spustí znovu.
   - Snapshoty se zálohují do složky `snapshot_html_backup_<datum>`.

2. Pokud chceš snapshoty porovnat ručně, použij:

   ```zsh
   ./compare_snapshots.sh
   ```

3. Pro úklid workspace:

   ```zsh
   ./cleanup_workspace.sh
   ```

> **Tip:** Pokud testy stále selhávají, zkontroluj diff a snapshoty ručně. Pro dlouhodobou robustnost můžeš upravit testy tak, aby ignorovaly dynamické hodnoty.

## Jak číst a řešit a11y reporty (Pa11y)

Po každém spuštění skriptu `./pa11y_batch.sh` najdeš v kořenovém adresáři HTML reporty (např. `pa11y_home_report.html`).

### Jak interpretovat report:
- Pokud report obsahuje větu **"No issues found"** nebo je sekce s issues prázdná, stránka je z pohledu základní automatizované kontroly v pořádku.
- Pokud jsou v reportu položky `<li class="issue">`, najdeš zde popis problému, jeho závažnost (error/warning/notice), a doporučení k opravě.
- Každý problém obsahuje:
  - **Popis chyby** (např. chybějící aria-label, špatný kontrast, nevalidní HTML)
  - **CSS selektor** prvku, kde se problém vyskytuje
  - **Doporučení** pro opravu

### Doporučený postup při nalezení chyb:
1. Otevři report v prohlížeči a najdi sekci s issues.
2. Projdi jednotlivé chyby a oprav je v šabloně nebo CSS.
3. Po opravě spusť znovu `./pa11y_batch.sh` a ověř, že problém zmizel.
4. Pokud si nejsi jistý, proč je chyba důležitá, zeptej se Copilota nebo si vyhledej konkrétní WCAG pravidlo.

### Tipy pro pokročilé:
- Pro testování s různými rolemi (přihlášený uživatel, admin) uprav skript `pa11y_batch.sh` a přidej cookies nebo autentizaci.
- Pokud přidáš novou stránku, rozšiř pole URL v `pa11y_batch.sh`.
- Pro CI/CD je vhodné archivovat reporty a porovnávat změny v čase.

---

Tento checklist pomůže udržet vysokou úroveň přístupnosti a zrychlí onboarding nových vývojářů.

## Troubleshooting

- Pokud se snapshoty nebo reporty negenerují, zkontrolujte logy CI/CD a správnost skriptů.
- Ověřte, že všechny skripty mají správná práva (`fix_script_permissions.sh`).
- Pokud jsou reporty prázdné, ověřte, že testovací data a server běží správně.

---
Tato sekce byla automaticky vygenerována pro lepší správu snapshotů a reportů v projektu.
