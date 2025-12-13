# -*- coding: utf-8 -*-
"""
Testy pro import klientů z CSV.
Testuje funkci import_klienti_from_csv z utils.py.
"""

import io
from datetime import date

import pytest

from klienti.models import Klient
from klienti.utils import import_klienti_from_csv


@pytest.mark.django_db
def test_import_csv_valid_file():
    """Test: úspěšný import validního CSV souboru."""
    csv_content = """jmeno,datum,vyber_banky,navrh_financovani_castka,duvod_zamitnuti,co_financuje,navrh_financovani,navrh_financovani_procento,cena
Jan Novák,2025-01-15,Česká spořitelna,5000000,,Byt v Praze,Hypotéka,80,6250000
Petra Svobodová,2025-02-20,ČSOB,3000000,,Rodinný dům,Hypotéka,70,4285714
"""
    file = io.StringIO(csv_content)
    
    # Před importem ověř, že klienti neexistují
    assert Klient.objects.count() == 0
    
    # Proveď import
    count = import_klienti_from_csv(file)
    
    # Ověř výsledky
    assert count == 2
    assert Klient.objects.count() == 2
    
    # Ověř data prvního klienta (pomocí jmeno_index, protože jmeno je šifrované)
    klient1 = Klient.objects.get(jmeno_index="Jan Novák")
    assert klient1.vyber_banky == "Česká spořitelna"
    assert klient1.navrh_financovani_castka == 5000000
    assert klient1.co_financuje == "Byt v Praze"


@pytest.mark.django_db
def test_import_csv_missing_required_fields():
    """Test: import CSV s chybějícími povinnými poli by měl přeskočit řádek."""
    csv_content = """jmeno,datum,vyber_banky,navrh_financovani_castka
,2025-01-15,KB,1000000
Jan Bez Banky,2025-01-16,,2000000
Kompletní Klient,2025-01-17,ČSOB,3000000
"""
    file = io.StringIO(csv_content)
    
    count = import_klienti_from_csv(file)
    
    # Pouze jeden klient by měl být importován (ten kompletní)
    assert count == 1
    assert Klient.objects.filter(jmeno_index="Kompletní Klient").exists()


@pytest.mark.django_db
def test_import_csv_invalid_date():
    """Test: import CSV s nevalidním datem by měl přeskočit řádek."""
    csv_content = """jmeno,datum,vyber_banky,navrh_financovani_castka
Nevalidní Datum,invalid-date,KB,1000000
Validní Klient,2025-03-01,ČSOB,2000000
"""
    file = io.StringIO(csv_content)
    
    count = import_klienti_from_csv(file)
    
    assert count == 1
    assert Klient.objects.filter(jmeno_index="Validní Klient").exists()
    assert not Klient.objects.filter(jmeno_index="Nevalidní Datum").exists()


@pytest.mark.django_db
def test_import_csv_duplicate_detection():
    """Test: duplicitní klienti (stejné jméno+datum) by měli být přeskočeni."""
    # Nejprve vytvoř existujícího klienta
    Klient.objects.create(
        jmeno="Existující Klient",
        datum=date(2025, 1, 15),
        vyber_banky="KB"
    )
    
    csv_content = """jmeno,datum,vyber_banky,navrh_financovani_castka
Existující Klient,2025-01-15,ČSOB,5000000
Nový Klient,2025-01-16,Moneta,3000000
"""
    file = io.StringIO(csv_content)
    
    count = import_klienti_from_csv(file)
    
    # Pouze nový klient by měl být importován
    assert count == 1
    assert Klient.objects.count() == 2
    
    # Existující klient by měl mít původní banku
    existujici = Klient.objects.get(jmeno_index="Existující Klient")
    assert existujici.vyber_banky == "KB"


@pytest.mark.django_db
def test_import_csv_empty_file():
    """Test: prázdný CSV soubor by měl vrátit 0."""
    csv_content = """jmeno,datum,vyber_banky,navrh_financovani_castka
"""
    file = io.StringIO(csv_content)
    
    count = import_klienti_from_csv(file)
    
    assert count == 0
    assert Klient.objects.count() == 0
