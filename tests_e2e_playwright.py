# Základní e2e test pro Django aplikaci pomocí Playwright (Python)
# Testuje přihlášení a zobrazení dashboardu/klientů
# Spouštějte: pytest tests_e2e_playwright.py

import pytest
from playwright.sync_api import sync_playwright

@pytest.mark.e2e
def test_login_and_dashboard():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        # Předpokládáme spuštěný Django server na http://localhost:8000
        page.goto('http://localhost:8000/login/')
        page.fill('input[name="username"]', 'testlist')
        page.fill('input[name="password"]', 'testpass')
        page.click('button[type="submit"]')
        # Po přihlášení počkej na některý z možných textů (Dashboard, Seznam klientů, Moje hypotéka)
        try:
            page.wait_for_selector('text=Dashboard', timeout=3000)
        except Exception:
            try:
                page.wait_for_selector('text=Seznam klientů', timeout=2000)
            except Exception:
                page.wait_for_selector('text=Moje hypotéka', timeout=2000)
        # Pro ladění vypiš aktuální URL po přihlášení
        print('Aktuální URL po přihlášení:', page.url)
        # Ověř, že je vidět některý z hlavních textů
        assert page.is_visible('text=Dashboard') or page.is_visible('text=Seznam klientů') or page.is_visible('text=Moje hypotéka')
        # Ověř, že je vidět uživatelské jméno
        assert page.is_visible('text=testlist')
        browser.close()

@pytest.mark.e2e
def test_vytvoreni_klienta():
    """
    E2E test: Přihlášení, vytvoření nového klienta, kontrola v seznamu a detailu.
    """
    from datetime import date
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        # Přihlášení
        page.goto('http://localhost:8000/login/')
        page.fill('input[name="username"]', 'testlist')
        page.fill('input[name="password"]', 'testpass')
        page.click('button[type="submit"]')
        # Počkej na přesměrování
        try:
            page.wait_for_selector('text=Dashboard', timeout=3000)
        except Exception:
            try:
                page.wait_for_selector('text=Seznam klientů', timeout=2000)
            except Exception:
                page.wait_for_selector('text=Moje hypotéka', timeout=2000)
        # Přejdi na stránku pro přidání klienta
        page.goto('http://localhost:8000/klient/pridat/')
        # Vyplň povinná pole
        page.fill('input[name="jmeno"]', 'Testovací Klient E2E')
        page.fill('input[name="datum"]', date.today().isoformat())
        page.fill('input[name="co_financuje"]', 'Byt v Praze')
        page.fill('input[name="cena"]', '5000000')
        page.fill('input[name="navrh_financovani"]', 'Standardní hypotéka')
        page.fill('input[name="navrh_financovani_procento"]', '80')
        # Odeslat formulář
        page.click('button[type="submit"]')
        # Po uložení by měl být klient v seznamu
        page.goto('http://localhost:8000/klienti/')
        page.wait_for_selector('text=Testovací Klient E2E', timeout=3000)
        assert page.is_visible('text=Testovací Klient E2E')
        # Otevři detail klienta přes první tlačítko "Detail" ve stejném řádku
        row = page.locator('tr', has_text='Testovací Klient E2E')
        row.locator('a:has-text("Detail")').first.click()
        # Pro ladění vypiš aktuální URL a ulož screenshot
        print('URL po kliknutí na detail:', page.url)
        page.screenshot(path='e2e_detail_klient.png')
        page.wait_for_selector('text=Detail klienta', timeout=3000)
        assert page.is_visible('text=Detail klienta')
        assert page.is_visible('text=Byt v Praze')
        browser.close()

# Poznámka: Pro běh testu spusťte Django server (python manage.py runserver) a Playwright musí být nainstalován:
# pip install pytest playwright
# playwright install
