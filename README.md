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
