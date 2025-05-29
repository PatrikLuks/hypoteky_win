from django.test import TestCase, override_settings
from django.core import mail
from klienti.models import NotifikaceLog, Klient, UserProfile
from django.contrib.auth.models import User, Group
from datetime import date, timedelta
from klienti.utils import odeslat_notifikaci_email

@override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
class NotifikaceZmenaStavuTestCase(TestCase):
    def setUp(self):
        # Zajisti existenci skupiny 'jplservis'
        group, _ = Group.objects.get_or_create(name='jplservis')
        # Vytvoř poradce a přidej ho do skupiny
        self.poradce = User.objects.create_user(username='poradce3', email='poradce3@example.com', password='testpass')
        self.poradce.groups.add(group)
        profile, created = UserProfile.objects.get_or_create(user=self.poradce, defaults={'role': 'poradce'})
        if not created:
            profile.role = 'poradce'
            profile.save()
        self.poradce.refresh_from_db()
        # Vytvoř klienta se změnou stavu
        self.klient = Klient.objects.create(
            jmeno='Klient Změna',
            datum=date.today(),
            vyber_banky='Moneta',
            navrh_financovani_castka=1800000
        )

    def test_zmena_stavu_notifikace_vygeneruje_email_a_log(self):
        # Simuluj odeslání notifikace o změně stavu
        predmet = 'Změna stavu hypotéky'
        zprava = f"U klienta {self.klient.jmeno} došlo ke změně stavu: Schváleno."
        odeslat_notifikaci_email(
            prijemce=self.poradce.email,
            predmet=predmet,
            zprava=zprava,
            typ='stav',
            klient=self.klient
        )
        # Ověř, že byl odeslán e-mail
        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[0]
        self.assertIn('Změna stavu hypotéky', email.subject)
        self.assertIn('Klient Změna', email.body)
        self.assertIn('Schváleno', email.body)
        # Ověř, že byl vytvořen záznam v NotifikaceLog
        log = NotifikaceLog.objects.filter(prijemce=self.poradce.email, klient=self.klient, typ='stav')
        self.assertTrue(log.exists(), 'NotifikaceLog nebyl vytvořen!')
        self.assertTrue(log.first().uspesne)
