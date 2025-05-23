import os
import django
import random
from datetime import date, timedelta
from django.apps import apps

# Nastavení Django prostředí
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hypoteky.settings')
django.setup()

Klient = apps.get_model('klienti', 'Klient')
User = apps.get_model('auth', 'User')
UserProfile = apps.get_model('klienti', 'UserProfile')

try:
    from faker import Faker
except ImportError:
    print("Pro generování dat je potřeba nainstalovat balíček faker: pip install faker")
    exit(1)

fake = Faker('cs_CZ')

# Smaž staré vzorové klienty
Klient.objects.all().delete()

kroky = [
    'co_financuje', 'navrh_financovani', 'vyber_banky', 'priprava_zadosti',
    'kompletace_podkladu', 'podani_zadosti', 'odhad', 'schvalovani',
    'priprava_uverove_dokumentace', 'podpis_uverove_dokumentace',
    'priprava_cerpani', 'cerpani', 'zahajeni_splaceni', 'podminky_pro_splaceni'
]
banky = ["ČSOB", "Komerční banka", "Moneta", "Raiffeisenbank", "UniCredit", "Fio banka", "mBank"]
duvody_zamitnuti = [
    "Nedostatečný příjem",
    "Negativní záznam v registrech",
    "Nedoložené příjmy",
    "Nedostatečná hodnota zástavy",
    "Příliš vysoký věk žadatele",
    "Nedostatečná bonita",
    "Nesplněné podmínky banky"
]

pocet_klientu = 50
pocet_zamitnutych = int(pocet_klientu * 0.2)

for i in range(pocet_klientu):
    datum = fake.date_between(start_date='-12M', end_date='today')
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
        'user': None,
    }
    dalsi_krok_index = random.randint(1, len(kroky)-1)
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
    # 20 % klientů bude zamítnutých
    if i < pocet_zamitnutych:
        klient_kwargs['duvod_zamitnuti'] = random.choice(duvody_zamitnuti)
    klient = Klient.objects.create(**klient_kwargs)
    print(f"Vytvořen klient: {jmeno} ({'Zamítnutý' if 'duvod_zamitnuti' in klient_kwargs else 'Schválený'})")

print("Hotovo! Vytvořeno 50 pečlivých a reálných vzorových klientů.")
