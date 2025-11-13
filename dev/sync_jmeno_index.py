# Skript pro synchronizaci pole jmeno_index u všech klientů
from klienti.models import Klient

count = 0
for klient in Klient.objects.all():
    klient.jmeno_index = klient.jmeno
    klient.save()
    count += 1
print(f'Synchronizováno {count} klientů.')
