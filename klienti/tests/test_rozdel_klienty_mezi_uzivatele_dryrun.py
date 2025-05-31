"""
Test: test_rozdel_klienty_mezi_uzivatele_dryrun.py
Popis: Ověří, že skript rozdel_klienty_mezi_uzivatele.py v režimu --dry-run pouze vypíše rozdělení a nemění DB.
Autor: GitHub Copilot
Datum: 2025-05-31
"""

import pytest
from django.contrib.auth.models import User
from klienti.models import Klient
from klienti.scripts.rozdel_klienty_mezi_uzivatele import rozdel_klienty_mezi_uzivatele

@pytest.mark.django_db
def test_rozdel_klienty_mezi_uzivatele_dryrun():
    # Vytvoříme 2 poradce a 4 klienty
    poradci = [User.objects.create_user(username=f'poradce{i}') for i in range(2)]
    for p in poradci:
        p.userprofile.role = 'poradce'
        p.userprofile.save()
    klienti = [Klient.objects.create(jmeno=f'Klient{i}') for i in range(4)]
    # Spustíme dry-run
    output = rozdel_klienty_mezi_uzivatele(dry_run=True)
    assert "Náhled rozdělení klientů mezi poradce" in output
    assert "poradce0" in output and "poradce1" in output
    assert "Klient0" in output and "Klient3" in output
    # Ověříme, že v DB stále nejsou klienti přiřazeni (user=None)
    for k in klienti:
        k.refresh_from_db()
        assert k.user is None
