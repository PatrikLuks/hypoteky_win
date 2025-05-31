"""
Test: test_klient_user_overview_csv.py
Popis: Ověří, že skript klient_user_overview.py správně exportuje přehled do CSV.
Autor: GitHub Copilot
Datum: 2025-05-31
"""

import os
import csv
import tempfile
import pytest
from django.contrib.auth.models import User
from klienti.models import Klient
from klienti.scripts.klient_user_overview import print_klient_user_overview, export_to_csv

@pytest.mark.django_db
def test_klient_user_overview_csv_export():
    # Vytvoříme testovacího uživatele a klienta
    user = User.objects.create_user(username='testuser', password='testpass')
    klient = Klient.objects.create(jmeno='Test Klient', user=user)
    data = print_klient_user_overview(return_data=True)
    # Exportujeme do dočasného souboru
    with tempfile.NamedTemporaryFile('w+', newline='', encoding='utf-8', delete=False) as tmp:
        export_to_csv(data, tmp.name)
        tmp.seek(0)
        reader = csv.DictReader(tmp)
        rows = list(reader)
    # Ověříme obsah CSV
    assert len(rows) == 1
    assert rows[0]['uzivatel'] == 'testuser'
    assert rows[0]['klient'] == 'Test Klient'
    # Úklid
    os.remove(tmp.name)
