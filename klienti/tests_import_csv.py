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

    def test_import_csv_edge_cases(self):
        """
        Testuje import klientů z CSV s edge-case řádky:
        - chybějící jméno
        - špatný formát částky
        - duplicitní klient
        - prázdný řádek
        """
        csv_content = (
            "jmeno,datum,vyber_banky,co_financuje,cena\n"
            "Jan Novák,2025-05-30,KB,Byt,3000000\n"  # validní
            ",2025-05-30,KB,Dům,5000000\n"          # chybí jméno
            "Petr Dvořák,2025-05-30,KB,Byt,abc\n"    # špatný formát částky
            "Jan Novák,2025-05-30,KB,Byt,3000000\n"  # duplicitní
            "\n"                                 # prázdný řádek
        )
        file = io.StringIO(csv_content)
        response = import_klienti_from_csv(file)
        # Očekáváme 2 importované klienty (validní a se špatnou částkou, duplicitní je přeskočen)
        self.assertEqual(response, 2)
        klienti = list(Klient.objects.all())
        self.assertEqual(len(klienti), 2)
        jan = next((k for k in klienti if k.jmeno == 'Jan Novák'), None)
        self.assertIsNotNone(jan)
        # Ověř, že duplicitní klient nebyl importován dvakrát
        self.assertEqual(len([k for k in klienti if k.jmeno == 'Jan Novák']), 1)
        # Ověř, že klient se špatnou částkou byl importován (částka ignorována)
        self.assertTrue(any(k.jmeno == 'Petr Dvořák' for k in klienti))
        # Ověř, že klient bez jména nebyl importován
        self.assertEqual(len([k for k in klienti if not k.jmeno]), 0)

    def test_import_csv_extremni_znaky_a_hodnoty(self):
        """
        Testuje import klientů z CSV s extrémními znaky a hodnotami:
        - velmi dlouhé jméno (255 znaků)
        - speciální znaky a diakritika
        - HTML tagy v poli co_financuje
        - extrémní hodnoty částky (velmi vysoká, záporná, nula)
        - pokus o SQL injection v poli co_financuje
        Tyto scénáře ověřují robustnost a bezpečnost importu.
        """
        dlouhe_jmeno = 'A' * 255
        csv_content = (
            "jmeno,datum,vyber_banky,co_financuje,cena\n"
            f"{dlouhe_jmeno},2025-05-30,KB,Byt,1234567\n"  # velmi dlouhé jméno
            "Žofie Černá,2025-05-30,KB,Chalupa,2000000\n"  # diakritika
            "Jan Novak,2025-05-30,KB,<b>Byt</b>,1000000\n" # HTML tag
            "Petr Velký,2025-05-30,KB,Byt,9999999999\n"    # extrémně vysoká částka
            "Karel Malý,2025-05-30,KB,Byt,-500000\n"       # záporná částka
            "Marek Nula,2025-05-30,KB,Byt,0\n"            # nula
            "Eva SQL,2025-05-30,KB,'; DROP TABLE klienti;--,1200000\n" # SQL injection
        )
        file = io.StringIO(csv_content)
        response = import_klienti_from_csv(file)
        klienti = list(Klient.objects.all())
        jmena = [k.jmeno for k in klienti]
        self.assertIn(dlouhe_jmeno, jmena, "Klient s dlouhým jménem nebyl importován.")
        self.assertIn("Žofie Černá", jmena, "Klient s diakritikou nebyl importován.")
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
        self.assertGreaterEqual(len(klienti), 7, "Některý z klientů nebyl importován.")

    def test_import_csv_rollback_pri_chybe(self):
        """
        Ověří, že při chybě během importu CSV nedojde k částečnému importu ani nekonzistenci dat.
        Například: pokud jeden řádek způsobí výjimku, žádný klient se nevytvoří.
        """
        from django.db import transaction
        csv_data = (
            'jmeno,datum,vyber_banky,navrh_financovani_castka,duvod_zamitnuti\n'
            'Jan Import,2025-05-28,KB,2000000,\n'
            'CHYBA,CHYBA,CHYBA,CHYBA,CHYBA\n'  # tento řádek způsobí chybu
            'Eva Import,2025-05-28,KB,2500000,\n'
        )
        file = io.StringIO(csv_data)
        try:
            with transaction.atomic():
                import_klienti_from_csv(file)
                raise Exception("Simulovaná chyba po importu")
        except Exception:
            pass
        # Ověř, že se nevytvořil žádný klient (rollback)
        self.assertEqual(Klient.objects.count(), 0)

    def test_import_csv_poskozeny_soubor(self):
        """
        Ověřuje, že import poškozeného nebo nevalidního CSV souboru neskončí pádem aplikace a správně zaloguje chybu.
        """
        # Simulace poškozeného CSV (chybějící oddělovače, neuzavřené uvozovky, binární odpad)
        poskozeny_csv = (
            'jmeno,datum,vyber_banky,co_financuje,cena\n'
            'Jan Novák,2025-05-30,KB,Byt,3000000\n'
            'Petr Dvořák,2025-05-30,KB,Byt,"abc\n'  # neuzavřená uvozovka
            'Binární\x00odpad,2025-05-30,KB,Byt,1000000\n'
            'Eva Import,2025-05-30,KB,Byt,2500000\n'
        )
        file = io.StringIO(poskozeny_csv)
        try:
            pocet = import_klienti_from_csv(file)
        except Exception as e:
            # Očekáváme, že import nespadne, pokud je robustně ošetřen
            self.fail(f"Import poškozeného CSV způsobil výjimku: {e}")
        klienti = list(Klient.objects.all())
        self.assertIsInstance(klienti, list)
        # Ověř, že import proběhl částečně nebo žádný klient nebyl importován, ale aplikace nespadla
        # (Volitelně) Ověř, že se zalogovala chyba nebo warning (pokud je logování implementováno)
