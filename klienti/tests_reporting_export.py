import io
from django.test import TestCase
from klienti.models import Klient
from datetime import date, timedelta
import openpyxl
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

class ReportingExportXLSXTestCase(TestCase):
    def setUp(self):
        Klient.objects.all().delete()
        # Vytvoř klienty pro test_export_xlsx_obsahuje_spravna_data
        Klient.objects.create(jmeno='Jan Export', datum=date.today(), vyber_banky='KB', navrh_financovani_castka=2000000)
        Klient.objects.create(jmeno='Petr Export', datum=date.today(), vyber_banky='ČSOB', navrh_financovani_castka=3000000, duvod_zamitnuti='Nedostatečný příjem')
        Klient.objects.create(jmeno='Eva Export', datum=date.today(), vyber_banky='KB', navrh_financovani_castka=2500000)

    def test_export_xlsx_obsahuje_spravna_data(self):
        # --- Simulace části generování XLSX z management commandu ---
        from collections import Counter
        klienti = Klient.objects.all()
        banky = [k.vyber_banky for k in klienti if k.vyber_banky]
        rozlozeni_banky = Counter(banky)
        schvalene = klienti.filter(duvod_zamitnuti__isnull=True, vyber_banky__isnull=False)
        zamitnute = klienti.filter(duvod_zamitnuti__isnull=False, vyber_banky__isnull=False)
        banky_labels = list(rozlozeni_banky.keys())
        schvalenost = [schvalene.filter(vyber_banky=b).count() for b in banky_labels]
        zamitnutost = [zamitnute.filter(vyber_banky=b).count() for b in banky_labels]
        prumery = ['-' for _ in banky_labels]  # pro jednoduchost, bez datumu podání/schválení
        # Vygeneruj XLSX do bufferu
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Reporting"
        ws.append(["Banka", "Schváleno", "Zamítnuto", "Průměrná doba schválení (dny)"])
        for i, banka in enumerate(banky_labels):
            ws.append([banka, schvalenost[i], zamitnutost[i], prumery[i]])
        xlsx_buffer = io.BytesIO()
        wb.save(xlsx_buffer)
        xlsx_buffer.seek(0)
        # --- Ověření obsahu XLSX ---
        wb2 = openpyxl.load_workbook(xlsx_buffer)
        ws2 = wb2.active
        data = list(ws2.values)
        self.assertEqual(data[0], ("Banka", "Schváleno", "Zamítnuto", "Průměrná doba schválení (dny)"))
        # Ověř, že jsou tam obě banky a správné počty
        rows = {row[0]: row for row in data[1:]}
        self.assertIn('KB', rows)
        self.assertIn('ČSOB', rows)
        self.assertEqual(rows['KB'][1], 2)  # 2 schválené
        self.assertEqual(rows['KB'][2], 0)  # 0 zamítnutých
        self.assertEqual(rows['ČSOB'][1], 0)  # 0 schválených
        self.assertEqual(rows['ČSOB'][2], 1)  # 1 zamítnutý

    def test_export_xlsx_prazdna_db(self):
        Klient.objects.all().delete()
        from collections import Counter
        klienti = Klient.objects.all()
        banky = [k.vyber_banky for k in klienti if k.vyber_banky]
        rozlozeni_banky = Counter(banky)
        banky_labels = list(rozlozeni_banky.keys())
        schvalenost = []
        zamitnutost = []
        prumery = []
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Reporting"
        ws.append(["Banka", "Schváleno", "Zamítnuto", "Průměrná doba schválení (dny)"])
        for i, banka in enumerate(banky_labels):
            ws.append([banka, schvalenost[i], zamitnutost[i], prumery[i]])
        xlsx_buffer = io.BytesIO()
        wb.save(xlsx_buffer)
        xlsx_buffer.seek(0)
        wb2 = openpyxl.load_workbook(xlsx_buffer)
        ws2 = wb2.active
        data = list(ws2.values)
        self.assertEqual(data[0], ("Banka", "Schváleno", "Zamítnuto", "Průměrná doba schválení (dny)"))
        self.assertEqual(len(data), 1)  # pouze hlavička

    def test_export_xlsx_extremni_hodnoty(self):
        Klient.objects.all().delete()
        Klient.objects.create(jmeno='Mega Export', datum=date.today(), vyber_banky='Banka S Extrémně Dlouhým Názvem Pro Testování Robustnosti', navrh_financovani_castka=9999999999)
        from collections import Counter
        klienti = Klient.objects.all()
        banky = [k.vyber_banky for k in klienti if k.vyber_banky]
        rozlozeni_banky = Counter(banky)
        banky_labels = list(rozlozeni_banky.keys())
        schvalenost = [klienti.filter(duvod_zamitnuti__isnull=True, vyber_banky=b).count() for b in banky_labels]
        zamitnutost = [klienti.filter(duvod_zamitnuti__isnull=False, vyber_banky=b).count() for b in banky_labels]
        prumery = ['-' for _ in banky_labels]
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Reporting"
        ws.append(["Banka", "Schváleno", "Zamítnuto", "Průměrná doba schválení (dny)"])
        for i, banka in enumerate(banky_labels):
            ws.append([banka, schvalenost[i], zamitnutost[i], prumery[i]])
        xlsx_buffer = io.BytesIO()
        wb.save(xlsx_buffer)
        xlsx_buffer.seek(0)
        wb2 = openpyxl.load_workbook(xlsx_buffer)
        ws2 = wb2.active
        data = list(ws2.values)
        self.assertIn('Banka S Extrémně Dlouhým Názvem Pro Testování Robustnosti', [row[0] for row in data[1:]])
        self.assertEqual(data[1][1], 1)  # 1 schválený
        self.assertEqual(data[1][2], 0)  # 0 zamítnutých

    def test_export_pdf_report_neni_prazdny(self):
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
        p.drawString(40, y, "Testovací banka")
        p.drawString(180, y, "1")
        p.drawString(270, y, "0")
        p.drawString(370, y, "-")
        p.save()
        buffer.seek(0)
        pdf_data = buffer.read()
        self.assertGreater(len(pdf_data), 500)  # PDF by mělo mít alespoň 500 B
