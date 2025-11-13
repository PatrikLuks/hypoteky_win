# Struktura Projektu Hypoteky

## 📁 Přehled Adresářů

```
hypoteky_win/
├── dev/                          ← Vývojové skripty a utility
│   ├── snapshots/                  HTML snímky UI (test artifacts)
│   ├── data/                        Testovací data a backup
│   ├── check_*.sh                  Diagnostické skripty
│   ├── cleanup_*.sh                Čistící skripty
│   ├── fix_*.sh                    Opravné skripty
│   ├── pa11y_*.sh                  Accessibility testovací skripty
│   └── ... další utility skripty
│
├── docs/                         ← Projektová dokumentace
│   ├── README.md                   Úvodní dokumentace
│   ├── ONBOARDING.md               Onboarding pro nové vývojáře
│   ├── TROUBLESHOOTING_GUIDE.md    Řešení problémů
│   ├── PROJECT_STRUCTURE.md        Tato dokumentace
│   ├── PHASE_*.md                  Reporty jednotlivých fází
│   └── ... další dokumenty
│
├── hypoteky/                     ← Django hlavní aplikace
│   ├── settings.py                 Hlavní nastavení
│   ├── urls.py                     Hlavní URL routing
│   ├── wsgi.py                     WSGI konfigurece
│   └── asgi.py                     ASGI konfigurace
│
├── klienti/                      ← Django aplikace pro správu klientů
│   ├── models.py                   Datové modely
│   ├── views.py                    Pohledy (view functions)
│   ├── forms.py                    Django formuláře
│   ├── serializers.py              DRF serializéry
│   ├── urls.py                     URL routing aplikace
│   ├── admin.py                    Django admin
│   ├── tests_views.py              View layer testy (23 testů)
│   ├── tests_e2e.py                End-to-end testy (4 testy)
│   └── tests/                      Test moduly
│
├── static/                       ← Statické soubory (CSS, JS, obrázky)
│   ├── css/
│   ├── js/
│   ├── images/
│   └── fonts/
│
├── tests/                        ← Integrační testy
│   ├── conftest.py                 Pytest konfigurace
│   └── test_*.py                   Integrační testy
│
├── .github/                      ← GitHub workflows
│   └── workflows/                  CI/CD pipeline
│
├── manage.py                     ← Django management script
├── pytest.ini                    ← Pytest konfigurace
├── pyproject.toml                ← Project metadata
├── requirements.txt              ← Production dependencies
├── requirements-dev.txt          ← Development dependencies
└── .gitignore                    ← Git ignore rules
```

## 📌 Důležité Lokace

| Co Hledáš | Kde Najdeš |
|-----------|-----------|
| **Zdrojový kód** | `klienti/` a `hypoteky/` |
| **Testy** | `klienti/tests_*.py` a `tests/` |
| **Nastavení** | `hypoteky/settings.py` |
| **Databázové modely** | `klienti/models.py` |
| **Pohledy (Views)** | `klienti/views.py` |
| **API endpointy** | `klienti/urls.py` a `klienti/views.py` |
| **Dokumentace** | `docs/` |
| **Dev skripty** | `dev/` |
| **Testy (E2E)** | `klienti/tests_e2e.py` |
| **Testy (Views)** | `klienti/tests_views.py` |

## 🧪 Test Struktura

### Testy Views (`klienti/tests_views.py`)
- `TestKlientCreateView` - 4 testy
- `TestKlientDetailView` - 3 testy
- `TestKlientEditView` - 3 testy
- `TestKlientDeleteView` - 2 testy
- `TestDashboardView` - 4 testy
- `TestReportingView` - 3 testy
- `TestReportingExportView` - 2 testy
- `TestViewPermissions` - 2 testy

**Výsledek:** 23/23 testů (100%) ✅

### E2E Testy (`klienti/tests_e2e.py`)
- `TestDashboardE2E` - API workflow testy
- `TestAPIEndpointsE2E` - CRUD operace
- `TestWorkflowProgressionE2E` - Komplexní scénáře
- `TestSecurityE2E` - Bezpečnostní testy

**Výsledek:** 4/5 testů (1 skipped) ✅

### Integrační Testy (`tests/test_*.py`)
- Ověření celkové integrity systému
- API v kontextu celé aplikace

**Výsledek:** 11/11 testů ✅

### Celková Pokrytí Kódem
- **Overall Coverage:** 85% (cíl: >70%) ✅
- **View Layer:** 74% (zlepšeno o +30%)
- **Models:** 90%
- **Admin:** 100%

## 🛠️ Spuštění & Vývoj

### Spuštění Serveru
```bash
source .venv/bin/activate
python manage.py runserver
```

### Spuštění Testů
```bash
# Všechny testy
pytest

# Jen view testy
pytest klienti/tests_views.py

# Jen E2E testy
pytest klienti/tests_e2e.py

# S pokrytím kódu
pytest --cov=klienti --cov-report=html

# Konkrétní test
pytest klienti/tests_views.py::TestKlientCreateView::test_create_success
```

### Nastavení Prostředí
```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput
```

## 📦 Závislosti

Všechny závislosti jsou v:
- `requirements.txt` - Produkční závislosti
- `requirements-dev.txt` - Vývojové závislosti (pytest, black, flake8, atd.)

## 🚀 Deployment

Aplikace je připravena na deployment s:
- ✅ 85% code coverage
- ✅ 95.7% test success rate (88/92)
- ✅ Bezpečnostní testy
- ✅ GDPR compliance checks
- ✅ Permission checks v testech

Viz `docs/PHASE_3_FINAL_REPORT.md` pro detaily deployment readiness.

## 📝 Git Workflow

- **Main branch** - Stabilní, produkční kód
- **Feature branches** - Vývoj nových features
- **PR reviews** - Code review proces

Všechny commity procházejí CI pipeline (viz `.github/workflows/`).

---

**Poslední aktualizace:** Červen 2025  
**Správce struktury:** Copilot & Team
