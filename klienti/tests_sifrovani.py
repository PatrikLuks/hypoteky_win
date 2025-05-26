from django.test import TestCase
from klienti.models import Klient, Poznamka, Zmena
from django.conf import settings
import base64
import MySQLdb

class SifrovaniTestCase(TestCase):
    def setUp(self):
        self.klient = Klient.objects.create(
            jmeno="Testovací Klient",
            co_financuje="Byt v Praze",
            duvod_zamitnuti="Nedostatečný příjem"
        )
        self.poznamka = Poznamka.objects.create(
            klient=self.klient,
            text="Toto je tajná poznámka",
            author="admin"
        )
        self.zmena = Zmena.objects.create(
            klient=self.klient,
            popis="Změna workflow",
            author="admin"
        )

    def test_decrypt_orm(self):
        """
        ORM musí správně dešifrovat data uložená v šifrovaných polích.
        """
        klient = Klient.objects.get(pk=self.klient.pk)
        self.assertEqual(klient.jmeno, "Testovací Klient")
        self.assertEqual(klient.co_financuje, "Byt v Praze")
        self.assertEqual(klient.duvod_zamitnuti, "Nedostatečný příjem")
        self.assertEqual(klient.poznamky.first().text, "Toto je tajná poznámka")
        self.assertEqual(klient.zmeny.first().popis, "Změna workflow")

    def test_data_in_db_are_encrypted(self):
        """
        Data v databázi musí být fyzicky nečitelná (neuložená v otevřeném tvaru).
        """
        # Připojíme se přímo na DB a načteme raw hodnoty
        db = MySQLdb.connect(
            host=settings.DATABASES['default']['HOST'],
            user=settings.DATABASES['default']['USER'],
            passwd=settings.DATABASES['default']['PASSWORD'],
            db=settings.DATABASES['default']['NAME'],
            charset='utf8mb4'
        )
        cursor = db.cursor()
        cursor.execute("SELECT jmeno, co_financuje, duvod_zamitnuti FROM klienti_klient WHERE id = %s", [self.klient.pk])
        row = cursor.fetchone()
        for value in row:
            self.assertNotIn("Testovací Klient", str(value))
            self.assertNotIn("Byt v Praze", str(value))
            self.assertNotIn("Nedostatečný příjem", str(value))
        cursor.execute("SELECT text FROM klienti_poznamka WHERE id = %s", [self.poznamka.pk])
        value = cursor.fetchone()[0]
        self.assertNotIn("Toto je tajná poznámka", str(value))
        cursor.execute("SELECT popis FROM klienti_zmena WHERE id = %s", [self.zmena.pk])
        value = cursor.fetchone()[0]
        self.assertNotIn("Změna workflow", str(value))
        db.close()
