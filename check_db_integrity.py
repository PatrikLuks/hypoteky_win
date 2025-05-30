# check_db_integrity.py
# Rychlá kontrola integrity a konzistence dat v DB (model Klient)
# Spouštěj: source venv/bin/activate && python check_db_integrity.py

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hypoteky.settings')
django.setup()

from klienti.models import Klient
from django.db.models import Count

print("\n--- Kontrola integrity dat v modelu Klient ---\n")

# 1. Duplicitní jména (pouze pro ilustraci, v praxi může být více klientů stejného jména)
duplicity = Klient.objects.values('jmeno').annotate(pocet=Count('id')).filter(pocet__gt=1)
if duplicity:
    print(f"[!] Nalezeno {len(duplicity)} duplicitních jmen:")
    for d in duplicity:
        print(f"  - {d['jmeno']} ({d['pocet']}x)")
else:
    print("✓ Žádné duplicitní jméno nenalezeno.")

# 2. Chybějící povinná pole
chybi_jmeno = Klient.objects.filter(jmeno__isnull=True) | Klient.objects.filter(jmeno='')
if chybi_jmeno.exists():
    print(f"[!] {chybi_jmeno.count()} klientů bez jména:")
    for k in chybi_jmeno[:5]:
        print(f"  - ID {k.id}")
else:
    print("✓ Všichni klienti mají jméno.")

chybi_datum = Klient.objects.filter(datum__isnull=True)
if chybi_datum.exists():
    print(f"[!] {chybi_datum.count()} klientů bez data:")
    for k in chybi_datum[:5]:
        print(f"  - {k.jmeno} (ID {k.id})")
else:
    print("✓ Všichni klienti mají datum.")

# 3. Nevalidní hodnoty (záporná nebo nulová částka)
nevalidni_castka = Klient.objects.filter(navrh_financovani_castka__lte=0)
if nevalidni_castka.exists():
    print(f"[!] {nevalidni_castka.count()} klientů s nevalidní částkou (<= 0):")
    for k in nevalidni_castka[:5]:
        print(f"  - {k.jmeno}: {k.navrh_financovani_castka}")
else:
    print("✓ Všichni klienti mají kladnou částku.")

print("\n--- Kontrola dokončena ---\n")
print("Pokud byly nalezeny chyby, doporučuji je opravit před exportem, reportingem nebo migrací dat.")
