# Skript pro vygenerování testovacích klientů pro reporting
# Vytvoří klienty s různými daty, bankami a stavem (schváleno/zamítnuto)
# Spouštěj v aktivním Django prostředí: python manage.py shell < create_sample_reporting_clients.py

import random
from datetime import date, timedelta
from klienti.models import Klient

BANKY = ["ČSOB", "Komerční banka", "Moneta", "Raiffeisenbank", "UniCredit"]
JMENA = ["Jan Novák", "Petr Svoboda", "Eva Dvořáková", "Lucie Malá", "Adam Malý", "Tereza Černá"]

start_date = date(2024, 7, 1)

for i in range(24):  # 2 roky, každý měsíc
    datum = start_date + timedelta(days=30*i)
    banka = random.choice(BANKY)
    jmeno = random.choice(JMENA)
    schvaleno = random.choice([True, False])
    klient = Klient(
        jmeno=jmeno,
        datum=datum,
        vyber_banky=banka,
        cena=random.randint(1500000, 6000000),
        duvod_zamitnuti=None if schvaleno else "Nesplněna kritéria",
        podani_zadosti=datum - timedelta(days=random.randint(5, 20)),
        schvalovani=datum
    )
    klient.save()
print("Testovací klienti pro reporting úspěšně vytvořeni.")
