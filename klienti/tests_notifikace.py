from django.test import TestCase, override_settings
from django.core import mail
from django.core.management import call_command
from klienti.models import NotifikaceLog, Klient, UserProfile
from django.contrib.auth.models import User
from datetime import date, timedelta

@override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
class NotifikaceDeadlineTestCase(TestCase):
    def setUp(self):
        from django.contrib.auth.models import Group
        # Zajisti existenci skupiny 'jplservis'
        group, _ = Group.objects.get_or_create(name='jplservis')
        # Vytvoř poradce a přidej ho do skupiny
        self.poradce = User.objects.create_user(username='poradce', email='poradce@example.com', password='testpass')
        self.poradce.groups.add(group)
        profile, created = UserProfile.objects.get_or_create(user=self.poradce, defaults={'role': 'poradce'})
        if not created:
            profile.role = 'poradce'
            profile.save()
        self.poradce.refresh_from_db()
        # Kontrola, že profil existuje a má správnou roli
        assert hasattr(self.poradce, 'userprofile'), 'Poradce nemá UserProfile!'
        assert self.poradce.userprofile.role == 'poradce', f"Role poradce: {self.poradce.userprofile.role}"
        # Vytvoř klienta s deadlinem do 2 dnů
        self.klient = Klient.objects.create(
            jmeno='Testovací Klient',
            datum=date.today(),
            vyber_banky='KB',
            navrh_financovani_castka=2000000,
            deadline_co_financuje=date.today() + timedelta(days=2)
        )

    def test_deadline_notifikace_vygeneruje_email_a_log(self):
        # Spusť command
        from klienti.models import UserProfile
        poradci = UserProfile.objects.filter(role='poradce')
        print(f"[DEBUG] Poradců v DB: {poradci.count()}")
        call_command('send_deadline_notifications')
        # Ověř, že byl odeslán e-mail
        from klienti.models import Klient
        klienti = Klient.objects.all()
        print(f"[DEBUG] Klientů v DB: {klienti.count()}")
        from klienti.models import NotifikaceLog
        logy = NotifikaceLog.objects.all()
        print(f"[DEBUG] NotifikaceLog v DB: {logy.count()}")
        from django.core import mail
        print(f"[DEBUG] Počet e-mailů v outboxu: {len(mail.outbox)}")
        for email in mail.outbox:
            print(f"[DEBUG] E-mail subject: {email.subject}, body: {email.body}")
        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[0]
        self.assertIn('Blíží se deadline', email.subject)
        self.assertIn('Testovací Klient', email.body)
        # Ověř, že byl vytvořen záznam v NotifikaceLog
        log = NotifikaceLog.objects.filter(prijemce='poradce@example.com', klient=self.klient, typ='deadline')
        self.assertTrue(log.exists(), 'NotifikaceLog nebyl vytvořen!')
        self.assertTrue(log.first().uspesne)
