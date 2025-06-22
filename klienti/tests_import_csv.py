# -*- coding: utf-8 -*-
"""
Testy pro import klientů z CSV.
Doporučení: Pokud import CSV není implementován, tento soubor můžeš smazat.
Pokud import existuje, doplň zde testy podle ukázky níže.
"""

import pytest
from django.urls import reverse
from django.test import Client

@pytest.mark.django_db
def test_import_csv_valid_file():
    """Ukázkový test: úspěšný import validního CSV souboru."""
    client = Client()
    # TODO: Připrav testovací CSV soubor a endpoint
    # response = client.post(reverse('import_csv'), {'file': open('test.csv', 'rb')})
    # assert response.status_code == 200
    # assert 'Import úspěšný' in response.content.decode()
    pass  # Odstraň až doplníš test

@pytest.mark.django_db
def test_import_csv_invalid_file():
    """Ukázkový test: import nevalidního CSV by měl selhat."""
    client = Client()
    # TODO: Připrav nevalidní CSV soubor a endpoint
    # response = client.post(reverse('import_csv'), {'file': open('invalid.csv', 'rb')})
    # assert response.status_code == 400
    # assert 'Chyba importu' in response.content.decode()
    pass
