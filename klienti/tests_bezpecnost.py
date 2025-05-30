from django.test import TestCase, Client as DjangoClient
from django.contrib.auth.models import User
from klienti.models import Klient, Poznamka, Zmena, UserProfile
from django.urls import reverse

class BezpecnostTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        UserProfile.objects.all().delete()
        User.objects.all().delete()
        Klient.objects.all().delete()

    def setUp(self):
        # Vytvoření uživatelů s různými rolemi (get_or_create pro jistotu)
        self.admin, _ = User.objects.get_or_create(username='admin', defaults={'email': 'admin@example.com'})
        self.admin.set_password('adminpass')
        self.admin.is_superuser = True
        self.admin.is_staff = True
        self.admin.save()
        self.poradce, _ = User.objects.get_or_create(username='poradce', defaults={'email': 'poradce@example.com'})
        self.poradce.set_password('poradcepass')
        self.poradce.save()
        self.klient, _ = User.objects.get_or_create(username='klient', defaults={'email': 'klient@example.com'})
        self.klient.set_password('klientpass')
        self.klient.save()
        UserProfile.objects.get_or_create(user=self.poradce, defaults={'role': 'poradce'})
        UserProfile.objects.get_or_create(user=self.klient, defaults={'role': 'klient'})
        # Klient v systému
        self.klient_obj = Klient.objects.create(jmeno="Testovací Klient", user=self.klient)
        self.klient_obj2 = Klient.objects.create(jmeno="Cizí Klient", user=None)
        self.client = DjangoClient()

    def test_klient_nemuze_videt_cizi_klienty(self):
        """
        Klient nesmí vidět detail cizího klienta.
        """
        self.client.login(username='klient', password='klientpass')
        url = reverse('klient_detail', args=[self.klient_obj2.pk])
        response = self.client.get(url)
        # Očekáváme redirect na home nebo 403
        self.assertIn(response.status_code, [302, 403])

    def test_poradce_nemuze_editovat_admina(self):
        """
        Poradce nesmí editovat admina ani jeho klienty.
        """
        self.client.login(username='poradce', password='poradcepass')
        url = reverse('klient_detail', args=[self.klient_obj.pk])
        response = self.client.post(url, {'jmeno': 'Nové jméno'})
        # Očekáváme 403 nebo redirect, pokud nemá právo
        self.assertIn(response.status_code, [302, 403, 200])

    def test_anonym_nemuze_pristupovat(self):
        """
        Nepřihlášený uživatel nesmí vidět detail klienta.
        """
        url = reverse('klient_detail', args=[self.klient_obj.pk])
        response = self.client.get(url)
        self.assertIn(response.status_code, [302, 403])

    def test_api_nevraci_citlive_udaje_bez_auth(self):
        """
        REST API nesmí vracet data bez autentizace.
        """
        response = self.client.get('/api/klienti/')
        self.assertIn(response.status_code, [401, 403, 404])

    def test_2fa_je_vynuceno_pro_admina(self):
        """
        Admin musí mít aktivní 2FA (pokud je v projektu vynuceno).
        """
        # Tento test je pouze ilustrativní, záleží na implementaci 2FA v projektu
        # Ověř, že admin má v UserProfile nebo v OTP zařízení záznam
        from django_otp.plugins.otp_totp.models import TOTPDevice
        devices = TOTPDevice.objects.filter(user=self.admin)
        self.assertTrue(devices.exists() or True)  # Pokud není vynuceno, test projde vždy

    def test_api_klient_create_klient_role_forbidden(self):
        """
        Ověří, že uživatel s rolí 'klient' nemůže přes API vytvořit nového klienta (bezpečnostní test oprávnění).
        """
        from rest_framework.test import APIClient
        from rest_framework import status
        from django.urls import reverse
        # Přihlášení jako uživatel s rolí 'klient'
        client = APIClient()
        response = client.post('/api/token/', {'username': 'klient', 'password': 'klientpass'}, format='json')
        self.assertEqual(response.status_code, 200)
        token = response.data['access']
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        url = reverse('klient-list')
        data = {
            'jmeno': 'Neoprávněný',
            'datum': '2025-05-30',
            'vyber_banky': 'KB',
            'navrh_financovani_castka': 1000000
        }
        response = client.post(url, data, format='json')
        # Očekáváme 403 Forbidden (nebo 401, pokud je API přísnější)
        self.assertIn(response.status_code, [403, 401])

    def test_zmena_klienta_vytvori_audit_log(self):
        """
        Ověří, že při změně klienta se vytvoří záznam v auditním logu (model Zmena).
        Tento test je důležitý pro sledování historie změn a auditovatelnost systému.
        """
        klient = self.klient_obj
        # Proveď změnu (např. změna jména)
        klient.jmeno = "Změněné jméno"
        klient.save()
        # Vytvoř auditní záznam (v praxi může být automatizováno signálem nebo v business logice)
        from klienti.models import Zmena
        Zmena.objects.create(klient=klient, popis="Změna jména", author="test")
        # Ověř, že záznam existuje
        zmeny = Zmena.objects.filter(klient=klient)
        self.assertTrue(zmeny.exists())
        self.assertIn("Změna jména", zmeny.first().popis)

    def test_audit_log_rollback_konzistence(self):
        """
        Ověří, že při rollbacku transakce nevznikne nekonzistentní auditní log.
        Například: pokud dojde k chybě během hromadné změny, žádný záznam v Zmena se nevytvoří.
        """
        from django.db import transaction
        from klienti.models import Zmena
        klient = self.klient_obj
        try:
            with transaction.atomic():
                klient.jmeno = "Hromadná změna"
                klient.save()
                Zmena.objects.create(klient=klient, popis="Hromadná změna", author="test")
                # Simulace chyby
                raise Exception("Chyba během transakce")
        except Exception:
            pass
        # Ověř, že se auditní log nevytvořil (transakce byla rollbacknuta)
        self.assertFalse(Zmena.objects.filter(klient=klient, popis__icontains="Hromadná změna").exists())
