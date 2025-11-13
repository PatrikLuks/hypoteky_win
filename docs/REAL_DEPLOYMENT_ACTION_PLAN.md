# Akční plán pro reálné nasazení hypoteční aplikace ve finančním poradenství

> Tento plán pokrývá bezpečnost, compliance, testování, provoz, onboarding a právní požadavky. Každý bod obsahuje konkrétní kroky, doporučené skripty a checklisty.

---

## 1. Bezpečnost a compliance
- [ ] **Penetrační testy**
    - Proveď externí i interní penetrační testy (SQLi, XSS, CSRF, brute-force, session hijacking).
    - Oprav nalezené zranitelnosti.
- [ ] **Šifrování citlivých dat**
    - Ověř, že citlivá pole jsou šifrována v DB (např. pomocí Django field encryption).
    - Ověř, že komunikace probíhá přes HTTPS (TLS certifikát).
- [ ] **2FA a silná autentizace**
    - Aktivuj dvoufaktorovou autentizaci pro poradce i adminy.
    - Otestuj edge-case scénáře (ztráta zařízení, recovery).
- [ ] **Auditní logování**
    - Ověř, že všechny změny, exporty a přístupy jsou logovány (uživatel, IP, čas, akce).
    - Pravidelně kontroluj logy a nastav alerty na podezřelé akce.
- [ ] **GDPR a správa souhlasů**
    - Implementuj správu souhlasů, export a smazání dat klienta na žádost.
    - Přidej sekci o zpracování osobních údajů do dokumentace.
- [ ] **Role a oprávnění**
    - Ověř, že každý uživatel má přístup jen ke svým datům a funkcím dle role.
    - Otestuj všechny role (poradce, admin, manažer) včetně edge-case scénářů.
- [ ] **Pravidelná kontrola závislostí**
    - Spouštěj `check_requirements_security.sh` a `safety scan` před každým nasazením.
    - Aktualizuj závislosti a řeš zranitelnosti.

## 2. Testování a spolehlivost
- [ ] **Pokrytí klíčových workflow testy**
    - Ověř, že všechny hlavní scénáře mají unit, integration, e2e, snapshot a a11y testy.
    - Spusť `run_all_maintenance.sh` a `run_e2e_with_server.sh`.
- [ ] **Testy edge-case scénářů**
    - Přidej testy na nevalidní data, duplicitní záznamy, selhání služeb, výpadky DB.
    - Ověř, že aplikace správně hlásí chyby a loguje incidenty.
- [ ] **Testy importu/exportu a notifikací**
    - Otestuj import/export klientů a hypoték (CSV, XLSX, PDF) včetně validace dat.
    - Otestuj e-mailové notifikace (deadliny, zamítnutí, změny stavu).
- [ ] **Zálohování a obnova**
    - Pravidelně zálohuj DB a snapshoty (`backup_workspace.sh`).
    - Ověř obnovitelnost dat (`restore_workspace_from_backup.sh`).

## 3. UI, UX a přístupnost
- [ ] **Ověření přístupnosti (a11y)**
    - Spouštěj `pa11y_batch_snapshots.sh` a oprav všechny chyby kontrastu, labelů, role, ovládání klávesnicí.
    - Ověř responsivitu a přepínání tmavý/světlý režim.
- [ ] **Snapshot a vizuální testy**
    - Ověř, že všechny hlavní stránky mají aktuální snapshoty a testy procházejí.
    - Archivuj snapshoty před většími změnami.
- [ ] **Dokumentace a onboarding**
    - Aktualizuj `ONBOARDING.md`, README a checklisty (E2E, migrace, snapshoty, a11y).
    - Přidej troubleshooting sekci a příklady pro nové vývojáře.

## 4. Provoz, monitoring a CI/CD
- [ ] **Monitoring a alerting**
    - Nastav monitoring výkonu, chybovosti, dostupnosti a bezpečnostních incidentů.
    - Nastav alerty na kritické chyby a podezřelé akce.
- [ ] **Automatizované nasazení (CI/CD)**
    - Ověř, že build, testy a deploy probíhají automaticky (viz `.github/workflows/ci.yml`).
    - Připrav rollback plán pro případ selhání nasazení.
- [ ] **Pravidelný úklid workspace a logů**
    - Spouštěj úklidové skripty (`cleanup_*`, `find_todos.sh`) a archivuj staré snapshoty mimo hlavní workspace.

## 5. Právní a procesní požadavky
- [ ] **Smluvní dokumentace**
    - Připrav VOP, zásady zpracování osobních údajů, souhlasy.
    - Ověř, že všechny právní požadavky jsou splněny (GDPR, AML, ...).
- [ ] **Disaster recovery plán**
    - Ověř, že lze obnovit data i po havárii (test obnovy).
- [ ] **Školení a podpora pro uživatele**
    - Připrav návody, helpdesk, FAQ a kontakty na podporu.

---

> **Doporučení:**
> - Každý bod checklistu pravidelně reviduj a aktualizuj podle vývoje projektu a legislativy.
> - Před ostrým nasazením proveď pilotní provoz s reálnými daty a audit bezpečnosti.
> - Všechny kroky a poznatky dokumentuj v ONBOARDING.md a sdílej s týmem.

---

*Plán připravil Copilot pro bezpečné a úspěšné nasazení hypoteční aplikace ve finančním poradenství.*
