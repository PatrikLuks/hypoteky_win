#!/usr/bin/env python3
"""
Skript: klient_user_overview.py
Popis: Přehled klientů přiřazených uživatelům (poradcům i klientům).
Autor: GitHub Copilot
Datum: 2025-05-31

Tento skript vypíše seznam uživatelů a jejich klientů. Vhodné pro kontrolu rozdělení práce.
Použití: python klient_user_overview.py

POZNÁMKA: Skript předpokládá spuštění v root složce Django projektu.
"""

import os
import django
from collections import defaultdict
import argparse
import csv


def print_klient_user_overview(return_data=False):
    from django.contrib.auth.models import User
    from klienti.models import Klient, UserProfile

    # Vytvoříme slovník: uživatel -> seznam klientů
    user_klients = defaultdict(list)
    for klient in Klient.objects.select_related('user').all():
        if klient.user:
            user_klients[klient.user].append(klient)
        else:
            user_klients[None].append(klient)

    output = []
    data = []  # Pro CSV
    output.append("\nPřehled klientů přiřazených uživatelům:\n" + "-"*40)
    for user, klienti in user_klients.items():
        if user:
            try:
                profile = user.userprofile
                role = profile.get_role_display()
            except Exception:
                role = "(bez profilu)"
            output.append(f"Uživatel: {user.username} [{role}] (ID: {user.id})")
            user_name = user.username
            user_role = role
            user_id = user.id
        else:
            output.append("Uživatel: (nepřiřazeno)")
            user_name = "(nepřiřazeno)"
            user_role = ""
            user_id = ""
        if klienti:
            for k in klienti:
                output.append(f"  - {k.jmeno} (ID: {k.id})")
                data.append({
                    'uzivatel': user_name,
                    'role': user_role,
                    'uzivatel_id': user_id,
                    'klient': k.jmeno,
                    'klient_id': k.id
                })
        else:
            output.append("  (žádní klienti)")
        output.append("-")
    output.append("Hotovo.\n")
    output.append("\nTIP: Pro export do CSV lze použít --csv nebo -o output.csv.\n")
    if return_data:
        return data
    return "\n".join(output)


def export_to_csv(data, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['uzivatel', 'role', 'uzivatel_id', 'klient', 'klient_id']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)


if __name__ == "__main__":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hypoteky.settings')
    django.setup()
    parser = argparse.ArgumentParser(description="Přehled klientů přiřazených uživatelům.")
    parser.add_argument('--csv', '-o', metavar='soubor.csv', help='Exportovat výstup do CSV souboru')
    args = parser.parse_args()
    if args.csv:
        data = print_klient_user_overview(return_data=True)
        export_to_csv(data, args.csv)
        print(f"Exportováno do {args.csv}")
    else:
        print(print_klient_user_overview())
