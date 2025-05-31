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

    def test_import_xlsx_edge_cases(self):
        """
        Testuje import klientů z XLSX s edge-case řádky:
        - chybějící jméno
        - špatný formát částky
        - duplicitní klient
        - prázdný řádek

        Tento test je důležitý, protože v reálných datech se často vyskytují chyby a aplikace je musí umět bezpečně ignorovat nebo správně zpracovat.
        """
        rows = [
            ['Jan Novák', '2025-05-30', '', '3000000', '', '', '', '', ''],  # validní s DATEM
            ['', '', '', '5000000', '', '', '', '', ''],           # chybí jméno
            ['Petr Dvořák', '', '', 'abc', '', '', '', '', ''],    # špatný formát částky
            ['Jan Novák', '', '', '3000000', '', '', '', '', ''],  # duplicitní (ale bez data)
            ['', '', '', '', '', '', '', '', ''],                  # prázdný řádek
        ]
        temp = self.vytvor_xlsx(rows)
        pocet = import_klienti_from_xlsx(temp.name)
        self.assertEqual(pocet, 1)
        klienti = list(Klient.objects.all())
        self.assertEqual(len(klienti), 1)
        jan = next((k for k in klienti if k.jmeno == 'Jan Novák'), None)
        self.assertIsNotNone(jan)
        # Ověř, že duplicitní klient nebyl importován dvakrát (porovnání podle dešifrovaného jména)
        jan_count = len([k for k in klienti if k.jmeno == 'Jan Novák'])
        self.assertEqual(jan_count, 1)
        # Ověř, že klient se špatnou částkou nebyl importován
        self.assertFalse(any(k.jmeno == 'Petr Dvořák' for k in klienti))
        # Ověř, že klient bez jména nebyl importován
        self.assertEqual(len([k for k in klienti if not k.jmeno]), 0)

    def test_import_xlsx_extremni_znaky_a_hodnoty(self):
        """
        Testuje import klientů z XLSX s extrémními znaky a hodnotami:
        - velmi dlouhé jméno (255 znaků)
        - speciální znaky a diakritika
        - emoji v jméně
        - HTML tagy v poli co_financuje
        - extrémní hodnoty částky (velmi vysoká, záporná, nula)
        - pokus o SQL injection v poli co_financuje
        Tyto scénáře ověřují robustnost a bezpečnost importu.
        """
        dlouhe_jmeno = 'B' * 255
        rows = [
            [dlouhe_jmeno, '2025-05-28', 'KB', 1234567, '', 'Byt', '', 80, 1234567],  # velmi dlouhé jméno
            ['Žofie Černá', '2025-05-28', 'KB', 2000000, '', 'Chalupa', '', 80, 2000000],  # diakritika
            ['Emil 😊', '2025-05-28', 'KB', 1500000, '', 'Dům', '', 80, 1500000],         # emoji
            ['Jan Novak', '2025-05-28', 'KB', 1000000, '', '<b>Byt</b>', '', 80, 1000000], # HTML tag
            ['Petr Velký', '2025-05-28', 'KB', 9999999999, '', 'Byt', '', 80, 9999999999], # extrémně vysoká částka
            ['Karel Malý', '2025-05-28', 'KB', -500000, '', 'Byt', '', 80, -500000],       # záporná částka
            ['Marek Nula', '2025-05-28', 'KB', 0, '', 'Byt', '', 80, 0],                  # nula
            ['Eva SQL', '2025-05-28', 'KB', 1200000, '', "'; DROP TABLE klienti;--", '', 80, 1200000], # SQL injection
        ]
        temp = self.vytvor_xlsx(rows)
        pocet = import_klienti_from_xlsx(temp.name)
        klienti = list(Klient.objects.all())
        jmena = [k.jmeno for k in klienti]
        self.assertIn(dlouhe_jmeno, jmena, "Klient s dlouhým jménem nebyl importován.")
        self.assertIn("Žofie Černá", jmena, "Klient s diakritikou nebyl importován.")
        self.assertIn("Emil 😊", jmena, "Klient s emoji nebyl importován.")
        self.assertIn("Jan Novak", jmena, "Klient s HTML tagem nebyl importován.")
        self.assertIn("Petr Velký", jmena, "Klient s extrémní částkou nebyl importován.")
        self.assertIn("Marek Nula", jmena, "Klient s nulovou nebo zápornou částkou nebyl importován.")
        self.assertIn("Eva SQL", jmena, "Klient s pokusem o SQL injection nebyl importován.")
        # Ověř, že pole co_financuje je správně uloženo (HTML tagy, SQL injection)
        jan = next((k for k in klienti if k.jmeno == "Jan Novak"), None)
        self.assertIsNotNone(jan)
        self.assertIn("<b>Byt</b>", jan.co_financuje)
        eva = next((k for k in klienti if k.jmeno == "Eva SQL"), None)
        self.assertIsNotNone(eva)
        self.assertIn("DROP TABLE", eva.co_financuje)
        # Ověř, že extrémní částka je správně uložena
        petr = next((k for k in klienti if k.jmeno == "Petr Velký"), None)
        self.assertIsNotNone(petr)
        self.assertEqual(petr.cena, 9999999999)
        # Ověř, že záporná a nulová částka je uložena (podle business logiky může být validní nebo ne)
        marek = next((k for k in klienti if k.jmeno == "Marek Nula"), None)
        self.assertIsNotNone(marek)
        self.assertEqual(marek.cena, 0)
        karel = next((k for k in klienti if k.jmeno == "Karel Malý"), None)
        self.assertIsNotNone(karel)
        self.assertEqual(karel.cena, -500000)
        # Ověř, že klienti s extrémními znaky nezpůsobili chybu v importu
        self.assertGreaterEqual(len(klienti), 8, "Některý z klientů nebyl importován.")
