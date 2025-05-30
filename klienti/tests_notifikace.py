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
        """
        Ověří, že po spuštění commandu se odešle e-mail a zaloguje notifikace.
        Testuje i edge-case: pokud není žádný klient s deadlinem, e-mail se neodešle.
        """
        # Spusť command
        call_command('send_deadline_notifications')
        # Ověř, že byl odeslán e-mail
        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[0]
        self.assertIn('Deadline', email.subject)
        self.assertIn('Testovací Klient', email.body)
        # Ověř, že byl zalogován záznam
        logy = NotifikaceLog.objects.all()
        self.assertEqual(logy.count(), 1)
        self.assertIn('Deadline', logy[0].typ)

    def test_deadline_notifikace_neexistujici_email(self):
        """
        Ověří, že pokud poradce nemá e-mail, notifikace se neodešle a log se nevytvoří.
        Tento test je důležitý, protože v reálném provozu může být uživatel bez e-mailu a aplikace musí tuto situaci bezpečně zvládnout.
        """
        # Nastav poradci prázdný e-mail
        self.poradce.email = ''
        self.poradce.save()
        # Spusť command
        call_command('send_deadline_notifications')
        # Ověř, že nebyl odeslán žádný e-mail
        self.assertEqual(len(mail.outbox), 0)
        # Ověř, že nebyl vytvořen žádný NotifikaceLog pro tento případ
        log = NotifikaceLog.objects.filter(prijemce='', klient=self.klient, typ='deadline')
        self.assertFalse(log.exists(), 'NotifikaceLog by neměl být vytvořen!')

    def test_deadline_notifikace_bez_klientu(self):
        """
        Ověří, že pokud není žádný klient s deadlinem, e-mail se neodešle a log se nevytvoří.
        """
        Klient.objects.all().delete()
        call_command('send_deadline_notifications')
        self.assertEqual(len(mail.outbox), 0)
        self.assertEqual(NotifikaceLog.objects.count(), 0)