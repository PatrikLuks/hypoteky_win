# Onboarding checklist pro nové vývojáře

Tento checklist ti pomůže rychle a bez chyb nastartovat vývoj v projektu hypoteky. Všechny kroky jsou optimalizované pro macOS a shell zsh.

---

## 1. První spuštění projektu
- [ ] Zkontroluj, že máš nainstalovaný Python 3.9+ a pip
- [ ] Vytvoř a aktivuj virtuální prostředí:
  ```zsh
  python3 -m venv venv
  source venv/bin/activate
  ```
- [ ] Nainstaluj závislosti:
  ```zsh
  pip install -r requirements.txt
  ```
- [ ] Nastav databázi podle `DB_SETUP_MYSQL.md`
- [ ] Proveď migrace:
  ```zsh
  python manage.py migrate
  ```
- [ ] Spusť server:
  ```zsh
  python manage.py runserver
  ```

## 2. Testování a úklid
- [ ] Spusť všechny testy:
  ```zsh
  pytest
  ```
- [ ] Spusť e2e a a11y testy:
  ```zsh
  ./pa11y_batch.sh
  ./pa11y_batch_csv.sh
  python tests_e2e_playwright.py
  ```
- [ ] Proveď úklid workspace:
  ```zsh
  ./cleanup_workspace.sh
  ```

## 3. Generování a kontrola reportů/snapshotů
- [ ] Zkomprimuj nové snapshoty a reporty:
  ```zsh
  zip -r snapshot_html_$(date +%Y-%m-%d).zip snapshot_html_$(date +%Y-%m-%d)/
  zip -r pa11y_a11y_reports_$(date +%Y-%m-%d).zip pa11y_a11y_reports_$(date +%Y-%m-%d)/
  ```
- [ ] Otevři report/snapshot v prohlížeči:
  ```zsh
  gunzip snapshot_html_2025-05-30/klient_list_snapshot.html.gz
  open snapshot_html_2025-05-30/klient_list_snapshot.html
  ```

## 4. Troubleshooting
- [ ] Pokud narazíš na chybu, zkontroluj logy a README sekci troubleshooting
- [ ] Ověř, že máš správně nastavené prostředí (Python, DB, závislosti)
- [ ] Proveď úklid workspace a restartuj server

## 5. Best practices a tipy
- [ ] Před commitem vždy spusť testy a úklid
- [ ] Pravidelně archivuj snapshoty a reporty
- [ ] Dodržuj pojmenování a strukturu složek
- [ ] Piš komentáře a dokumentuj edge-case scénáře

---

Více checklistů najdeš v adresáři `tests/`.
