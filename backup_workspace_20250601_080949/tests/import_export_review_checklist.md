"""
Checklist pro review import/export funkcí
----------------------------------------
Používej tento checklist při každé změně nebo přidání import/export funkcionality.
"""

# ✅ Import/export review checklist
#
# Tento checklist použij při testování importu/exportu klientů a hypoték (CSV, XLSX, PDF). Pomůže ti odhalit edge-case chyby a zvýšit robustnost systému.
#
# ## 1. Validace dat
# - [ ] Otestuj import s nevalidními daty (chybějící pole, špatný formát, nečíselné hodnoty)
# - [ ] Ověř, že systém správně hlásí chyby a neimportuje nevalidní záznamy
# - [ ] Otestuj import s duplicitními záznamy (stejné ID, e-mail, rodné číslo)
# - [ ] Ověř, že duplicitní záznamy jsou správně ošetřeny (upozornění, přeskočení, merge)
#
# ## 2. Edge-case scénáře
# - [ ] Otestuj import/export s extrémně velkým objemem dat (tisíce záznamů)
# - [ ] Ověř, že systém zvládne import/export bez pádu a s rozumnou dobou odezvy
# - [ ] Otestuj import/export s prázdným souborem
# - [ ] Ověř, že export obsahuje všechny povinné sloupce a správné formáty
#
# ## 3. Chybové stavy a notifikace
# - [ ] Otestuj chování při selhání importu/exportu (např. nedostupná DB, špatná přípona souboru)
# - [ ] Ověř, že uživatel dostane srozumitelnou chybovou hlášku
# - [ ] Otestuj notifikace o úspěšném/selhaném importu/exportu
#
# ## 4. Best practices
# - [ ] Pravidelně přidávej testy pro nové edge-case scénáře
# - [ ] Dokumentuj typické chyby a jejich řešení v README
# - [ ] Ověř, že import/export testy jsou součástí CI/CD pipeline
#
# ---
#
# Checklist pravidelně aktualizuj podle nových požadavků a zkušeností z provozu.
