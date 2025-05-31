# Hypotéky – moderní správa případů pro finanční poradce

![Django](https://img.shields.io/badge/Django-4.2-green?logo=django)
![MySQL](https://img.shields.io/badge/MySQL-8.0-blue?logo=mysql)
![REST%20API](https://img.shields.io/badge/REST%20API-ready-orange?logo=fastapi)
![2FA](https://img.shields.io/badge/2FA-enabled-success?logo=auth0)
![Testy](https://img.shields.io/badge/tests-pytest%20%26%20drf--test-green?logo=pytest)

Tento projekt je moderní webová aplikace pro správu hypoték určená finančním poradcům, manažerům a administrátorům. Umožňuje detailní evidenci a správu případů klientů podle přesně definovaného workflow (15 kroků od záměru klienta po čerpání a splácení), reporting, auditní log, pokročilé filtrování, exporty, REST API a mnoho dalšího.

---

## 🚀 Hlavní funkce
- **Kompletní workflow hypotéky** (15 kroků, deadliny, poznámky, úkoly)
- **Pokročilý reporting a statistiky** (grafy, trendy, heatmapy, export do PDF)
- **Automatizované reporty e-mailem** (management command)
- **Auditní log všech změn** (kdo, kdy, co upravil)
- **Role a oprávnění** (poradce, administrátor, manažer, klient)
- **Dvoufaktorová autentizace (2FA)**
- **REST API** (DRF, JWT, Swagger, Redoc)
- **Notifikace e-mailem** (deadliny, změny, zamítnutí)
- **Export deadlinů do iCal** (Google/Outlook)
- **Responsivní moderní UI** (Bootstrap 5, tmavý režim)
- **Testy (unit/integration)**
- **Generování testovacích dat** (viz `sample_data.py`)

---

## 🛠️ Technologie
- Python 3.9+, Django 4.2+
- MySQL 8+
- Django REST Framework, JWT, drf-yasg (Swagger)
- Bootstrap 5, Chart.js, FontAwesome
- openpyxl, reportlab, matplotlib (exporty, PDF, grafy)
- django-otp, two-factor-auth (2FA)
- phonenumberslite, Faker (test data)

---

## ⚡ Instalace a spuštění
1. **Klonuj repozitář a přepni se do složky projektu:**
   ```sh
   git clone https://github.com/PatrikLuks/hypoteky_django.git
   cd hypoteky
   ```
2. **Vytvoř a aktivuj virtuální prostředí:**
   ```sh
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. **Nainstaluj závislosti:**
   ```sh
   pip install -r requirements.txt
   ```
4. **Vytvoř a nastav MySQL databázi:**
   - Postup najdeš v [DB_SETUP_MYSQL.md](DB_SETUP_MYSQL.md)
   - Uprav `hypoteky/settings.py` podle svých údajů
5. **Proveď migrace a vytvoř superuživatele:**
   ```sh
   python manage.py migrate
   python manage.py createsuperuser
   ```
6. **(Volitelné) Vygeneruj testovací data:**
   ```sh
   python sample_data.py
   ```
7. **Spusť server:**
   ```sh
   python manage.py runserver
   ```
8. **Přihlas se do administrace:**
   - [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

## ⚡ Rychlý start (Windows, macOS, Linux)

### 1. Klonování repozitáře
```sh
git clone https://github.com/PatrikLuks/hypoteky_django.git
cd hypoteky
```

### 2. Vytvoření a aktivace virtuálního prostředí
- **macOS/Linux:**
  ```sh
  python3 -m venv .venv
  source .venv/bin/activate
  ```
- **Windows:**
  ```sh
  python -m venv .venv
  .venv\Scripts\activate
  ```

### 3. Instalace závislostí
- **macOS/Linux (doporučeno):**
  ```sh
  pip install -r requirements.txt
  ```
- **Windows (pokud selže mysqlclient):**
  ```sh
  pip install mysql-connector-python
  pip install -r requirements.txt
  ```
  (nebo odkomentuj řádek s mysql-connector-python v requirements.txt)

### 4. Nastavení databáze
- Pro MySQL je potřeba mít běžící server a vytvořenou DB (viz DB_SETUP_MYSQL.md)
- Pro testování lze použít SQLite (úprava settings.py)

### 5. Migrace a superuživatel
```sh
python manage.py migrate
python manage.py createsuperuser
```

### 6. Spuštění serveru
```sh
python manage.py runserver
```

### 7. (Volitelné) Testy a Playwright
```sh
pip install pytest playwright
playwright install
pytest tests_e2e_playwright.py
```

---

## 🛠️ Nejčastější problémy na Windows
- Pokud selže instalace `mysqlclient`, nainstaluj Visual C++ build tools nebo použij `mysql-connector-python` (viz výše).
- Pokud pip nenajde Python, zkontroluj, že je přidán do PATH.
- Pokud máš problém s venv, použij `python -m venv .venv` a aktivuj `.venv\Scripts\activate`.
- Pokud Playwright hlásí chybu, spusť `playwright install`.

---

## 🏦 Workflow hypotéky (kroky)
1. Jméno klienta
2. Co chce klient financovat
3. Návrh financování
4. Výběr banky
5. Příprava žádosti
6. Kompletace podkladů
7. Podání žádosti
8. Odhad
9. Schvalování
10. Příprava úvěrové dokumentace
11. Podpis úvěrové dokumentace
12. Příprava čerpání
13. Čerpání
14. Zahájení splácení
15. Podmínky pro splacení

---

## 📊 Reporting a analytika
- **Dashboard**: trendy, workflow, rozložení podle bank, poslední změny
- **Reporting**: filtry podle období, heatmapy, export do PDF, automatizované reporty e-mailem
- **Auditní log**: historie změn u každého klienta

---

## 🔒 Bezpečnost a správa
- **Role a oprávnění**: poradce, administrátor, manažer, klient
- **Dvoufaktorová autentizace (2FA)**
- **Auditní log** všech důležitých akcí
- **Ochrana dat, validace vstupů, bezpečné heslování**

---

## 🔗 Integrace a API
- **REST API** (DRF, JWT): `/api/`, `/swagger/`, `/redoc/`
- **Export deadlinů do iCal** (Google/Outlook)
- **Automatizované e-mailové notifikace**

---

## 🧪 Testy a automatizace
- **Unit a integrační testy**: `klienti/tests_api.py`
- **Automatizované reporty**: `python manage.py send_reporting_email`
- **Generování testovacích dat**: `python sample_data.py`

---

## 🧪 E2E testy (Playwright) – návod a best practices

Projekt obsahuje automatizované end-to-end (e2e) testy pomocí [Playwright](https://playwright.dev/python/), které ověřují hlavní workflow aplikace přes reálné UI.

### Jak spustit e2e testy

1. Ujisti se, že máš nainstalovaný Playwright a pytest:
   ```sh
   pip install pytest playwright
   playwright install
   ```
2. Spusť Django server (v jiném terminálu):
   ```sh
   python manage.py runserver
   ```
3. Spusť e2e testy:
   ```sh
   pytest tests_e2e_playwright.py
   ```

### Co e2e testy ověřují?
- Přihlášení uživatele
- Vytvoření nového klienta přes UI
- Kontrola, že klient je v seznamu i detailu
- (Lze snadno rozšířit o další scénáře: editace, workflow, exporty, notifikace...)

### Jak přidat nový e2e scénář?
- Přidej novou funkci do `tests_e2e_playwright.py` s prefixem `test_`
- Používej Playwright API pro interakci s UI (vyplňování formulářů, klikání, assertions)
- Vždy ověř, že test:
  - čeká na správné načtení stránky (`wait_for_selector`)
  - používá unikátní testovací data (např. jméno klienta)
  - po sobě zanechává čistý stav (volitelné: smaž testovací data)

### Ladění a snapshoty
- Pro ladění můžeš v testu použít `page.screenshot(path='soubor.png')` nebo `print(page.url)`
- Pokud test selže, zkontroluj screenshot a logy
- Testy jsou navrženy tak, aby byly robustní vůči duplicitám (vybírají první výskyt v tabulce)

### Best practices
- Každý test by měl být nezávislý a opakovatelný
- Používej unikátní hodnoty (např. jméno klienta s časovým razítkem)
- Pokud testuješ mazání, ověř i chybové stavy (např. pokus o smazání neexistujícího klienta)
- Rozšiřuj testy podle reálných uživatelských scénářů (viz sekce „Cíle testování“ v .github/copilot-instructions.md)

---

## ⚙️ CI/CD – Automatizované testy (GitHub Actions)

Projekt obsahuje ukázkový workflow `.github/workflows/ci.yml` pro automatizované spouštění testů při každém commitu nebo pull requestu.

### Jak to funguje?
- Po každém push/pull requestu na hlavní větev se automaticky spustí:
  - Instalace závislostí
  - Nastavení MySQL (testovací DB)
  - Migrace
  - Spuštění všech testů (`python manage.py test`)
- Výsledek najdeš v záložce **Actions** na GitHubu.

### Best practices pro CI/CD
- Před commitem ověř, že všechny testy procházejí i lokálně.
- Pokud přidáváš nové závislosti, aktualizuj `requirements.txt`.
- Pro edge-case scénáře přidej testy a ověř je i v CI.
- Pokud testy selžou v CI, zkontroluj logy a troubleshooting sekci výše.

---

## 📚 Další zdroje a doporučení
- [DB_SETUP_MYSQL.md](DB_SETUP_MYSQL.md) – nastavení databáze, kódování, migrace
- [docs/](docs/) – rozšířená dokumentace, příklady testů, CI/CD, edge-case scénáře
- [sample_data.py](sample_data.py) – generování testovacích dat
- [tests/](tests/) – ukázky testů pro import, export, reporting, bezpečnost, notifikace

---

Máte-li dotazy nebo narazíte na problém, otevřete issue na GitHubu nebo kontaktujte hlavního správce projektu.

---

## 🧪 Jak spouštět testy a řešit běžné chyby

### Spouštění testů
- **Doporučený způsob:**
  - Pro všechny Django testy (včetně UI/snapshot testů) používej:
    ```sh
    python manage.py test
    ```
  - Tento příkaz automaticky nastaví proměnnou `DJANGO_SETTINGS_MODULE` a správně načte konfiguraci.
- **Nedoporučené:**
  - Přímé spouštění testů přes `pytest klienti/tests_ui.py` může selhat s chybou:
    > Requested setting DATABASES, but settings are not configured.
  - Pokud potřebuješ použít pytest (např. pro custom mark), spusť ho s nastavenou proměnnou:
    ```sh
    DJANGO_SETTINGS_MODULE=hypoteky.settings pytest
    ```
    - Na Windows použij:
      ```sh
      set DJANGO_SETTINGS_MODULE=hypoteky.settings
      pytest
      ```

### Nejčastější chyby a jejich řešení (Troubleshooting)
- **Chyba: `DATABASES, but settings are not configured`**
  - Řešení: Spouštěj testy přes `python manage.py test` nebo nastav `DJANGO_SETTINGS_MODULE`.
- **Chyba s kódováním/emoji v MySQL:**
  - Doporučujeme použít kódování `utf8mb4` v databázi (viz níže).
- **Chyba s migracemi:**
  - Ujisti se, že máš aktuální migrace (`python manage.py makemigrations && python manage.py migrate`).
- **Chyba při importu CSV/XLSX:**
  - Zkontroluj, zda soubor obsahuje povinná pole (`jméno`, `datum`).
  - Řádky bez těchto polí se přeskočí a zaloguje se důvod.

### Podpora emoji a kódování databáze
- **MySQL doporučení:**
  - Pro plnou podporu speciálních znaků a emoji nastav databázi na `utf8mb4`.
  - Pokud používáš pouze `utf8`, některé znaky (např. emoji) nebudou uloženy.
  - Viz příklad nastavení v `DB_SETUP_MYSQL.md`.

---

## 🔌 Jak psát a spouštět API testy

API testy najdeš ve složce `klienti/tests_api.py`. Používají Django REST Framework a knihovnu `rest_framework.test`.

### Příklad edge-case testu (neautorizovaný přístup):
```python
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status

def test_klient_create_unauthorized():
    client = APIClient()
    url = reverse('klient-list')
    data = {'jmeno': 'Neoprávněný', 'datum': '2025-05-30', 'vyber_banky': 'KB', 'navrh_financovani_castka': 1000000}
    response = client.post(url, data, format='json')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
```

### Jak spustit API testy
- Nejjednodušší způsob:
  ```zsh
  python manage.py test klienti.tests_api
  ```
- Pro všechny testy:
  ```zsh
  python manage.py test
  ```
- Pokud chceš použít pytest:
  ```zsh
  export DJANGO_SETTINGS_MODULE=hypoteky.settings
  pytest klienti/tests_api.py
  ```

### Doporučení
- Vždy testuj i edge-case scénáře (neautorizace, nevalidní vstupy, chybějící pole, limity).
- Ověřuj, že API správně vrací chybové kódy a zprávy.
- Pro testování autentizace používej JWT tokeny (viz příklady v testech).

---

## 🛠️ Troubleshooting API/testů
- **Chyba 401 Unauthorized:**
  - Zkontroluj, zda posíláš správný token v hlavičce `Authorization: Bearer ...`.
- **Chyba 400 Bad Request:**
  - Zkontroluj, zda posíláš všechna povinná pole a správné formáty dat.
- **Chyba s DJANGO_SETTINGS_MODULE:**
  - Spouštěj testy přes `python manage.py test` nebo nastav proměnnou prostředí.
- **Chyba s databází:**
  - Ověř, že máš spuštěnou a správně nastavenou testovací DB (viz DB_SETUP_MYSQL.md).

---

## 📂 Struktura projektu (důležité složky)
- `klienti/` – hlavní aplikace (modely, views, API, šablony, management commands)
- `hypoteky/` – konfigurace projektu
- `templates/` – šablony (Bootstrap, tmavý režim)
- `sample_data.py` – generátor testovacích dat
- `DB_SETUP_MYSQL.md` – návod na MySQL

---

## 👤 Autoři a kontakt
- Patrik Luks ([GitHub](https://github.com/PatrikLuks))
- Kontakt: podpora@hypoteky.cz

---

## 📝 Licence
Projekt je poskytován pod MIT licencí.

---

> **Tip:** Pokud narazíš na problém, podívej se do README, DB_SETUP_MYSQL.md nebo mi napiš issue na GitHubu!

---

# Onboarding a rychlý start pro nové vývojáře

Tato sekce ti umožní rychle začít pracovat na projektu, pochopit strukturu workspace a efektivně využívat všechny automatizace a testy. Doporučeno pro každého nového člena týmu i při návratu k projektu po delší době.

## 1. Požadavky
- macOS, zsh
- Python 3.9+ (doporučeno 3.11)
- Node.js (pro Playwright E2E testy)
- MySQL 8+

## 2. První spuštění projektu
```zsh
# Klonuj repozitář a přejdi do složky
cd hypoteky

# Vytvoř a aktivuj virtuální prostředí
python3 -m venv .venv
source .venv/bin/activate

# Nainstaluj závislosti
pip install -r requirements.txt
pip install playwright
python -m playwright install --with-deps

# Nastav MySQL (viz DB_SETUP_MYSQL.md)
# Proveď migrace
python manage.py migrate

# Vytvoř superuživatele (volitelné)
python manage.py createsuperuser

# Spusť server
python manage.py runserver
```

## 3. Spuštění všech testů (unit, integration, E2E, a11y)
```zsh
# Aktivuj venv
source .venv/bin/activate

# Spusť všechny testy a údržbu workspace
./run_all_checks.sh

# Nebo pouze E2E/UI testy s automatickým serverem:
./run_e2e_with_server.sh
```

## 4. CI/CD a best practices
- Každý push/pull request spouští automatizované testy a údržbu (viz `.github/workflows/ci.yml`).
- Výsledky testů a reporty najdeš v `test-results/`, `pa11y_a11y_reports_*/`, `snapshot_html_*/`.
- Dodržuj checklisty v `E2E_TESTING_CHECKLIST.md` a `README_snapshot_a11y_management.md`.

## 5. Přidání nového testu
- Unit/integration testy: `klienti/tests_*.py`, `tests/`
- E2E/UI testy: `tests_e2e_playwright.py`
- a11y/snapshot: `pa11y_batch.sh`, `compare_snapshots.sh`

## 6. Troubleshooting
- Pokud testy selžou, zkontroluj logy a výstupy v terminálu.
- Ověř, že server běží a port 8000 není blokován.
- Pro obnovu workspace použij `restore_archives.sh` nebo `backup_workspace.sh`.

---

> Tento onboarding je určen pro studenty i zkušené vývojáře. Pokud narazíš na problém, začni od checklistu a logů, nebo se ptej v týmu.

---

## 🧪 Ukázka snapshot testu UI (Playwright)

Snapshot testy ověřují, že se UI nezměnilo nečekaným způsobem. V Pythonu lze použít Playwright:

```python
# klienti/tests_ui.py
import pytest
from playwright.sync_api import sync_playwright

def test_klient_list_snapshot(snapshot):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto('http://localhost:8000/klienti/')
        html = page.content()
        # Porovná aktuální HTML s uloženým snapshotem
        snapshot.assert_match(html, 'klient_list_snapshot.html')
        browser.close()
```

---

## ♿ Ukázka a11y (přístupnostního) testu

Pro ověření přístupnosti lze použít Playwright s axe-core:

```python
# klienti/tests_ui.py
from playwright.sync_api import sync_playwright
import axe_selenium_python

def test_klient_list_accessibility():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto('http://localhost:8000/klienti/')
        # Spustí a11y audit pomocí axe-core
        results = page.evaluate("axe.run()")
        assert results['violations'] == []
        browser.close()
```

---

## 🧪 Best practices pro e2e a a11y testy

### Proč psát e2e a a11y testy?
- e2e testy ověřují hlavní workflow z pohledu uživatele (např. přihlášení, vytvoření klienta, export, notifikace).
- a11y testy (přístupnost) zajišťují, že aplikace je použitelná i pro uživatele s hendikepem (klávesnice, čtečky, kontrast, role, popisky).
- Automatizované testy chrání před regresí a zvyšují kvalitu produktu.

### Příklad e2e testu (Playwright):
```python
import pytest
from playwright.sync_api import sync_playwright

@pytest.mark.e2e
def test_vytvoreni_klienta():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto('http://localhost:8000/login/')
        page.fill('input[name="username"]', 'testlist')
        page.fill('input[name="password"]', 'testpass')
        page.click('button[type="submit"]')
        page.wait_for_selector('text=Dashboard', timeout=3000)
        # ...workflow vytvoření klienta...
        browser.close()
```

### Příklad a11y testu (axe-core/Playwright):
```python
import pytest
from playwright.sync_api import sync_playwright

@pytest.mark.e2e
def test_a11y_dashboard():
    try:
        from playwright_axe import Axe
    except ImportError:
        pytest.skip("playwright-axe není nainstalován")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto('http://localhost:8000/login/')
        page.fill('input[name="username"]', 'testlist')
        page.fill('input[name="password"]', 'testpass')
        page.click('button[type="submit"]')
        page.wait_for_selector('text=Dashboard', timeout=3000)
        axe = Axe(page)
        axe.inject()
        results = axe.run()
        violations = [v for v in results['violations'] if v['impact'] in ('critical', 'serious')]
        assert not violations, f"A11y chyby: {violations}"
        browser.close()
```

### Doporučení
- Piš e2e testy pro hlavní workflow (login, CRUD, export, notifikace).
- Ověřuj přístupnost klíčových view (formuláře, dashboard, detail klienta) pomocí axe-core nebo pa11y.
- Testuj i edge-case scénáře (nevalidní vstupy, selhání služeb, chybějící pole).
- Dokumentuj, jak testy spouštět a jak řešit běžné chyby.

### Troubleshooting
- **Chyba: playwright-axe není nainstalován:**
  - Nainstaluj pomocí: `pip install playwright-axe`
- **Chyba: server neběží:**
  - Spusť Django server: `python manage.py runserver`
- **Chyba: test selže na přihlášení:**
  - Ověř, že existuje testovací uživatel a správné heslo.

# Jak generovat a archivovat pa11y reporty

## Hromadné testování přístupnosti (a11y)

1. Ujisti se, že běží Django server (např. `python manage.py runserver`)
2. Spusť skript pro HTML reporty:
   
   ```zsh
   ./pa11y_batch.sh
   ```
   Výsledky najdeš ve složce `pa11y_a11y_reports_YYYY-MM-DD/` a v ZIP archivu.

3. Pro CSV reporty spusť:
   
   ```zsh
   ./pa11y_batch_csv.sh
   ```

4. Archivace:
   
   ```zsh
   zip -r pa11y_a11y_reports_$(date +%Y-%m-%d).zip pa11y_a11y_reports_$(date +%Y-%m-%d)/
   ```

## Interpretace výsledků
- HTML reporty otevři v prohlížeči (např. `open pa11y_a11y_reports_2025-05-30/pa11y_klienti_report.html`)
- CSV reporty lze načíst v Excelu nebo Google Sheets
- Pokud jsou reporty prázdné (pouze hlavička), nebyly nalezeny žádné zásadní chyby

## Sdílení a archivace
- ZIP archiv můžeš přiložit k dokumentaci, auditu nebo sdílet v týmu
- Staré reporty můžeš mazat nebo archivovat podle potřeby

# Správa snapshotů a reportů

Pro udržení přehledného workspace a efektivní spolupráci je důležité pravidelně archivovat, čistit a spravovat snapshoty UI a reporty přístupnosti (a11y). Následující postupy a příkazy jsou optimalizované pro macOS a shell zsh.

## Archivace snapshotů a reportů

- **Zkomprimování složky se snapshoty nebo reporty do ZIP archivu:**
  ```zsh
  zip -r snapshot_html_$(date +%Y-%m-%d).zip snapshot_html_$(date +%Y-%m-%d)/
  zip -r pa11y_a11y_reports_$(date +%Y-%m-%d).zip pa11y_a11y_reports_$(date +%Y-%m-%d)/
  ```
- **Rozbalení archivu:**
  ```zsh
  unzip snapshot_html_2025-05-30.zip
  unzip pa11y_a11y_reports_2025-05-30.zip
  ```

## Úklid dočasných a nepotřebných souborů

- **Smazání dočasných souborů:**
  ```zsh
  find . -name '*.bak' -delete
  find . -name '*.log' -delete
  find . -name '*.pyc' -delete
  find . -name '__pycache__' -type d -exec rm -r {} +
  find . -name '*.png' -delete
  ```
- **Smazání starých snapshotů a reportů (např. starších než 14 dní):**
  ```zsh
  find . -type f -name '*snapshot*.gz' -mtime +14 -delete
  find . -type f -name '*report*.gz' -mtime +14 -delete
  ```

## Vizuální kontrola reportů a snapshotů

- **Otevření HTML snapshotu/reportu v prohlížeči (po rozbalení a dekomprimaci):**
  ```zsh
  gunzip snapshot_html_2025-05-30/klient_list_snapshot.html.gz
  open snapshot_html_2025-05-30/klient_list_snapshot.html
  ```

## Automatizace úklidu

- Pro pravidelný úklid workspace použij shell skript `cleanup_workspace.sh` (viz níže) a/nebo nastav cron úlohu.
- Příklad nastavení cron úlohy na macOS:
  ```zsh
  crontab -e
  # Přidej řádek pro denní úklid v 1:00
  0 1 * * * /Users/patrikluks/Applications/hypoteky/cleanup_workspace.sh
  ```

---

Více best practices a příkladů najdeš v sekci [Onboarding a troubleshooting](#onboarding-a-troubleshooting).

---

## Správa snapshotů a a11y reportů (automatizace v CI/CD)

Podrobné informace najdete v souboru `README_snapshot_a11y_management.md`.

- Snapshoty UI a a11y reporty jsou generovány a kontrolovány automaticky při každém commitu (viz workflow `.github/workflows/ci.yml`).
- Výsledky najdete v artefaktech buildu na GitHubu.
- Pro troubleshooting a správu viz doporučení v přiloženém README.

