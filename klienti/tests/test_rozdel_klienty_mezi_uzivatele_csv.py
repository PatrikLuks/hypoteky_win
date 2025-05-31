"""
Test: test_rozdel_klienty_mezi_uzivatele_csv.py
Popis: Ověří, že skript rozdel_klienty_mezi_uzivatele.py v režimu --dry-run správně exportuje rozdělení do CSV.
Autor: GitHub Copilot
Datum: 2025-05-31
"""

import os
import csv
import tempfile
import pytest
from django.contrib.auth.models import User
from klienti.models import Klient
from klienti.scripts.rozdel_klienty_mezi_uzivatele import rozdel_klienty_mezi_uzivatele, export_rozdeleni_to_csv

@pytest.mark.django_db
def test_rozdel_klienty_mezi_uzivatele_csv_export():
    # Vytvoříme 2 poradce a 3 klienty
    poradci = [User.objects.create_user(username=f'poradce{i}') for i in range(2)]
    for p in poradci:
        p.userprofile.role = 'poradce'
        p.userprofile.save()
    klienti = [Klient.objects.create(jmeno=f'Klient{i}') for i in range(3)]
    # Získáme rozdělení v dry-run režimu
    data = rozdel_klienty_mezi_uzivatele(dry_run=True, return_data=True)
    # Exportujeme do dočasného souboru
    with tempfile.NamedTemporaryFile('w+', newline='', encoding='utf-8', delete=False) as tmp:
        export_rozdeleni_to_csv(data, tmp.name)
        tmp.seek(0)
        reader = csv.DictReader(tmp)
        rows = list(reader)
    # Ověříme obsah CSV
    assert len(rows) == 3
    assert set(r['poradce'] for r in rows) == {'poradce0', 'poradce1'}
    assert set(r['klient'] for r in rows) == {'Klient0', 'Klient1', 'Klient2'}
    # Úklid
    os.remove(tmp.name)
