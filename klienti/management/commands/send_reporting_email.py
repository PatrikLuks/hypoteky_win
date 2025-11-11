import io
from collections import Counter

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage
from django.core.management.base import BaseCommand

import openpyxl
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from klienti.models import Klient, UserProfile


class Command(BaseCommand):
    help = "Odešle reporting/statistiky e-mailem manažerům a administrátorům."

    def handle(self, *args, **options):
        # Získání příjemců (manažeři a administrátoři)
        User = get_user_model()
        prijemci = list(
            User.objects.filter(
                userprofile__role__in=["manažer", "administrátor"], is_active=True
            ).values_list("email", flat=True)
        )
        if not prijemci:
            self.stdout.write(
                self.style.WARNING(
                    "Žádní příjemci reportu (role manažer/administrátor)"
                )
            )
            return
        # Data pro reporting
        klienti = Klient.objects.all()
        banky = [k.vyber_banky for k in klienti if k.vyber_banky]
        rozlozeni_banky = Counter(banky)
        schvalene = klienti.filter(
            duvod_zamitnuti__isnull=True, vyber_banky__isnull=False
        )
        zamitnute = klienti.filter(
            duvod_zamitnuti__isnull=False, vyber_banky__isnull=False
        )
        banky_labels = list(rozlozeni_banky.keys())
        schvalenost = [schvalene.filter(vyber_banky=b).count() for b in banky_labels]
        zamitnutost = [zamitnute.filter(vyber_banky=b).count() for b in banky_labels]
        prumery = []
        for banka in banky_labels:
            klienti_banka = klienti.filter(
                vyber_banky=banka,
                podani_zadosti__isnull=False,
                schvalovani__isnull=False,
            )
            doby = [
                (k.schvalovani - k.podani_zadosti).days
                for k in klienti_banka
                if k.schvalovani and k.podani_zadosti
            ]
            prumery.append(round(sum(doby) / len(doby), 1) if doby else None)
        # Vygenerovat PDF report
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4)
        p.setFont("Helvetica-Bold", 16)
        p.drawString(40, 800, "Reporting – úspěšnost podle banky")
        p.setFont("Helvetica", 11)
        y = 770
        p.drawString(40, y, "Banka")
        p.drawString(180, y, "Schváleno")
        p.drawString(270, y, "Zamítnuto")
        p.drawString(370, y, "Průměrná doba schválení (dny)")
        y -= 20
        for i, banka in enumerate(banky_labels):
            p.drawString(40, y, str(banka))
            p.drawString(180, y, str(schvalenost[i]))
            p.drawString(270, y, str(zamitnutost[i]))
            p.drawString(370, y, str(prumery[i]) if prumery[i] is not None else "-")
            y -= 18
            if y < 60:
                p.showPage()
                y = 800
        p.save()
        buffer.seek(0)
        pdf_data = buffer.read()
        # Vygenerovat XLSX report
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Reporting"
        ws.append(["Banka", "Schváleno", "Zamítnuto", "Průměrná doba schválení (dny)"])
        for i, banka in enumerate(banky_labels):
            ws.append(
                [
                    banka,
                    schvalenost[i],
                    zamitnutost[i],
                    prumery[i] if prumery[i] is not None else "-",
                ]
            )
        xlsx_buffer = io.BytesIO()
        wb.save(xlsx_buffer)
        xlsx_data = xlsx_buffer.getvalue()
        # Odeslat e-mail
        subject = "Automatizovaný reporting hypoték"
        body = "Dobrý den,\n\npřikládáme aktuální reporting/statistiky hypoték.\n\nS pozdravem,\nTým hypoteční aplikace"
        email = EmailMessage(subject, body, settings.DEFAULT_FROM_EMAIL, prijemci)
        email.attach("reporting.pdf", pdf_data, "application/pdf")
        email.attach(
            "reporting.xlsx",
            xlsx_data,
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        email.send()
        # Audit logování odeslání reportu
        from klienti.models import Zmena

        popis = f"Automatizovaný reporting odeslán na: {', '.join(prijemci)} (PDF a XLSX v příloze)"
        # Ověř, že existuje alespoň jeden klient, jinak nevytvářej záznam s klient=None
        if klienti.exists():
            for klient in klienti:
                Zmena.objects.create(klient=klient, popis=popis, author="automatizace")
        else:
            # Pokud není žádný klient, zaloguj pouze do konzole nebo použij jiný mechanismus
            self.stdout.write(
                self.style.WARNING(
                    "Audit log: report odeslán bez klientů – žádný záznam do Zmena."
                )
            )
        self.stdout.write(
            self.style.SUCCESS(f'Report byl úspěšně odeslán na: {", ".join(prijemci)}')
        )
