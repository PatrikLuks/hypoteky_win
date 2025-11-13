# 🏦 Hypotéky – Profesionální správa hypoték pro finanční poradce

[![Python](https://img.shields.io/badge/Python-3.12%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-4.2-green?logo=django&logoColor=white)](https://www.djangoproject.com/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0%2B-blue?logo=mysql&logoColor=white)](https://www.mysql.com/)
[![REST API](https://img.shields.io/badge/REST%20API-DRF%2B%20JWT-orange?logo=fastapi&logoColor=white)](https://www.django-rest-framework.org/)
[![Tests](https://img.shields.io/badge/Tests-Pytest%2B%20Playwright-green?logo=pytest&logoColor=white)](https://pytest.org/)
[![2FA](https://img.shields.io/badge/2FA-Enabled-success?logo=auth0&logoColor=white)](https://github.com/wolph/django-otp)
[![Code Style](https://img.shields.io/badge/Code%20Style-Black%2B%20isort-000?logo=github&logoColor=white)](https://github.com/psf/black)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> **Moderní webová aplikace pro správu hypoték s kompletním workflow, reporting, API a bezpečnostními prvky.**  
> Určena finančním poradcům, manažerům a administrátorům pro evidenci a správu případů klientů.

---

## 🎯 Hlavní Funkce

### 📊 Workflow & Správa
- ✅ **15-kroký workflow hypotéky** (od záměru po splácení)
- ✅ **Deadline management** s notifikacemi (e-mail, UI)
- ✅ **Poznámky a úkoly** na každém kroku
- ✅ **Auditní log** všech změn (kdo, kdy, co)
- ✅ **Pokročilé filtrování** a vyhledávání

### 📈 Reporting & Analýzy
- ✅ **Live dashboard** s KPI a statistikami
- ✅ **Grafy** (timeline, workflow heatmapy, trendy)
- ✅ **Export do PDF, Excel, iCal** (Google/Outlook)
- ✅ **Email reporty** (plánované)
- ✅ **CSV import/export**

### 🔐 Bezpečnost & Správa
- ✅ **2-Factor Authentication (2FA)** – TOTP + SMS
- ✅ **Šifrování citlivých dat** (encrypted-model-fields)
- ✅ **Role & Oprávnění** (poradce, admin, manažer, klient)
- ✅ **API s JWT autentizací** + session auth
- ✅ **GDPR support** (export/smazání dat)

### 🚀 Technologie
- ✅ **REST API** (Django REST Framework + Swagger/Redoc)
- ✅ **Responsivní UI** (Bootstrap 5, tmavý režim)
- ✅ **Real-time notifikace** (e-mail)
- ✅ **Automatizované reporty** (management command)
- ✅ **Testy** (unit, integration, e2e)

---

## 🛠️ Technologický Stack

| Komponenta | Technologie |
|-----------|-------------|
| Backend | Python 3.12, Django 4.2 |
| API | Django REST Framework, JWT, Swagger |
| Database | MySQL 8.0+ (SQLite pro dev/testy) |
| Frontend | HTML5, Bootstrap 5, Chart.js, FontAwesome |
| 2FA | django-otp, two-factor-auth |
| Šifrování | cryptography, Fernet |
| Export | openpyxl (Excel), reportlab (PDF), icalendar (iCal) |
| Testing | pytest, Playwright, coverage |
| Code Quality | Black, isort, Flake8, mypy |

---

## 🚀 Quick Start (1 minuta)

### Na macOS / Linux
```bash
git clone https://github.com/PatrikLuks/hypoteky_django.git
cd hypoteky
./start.sh
```
Server poběží na http://localhost:8000

### Na Windows
```cmd
git clone https://github.com/PatrikLuks/hypoteky_django.git
cd hypoteky
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
Server poběží na http://localhost:8000

---

## 📖 Kompletní Instalace

### 1. Klonování a Setup
```bash
git clone https://github.com/PatrikLuks/hypoteky_django.git
cd hypoteky
```

### 2. Virtuální Prostředí
```bash
# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate

# Windows
python -m venv .venv
.venv\Scripts\activate
```

### 3. Instalace Závislostí
```bash
pip install -r requirements.txt

# Dev/Test dependencies (volitelné)
pip install -r requirements-dev.txt
pip install playwright
python -m playwright install --with-deps
```

### 4. Nastavení Prostředí (.env)
```bash
cp .env.example .env
```

**Vyplň hodnoty v `.env`:**
- `DEBUG=True` (development) či `False` (production)
- `ALLOWED_HOSTS=localhost,127.0.0.1`
- `DB_NAME, DB_USER, DB_PASSWORD, DB_HOST` (MySQL)
- `ENCRYPTED_MODEL_FIELDS_KEY` (ze `cryptography.fernet.Fernet.generate_key()`)
- `EMAIL_HOST_USER, EMAIL_HOST_PASSWORD` (Gmail + App Password)

### 5. Database Setup

**Pro MySQL:**
```bash
# Vytvoř databázi a uživatele (viz DB_SETUP_MYSQL.md)
python manage.py migrate
python manage.py createsuperuser
```

**Pro SQLite (vývoj):**
- Settings.py automaticky detekuje SQLite pro testy
- Nebo manuálně: uprav DATABASES v settings.py

### 6. Spuštění Serveru
```bash
python manage.py runserver
# nebo
gunicorn hypoteky.wsgi:application  # production
```

### 7. Admin Přístup
- 🔗 Admin: http://localhost:8000/admin/
- 📊 Dashboard: http://localhost:8000/
- 📚 API Docs: http://localhost:8000/api/docs/

---

## 🧪 Testování

### Unit & Integration Testy
```bash
# Spustit všechny testy
pytest

# Konkrétní test file
pytest klienti/tests/ -v

# S coverage reportem
pytest --cov=klienti --cov-report=html
# Viz htmlcov/index.html
```

### E2E Testy (Playwright)
```bash
# Spuštění serveru + testy
./run_e2e_with_server.sh
# nebo
pytest -m e2e
```

### Bezpečnostní Testy
```bash
# SQL Injection, XSS, CSRF, brute-force
pytest klienti/tests_bezpecnost.py -v

# Linting + security scan
./check_requirements_security.sh
safety scan
bandit -r klienti/ hypoteky/
```

---

## 📦 Deployment

### Development Server
```bash
python manage.py runserver
```

### Production (Gunicorn + Nginx)
```bash
# Build static files
python manage.py collectstatic --noinput

# Spustit Gunicorn
gunicorn hypoteky.wsgi:application --workers 4 --bind 0.0.0.0:8000

# Nginx config (viz deployment/nginx.conf.example)
```

### Docker (volitelně)
```bash
docker build -t hypoteky .
docker run -p 8000:8000 -e DEBUG=False hypoteky
```

### Deploymentní Checklist
Viz **DEPLOYMENT_CHECKLIST.md** pro kompletní instrukce:
- [ ] `.env` nastavená pro produkci
- [ ] DEBUG=False
- [ ] ALLOWED_HOSTS správně
- [ ] SSL/HTTPS certifikát
- [ ] Databáze zálohovaná
- [ ] Static files buildnuty
- [ ] Testy prošly
- [ ] Security audit prošel

---

## 📚 Dokumentace

| Dokument | Obsah |
|----------|-------|
| [ONBOARDING.md](ONBOARDING.md) | Setup pro nové vývojáře |
| [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md) | Nasazení na produkci |
| [SECURITY_AUDIT_CHECKLIST.md](SECURITY_AUDIT_CHECKLIST.md) | Bezpečnostní audit |
| [TROUBLESHOOTING_GUIDE.md](TROUBLESHOOTING_GUIDE.md) | Řešení problémů |
| [DB_SETUP_MYSQL.md](DB_SETUP_MYSQL.md) | MySQL konfigurace |
| [API_DOCUMENTATION.md](API_DOCUMENTATION.md) | REST API endpoints |

---

## 🔌 REST API

### Authentication
```bash
# Získat token
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"user","password":"pass"}'

# Refresh token
curl -X POST http://localhost:8000/api/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{"refresh":"<refresh_token>"}'
```

### Endpoints
- `GET /api/klienti/` – Výpis klientů
- `POST /api/klienti/` – Vytvoření klienta
- `GET /api/klienti/{id}/` – Detail klienta
- `PATCH /api/klienti/{id}/` – Aktualizace
- `DELETE /api/klienti/{id}/` – Smazání

### API Dokumentace
- 📖 **Swagger UI:** http://localhost:8000/api/docs/
- 📋 **ReDoc:** http://localhost:8000/api/redoc/

---

## ⚙️ Konfigurace

### Nastavení E-mailu (Gmail)
1. Aktivuj 2-factor authentication v Google Account
2. Jdi na https://myaccount.google.com/apppasswords
3. Vytvoř "App Password" (16 znaků)
4. Vložit do `.env`:
```env
EMAIL_HOST_USER=tvoj@gmail.com
EMAIL_HOST_PASSWORD=xxxx xxxx xxxx xxxx
```

### Encryption Key
```bash
# Vygeneruj nový klíč
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"

# Vložit do .env
ENCRYPTED_MODEL_FIELDS_KEY=<vygenerovaný klíč>
```

### Databáze (MySQL)
Viz `DB_SETUP_MYSQL.md` pro kompletní instrukce:
```bash
mysql -u root -p
> CREATE DATABASE hypoteky CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
> CREATE USER 'hypoteky'@'localhost' IDENTIFIED BY 'heslo';
> GRANT ALL PRIVILEGES ON hypoteky.* TO 'hypoteky'@'localhost';
> FLUSH PRIVILEGES;
```

---

## 🐛 Troubleshooting

### „ModuleNotFoundError: No module named 'mysqlclient'"
**Řešení:**
```bash
# Linux/macOS
brew install mysql@5.7
pip install mysqlclient

# Windows
pip install mysql-connector-python
```

### „PermissionError: [Errno 13] Permission denied"
**Řešení:**
```bash
chmod -R 755 .
python manage.py collectstatic
```

### „FIELD_ENCRYPTION_KEY defined incorrectly"
**Řešení:**
1. Zkontroluj `.env` – má klíč v ENCRYPTED_MODEL_FIELDS_KEY?
2. Vygeneruj nový: `python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"`

### Testy padají na MySQL
**Řešení:** Použij SQLite pro testy (je v `settings_test.py`)
```bash
DJANGO_SETTINGS_MODULE=hypoteky.settings_test pytest
```

Více: Viz **TROUBLESHOOTING_GUIDE.md**

---

## 🤝 Contributing

1. Vytvoř feature branch: `git checkout -b feature/nova-funkce`
2. Commituj změny: `git commit -am 'Add nova funkce'`
3. Pushni na GitHub: `git push origin feature/nova-funkce`
4. Vytvoř Pull Request

**Před PR:**
- [ ] Testy procházejí (`pytest`)
- [ ] Kód je zformátovaný (`black .`)
- [ ] Importy seřazeny (`isort .`)
- [ ] Linting OK (`flake8 .`)
- [ ] Dokumentace aktuální

---

## 📝 License

MIT – Viz [LICENSE](LICENSE)

---

## 👨‍💼 Autор

**Patrik Luks** – Maturitní projekt  
Praktikant v rodinné firmě na finanční poradenství

---

## 🎯 Budoucí Rozvoj

- [ ] Mobile app (React Native)
- [ ] Integrace s bankovními API
- [ ] Pokročilé reporty (BI dashboards)
- [ ] Multi-language support
- [ ] Mobilní push notifikace

---

## 📞 Support

- 📧 Email: [pluks120@gmail.com](mailto:pluks120@gmail.com)
- 🐙 GitHub: [PatrikLuks/hypoteky_django](https://github.com/PatrikLuks/hypoteky_django)
- 📖 Dokumentace: Viz soubory v kořenovém adresáři

---

**Poslední update:** 11. listopadu 2025  
**Status:** ✅ Production Ready (v1.0)

