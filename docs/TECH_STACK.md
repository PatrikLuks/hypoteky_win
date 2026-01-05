# 🛠️ Tech Stack - Detailní Seznam Technologií

**Projekt:** Hypoteky - Django aplikace pro správu hypotečních klientů  
**Datum:** Prosinec 2025  
**Status:** Production Ready

---

## 📋 Obsah
1. [Backend - Python & Django](#backend---python--django)
2. [Frontend - HTML/CSS/JS](#frontend---htmlcssjs)
3. [Databáze](#databáze)
4. [API & REST](#api--rest)
5. [Šifrování & Bezpečnost](#šifrování--bezpečnost)
6. [Testing & QA](#testing--qa)
7. [Data Processing & Export](#data-processing--export)
8. [DevOps & CI/CD](#devops--cicd)
9. [Vývojové Nástroje](#vývojové-nástroje)
10. [Externí Služby](#externí-služby)

---

## Backend - Python & Django

### Core Framework
| Technologie | Verze | Účel |
|---|---|---|
| **Python** | 3.12.3 | Runtime |
| **Django** | 4.2.27 | Web framework |
| **Django ORM** | 4.2.27 | Databázové mapování |

### Django Extensions & Add-ons
| Balíček | Verze | Účel |
|---|---|---|
| **djangorestframework** | 3.16.1 | REST API |
| **djangorestframework-simplejwt** | 5.5.1 | JWT autentizace |
| **drf-yasg** | 1.21.10 | Swagger/OpenAPI dokumentace |
| **django-filter** | 25.1 | Filtrování v API |
| **django-otp** | 1.6.3 | One-Time Password (OTP) |
| **django-two-factor-auth** | 1.18.1 | 2FA autentizace |
| **django-encrypted-model-fields** | 0.6.5 | Šifrování polí v DB |
| **django-formtools** | 2.5.1 | Vícekrokové formuláře |
| **django-phonenumber-field** | 8.3.0 | Telefonní čísla |

### Aplikace v Projektu
| Aplikace | Obsah |
|---|---|
| **klienti** | Models, Views, API, Permissions |
| **hypoteky** | Django settings, URLs, ASGI/WSGI |

---

## Frontend - HTML/CSS/JS

### CSS Framework
| Technologie | Verze | Účel |
|---|---|---|
| **Bootstrap** | 5.3.0 | CSS framework (CDN) |
| **Vlastní CSS** | - | Dark theme, custom styling |

### Icon Library
| Technologie | Verze | Účel |
|---|---|---|
| **FontAwesome** | 6.x | Icons (local + CDN) |

### Typography
| Technologie | Účel |
|---|---|
| **Google Fonts - Inter** | Bezpatkové písmo |

### JavaScript Grafika
| Technologie | Verze | Účel |
|---|---|---|
| **Chart.js** | latest (CDN) | Grafy a vizualizace (pie, bar, line) |

### Frontend Features
- **Responsive Design** - Mobile-first design (Bootstrap)
- **Dark Theme** - Custom CSS pro tmavý design (#181a1b, #ffd700)
- **Grafy:** Pie chart, Bar chart, Line chart (workflow, klienti, objem)
- **Tabulky** - Bootstrap tables s custom styling
- **Modální okna** - Bootstrap modals
- **Formuláře** - Django forms + Bootstrap styling

---

## Databáze

### Primární Databáze
| Technologie | Verze | Účel |
|---|---|---|
| **MySQL** | 8.0+ | Produkční databáze |
| **mysqlclient** | 2.2.7 | Python MySQL driver |

### Testovací Databáze
| Technologie | Verze | Účel |
|---|---|---|
| **SQLite** | 3.x | Unit testy (in-memory) |

### Konfigurační Features
- Charset: **UTF-8MB4**
- Collation: **utf8mb4_unicode_ci**
- Mode: **STRICT_TRANS_TABLES**
- Šifrování: **Fernet (cryptography)** pro citlivá pole

---

## API & REST

### REST API Stack
| Komponenta | Technologie | Verze |
|---|---|---|
| **Framework** | Django REST Framework | 3.16.1 |
| **Autentizace** | SimplJWT | 5.5.1 |
| **Dokumentace** | drf-yasg (Swagger/OpenAPI) | 1.21.10 |
| **Filtrování** | django-filter | 25.1 |

### Endpoint Typy
- **CRUD operace** - KlientViewSet, HypotekaWorkflowViewSet, PoznamkaViewSet, ZmenaViewSet
- **Filtrace** - Banka, stav, částka (min/max), datum (od/do), zamítnutí
- **Řazení** - Datum, částka financování
- **Hledání** - Banka, co financuje (šifrované pole)

### Authentication Mechanisms
1. **JWT** (JSON Web Tokens) - Pro SPA/mobilní klienty
2. **Session Auth** - Pro prohlížeč
3. **Basic Auth** - Pro API testy

---

## Šifrování & Bezpečnost

### Cryptography
| Technologie | Verze | Účel |
|---|---|---|
| **cryptography** | 45.0.3 | Fernet šifrování |
| **django-encrypted-model-fields** | 0.6.5 | Encryption v databázi |

### Šifrovaná Pole (Modely)
```python
- jmeno (EncryptedCharField)
- co_financuje (EncryptedCharField)
```

### Bezpečnostní Middleware & Features
| Feature | Popis |
|---|---|
| **HTTPS Redirect** | `SECURE_SSL_REDIRECT=True` (produkce) |
| **HSTS** | `SECURE_HSTS_SECONDS=31536000` (1 rok) |
| **CSRF Protection** | Django CSRF middleware |
| **Session Security** | `SESSION_COOKIE_SECURE=True` |
| **X-Frame-Options** | `DENY` (anti-clickjacking) |
| **XSS Protection** | `SECURE_BROWSER_XSS_FILTER=True` |
| **Content-Type Sniffing** | `SECURE_CONTENT_TYPE_NOSNIFF=True` |
| **OTP** | django-otp (one-time passwords) |
| **2FA** | django-two-factor-auth |

### Encryption Keys
- **ENCRYPTED_MODEL_FIELDS_KEY** - Fernet klíč (z .env)
- **SECRET_KEY** - Django secret (z .env)

---

## Testing & QA

### Test Runners
| Technologie | Verze | Účel |
|---|---|---|
| **pytest** | 8.3.5 | Test framework |
| **pytest-django** | 4.11.1 | Django integrace |
| **Faker** | 37.3.0 | Generování testovacích dat |

### Test Automation & E2E
| Technologie | Verze | Účel |
|---|---|---|
| **Playwright** | 1.52.0 | Browser automation (E2E) |

### Test Coverage
| Metrika | Hodnota |
|---|---|
| **Code Coverage** | 85% |
| **Počet Testů** | 93+ |
| **Test Kategorie** | unit, integration, e2e, api |

### Test Typy v Projektu
1. **Unit Tests** - models, utils, serializers
2. **View Tests** - HTTP responses, permissions
3. **API Tests** - REST endpoints, filtering
4. **E2E Tests** - Playwright (browser automation)
5. **Security Tests** - encryption, permissions, GDPR
6. **Import/Export Tests** - CSV, XLSX
7. **Notifikace Tests** - email notifications
8. **Reporting Tests** - export, PDF generation

---

## Data Processing & Export

### Excel & XLSX
| Technologie | Verze | Účel |
|---|---|---|
| **openpyxl** | 3.1.5 | Excel workbook manipulation |

### Image & PDF
| Technologie | Verze | Účel |
|---|---|---|
| **Pillow** | 11.3.0 | Image processing |
| **reportlab** | - | PDF generation (plánováno) |

### HTML Parsing
| Technologie | Verze | Účel |
|---|---|---|
| **beautifulsoup4** | 4.13.4 | HTML parsing (testy) |

### QR Kódy
| Technologie | Verze | Účel |
|---|---|---|
| **qrcode** | 7.4.2 | Generování QR kódů |

### Data Utilities
| Technologie | Verze | Účel |
|---|---|---|
| **requests** | 2.32.4 | HTTP klient |
| **python-dateutil** | 2.9.0 | Date utilities |
| **PyYAML** | 6.0.2 | YAML parsing |
| **sqlparse** | 0.5.3 | SQL parsing |
| **phonenumbers** | 9.0.5 | Phone number utils |
| **phonenumberslite** | 9.0.6 | Phone number lite |

---

## DevOps & CI/CD

### Konfigurační Systém
| Technologie | Verze | Účel |
|---|---|---|
| **python-dotenv** | 1.1.0 | Environment variables (.env) |

### Web Server (Produkce)
| Technologie | Účel |
|---|---|
| **Gunicorn** | WSGI app server |
| **Uvicorn** | ASGI app server (alternativa) |
| **Nginx** | Reverse proxy |

### CI/CD Pipeline
| Nástroj | Soubor |
|---|---|
| **GitHub Actions** | `.github/workflows/ci.yml` |

### Workflow Kroku
1. Lint (isort, pylint)
2. Type checking (mypy)
3. Unit & API testy (pytest)
4. E2E testy (Playwright)
5. Code coverage report
6. Security checks
7. Collectstatic
8. (Volitelně) Deploy

---

## Vývojové Nástroje

### Linting & Formatting
| Technologie | Verze | Účel |
|---|---|---|
| **pylint** | 3.3.7 | Linting |
| **isort** | 6.0.1 | Import sorting |
| **black** | - | Code formatting (pyproject.toml) |

### Type Checking
| Technologie | Verze | Účel |
|---|---|---|
| **mypy** | 1.15.0 | Static type checking |

### Security Tools
| Technologie | Verze | Účel |
|---|---|---|
| **safety** | 3.5.1 | Dependency vulnerability check |

### Code Quality
| Nástoj | Účel |
|---|---|
| **pytest-cov** | Coverage reporting |
| **htmlcov** | HTML coverage reports |

### Configuration Files
| Soubor | Obsah |
|---|---|
| **pyproject.toml** | Black, isort, mypy, pylint config |
| **pytest.ini** | Pytest markers (unit, e2e, api, security) |

---

## Externí Služby

### Email
| Služba | Konfigurace |
|---|---|
| **Gmail SMTP** | `EMAIL_BACKEND`, `EMAIL_HOST`, `EMAIL_PORT=587` |
| **Custom SMTP** | Podporováno přes .env |

### Telefonní Čísla
| Technologie | Verze | Účel |
|---|---|---|
| **phonenumber_field** | 8.3.0 | Telefonní pole |
| **phonenumbers** | 9.0.5 | Phone number library |

### Časozóny
| Technologie | Verze | Účel |
|---|---|---|
| **pytz** | 2025.2 | Timezone data |
| **tzdata** | 2025.2 | IANA timezone data |

---

## 📦 Zависимости - Přehled

### Production Dependencies (21)
```
Django==4.2.27
django-encrypted-model-fields==0.6.5
django-filter==25.1
django-formtools==2.5.1
django-otp==1.6.3
django-phonenumber-field==8.3.0
django-two-factor-auth==1.18.1
djangorestframework==3.16.1
djangorestframework-simplejwt==5.5.1
mysqlclient==2.2.7
phoneumbers==9.0.5
phonenumberslite==9.0.6
pillow==11.3.0
python-dateutil==2.9.0.post0
python-dotenv==1.1.0
pytz==2025.2
PyYAML==6.0.2
qrcode==7.4.2
requests==2.32.4
sqlparse==0.5.3
tzdata==2025.2
```

### Development Dependencies (60+)
- **Testing:** pytest, pytest-django, playwright, Faker
- **Linting:** pylint, isort, black, mypy
- **Security:** cryptography, safety
- **Data:** openpyxl, beautifulsoup4, matplotlib, numpy, pandas
- **API Docs:** drf-yasg
- **Utilities:** Various supporting libraries

---

## 🎯 Architekturní Schéma

```
┌─────────────────────────────────────────────────────┐
│           Frontend (Browser)                        │
│  ┌──────────┐  ┌──────────┐  ┌──────────────┐      │
│  │Bootstrap │  │Chart.js  │  │FontAwesome   │      │
│  │CSS/JS    │  │Grafy     │  │Icons         │      │
│  └──────────┘  └──────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────┘
                      ↓ HTTP/HTTPS
┌─────────────────────────────────────────────────────┐
│     Django Application (Python 3.12)               │
│  ┌──────────────────────────────────────────┐      │
│  │  Views, Models, Forms, Templates        │      │
│  │  (Views, Templates, Static Files)       │      │
│  └──────────────────────────────────────────┘      │
│  ┌──────────────────────────────────────────┐      │
│  │  Django REST Framework (API)             │      │
│  │  (ViewSets, Serializers, Permissions)   │      │
│  └──────────────────────────────────────────┘      │
│  ┌──────────────────────────────────────────┐      │
│  │  Middleware & Security                   │      │
│  │  (CSRF, HTTPS, OTP, 2FA)                │      │
│  └──────────────────────────────────────────┘      │
│  ┌──────────────────────────────────────────┐      │
│  │  Encryption (Fernet, django-encrypted)   │      │
│  │  (Šifrovaná pole: jmeno, co_financuje)  │      │
│  └──────────────────────────────────────────┘      │
└─────────────────────────────────────────────────────┘
                      ↓ SQL
┌─────────────────────────────────────────────────────┐
│     MySQL Database (UTF-8MB4)                       │
│  ┌──────────────────────────────────────────┐      │
│  │  Tables: Klient, Zmena, Poznamka, User  │      │
│  │  Encrypted Fields                        │      │
│  │  Charset: utf8mb4_unicode_ci             │      │
│  └──────────────────────────────────────────┘      │
└─────────────────────────────────────────────────────┘
```

---

## ✅ Klíčové Features

### Autentizace & Autorizace
- Session-based (Django)
- JWT (REST API)
- OTP (one-time passwords)
- Two-factor authentication (2FA)
- Role-based access control (RBAC) - Poradce vs Klient

### Data Management
- CRUD operace (Django admin + Web UI + REST API)
- Import/Export (CSV, XLSX)
- Šifrování citlivých dat (Fernet)
- Auditní logy (Zmena model)
- Soft-delete fields

### Komunikace
- Email notifikace (Django signals)
- Phone number validation
- QR kódy

### Reporting
- Excel export (openpyxl)
- PDF generation (reportlab)
- Grafy a statistiky (Chart.js, matplotlib)
- Dashboard visualization

### Testing
- 85% code coverage
- 93+ automatizovaných testů
- Unit, API, E2E, Security testy
- Playwright browser automation

---

## 🔐 Bezpečnostní Standard

| Aspekt | Implementace |
|---|---|
| **Šifrování v tránsitu** | HTTPS, TLS 1.2+ |
| **Šifrování dat** | Fernet (128-bit) |
| **Hesla** | Django password hasher (PBKDF2, Argon2) |
| **CSRF** | Django CSRF token |
| **XSS** | Template escaping, CSP (volitelně) |
| **SQL Injection** | ORM + parameterized queries |
| **Session** | Secure session cookies |
| **Autentizace** | 2FA + OTP |

---

## 📊 Statistiky

| Metrika | Hodnota |
|---|---|
| **Python Verze** | 3.12.3 |
| **Django Verze** | 4.2.27 |
| **Počet Dependencies** | 81+ |
| **Code Coverage** | 85% |
| **Test Count** | 93+ |
| **API Endpoints** | 10+ |
| **Database Tables** | 6+ |

---

## 🚀 Nasazení

### Produkční Server
```bash
Gunicorn + Nginx + MySQL + HTTPS
Environment: Linux (preferován)
```

### Development
```bash
Python manage.py runserver
SQLite (automaticky v testech)
DEBUG=True
```

### Testing
```bash
pytest - unit, integration, e2e
Playwright - browser automation
Coverage reporting - htmlcov/
```

---

## 📝 Poznámky

1. **Dependencies se mohou měnit** - Zkontroluj `requirements.txt` a `requirements-dev.txt` pro aktuální verze
2. **Frontend libraries jsou z CDN** - Bootstrap, Chart.js, FontAwesome (CDN links)
3. **Lokální FontAwesome** - Je v `static/fontawesome/` (offline dostupnost)
4. **Šifrování vyžaduje KEY** - `ENCRYPTED_MODEL_FIELDS_KEY` musí být v `.env`
5. **Email config** - Je načítán z `.env` (EMAIL_HOST, EMAIL_PORT, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)

---

**Poslední aktualizace:** Prosinec 2025  
**Údržba:** Patří do Regular Code Reviews a Dependency Updates
