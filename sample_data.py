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

banky = ["ČSOB", "Komerční banka", "Moneta", "Raiffeisenbank", "UniCredit", "Fio banka", "mBank"]

for i in range(10):
    datum = fake.date_between(start_date='-7M', end_date='today')
    jmeno = fake.name()
    cena = round(random.uniform(1500000, 12000000), 2)
    procento = round(random.uniform(60, 90), 2)
    castka = round(cena * procento / 100, 2)
    vybrana_banka = random.choice(banky)
    klient_kwargs = {
        'jmeno': jmeno,
        'datum': datum,
        'cena': cena,
        'navrh_financovani_procento': procento,
        'navrh_financovani_castka': castka,
        'vyber_banky': vybrana_banka,
    }
    dalsi_krok_index = i % len(kroky)
    last_date = datum
    for idx, krok in enumerate(kroky):
        deadline_field = f'deadline_{krok}'
        splneno_field = f'splneno_{krok}'
        deadline = last_date + timedelta(days=random.randint(5, 30))
        if idx < dalsi_krok_index:
            klient_kwargs[krok] = fake.sentence(nb_words=3)
            klient_kwargs[deadline_field] = deadline
            klient_kwargs[splneno_field] = deadline + timedelta(days=random.randint(0, 10))
            last_date = klient_kwargs[splneno_field]
        else:
            klient_kwargs[krok] = ''
            klient_kwargs[deadline_field] = deadline
            klient_kwargs[splneno_field] = None
    klient = Klient.objects.create(**klient_kwargs)
    print(f"Vytvořen klient: {jmeno} – další krok: {kroky[dalsi_krok_index]}, %: {procento}, částka: {castka}, banka: {vybrana_banka}")

print("Hotovo! Bylo vytvořeno 10 vzorových klientů se všemi poli včetně částky a banky.")
