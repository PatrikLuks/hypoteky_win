"""
Checklist pro review PDF/e-mailových reportů
-------------------------------------------
Používej tento checklist při každé změně nebo přidání PDF/e-mail reporting funkcionality.
"""

# ✅ PDF/e-mail reporting review checklist
#
# [ ] Exporty probíhají v rámci transakce (atomic) a jsou ošetřeny rollbacky
# [ ] Testy pokrývají edge-case scénáře (prázdná data, neexistující e-mail, selhání exportu)
# [ ] Při chybě nevznikne neúplný nebo poškozený soubor/příloha
# [ ] Auditní log je konzistentní a odpovídá změnám
# [ ] Dokumentace obsahuje příklady PDF/e-mail scénářů a troubleshooting
# [ ] Onboarding a troubleshooting sekce v README jsou aktualizovány

# PDF & e-mail reporting review checklist

Tento checklist použij při testování generování PDF reportů a doručování e-mailů (včetně příloh, lokalizace a edge-case situací).

## 1. Generování PDF
- [ ] Ověř, že PDF reporty obsahují všechny povinné informace a správné formátování
- [ ] Otestuj generování PDF s různými daty (prázdné, velké objemy, speciální znaky)
- [ ] Ověř, že PDF lze otevřít ve všech běžných prohlížečích a aplikacích

## 2. Doručování e-mailů
- [ ] Otestuj odeslání e-mailu s PDF přílohou (úspěch, selhání SMTP)
- [ ] Ověř, že e-mail dorazí správnému příjemci a není označen jako spam
- [ ] Otestuj lokalizaci obsahu e-mailu (CZ/EN)
- [ ] Ověř, že příloha není poškozená a má správnou velikost

## 3. Edge-case scénáře
- [ ] Otestuj chování při selhání generování PDF nebo odeslání e-mailu
- [ ] Ověř, že uživatel dostane srozumitelnou chybovou hlášku
- [ ] Otestuj doručení e-mailu s velkou přílohou (limit velikosti)

## 4. Best practices
- [ ] Pravidelně přidávej testy pro nové edge-case scénáře
- [ ] Dokumentuj typické chyby a jejich řešení v README
- [ ] Ověř, že PDF/e-mail testy jsou součástí CI/CD pipeline

---

Checklist pravidelně aktualizuj podle nových požadavků a zkušeností z provozu.
