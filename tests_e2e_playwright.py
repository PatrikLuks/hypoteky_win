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

@pytest.mark.e2e
def test_editace_klienta():
    """
    E2E test: Editace existujícího klienta, ověření změny v detailu i seznamu.
    """
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
        # Najdi klienta v seznamu
        page.goto('http://localhost:8000/klienti/')
        page.wait_for_selector('text=Testovací Klient E2E', timeout=3000)
        row = page.locator('tr', has_text='Testovací Klient E2E')
        row.locator('a:has-text("Detail")').first.click()
        page.wait_for_selector('text=Detail klienta', timeout=3000)
        # Klikni na tlačítko Upravit (místo Editace)
        page.click('a:has-text("Upravit")')
        page.wait_for_selector('input[name="co_financuje"]', timeout=3000)
        # Změň pole "Co chce klient financovat"
        page.fill('input[name="co_financuje"]', 'Rodinný dům')
        page.click('button[type="submit"]')
        # Ověř změnu v detailu
        page.wait_for_selector('text=Detail klienta', timeout=3000)
        assert page.is_visible('text=Rodinný dům')
        # Ověř změnu v seznamu
        page.goto('http://localhost:8000/klienti/')
        page.wait_for_selector('text=Rodinný dům', timeout=3000)
        assert page.is_visible('text=Rodinný dům')
        browser.close()

# POZOR: Tento test není robustní vůči duplicitám a slouží pouze jako ukázka edge-case selhání.
# Doporučujeme používat pouze test_smazani_klienta_unikat pro ostré testování.
@pytest.mark.skip(reason="Test není robustní vůči duplicitám, používej test_smazani_klienta_unikat.")
def test_smazani_klienta():
    """
    E2E test: Smazání klienta přes UI, ověření že není v seznamu.
    """
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
        # Najdi klienta v seznamu
        page.goto('http://localhost:8000/klienti/')
        page.wait_for_selector('text=Testovací Klient E2E', timeout=3000)
        row = page.locator('tr', has_text='Testovací Klient E2E')
        row.locator('a:has-text("Detail")').first.click()
        page.wait_for_selector('text=Detail klienta', timeout=3000)
        # Klikni na tlačítko Smazat
        page.click('a:has-text("Smazat")')
        # Po kliknutí na Smazat čekej na nadpis potvrzovací stránky
        page.wait_for_selector('text=Potvrzení smazání klienta', timeout=3000)
        # Potvrď smazání
        page.click('button:has-text("Ano, smazat")')
        # Ověř, že klient už není v seznamu
        page.goto('http://localhost:8000/klienti/')
        page.wait_for_timeout(1000)
        assert not page.is_visible('text=Testovací Klient E2E')
        browser.close()

@pytest.mark.e2e
def test_smazani_klienta_unikat():
    """
    E2E test: Vytvoření a smazání unikátního klienta přes UI, ověření že není v seznamu.
    """
    from datetime import datetime
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
        # Vytvoř unikátního klienta
        unik_jmeno = f"Testovací Klient E2E {datetime.now().strftime('%Y%m%d%H%M%S')}"
        page.goto('http://localhost:8000/klient/pridat/')
        page.fill('input[name="jmeno"]', unik_jmeno)
        page.fill('input[name="datum"]', datetime.now().date().isoformat())
        page.fill('input[name="co_financuje"]', 'Byt na testování')
        page.fill('input[name="cena"]', '1234567')
        page.fill('input[name="navrh_financovani"]', 'Test hypotéka')
        page.fill('input[name="navrh_financovani_procento"]', '80')
        page.click('button[type="submit"]')
        # Ověř, že klient je v seznamu
        page.goto('http://localhost:8000/klienti/')
        page.wait_for_selector(f'text={unik_jmeno}', timeout=3000)
        assert page.is_visible(f'text={unik_jmeno}')
        # Otevři detail a smaž klienta
        row = page.locator('tr', has_text=unik_jmeno)
        row.locator('a:has-text("Detail")').first.click()
        page.wait_for_selector('text=Detail klienta', timeout=3000)
        page.click('a:has-text("Smazat")')
        page.wait_for_selector('text=Potvrzení smazání klienta', timeout=3000)
        page.click('button:has-text("Ano, smazat")')
        # Ověř, že klient už není v seznamu
        page.goto('http://localhost:8000/klienti/')
        page.wait_for_timeout(1000)
        assert not page.is_visible(f'text={unik_jmeno}')
        browser.close()

@pytest.mark.e2e
def test_export_report_pdf():
    """
    E2E test: Vytvoření klienta a export reportu do PDF přes UI.
    """
    from datetime import datetime
    import os
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(accept_downloads=True)
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
        # Vytvoř unikátního klienta
        unik_jmeno = f"Testovací Klient E2E {datetime.now().strftime('%Y%m%d%H%M%S')}"
        page.goto('http://localhost:8000/klient/pridat/')
        page.fill('input[name="jmeno"]', unik_jmeno)
        page.fill('input[name="datum"]', datetime.now().date().isoformat())
        page.fill('input[name="co_financuje"]', 'Byt na export')
        page.fill('input[name="cena"]', '1234567')
        page.fill('input[name="navrh_financovani"]', 'Test hypotéka')
        page.fill('input[name="navrh_financovani_procento"]', '80')
        page.click('button[type="submit"]')
        # Přejdi na reporting a spusť export do PDF
        page.goto('http://localhost:8000/reporting/')
        page.wait_for_selector('a:has-text("Export do PDF")', timeout=3000)
        with page.expect_download() as download_info:
            page.click('a:has-text("Export do PDF")')
        download = download_info.value
        path = download.path()
        assert path is not None and os.path.exists(path)
        # Ověř, že PDF není prázdné
        assert os.path.getsize(path) > 1000  # typicky několik kB
        browser.close()

@pytest.mark.e2e
def test_a11y_dashboard():
    """
    Ověří přístupnost dashboardu pomocí axe-core (vyžaduje playwright-axe).
    Pokud není playwright-axe nainstalován, test se přeskočí.
    """
    try:
        import importlib
        if importlib.util.find_spec('playwright_axe') is None:
            import pytest
            pytest.skip("playwright-axe není nainstalován")
        from playwright_axe import Axe
    except ImportError:
        import pytest
        pytest.skip("playwright-axe není nainstalován")
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto('http://localhost:8000/login/')
        page.fill('input[name="username"]', 'testlist')
        page.fill('input[name="password"]', 'testpass')
        page.click('button[type="submit"]')
        page.wait_for_selector('text=Dashboard', timeout=3000)
        axe = Axe(page)
        axe.inject()
        results = axe.run()
        violations = [v for v in results['violations'] if v['impact'] in ('critical', 'serious')]
        assert not violations, f"A11y chyby: {violations}"
        browser.close()

# Poznámka: Pro běh testu spusťte Django server (python manage.py runserver) a Playwright musí být nainstalován:
# pip install pytest playwright
# playwright install
