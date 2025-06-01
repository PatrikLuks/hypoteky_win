"""
Checklist pro review export/reporting funkcí
-------------------------------------------
Používej tento checklist při každé změně nebo přidání export/reporting funkcionality.
"""

# ✅ Export/reporting review checklist
#
# [ ] Exporty probíhají v rámci transakce (atomic) a jsou ošetřeny rollbacky
# [ ] Testy pokrývají edge-case scénáře (prázdná data, velký objem, selhání exportu)
# [ ] Při chybě nevznikne neúplný nebo poškozený soubor
# [ ] Auditní log je konzistentní a odpovídá změnám
# [ ] Dokumentace obsahuje příklady export/reporting scénářů a troubleshooting
# [ ] Onboarding a troubleshooting sekce v README jsou aktualizovány

# Export & reporting review checklist

Tento checklist použij při testování exportů (CSV, XLSX, PDF) a generování reportů. Pomůže ti odhalit edge-case chyby a zvýšit robustnost systému.

## 1. Validace exportovaných dat
- [ ] Ověř, že export obsahuje všechny povinné sloupce a správné formáty
- [ ] Otestuj export s různými filtry (stav, banka, datum, částka)
- [ ] Ověř, že exportované soubory lze otevřít v Excelu, Google Sheets i LibreOffice

## 2. Edge-case scénáře
- [ ] Otestuj export/reporting s prázdnými daty (žádný klient, žádná hypotéka)
- [ ] Otestuj export/reporting s extrémně velkým objemem dat
- [ ] Ověř, že exportované soubory nejsou poškozené a mají správnou velikost

## 3. Chybové stavy a notifikace
- [ ] Otestuj chování při selhání exportu/reportingu (např. nedostupná DB, chyba generování PDF)
- [ ] Ověř, že uživatel dostane srozumitelnou chybovou hlášku
- [ ] Otestuj notifikace o úspěšném/selhaném exportu/reportingu

## 4. Best practices
- [ ] Pravidelně přidávej testy pro nové edge-case scénáře
- [ ] Dokumentuj typické chyby a jejich řešení v README
- [ ] Ověř, že export/reporting testy jsou součástí CI/CD pipeline

---

Checklist pravidelně aktualizuj podle nových požadavků a zkušeností z provozu.
