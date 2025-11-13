# SECURITY_AUDIT_CHECKLIST.md

> Praktický checklist pro bezpečnostní audit hypoteční aplikace (Django, MySQL, shell skripty)
> Pomáhá odhalit slabiny před reálným nasazením a zvýšit důvěryhodnost aplikace.

---

## 1. Závislosti a aktualizace
- [ ] Proveď `check_requirements_security.sh` a `safety scan` – oprav všechny nalezené zranitelnosti.
- [ ] Ověř, že nejsou použity balíčky s kritickými CVE bez známé opravy.
- [ ] Aktualizuj všechny závislosti na bezpečné verze.

## 2. Autentizace a autorizace
- [ ] Ověř, že je aktivní 2FA pro poradce i adminy.
- [ ] Otestuj edge-case scénáře (ztráta zařízení, recovery, změna hesla).
- [ ] Ověř, že každý endpoint a šablona správně validuje oprávnění a role.

## 3. Šifrování a ochrana dat
- [ ] Ověř, že všechna citlivá data jsou šifrována v DB (např. pomocí Django field encryption).
- [ ] Ověř, že komunikace probíhá pouze přes HTTPS (TLS certifikát).
- [ ] Otestuj exporty a zálohy – neobsahují citlivá data v nešifrované podobě?

## 4. Ochrana proti útokům
- [ ] Otestuj SQL injection, XSS, CSRF, brute-force, session hijacking (ručně nebo pomocí penetračních nástrojů).
- [ ] Ověř, že všechny vstupy jsou validovány a ošetřeny.
- [ ] Ověř, že session cookies mají atributy Secure, HttpOnly, SameSite.

## 5. Auditní logování a monitoring
- [ ] Ověř, že všechny změny, exporty a přístupy jsou logovány (uživatel, IP, čas, akce).
- [ ] Pravidelně kontroluj logy a nastav alerty na podezřelé akce.
- [ ] Ověř, že logy neobsahují citlivá data.

## 6. GDPR a compliance
- [ ] Implementuj správu souhlasů, export a smazání dat klienta na žádost.
- [ ] Přidej sekci o zpracování osobních údajů do dokumentace.
- [ ] Ověř, že lze data anonymizovat nebo smazat dle požadavku klienta.

## 7. Disaster recovery a zálohování
- [ ] Pravidelně zálohuj DB a snapshoty (`backup_workspace.sh`).
- [ ] Ověř obnovitelnost dat (`restore_workspace_from_backup.sh`).
- [ ] Připrav disaster recovery plán a ověř jeho funkčnost.

---

> **Tip:** Audit prováděj před každým větším releasem a po každé změně v bezpečnostní infrastruktuře.

---

*Checklist připravil Copilot pro bezpečné nasazení a audit hypoteční aplikace.*
