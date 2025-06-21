"""
Test: test_rozdel_klienty_mezi_uzivatele.py
Popis: Testuje skript rozdel_klienty_mezi_uzivatele.py – ověří, že klienti jsou rovnoměrně rozděleni mezi poradce.
Autor: GitHub Copilot
Datum: 2025-05-31
"""

import pytest
from django.contrib.auth.models import User
from klienti.models import Klient
from klienti.scripts.rozdel_klienty_mezi_uzivatele import rozdel_klienty_mezi_uzivatele

@pytest.mark.django_db
def test_rozdel_klienty_mezi_uzivatele():
    # Vytvoříme 3 poradce a 6 klientů
    poradci = [User.objects.create_user(username=f'poradce{i}') for i in range(3)]
    for p in poradci:
        p.userprofile.role = 'poradce'
        p.userprofile.save()
    klienti = [Klient.objects.create(jmeno=f'Klient{i}') for i in range(6)]
    # Spustíme rozdělení
    result = rozdel_klienty_mezi_uzivatele()
    assert "Přiřazeno 6 klientů 3 poradcům" in result
    # Ověříme, že každý poradce má 2 klienty
    counts = [Klient.objects.filter(user=p).count() for p in poradci]
    assert all(c == 2 for c in counts)

@pytest.mark.django_db
def test_rozdel_klienty_mezi_uzivatele_bez_poradcu():
    """
    Testuje edge-case: v systému není žádný poradce (User s rolí 'poradce').
    Ověří, že skript vrátí správnou hlášku a klienti nejsou přiřazeni žádnému poradci.
    Každý klient má vždy uživatele, ale nemá přiřazeného poradce.
    """
    from klienti.models import Klient
    klienti = [Klient.objects.create(jmeno=f'Klient{i}') for i in range(2)]
    result = rozdel_klienty_mezi_uzivatele()
    assert 'Žádní poradci v systému.' in result
    # Ověříme, že klienti nejsou přiřazeni žádnému poradci (role != 'poradce')
    for k in klienti:
        k.refresh_from_db()
        assert not hasattr(k.user, 'userprofile') or k.user.userprofile.role != 'poradce'
