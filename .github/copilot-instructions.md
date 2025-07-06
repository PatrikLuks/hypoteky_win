# Copilot Instructions for Project Management
# AKTUÁLNÍ PRIORITY (červen 2025)

## 1. Nasazení (deployment)
- Vždy ověř build frontendu (`npm run build`) a proveď `python manage.py collectstatic --noinput`.
- Před nasazením spusť všechny testy (`pytest`), proveď zálohu DB a ověř migrace (`python manage.py migrate --plan`).
- Ověř, že jsou správně nastavené proměnné prostředí (DB, SECRET_KEY, DEBUG, EMAIL, HTTPS).
- Pro produkci používej Gunicorn/Uvicorn + Nginx/Apache, logování a monitoring.

## 2. CI/CD
- Všechny commity na main/pull requesty musí projít CI (viz `.github/workflows/ci.yml`).
- CI pipeline: build, testy, collectstatic, lint, (volitelně deploy).
- Chyby v CI řeš ihned, build musí být vždy zelený.

## 3. Bezpečnostní audit
- Pravidelně spouštěj bezpečnostní skripty (`./check_requirements_security.sh`, `safety check`).
- Ověř role, šifrování citlivých dat, auditní logy, HTTPS, GDPR.
- Proveď penetrační testy (SQLi, XSS, CSRF, brute-force, session hijacking).
- Ověř možnost exportu/smazání dat klienta (GDPR).

## 4. Onboarding
- Udržuj aktuální README a ONBOARDING.md – popis instalace, testů, buildů, nasazení, troubleshooting.
- Přidávej příklady, komentáře a návody pro nové vývojáře.
- Vysvětluj workflow pro review, merge, CI/CD a nasazení.

## 5. README
- README musí obsahovat: rychlý start, build, testy, nasazení, CI/CD, bezpečnost, onboarding, troubleshooting.
- Pravidelně aktualizuj podle změn v projektu a procesů.

## 6. Finální checklist pro předprodukční fázi (červen 2025)
- Projdi všechny klíčové workflow aplikace ručně i automatizovaně (unit, integrační, e2e testy, edge-cases).
- Otestuj import/export, reporting, notifikace, bezpečnostní funkce.
- Proveď penetrační testy (SQLi, XSS, CSRF, brute-force, session hijacking).
- Ověř šifrování citlivých dat, auditní logy, správné nastavení rolí a oprávnění.
- Zkontroluj GDPR – možnost exportu/smazání dat klienta.
- Ověř build frontendu a statiku, proveď collectstatic.
- Zkontroluj konfiguraci prostředí (SECRET_KEY, DEBUG=False, DB, EMAIL, HTTPS).
- Připrav rollback plán a zálohu databáze.
- Aktualizuj README a ONBOARDING.md – popiš build, testy, nasazení, troubleshooting, onboarding.
- Ověř, že onboarding je srozumitelný i pro nováčky.
- Ověř, že CI pipeline je plně automatizovaná a spolehlivá.
- Nastav monitoring výkonu, chyb a alerty na kritické události.
- Spusť pilotní provoz s reálnými daty, sleduj chování aplikace, logy a zpětnou vazbu uživatelů.
- Pokud je vše splněno, zaměř se na optimalizaci výkonu, UX, rozšíření testů nebo plánování dalšího rozvoje produktu.

## 7. Priority pro předprodukční a postprodukční fázi (červen 2025)
- Důsledně otestuj všechny workflow (unit, integrační, e2e, edge-cases) – ručně i automatizovaně.
- Pravidelně prováděj bezpečnostní kontroly a penetrační testy (SQLi, XSS, CSRF, brute-force, session hijacking).
- Ověř šifrování citlivých dat, auditní logy, správné nastavení rolí a GDPR.
- Udržuj aktuální a srozumitelný onboarding pro nové vývojáře (README, ONBOARDING.md, troubleshooting, příklady).
- Nastav monitoring výkonu, chyb a alerty na kritické události (např. Sentry, Grafana, e-mail/SMS notifikace).
- Připrav rollback plán a pravidelně zálohuj databázi i statiku.
- Spusť pilotní provoz s reálnými daty, sleduj chování aplikace, logy a zpětnou vazbu uživatelů.
- Po pilotním provozu zaměř se na optimalizaci výkonu, UX, rozšíření testů a plánování dalšího rozvoje produktu.
- Pravidelně iteruj a zlepšuj procesy podle reálných zkušeností a zpětné vazby.

---

> **Poznámka pro Copilot:**
> Všechny generované odpovědi, kód i komentáře musí reflektovat tyto aktuální priority. Vždy přidávej konkrétní rady, checklisty a návody pro nasazení, CI/CD, audit, onboarding a údržbu README. Pokud uživatel neví, co dál, navrhni další krok z těchto oblastí.
