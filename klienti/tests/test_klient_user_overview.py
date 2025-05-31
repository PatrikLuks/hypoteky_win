"""
Test: test_klient_user_overview.py
Popis: Testuje skript klient_user_overview.py – ověří, že skript vypíše přiřazení klientů k uživatelům bez chyb.
Autor: GitHub Copilot
Datum: 2025-05-31

Tento test ověřuje, že funkce print_klient_user_overview správně vrací přehled klientů přiřazených uživatelům.
"""

import pytest
from django.contrib.auth.models import User
from klienti.models import Klient
from klienti.scripts.klient_user_overview import print_klient_user_overview

@pytest.mark.django_db
def test_klient_user_overview_output():
    # Vytvoříme testovacího uživatele a klienta
    user = User.objects.create_user(username='testuser', password='testpass')
    klient = Klient.objects.create(jmeno='Test Klient', user=user)
    # Zavoláme přímo funkci, která vrací výstup
    output = print_klient_user_overview()
    assert "Přehled klientů přiřazených uživatelům" in output
    assert "testuser" in output
    assert "Test Klient" in output
    assert "Hotovo." in output

@pytest.mark.django_db
def test_klient_user_overview_klient_bez_uzivatele():
    """
    Testuje edge-case: klient bez přiřazeného uživatele (user=None).
    Ověří, že skript správně vypíše sekci 'Uživatel: (nepřiřazeno)' a klienta v této sekci.
    Tento scénář může nastat např. při importu dat nebo po smazání uživatele.
    """
    klient = Klient.objects.create(jmeno='Klient Bez Uživatele', user=None)
    output = print_klient_user_overview()
    assert 'Uživatel: (nepřiřazeno)' in output
    assert 'Klient Bez Uživatele' in output
    assert 'Hotovo.' in output
