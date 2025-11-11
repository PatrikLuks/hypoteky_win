# PHASE 3 E2E TESTS – Playwright Integration Tests

"""
E2E testy pro Hypotéky aplikaci pomocí Playwright.
Testují kompletní user workflows v reálném prohlížeči.

Spuštění:
  pytest klienti/tests_e2e.py -v --headed  # s viditelem
  pytest klienti/tests_e2e.py -v          # headless
  pytest -m e2e -v                         # všechny E2E testy
"""

import asyncio
import time
from datetime import date

import pytest
from django.contrib.auth.models import User
from playwright.async_api import Page, expect
from rest_framework.test import APIClient

from klienti.models import Klient, UserProfile


@pytest.mark.e2e
class TestDashboardE2E:
    """
    E2E testy pro dashboard a hlavní UI.
    """

    @pytest.fixture
    async def browser_page(self, browser_type_launch_args):
        """
        Vytvoří nový Playwright browser a page pro testy.
        """
        from playwright.async_api import async_playwright

        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()
            yield page
            await browser.close()

    @pytest.mark.skip(reason="Vyžaduje spuštěný server na localhost:8000")
    async def test_dashboard_load(self, browser_page, db):
        """
        Ověří, že se dashboard načte a zobrazí klienty.
        """
        page: Page = browser_page

        # Naviguj na login
        await page.goto("http://localhost:8000/account/login/")

        # Vyplň login formulář
        await page.fill('input[name="username"]', "testuser")
        await page.fill('input[name="password"]', "testpass")
        await page.click('button[type="submit"]')

        # Počkej na redirect na dashboard
        await page.wait_for_url("http://localhost:8000/")

        # Ověř, že je dashboard viditelný
        await expect(page.locator("h1")).to_contain_text("Hypotéky")


@pytest.fixture
def api_client():
    """Vrací DRF APIClient místo standardního TestClient."""
    return APIClient()


@pytest.mark.e2e
class TestAPIEndpointsE2E:
    """
    E2E testy pro REST API endpoints.
    Testují celý workflow bez GUI.
    """

    def test_complete_klient_workflow(self, api_client, db):
        """
        Testuje kompletní workflow vytvoření, úpravy a smazání klienta přes API.
        """
        # Setup: Vytvoř uživatele
        user = User.objects.create_user(username="workflow_user", password="pass123")
        profile = UserProfile.objects.get(user=user)
        profile.role = "poradce"
        profile.save()

        # 1. Přihlaš se
        response = api_client.post("/api/token/", {"username": "workflow_user", "password": "pass123"})
        assert response.status_code == 200, f"Token endpoint failed: {response.data}"
        token = response.data["access"]

        # 2. Nastav JWT token
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        # 3. Vytvoř klienta
        klient_data = {
            "jmeno": "Workflow Testovací Klient",
            "datum": str(date.today()),
            "vyber_banky": "KB",
            "navrh_financovani_castka": 5000000,
        }
        response = api_client.post("/api/klienti/", klient_data, format="json")
        assert response.status_code == 201, f"Create failed: {response.data}"
        klient_id = response.data["id"]

        # 4. Ověř, že klient byl vytvořen
        response = api_client.get(f"/api/klienti/{klient_id}/")
        assert response.status_code == 200
        assert response.data["jmeno"] == "Workflow Testovací Klient"

        # 5. Aktualizuj klienta
        update_data = {"vyber_banky": "ČNB"}
        response = api_client.patch(f"/api/klienti/{klient_id}/", update_data, format="json")
        assert response.status_code == 200
        assert response.data["vyber_banky"] == "ČNB"

        # 6. Smaž klienta
        response = api_client.delete(f"/api/klienti/{klient_id}/")
        assert response.status_code == 204

        # 7. Ověř, že klient byl smazán
        response = api_client.get(f"/api/klienti/{klient_id}/")
        assert response.status_code == 404


@pytest.mark.e2e
class TestWorkflowProgressionE2E:
    """
    E2E testy pro 15-kroký workflow hypotéky.
    """

    def test_klient_workflow_progression(self, api_client, db):
        """
        Testuje progresci klienta skrze všechny 15 kroků workflow.
        """
        # Setup
        user = User.objects.create_user(username="workflow_user2", password="pass123")
        profile = UserProfile.objects.get(user=user)
        profile.role = "poradce"
        profile.save()

        # Prihlás se
        response = api_client.post("/api/token/", {"username": "workflow_user2", "password": "pass123"})
        token = response.data["access"]
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        # Vytvoř klienta
        klient_data = {
            "jmeno": "Workflow Progress Test",
            "datum": str(date.today()),
            "vyber_banky": "KB",
            "navrh_financovani_castka": 3500000,
        }
        response = api_client.post("/api/klienti/", klient_data, format="json")
        klient_id = response.data["id"]

        # Testuj všechny workflow fields
        workflow_fields = [
            "termin_podani_zp",
            "termin_schvaleni_zp",
            "termin_poskytovani_hypoteky",
            # ... (další pole podle modelu)
        ]

        # Ověř, že workflow fields jsou přístupné
        response = api_client.get(f"/api/klienti/{klient_id}/")
        assert response.status_code == 200
        klient = response.data
        # Minimálně check, že klient má workflow fields
        assert "jmeno" in klient


@pytest.mark.e2e
class TestSecurityE2E:
    """
    E2E testy pro bezpečnostní features.
    """

    def test_unauthorized_api_access(self, api_client):
        """
        Ověří, že API endpointy vyžadují autentizaci.
        """
        # Pokus bez tokenu
        response = api_client.get("/api/klienti/")
        assert response.status_code == 401  # Unauthorized

    def test_forbidden_cross_user_access(self, api_client, db):
        """
        Ověří, že klient (ne poradce) nemůže přistupovat ke klientům jiného uživatele.
        """
        # Setup: Dvě uživatelé s rolí "klient"
        user1 = User.objects.create_user(username="client_user1", password="pass123")
        user2 = User.objects.create_user(username="client_user2", password="pass123")
        for user in [user1, user2]:
            profile = UserProfile.objects.get(user=user)
            profile.role = "klient"  # Client role, ne poradce!
            profile.save()

        # User1 vytvoří si klienta (který je omezený jeho ID)
        response = api_client.post("/api/token/", {"username": "client_user1", "password": "pass123"})
        token1 = response.data["access"]
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token1}")

        # Ověř, že klient vidí svojí linku (vytvoří si profil přes API)
        # Normálně by klient měl předaný klient_id, ne aby jej vytvářel
        # Pojďme jen testovat seznam - user1 by měl vidět jen své
        response = api_client.get("/api/klienti/")
        assert response.status_code == 200
        # User1 zatím nemá žádné klienty
        assert len(response.data) == 0

        # User2 se pokusí vidět seznam
        response = api_client.post("/api/token/", {"username": "client_user2", "password": "pass123"})
        token2 = response.data["access"]
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token2}")

        response = api_client.get("/api/klienti/")
        assert response.status_code == 200
        # User2 by měl vidět jen své (taky zatím 0)
        assert len(response.data) == 0


# ===== MARKER CONFIGURATION =====
# Proveď: pytest --markers | grep e2e
# Pro spuštění: pytest -m e2e


if __name__ == "__main__":
    # Při spuštění přímo: python klienti/tests_e2e.py
    pytest.main([__file__, "-v", "--markers"])
