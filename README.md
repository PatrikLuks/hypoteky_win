# Hypotéky – správa případů pro finanční poradce

Tento projekt je moderní webová aplikace pro správu hypoték určená finančním poradcům. Umožňuje evidenci případů klientů krok po kroku podle workflow finančního poradce (15 kroků od záměru klienta po čerpání a splácení).

## Technologie
- Python, Django
- MySQL

## Spuštění projektu
1. Vytvořte a aktivujte virtuální prostředí:
   ```sh
   python3 -m venv venv
   source venv/bin/activate
   ```
2. Nainstalujte závislosti:
   ```sh
   pip install -r requirements.txt
   ```
3. Proveďte migrace a spusťte server:
   ```sh
   python manage.py migrate
   python manage.py runserver
   ```

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
15. Podmínky pro vyčerpání

## Poznámky
- Pro připojení k MySQL upravte `settings.py` dle údajů k databázi.
- Projekt je ve vývoji.
