from datetime import date

from django.contrib.auth.models import Group, User
from django.core import mail
from django.test import TestCase, override_settings

from klienti.models import Klient, NotifikaceLog, UserProfile


@override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
class NotifikaceZamitnutiTestCase(TestCase):
    def setUp(self):
        # Zajisti existenci skupiny 'jplservis'
        group, _ = Group.objects.get_or_create(name="jplservis")
        # Vytvoř poradce a přidej ho do skupiny
        self.poradce = User.objects.create_user(
            username="poradce2", email="poradce2@example.com", password="testpass"
        )
        self.poradce.groups.add(group)
        profile, created = UserProfile.objects.get_or_create(
            user=self.poradce, defaults={"role": "poradce"}
        )
        if not created:
            profile.role = "poradce"
            profile.save()
        self.poradce.refresh_from_db()
        # Vytvoř klienta se zamítnutím
        self.klient = Klient.objects.create(
            jmeno="Zamítnutý Klient",
            datum=date.today(),
            vyber_banky="ČSOB",
            navrh_financovani_castka=1500000,
            duvod_zamitnuti="Nedostatečný příjem",
        )

    def test_zamitnuti_notifikace_vygeneruje_email_a_log(self):
        # Simuluj odeslání notifikace o zamítnutí
        from klienti.utils import odeslat_notifikaci_email

        predmet = "Zamítnutí hypotéky"
        zprava = f"Klient {self.klient.jmeno} byl zamítnut. Důvod: {self.klient.duvod_zamitnuti}"
        odeslat_notifikaci_email(
            prijemce=self.poradce.email,
            predmet=predmet,
            zprava=zprava,
            typ="zamítnutí",
            klient=self.klient,
        )
        # Ověř, že byl odeslán e-mail
        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[0]
        self.assertIn("Zamítnutí hypotéky", email.subject)
        self.assertIn("Zamítnutý Klient", email.body)
        self.assertIn("Nedostatečný příjem", email.body)
        # Ověř, že byl vytvořen záznam v NotifikaceLog
        log = NotifikaceLog.objects.filter(
            prijemce=self.poradce.email, klient=self.klient, typ="zamítnutí"
        )
        self.assertTrue(log.exists(), "NotifikaceLog nebyl vytvořen!")
        self.assertTrue(log.first().uspesne)
