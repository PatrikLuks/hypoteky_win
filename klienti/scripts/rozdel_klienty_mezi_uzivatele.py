#!/usr/bin/env python3
"""
Skript: rozdel_klienty_mezi_uzivatele.py
Popis: Rozdělení klientů mezi uživatele (poradce/klienty) – např. rovnoměrně.
Autor: GitHub Copilot
Datum: 2025-05-31

Tento skript přiřadí klienty uživatelům (např. poradci) podle jednoduchého algoritmu.
Použití: python rozdel_klienty_mezi_uzivatele.py

POZNÁMKA: Skript předpokládá spuštění v root složce Django projektu.
"""

import os
import django
import argparse
import csv
from itertools import cycle

def rozdel_klienty_mezi_uzivatele(dry_run=False, return_data=False):
    from django.contrib.auth.models import User
    from klienti.models import Klient
    user_klients = {p: [] for p in User.objects.filter(userprofile__role='poradce')}
    poradci = list(user_klients.keys())
    klienti = list(Klient.objects.all())
    if not poradci:
        return "Žádní poradci v systému." if not return_data else []
    if not klienti:
        return "Žádní klienti v systému." if not return_data else []
    cyklovani = cycle(poradci)
    for klient in klienti:
        poradce = next(cyklovani)
        user_klients[poradce].append(klient)
        if not dry_run:
            klient.user = poradce
            klient.save()
    if dry_run:
        output = ["\nNáhled rozdělení klientů mezi poradce (dry-run):\n" + "-"*40]
        data = []
        for poradce, klienti in user_klients.items():
            output.append(f"Poradce: {poradce.username} (ID: {poradce.id})")
            if klienti:
                for k in klienti:
                    output.append(f"  - {k.jmeno} (ID: {k.id})")
                    data.append({
                        'poradce': poradce.username,
                        'poradce_id': poradce.id,
                        'klient': k.jmeno,
                        'klient_id': k.id
                    })
            else:
                output.append("  (žádní klienti)")
            output.append("-")
        output.append("Hotovo.\n")
        if return_data:
            return data
        return "\n".join(output)
    else:
        return f"Přiřazeno {len(klienti)} klientů {len(poradci)} poradcům."

def export_rozdeleni_to_csv(data, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['poradce', 'poradce_id', 'klient', 'klient_id']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

if __name__ == "__main__":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hypoteky.settings')
    django.setup()
    parser = argparse.ArgumentParser(description="Rozdělení klientů mezi poradce.")
    parser.add_argument('--dry-run', action='store_true', help='Pouze zobrazit rozdělení, neprovádět změny v DB')
    parser.add_argument('--csv', '-o', metavar='soubor.csv', help='Exportovat rozdělení do CSV (pouze s --dry-run)')
    args = parser.parse_args()
    if args.dry_run and args.csv:
        data = rozdel_klienty_mezi_uzivatele(dry_run=True, return_data=True)
        export_rozdeleni_to_csv(data, args.csv)
        print(f"Exportováno do {args.csv}")
    else:
        print(rozdel_klienty_mezi_uzivatele(dry_run=args.dry_run))
