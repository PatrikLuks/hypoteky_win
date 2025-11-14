# -*- coding: utf-8 -*-
from django.db import connection
from django.test import TestCase

from klienti.models import Klient, Poznamka, Zmena


class SifrovaniTestCase(TestCase):
    def setUp(self):
        self.klient = Klient.objects.create(
            jmeno="Testovací Klient",
            co_financuje="Byt v Praze",
            duvod_zamitnuti="Nedostatečný příjem",
        )
        self.poznamka = Poznamka.objects.create(
            klient=self.klient, text="Toto je tajná poznámka", author="admin"
        )
        self.zmena = Zmena.objects.create(
            klient=self.klient, popis="Změna workflow", author="admin"
        )

    def test_decrypt_orm(self):
        """
        Ověří, že ORM správně dešifruje data uložená v šifrovaných polích.
        Testuje, že aplikace zůstává plně funkční i při šifrování citlivých údajů.
        """
        klient = Klient.objects.get(pk=self.klient.pk)
        self.assertEqual(klient.jmeno, "Testovací Klient")
        self.assertEqual(klient.co_financuje, "Byt v Praze")
        self.assertEqual(klient.duvod_zamitnuti, "Nedostatečný příjem")
        self.assertEqual(klient.poznamky.first().text, "Toto je tajná poznámka")
        self.assertEqual(klient.zmeny.first().popis, "Změna workflow")

    def test_data_in_db_are_encrypted(self):
        """
        Ověří, že citlivá data jsou v DB fyzicky šifrovaná (nečitelná v otevřeném tvaru).
        Tento test je důležitý pro bezpečnost a GDPR compliance.
        Příklad: pokud někdo získá přímý přístup k DB, nesmí přečíst jména klientů.
        """
        # Nejprve smaž závislé záznamy, pak klienty
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM klienti_poznamka")
            cursor.execute("DELETE FROM klienti_zmena")
            cursor.execute("DELETE FROM klienti_klient")
        self.klient = Klient.objects.create(
            jmeno="Testovací Klient",
            co_financuje="Byt v Praze",
            duvod_zamitnuti="Nedostatečný příjem",
        )
        self.poznamka = Poznamka.objects.create(
            klient=self.klient, text="Toto je tajná poznámka", author="admin"
        )
        self.zmena = Zmena.objects.create(
            klient=self.klient, popis="Změna workflow", author="admin"
        )
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT jmeno, co_financuje, duvod_zamitnuti FROM klienti_klient WHERE id = %s",
                [self.klient.pk],
            )
            row = cursor.fetchone()
            self.assertIsNotNone(
                row,
                "Klient nebyl nalezen v databázi (pravděpodobně nebyl uložen nebo byl smazán).",
            )
            for value in row:
                self.assertNotIn("Testovací Klient", str(value))
                self.assertNotIn("Byt v Praze", str(value))
                self.assertNotIn("Nedostatečný příjem", str(value))
            cursor.execute(
                "SELECT text FROM klienti_poznamka WHERE id = %s", [self.poznamka.pk]
            )
            value = cursor.fetchone()
            self.assertIsNotNone(value, "Poznámka nebyla nalezena v databázi.")
            value = value[0]
            self.assertNotIn("Toto je tajná poznámka", str(value))
            cursor.execute(
                "SELECT popis FROM klienti_zmena WHERE id = %s", [self.zmena.pk]
            )
            value = cursor.fetchone()
            self.assertIsNotNone(value, "Změna nebyla nalezena v databázi.")
            value = value[0]
            self.assertNotIn("Změna workflow", str(value))
