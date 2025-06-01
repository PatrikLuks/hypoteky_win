# 🧑‍💻 ONBOARDING – rychlý start pro nové vývojáře

Tento soubor slouží jako stručný rozcestník pro nové členy týmu i studenty. Najdeš zde nejdůležitější kroky, checklisty a odkazy pro efektivní práci v projektu.

---

## 🚀 Rychlý start

1. **Klonuj repozitář a přejdi do složky:**
   ```zsh
   git clone https://github.com/PatrikLuks/hypoteky_django.git
   cd hypoteky
   ```
2. **Vytvoř a aktivuj virtuální prostředí:**
   ```zsh
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. **Nainstaluj závislosti:**
   ```zsh
   pip install -r requirements.txt
   pip install playwright
   python -m playwright install --with-deps
   ```
4. **Nastav MySQL a proveď migrace:**
   - Viz `DB_SETUP_MYSQL.md`
   - 
   ```zsh
   python manage.py migrate
   ```
5. **Spusť server:**
   ```zsh
   python manage.py runserver
   ```
6. **Spusť testy a údržbu workspace:**
   ```zsh
   ./run_all_checks.sh
   ```

---

## 🧑‍🔬 Rychlá kontrola prostředí (doporučeno)

Před prvním vývojem spusť skript:

```zsh
source .venv/bin/activate
./quick_check_onboarding.sh
```

Skript ověří:
- Aktivaci virtuálního prostředí
- Instalaci klíčových balíčků (django, pytest, playwright)
- Připojení k databázi a migrace
- Základní testy

Pokud vše projde, můžeš bezpečně pokračovat v práci!

---

## 🧪 Jak přidat nový skript/test (best practices)
- Inspiruj se soubory:
  - `klienti/scripts/klient_user_overview.py` (+ test, CSV export)
  - `klienti/scripts/rozdel_klienty_mezi_uzivatele.py` (+ test, dry-run, CSV export)
- Hlavní logiku vždy dávej do funkce, kterou lze importovat a testovat.
- Pro CLI použij `argparse` a umožni např. `--csv`, `--dry-run`.
- Testuj přímo funkci, ne přes subprocess.
- Pro export do CSV použij `csv` a `tempfile` v testu.

---

## ✅ Checklist pro přispěvatele
- [ ] Hlavní logika je v samostatné funkci (importovatelná, testovatelná)
- [ ] Skript podporuje CLI parametry (`--csv`, `--dry-run`, `--help`)
- [ ] Existuje odpovídající test v `tests/`, který ověřuje i edge-case scénáře
- [ ] Testy procházejí lokálně i v CI
- [ ] Kód je okomentovaný a srozumitelný
- [ ] Pokud skript mění data, je k dispozici i bezpečný režim (dry-run)
- [ ] Pokud skript exportuje data, je ověřen i obsah exportu

---

## 🛠️ Jak psát a testovat údržbové shell skripty

Každý shell skript ve workspace musí splňovat tyto požadavky:

- **Hlavička s popisem a autorem** v prvních 5 řádcích, např.:
  ```sh
  # cleanup_snapshot_backups.sh
  # Popis: Skript pro úklid záložních snapshotů (bak, bak2, bak_fix, bak_autofix_*) – přesune je do složky snapshot_backups_YYYYMMDD/.
  # Autor: Tvé jméno, 2025
  # Použití: ./cleanup_snapshot_backups.sh
  ```
- **Správný shebang** (`#!/bin/zsh` nebo `#!/bin/bash`)
- **Skript musí být spustitelný** (příkaz `chmod +x <název_skriptu.sh>`)
- **Nesmí být prázdný** a měl by být stručně okomentovaný

### Automatizované testování skriptů

1. **Přidej název skriptu do pole `SCRIPTS_TO_TEST` v `tests/test_scripts.py`**
2. **Spusť testy:**
   ```zsh
   python tests/test_scripts.py
   ```
3. **Oprav případné chyby podle výstupu testu** (např. chybějící hlavička, špatný shebang, není spustitelný)

### Checklist pro shell skripty
- [ ] Hlavička s popisem a autorem
- [ ] Správný shebang
- [ ] Skript je spustitelný (`chmod +x`)
- [ ] Není prázdný, má komentáře
- [ ] Prošel testem `tests/test_scripts.py`

---

## Úklid duplicitních a prázdných souborů

### Rychlý skript pro kontrolu a úklid

Ve workspace je připraven skript `cleanup_duplicates_and_empty.sh`, který:
- Najde a vypíše duplicitní soubory (podle obsahu, využívá `fdupes`).
- Najde a vypíše prázdné soubory (kromě .gitkeep a .venv).
- Umožní bezpečné mazání (s potvrzením) pomocí parametrů `--delete-duplicates` a `--delete-empty`.

#### Použití:
```zsh
# Výpis duplicit a prázdných souborů
./cleanup_duplicates_and_empty.sh

# Smazání duplicit (s potvrzením)
./cleanup_duplicates_and_empty.sh --delete-duplicates

# Smazání prázdných souborů (s potvrzením)
./cleanup_duplicates_and_empty.sh --delete-empty
```

> Pro detekci duplicit je potřeba mít nainstalovaný nástroj `fdupes` (`brew install fdupes`).

---

**Doporučení:**
- Skript spouštějte pravidelně, zejména po větších úpravách, importech nebo refaktoringu.
- Nikdy nemažte automaticky bez kontroly – vždy zkontrolujte výpis před potvrzením mazání.
- Pokud chcete úklid automatizovat v CI, použijte pouze výpis (bez mazání) a výstup kontrolujte v logu.

---

### Automatizovaná kontrola čistoty workspace (CI)

