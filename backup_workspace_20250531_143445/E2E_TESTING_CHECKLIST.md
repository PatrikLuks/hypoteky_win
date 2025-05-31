# Checklist pro E2E/UI/a11y testování a údržbu workspace

## 1. E2E/UI testy (Playwright)
- [x] Automatizované spuštění serveru a testů (`run_e2e_with_server.sh`)
- [ ] Pravidelně spouštět testy před každým nasazením
- [ ] Přidat testy pro edge-case scénáře (nevalidní data, chybějící pole, duplicitní klienti)
- [ ] Snapshot testy hlavních obrazovek (porovnání HTML)
- [ ] Testy přístupnosti (a11y) – např. pomocí pa11y nebo axe-core
- [ ] Ověřit responsivitu a tmavý/světlý režim
- [ ] Ověřit ovládání klávesnicí a ARIA role

## 2. Údržba workspace
- [x] Automatizované skripty pro kontrolu a úklid (`full_workspace_maintenance.sh`)
- [x] Kontrola bezpečnosti závislostí (`check_requirements_security.sh`)
- [x] Kontrola a oprava práv, hlaviček a syntaxe skriptů
- [ ] Pravidelná archivace snapshotů a reportů
- [ ] Kontrola integrity dat a záloh

## 3. CI/CD a onboarding
- [ ] Zařadit E2E testy do CI pipeline (GitHub Actions, GitLab CI, ...)
- [ ] Přidat onboarding sekci do README (jak spustit všechny testy, jak přidat nový test)
- [ ] Vysvětlit best practices pro psaní testů a údržbu

## 4. Další doporučení
- [ ] Pravidelně aktualizovat checklist podle vývoje projektu
- [ ] Sdílet checklist s týmem a revidovat před releasem

---

> Tento checklist slouží jako vzor pro studenta i tým. Každý bod obsahuje doporučení, proč je důležitý a jak jej splnit. Pravidelným používáním checklistu zvýšíš kvalitu, bezpečnost a spolehlivost projektu.
