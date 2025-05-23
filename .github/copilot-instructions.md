<!-- Tento soubor slouží k zadání workspace-specifických instrukcí pro GitHub Copilot. Další informace: https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# Kontext projektu

Tento projekt je moderní webová aplikace pro správu hypoték, určená finančním poradcům. Umožňuje detailní evidenci a správu případů klientů podle přesně definovaného workflow (15 kroků od záměru klienta po čerpání a splácení). Backend je postaven na Django, databáze je MySQL.

## Workflow hypotéky (kroky)

1. Jméno klienta
2. Co chce klient financovat
3. Návrh financování
4. Výběr banky
5. Příprava žádosti
6. Kompletace podkladů
7. Podání žádosti
8. Odhad
9. Schvalování
10. Příprava úvěrové dokumentace
11. Podpis úvěrové dokumentace
12. Příprava čerpání
13. Čerpání
14. Zahájení splácení
15. Podmínky pro splacení

Každý klient prochází těmito kroky. Krok je vždy jednoznačně identifikovatelný a má svůj stav, datum, případně poznámku.

---

# Hlavní cíle a doporučení pro generovaný kód

## Uživatelská zkušenost a UI

- Implementuj e-mailové notifikace pro klienty i poradce (deadliny, změny stavu, zamítnutí).
- Dbej na plně responsivní design (tabulky, grafy, formuláře).
- Přidej možnost přepínání tmavého/světlého režimu.

## Funkcionalita

- U každého klienta eviduj historii změn (kdo, kdy, co upravil).
- Umožni přidávat poznámky, úkoly a připomínky ke klientovi.
- Implementuj export/import klientů a hypoték do/z CSV/XLSX.
- Umožni pokročilé filtrování a vyhledávání klientů (stav, banka, částka, datum atd.).

## Bezpečnost a správa

- Vytvoř auditní log všech důležitých akcí v systému.
- Implementuj role a oprávnění (poradce, administrátor, manažer).
- Přidej dvoufaktorovou autentizaci.

## Analytika a reporting

- Zobrazuj pokročilé statistiky (trendy, úspěšnost podle banky, průměrná doba schválení, heatmapy).
- Umožni automatizované reporty zasílané e-mailem.

## Integrace

- Vytvoř REST API pro napojení na externí systémy.
- Umožni export deadlinů do Google/Outlook kalendáře.

---

# Další doporučení pro Copilot

- Preferuj čistý, čitelný a dobře komentovaný kód.
- Dodržuj best practices Django a Pythonu.
- Používej pojmenované konstanty a typové anotace.
- Vždy validuj vstupy a ošetřuj chybové stavy.
- Piš testy pro klíčové části logiky (unit/integration).
- Respektuj bezpečnostní zásady (ochrana dat, autentizace, autorizace).
- Kód piš v češtině, pokud je to vhodné (např. názvy modelů, proměnných, komentáře).

---

Tento soubor pravidelně aktualizuj podle vývoje projektu a potřeb týmu.