"""
Checklist pro review e2e a a11y testů
-------------------------------------
Používej tento checklist při každé změně nebo přidání e2e/a11y testů.
"""

# ✅ e2e/a11y review checklist
#
# Tento checklist použij při end-to-end testování přístupnosti (a11y) pomocí nástrojů jako pa11y, axe nebo Playwright. Pomůže ti ověřit, že aplikace je přístupná pro všechny uživatele.
#
# ## 1. Klávesnicová ovladatelnost
# - [ ] Ověř, že všechny formuláře, tabulky a tlačítka lze ovládat pouze klávesnicí
# - [ ] Otestuj správné pořadí focusu (tabindex)
# - [ ] Ověř, že všechny interaktivní prvky mají viditelný focus
#
# ## 2. Kontrast a barvy
# - [ ] Otestuj kontrast textu a pozadí (min. 4.5:1 pro běžný text)
# - [ ] Ověř, že aplikace je čitelná v tmavém i světlém režimu
#
# ## 3. Role, aria-label a popisky
# - [ ] Ověř, že všechny důležité prvky mají správné role a aria-label
# - [ ] Otestuj, že obrázky mají alt popisky
# - [ ] Ověř, že tabulky mají popisky a záhlaví
#
# ## 4. Edge-case scénáře
# - [ ] Otestuj přístupnost při chybových stavech (zobrazování chybových hlášek)
# - [ ] Ověř, že modální okna a dialogy jsou přístupná a správně uzavíratelná
# - [ ] Otestuj přístupnost na různých zařízeních a velikostech obrazovky
#
# ## 5. Automatizace a best practices
# - [ ] Pravidelně spouštěj pa11y_batch.sh a pa11y_batch_csv.sh
# - [ ] Archivuj a kontroluj a11y reporty (HTML, CSV)
# - [ ] Ověř, že a11y testy jsou součástí CI/CD pipeline
# - [ ] Dokumentuj typické chyby a jejich řešení v README
#
# ---
#
# Checklist pravidelně aktualizuj podle nových požadavků a zkušeností z provozu.
