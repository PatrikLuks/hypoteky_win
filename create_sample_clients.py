import os
import django
import random
from datetime import date, timedelta

# Nastavení Django prostředí
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hypoteky.settings')
django.setup()

from django.contrib.auth.models import User
from klienti.models import Klient

# Smaž všechny stávající vzorové klienty (podle jména)
Klient.objects.filter(jmeno__startswith='Vzorový klient').delete()

poradce = User.objects.get(username='patrikluks')
banky = ['ČSOB', 'Komerční banka', 'Moneta', 'Raiffeisenbank', 'UniCredit', 'Fio banka', 'mBank']
ucely = ['Byt', 'Dům', 'Pozemek', 'Rekonstrukce', 'Komerční nemovitost', 'Konsolidace', 'Jiné']
prijmeni = ['Novák', 'Svoboda', 'Dvořák', 'Černý', 'Procházka', 'Kučera', 'Veselý', 'Horák', 'Němec', 'Marek']
jmena = ['Jan', 'Petr', 'Lucie', 'Eva', 'Martin', 'Tereza', 'Tomáš', 'Anna', 'Jakub', 'Barbora']

for i in range(1, 21):
    jmeno = f"{random.choice(jmena)} {random.choice(prijmeni)}"
    co_financuje = random.choice(ucely)
    cena = random.randint(1200000, 12000000)
    procento = random.randint(55, 90)
    castka = int(cena * procento / 100)
    banka = random.choice(banky)
    navrh = random.choice(['Hypotéka', 'Refinancování', 'Konsolidace', 'Americká hypotéka'])
    today = date.today()
    # Každý klient bude mít jiný stav workflow (některé kroky splněné, některé ne)
    krok_index = random.randint(1, 15)  # Počet splněných kroků (1–15)
    workflow_kroky = [
        'priprava_zadosti', 'kompletace_podkladu', 'podani_zadosti', 'odhad', 'schvalovani',
        'priprava_uverove_dokumentace', 'podpis_uverove_dokumentace', 'priprava_cerpani',
        'cerpani', 'zahajeni_splaceni', 'podminky_pro_splaceni'
    ]
    klient_kwargs = dict(
        jmeno=jmeno,
        datum=today - timedelta(days=random.randint(0, 730)),
        co_financuje=co_financuje,
        cena=cena,
        navrh_financovani=navrh,
        navrh_financovani_castka=castka,
        navrh_financovani_procento=procento,
        vyber_banky=banka,
        user=poradce
    )
    # Nastav workflow kroky a deadliny
    for idx, krok in enumerate(workflow_kroky):
        deadline_field = f'deadline_{krok}'
        splneno_field = f'splneno_{krok}'
        deadline = today + timedelta(days=idx*7 + random.randint(-3, 3))
        klient_kwargs[deadline_field] = deadline
        if idx < krok_index:
            klient_kwargs[krok] = f"Splněno {krok.replace('_', ' ')}"
            klient_kwargs[splneno_field] = deadline + timedelta(days=random.randint(0, 5))
        else:
            klient_kwargs[krok] = ""
            klient_kwargs[splneno_field] = None
    Klient.objects.create(**klient_kwargs)
print('Hotovo! 20 rozmanitých vzorových klientů s různým workflow stavem bylo přidáno poradci patrikluks.')
