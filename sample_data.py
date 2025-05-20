import os
import django
import random
from datetime import date, timedelta

# Nastavení Django prostředí
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hypoteky.settings')
django.setup()

from klienti.models import Klient

try:
    from faker import Faker
except ImportError:
    print("Pro generování dat je potřeba nainstalovat balíček faker: pip install faker")
    exit(1)

fake = Faker('cs_CZ')

# Smaž staré vzorové klienty (volitelné)
Klient.objects.all().delete()

kroky = [
    'co_financuje', 'navrh_financovani', 'vyber_banky', 'priprava_zadosti',
    'kompletace_podkladu', 'podani_zadosti', 'odhad', 'schvalovani',
    'priprava_uverove_dokumentace', 'podpis_uverove_dokumentace',
    'priprava_cerpani', 'cerpani', 'zahajeni_splaceni', 'podminky_pro_splaceni'
]

for i in range(10):
    datum = fake.date_between(start_date='-2y', end_date='today')
    jmeno = fake.name()
    cena = round(random.uniform(1500000, 12000000), 2)
    procento = round(random.uniform(60, 90), 2)  # náhodné % mezi 60 a 90
    klient_kwargs = {
        'jmeno': jmeno,
        'datum': datum,
        'cena': cena,
        'navrh_financovani_procento': procento,
    }
    # Každý klient bude mít jiný "další krok" (první nevyplněný krok)
    dalsi_krok_index = i % len(kroky)  # rozprostře klienty přes všechny kroky
    last_date = datum
    for idx, krok in enumerate(kroky):
        deadline_field = f'deadline_{krok}'
        splneno_field = f'splneno_{krok}'
        deadline = last_date + timedelta(days=random.randint(5, 30))
        if idx < dalsi_krok_index:
            # Vyplň splněné kroky
            klient_kwargs[krok] = fake.sentence(nb_words=3)
            klient_kwargs[deadline_field] = deadline
            klient_kwargs[splneno_field] = deadline + timedelta(days=random.randint(0, 10))
            last_date = klient_kwargs[splneno_field]
        else:
            # Nevyplněné kroky (další krok a vše za ním)
            klient_kwargs[krok] = ''
            klient_kwargs[deadline_field] = deadline
            klient_kwargs[splneno_field] = None
    klient = Klient.objects.create(**klient_kwargs)
    print(f"Vytvořen klient: {jmeno} – další krok: {kroky[dalsi_krok_index]}, %: {procento}")

print("Hotovo! Bylo vytvořeno 10 vzorových klientů se všemi poli.")
