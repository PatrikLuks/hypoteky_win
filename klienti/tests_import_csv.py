import io
from django.test import TestCase
from klienti.models import Klient
from klienti.utils import import_klienti_from_csv

class ImportKlientuCSVTestCase(TestCase):
    def test_importuje_klienty_z_csv(self):
        # Připrav CSV v paměti
        csv_data = (
            'jmeno,datum,vyber_banky,navrh_financovani_castka,duvod_zamitnuti\n'
            'Jan Import,2025-05-28,KB,2000000,\n'
            'Petr Import,2025-05-28,ČSOB,3000000,Nedostatečný příjem\n'
            'Eva Import,2025-05-28,KB,2500000,\n'
        )
        file = io.StringIO(csv_data)
        pocet = import_klienti_from_csv(file)
        self.assertEqual(pocet, 3)
        klienti = list(Klient.objects.all())
        self.assertEqual(len(klienti), 3)
        # Hledání podle jména v Pythonu kvůli šifrování
        jan = next((k for k in klienti if k.jmeno == 'Jan Import'), None)
        self.assertIsNotNone(jan)
        self.assertEqual(jan.vyber_banky, 'KB')
        petr = next((k for k in klienti if k.jmeno == 'Petr Import'), None)
        self.assertIsNotNone(petr)
        self.assertEqual(petr.duvod_zamitnuti, 'Nedostatečný příjem')
        eva = next((k for k in klienti if k.jmeno == 'Eva Import'), None)
        self.assertIsNotNone(eva)
        self.assertEqual(eva.vyber_banky, 'KB')

    def test_import_ignoruje_radky_bez_jmena(self):
        csv_data = (
            'jmeno,datum,vyber_banky,navrh_financovani_castka,duvod_zamitnuti\n'
            ',2025-05-28,KB,2000000,\n'
            'Jan Import,2025-05-28,KB,2000000,\n'
        )
        file = io.StringIO(csv_data)
        pocet = import_klienti_from_csv(file)
        self.assertEqual(pocet, 1)
        klienti = list(Klient.objects.all())
        self.assertEqual(len(klienti), 1)
        jan = next((k for k in klienti if k.jmeno == 'Jan Import'), None)
        self.assertIsNotNone(jan)
        self.assertEqual(jan.vyber_banky, 'KB')

    def test_sifrovane_pole_jmeno_vytvoreni_a_nalezeni(self):
        # Ověříme, že lze vytvořit a najít klienta podle jména
        Klient.objects.create(jmeno='Testovací Klient', vyber_banky='Testovací Banka')
        klienti = list(Klient.objects.all())
        nalezen = any(k.jmeno == 'Testovací Klient' for k in klienti)
        self.assertTrue(nalezen)
        klient = next((k for k in klienti if k.jmeno == 'Testovací Klient'), None)
        self.assertIsNotNone(klient)
        self.assertEqual(klient.vyber_banky, 'Testovací Banka')
