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
# Smaž všechny testovací klienty vytvořené tímto skriptem (podle uživatele a jména)
Klient.objects.filter(user__username='patrikluks').delete()

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

# Přidání 15 klientů s různými stavy workflow
for stav in range(1, 16):
    jmeno = f"Testovací workflow {stav}"
    co_financuje = "Byt" if stav >= 2 else ""
    navrh_financovani = "Hypotéka" if stav >= 3 else ""
    vyber_banky = "mBank" if stav >= 4 else ""
    priprava_zadosti = "Příprava" if stav >= 5 else ""
    kompletace_podkladu = "Kompletace" if stav >= 6 else ""
    podani_zadosti = "Podání" if stav >= 7 else ""
    odhad = "Odhad" if stav >= 8 else ""
    schvalovani = "Schvalování" if stav >= 9 else ""
    priprava_uverove_dokumentace = "Příprava úvěrové dokumentace" if stav >= 10 else ""
    podpis_uverove_dokumentace = "Podpis úvěrové dokumentace" if stav >= 11 else ""
    priprava_cerpani = "Příprava čerpání" if stav >= 12 else ""
    cerpani = "Čerpání" if stav >= 13 else ""
    zahajeni_splaceni = "Zahájení splácení" if stav >= 14 else ""
    podminky_pro_splaceni = "Podmínky pro splacení" if stav >= 15 else ""
    Klient.objects.create(
        jmeno=jmeno,
        datum=today,
        co_financuje=co_financuje,
        navrh_financovani=navrh_financovani,
        vyber_banky=vyber_banky,
        priprava_zadosti=priprava_zadosti,
        kompletace_podkladu=kompletace_podkladu,
        podani_zadosti=podani_zadosti,
        odhad=odhad,
        schvalovani=schvalovani,
        priprava_uverove_dokumentace=priprava_uverove_dokumentace,
        podpis_uverove_dokumentace=podpis_uverove_dokumentace,
        priprava_cerpani=priprava_cerpani,
        cerpani=cerpani,
        zahajeni_splaceni=zahajeni_splaceni,
        podminky_pro_splaceni=podminky_pro_splaceni,
        cena=2000000,
        navrh_financovani_castka=1500000,
        navrh_financovani_procento=75,
        user=poradce
    )

print('Hotovo! 20 rozmanitých vzorových klientů s různým workflow stavem bylo přidáno poradci patrikluks.')