Každý push a pull request na hlavní větev spouští GitHub Actions workflow `.github/workflows/cleanliness.yml`, který:
- Spustí skript `cleanup_duplicates_and_empty.sh` (pouze výpis, nemaže!).
- Výsledek kontroly je vidět v logu CI (duplicitní/prázdné soubory).
- Pokud workflow najde problém, doporučujeme úklid provést lokálně dle návodu výše.

> Tato automatizace pomáhá udržet workspace dlouhodobě čistý a onboarding bez překvapení.

---

## Úklid záložních složek (backup_workspace_*)

Ve workspace se mohou hromadit záložní složky (např. `backup_workspace_20250531_150813`), které zvyšují nepořádek a mohou způsobit záměnu souborů.

### Rychlý skript pro přesun/mazání záloh

Použijte skript `cleanup_backups.sh`:
- Najde všechny záložní složky v hlavním workspace.
- Umožní bezpečný přesun do archivu nebo jejich smazání (vždy s potvrzením).

#### Použití:
```zsh
# Výpis záložních složek
./cleanup_backups.sh

# Přesun všech záloh do složky ~/workspace_archiv
./cleanup_backups.sh --move ~/workspace_archiv

# Smazání všech záloh (s potvrzením)
./cleanup_backups.sh --delete
```

> Doporučení: Zálohy pravidelně archivujte mimo hlavní workspace, případně mažte po ověření integrity dat.

---

## Úklid .bak* souborů (zálohy snapshotů)

Ve workspace i zálohách se mohou hromadit soubory typu `*.bak*` (např. `dashboard_snapshot.html.bak_fix`, `klient_detail_snapshot.html.bak2` apod.). Tyto soubory nejsou potřeba pro běžný provoz a zvyšují nepořádek.

### Rychlý skript pro mazání .bak* souborů

Použijte skript `cleanup_bak_files.sh`:
- Najde všechny .bak* soubory ve workspace i zálohách.
- Umožní jejich bezpečné smazání (vždy s potvrzením).

#### Použití:
```zsh
# Výpis všech .bak* souborů
./cleanup_bak_files.sh

# Smazání všech .bak* souborů (s potvrzením)
./cleanup_bak_files.sh --delete
```

> Doporučení: Smažte .bak* soubory pravidelně, zejména po úpravách snapshotů nebo větších refaktoringách.

---

## Hromadné spuštění údržbových skriptů

Pro rychlou kontrolu stavu workspace a onboarding použijte skript `run_all_maintenance.sh`:
- Spustí všechny bezpečné údržbové skripty (check_*, fix_*, cleanup_*) v dávce (pouze výpis, bez mazání).
- Přeskakuje skripty, které by mohly mazat data bez potvrzení.
- Výsledek je barevně zvýrazněn, případné chyby jsou jasně viditelné.

#### Použití:
```zsh
./run_all_maintenance.sh
```

> Doporučení: Spouštějte pravidelně, zejména před commitem, po větších úpravách nebo při onboardingu nového vývojáře.

---

## 🧹 Pravidelný úklid workspace (doporučeno pro MacBook Air)

- Pravidelně spouštěj skript `cleanup_snapshots_archives.sh` pro smazání snapshotů, záloh, archivů a reportů:
  ```zsh
  ./cleanup_snapshots_archives.sh
  ```
- Udržuj workspace co nejmenší – snapshoty, zálohy a reporty archivuj mimo hlavní složku projektu.
- Pracuj pouze s klíčovými složkami (`hypoteky/`, `tests/`, `klienti/` atd.), ostatní ignoruj ve VS Code.
- Omez počet aktivních rozšíření ve VS Code, pravidelně restartuj editor.
- Pravidelně kontroluj `.gitignore` a `.vscode/settings.json`, zda obsahují aktuální ignore vzory.
- Pokud workspace zpomaluje, spusť i další úklidové skripty (`cleanup_*`, `shrink_workspace_for_vscode.sh`).

---

## 📚 Důležité odkazy
- [README.md](README.md) – detailní dokumentace, troubleshooting, workflow
- [DB_SETUP_MYSQL.md](DB_SETUP_MYSQL.md) – nastavení databáze
- [E2E_TESTING_CHECKLIST.md](E2E_TESTING_CHECKLIST.md) – checklist pro e2e testy
- [README_snapshot_a11y_management.md](README_snapshot_a11y_management.md) – správa snapshotů a a11y
- `klienti/scripts/` – vzorové skripty
- `klienti/tests/` – vzorové testy

---

## Doporučení pro rychlejší a stabilnější vývoj na MacBook Air (VS Code)

- **Ignoruj snapshoty, zálohy, archivy a reporty** – jsou nyní v `.gitignore` a `.vscode/settings.json`, VS Code je nebude indexovat ani zobrazovat.
- **Pravidelně spouštěj úklidové skripty** (`cleanup_*`, `run_all_maintenance.sh`) a archivuj staré snapshoty mimo hlavní workspace.
- **Otevírej pouze potřebné složky** – např. `klienti`, `manage.py`, `requirements.txt`, vyhni se zálohám a velkým archivům.
- **Omez rozšíření a background procesy ve VS Code** – vypni nepotřebné pluginy, automatické lintování a formátování na velkých souborech.
- **Restartuj VS Code po větším úklidu nebo změně workspace** – uvolníš paměť a zrychlíš indexaci.
- **Pravidelně zálohuj a pushuj změny na GitHub** – minimalizuješ riziko ztráty dat.

> Pokud i po těchto krocích VS Code zamrzá, zvaž rozdělení workspace na menší části (např. pouze backend, pouze testy) nebo použij VS Code Remote/Dev Containers.

---

> Pokud narazíš na problém, začni od checklistu a logů, nebo se ptej v týmu. Hodně štěstí!
