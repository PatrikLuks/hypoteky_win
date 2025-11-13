# CODE_REVIEW_CHECKLIST.md

> Praktický checklist pro code review v hypoteční aplikaci (Django, React, shell skripty)
> Pomáhá udržet vysokou kvalitu, bezpečnost a onboarding nových vývojářů.

---

## 1. Kód a architektura
- [ ] Kód je čitelný, dobře komentovaný a srozumitelný i pro studenta.
- [ ] Dodržuje best practices (Django, Python, React, shell skripty).
- [ ] Používá typové anotace, pojmenované konstanty, validuje vstupy.
- [ ] Neobsahuje zbytečné duplicity, TODO/FIXME, mrtvý kód.
- [ ] Kód je optimalizován pro slabší hardware (dávkování, lazy loading, omezený paralelismus).

## 2. Testy a spolehlivost
- [ ] Nová logika má unit/integration testy, snapshoty, případně e2e/a11y testy.
- [ ] Testy pokrývají edge-case scénáře a chybové stavy.
- [ ] Všechny testy procházejí v CI.

## 3. Bezpečnost a compliance
- [ ] Kód neobsahuje hardcoded credentials, citlivá data ani klíče.
- [ ] Ošetřuje vstupy, chrání proti XSS, CSRF, SQLi, session hijackingu.
- [ ] Respektuje role, oprávnění a auditní logování.
- [ ] Závislosti jsou bezpečné (viz safety scan, check_requirements_security.sh).

## 4. UI, UX a přístupnost
- [ ] UI je přístupné (a11y), má správné role, aria-label, kontrast, ovládání klávesnicí.
- [ ] Snapshoty a vizuální testy odpovídají aktuálnímu stavu.
- [ ] Kód je responsivní a podporuje tmavý/světlý režim.

## 5. Dokumentace a onboarding
- [ ] README, ONBOARDING a checklisty jsou aktuální a srozumitelné.
- [ ] Nové skripty mají popis, příklady použití a komentáře.
- [ ] Všechny změny jsou zdokumentované v changelogu nebo v pull requestu.

---

> **Tip:** Checklist pravidelně aktualizuj podle vývoje projektu a potřeb týmu.

---

*Checklist připravil Copilot pro efektivní code review a onboarding.*
