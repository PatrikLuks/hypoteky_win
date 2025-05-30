"""
Checklist pro code review a přidávání nových funkcí/testů
---------------------------------------------------------
Používej tento checklist při každém pull requestu nebo větší změně v projektu.
"""

# ✅ Code review checklist
#
# [ ] Kód je čitelný, dobře komentovaný a srozumitelný i pro studenta
# [ ] Všechny nové funkce mají odpovídající unit/integration testy
# [ ] Jsou pokryty edge-case scénáře (nevalidní vstupy, chybějící pole, selhání služeb)
# [ ] Testy procházejí lokálně i v CI (GitHub Actions)
# [ ] Vstupy jsou validovány a chybové stavy správně ošetřeny
# [ ] Kód respektuje bezpečnostní zásady (autentizace, autorizace, šifrování)
# [ ] Dokumentace (README, komentáře) je aktuální a srozumitelná
# [ ] Pokud je to relevantní, jsou přidány snapshot/a11y/UI/e2e testy
# [ ] Nové šablony nebo změny v UI jsou responsivní a přístupné
# [ ] Onboarding a troubleshooting sekce v README jsou aktualizovány

# ✅ Checklist pro přidání nové funkce/testu
#
# [ ] Funkce je pokryta testy (včetně edge-case)
# [ ] Testy jsou srozumitelné a obsahují komentáře
# [ ] Pokud je to relevantní, je přidán příklad do dokumentace
# [ ] Kód je v češtině tam, kde je to vhodné
# [ ] Funkce je bezpečná a validuje vstupy
# [ ] Všechny změny jsou commitnuty a pushnuty na GitHub

# Best practices & code review checklist

"""
Tento checklist používej při psaní nových testů, rozšiřování projektu nebo code review. Pomůže ti udržet vysokou kvalitu, bezpečnost a čitelnost kódu.
"""

## 1. Psaní testů
# - [ ] Každá klíčová funkce má unit/integration test (včetně edge-case scénářů)
# - [ ] Testy pokrývají import/export, reporting, notifikace, API, šifrování, bezpečnost
# - [ ] Pro UI a e2e testy používej Playwright/Selenium, pro a11y pa11y/axe
# - [ ] Testy obsahují komentáře a příklady pro studenty
# - [ ] Testuj chybové stavy, selhání externích služeb, limity API
#
## 2. Validace vstupů a edge-case
# - [ ] Všechny vstupy jsou validovány (formuláře, API, importy)
# - [ ] Ošetřeny jsou nevalidní data, duplicitní záznamy, chybějící pole, špatné formáty
# - [ ] Testuj extrémní objemy dat a nestandardní situace
#
## 3. Bezpečnost a role
# - [ ] Ověř, že role a oprávnění jsou správně nastaveny (poradce, admin, manažer)
# - [ ] Testuj pokusy o zneužití práv, neautorizované akce, šifrování citlivých dat
# - [ ] Ověř, že auditní log a 2FA fungují a jsou testovány
#
## 4. Rozšiřování modelů, API, UI
# - [ ] Nové modely mají migrace, testy a validace
# - [ ] API endpointy mají testy (včetně edge-case a chybových stavů)
# - [ ] UI je responsivní, přístupné (a11y), s možností tmavého/světlého režimu
# - [ ] Všechny změny jsou zdokumentovány v README a checklistu
#
## 5. Dokumentace a onboarding
# - [ ] README obsahuje příklady testování, onboarding, troubleshooting
# - [ ] Checklisty v adresáři `tests/` jsou aktuální a přehledné
# - [ ] Nové testy a edge-case scénáře jsou popsány v dokumentaci
#
# ---
#
# Checklist pravidelně aktualizuj podle vývoje projektu a zkušeností z provozu. Odkazuj na další checklisty a sekce v README pro detailní návody.
