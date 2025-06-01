"""
Checklist pro auditní a bezpečnostní review
-------------------------------------------
Používej tento checklist při každém větším releasu nebo bezpečnostním auditu.
"""

# ✅ Auditní a bezpečnostní review checklist
#
# [ ] Všechny důležité akce (editace, smazání, import) vytvářejí záznam v audit logu (model Zmena)
# [ ] Auditní log je chráněn před úpravami a mazáním běžnými uživateli
# [ ] Testy pokrývají rollbacky, hromadné změny a edge-case scénáře
# [ ] Citlivá data jsou šifrována a testována na úrovni DB
# [ ] Oprávnění a role jsou správně nastaveny a testovány (včetně API)
# [ ] Všechny testy procházejí v CI (včetně bezpečnostních a auditních)
# [ ] Dokumentace (README, komentáře) je aktuální a obsahuje příklady bezpečnostních a auditních testů
# [ ] Onboarding a troubleshooting sekce v README jsou aktualizovány

# Audit & security review checklist

"""
Tento checklist použij při bezpečnostním review, auditu nebo při návrhu nových funkcí. Pomůže ti ověřit, že aplikace je robustní, bezpečná a připravená na reálné útoky i edge-case scénáře.
"""

## 1. Oprávnění a role
- [ ] Otestuj, že každý uživatel má pouze přístup ke svým povoleným akcím (poradce, admin, manažer)
- [ ] Ověř, že není možné obejít oprávnění přes API nebo přímé URL
- [ ] Otestuj pokusy o zneužití práv (např. změna cizího klienta, export cizích dat)

## 2. Dvoufaktorová autentizace (2FA)
- [ ] Ověř, že 2FA je vyžadována při přihlášení (OTP, recovery kódy)
- [ ] Otestuj chybné zadání OTP a blokaci po více pokusech
- [ ] Ověř, že recovery kódy fungují a jsou bezpečně generovány

## 3. Šifrování a citlivá data
- [ ] Ověř, že citlivá pole (např. osobní údaje, poznámky) jsou šifrována v DB
- [ ] Otestuj, že šifrovací klíče nejsou ve veřejném repozitáři
- [ ] Ověř, že logy neobsahují citlivá data

## 4. Auditní log a sledování změn
- [ ] Ověř, že všechny důležité akce (změna stavu, export, přihlášení) jsou logovány
- [ ] Otestuj, že auditní log nelze upravit běžným uživatelem
- [ ] Ověř, že logy jsou pravidelně archivovány a chráněny

## 5. Edge-case bezpečnostní scénáře
- [ ] Otestuj chování při selhání DB, SMTP, exportní služby
- [ ] Ověř, že systém správně reaguje na nevalidní vstupy a útoky (XSS, SQLi, CSRF)
- [ ] Otestuj limity API (rate limiting, throttling)

## 6. Best practices
- [ ] Pravidelně aktualizuj závislosti a kontroluj CVE
- [ ] Ověř, že všechny testy bezpečnosti jsou součástí CI/CD pipeline
- [ ] Přidej komentáře a příklady edge-case útoků do testů

---

Checklist pravidelně aktualizuj podle vývoje projektu a nových hrozeb.
