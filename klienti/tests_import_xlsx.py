import io
import tempfile
import openpyxl
from django.test import TestCase
from klienti.models import Klient
from klienti.utils import import_klienti_from_xlsx

class ImportKlientuXLSXTestCase(TestCase):
    def vytvor_xlsx(self, rows):
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.append([
            'jmeno','datum','vyber_banky','navrh_financovani_castka','duvod_zamitnuti',
            'co_financuje','navrh_financovani','navrh_financovani_procento','cena'
        ])
        for row in rows:
            ws.append(row)
        temp = tempfile.NamedTemporaryFile(suffix='.xlsx')
        wb.save(temp.name)
        temp.seek(0)
        return temp

    def test_importuje_klienty_z_xlsx(self):
        rows = [
            ['Jan XLSX','2025-05-28','KB',2000000,'','','',80,2000000],
            ['Petr XLSX','2025-05-28','ČSOB',3000000,'Nedostatečný příjem','','',90,3000000],
            ['Eva XLSX','2025-05-28','KB',2500000,'','','',85,2500000],
        ]
        temp = self.vytvor_xlsx(rows)
        pocet = import_klienti_from_xlsx(temp.name)
        self.assertEqual(pocet, 3)
        klienti = list(Klient.objects.all())
        self.assertEqual(len(klienti), 3)
        jan = next((k for k in klienti if k.jmeno == 'Jan XLSX'), None)
        self.assertIsNotNone(jan)
        self.assertEqual(jan.vyber_banky, 'KB')
        petr = next((k for k in klienti if k.jmeno == 'Petr XLSX'), None)
        self.assertIsNotNone(petr)
        self.assertEqual(petr.duvod_zamitnuti, 'Nedostatečný příjem')
        eva = next((k for k in klienti if k.jmeno == 'Eva XLSX'), None)
        self.assertIsNotNone(eva)
        self.assertEqual(eva.vyber_banky, 'KB')

    def test_import_ignoruje_radky_bez_jmena(self):
        rows = [
            ['', '2025-05-28', 'KB', 2000000, '', '', '', 80, 2000000],
            ['Jan XLSX', '2025-05-28', 'KB', 2000000, '', '', '', 80, 2000000],
        ]
        temp = self.vytvor_xlsx(rows)
        pocet = import_klienti_from_xlsx(temp.name)
        self.assertEqual(pocet, 1)
        klienti = list(Klient.objects.all())
        self.assertEqual(len(klienti), 1)
        jan = next((k for k in klienti if k.jmeno == 'Jan XLSX'), None)
        self.assertIsNotNone(jan)
        self.assertEqual(jan.vyber_banky, 'KB')
