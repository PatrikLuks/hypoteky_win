from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from klienti.models import Klient, UserProfile
from datetime import date

class KlientAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        profile = UserProfile.objects.get(user=self.user)
        profile.role = 'poradce'
        profile.save()
        self.user.refresh_from_db()  # Důležité! Načte aktuální profil z DB
        profile = UserProfile.objects.get(user=self.user)  # Znovu načíst profil
        assert profile.role == 'poradce', f"Role není poradce, ale {profile.role}"
        self.client = APIClient()
        response = self.client.post('/api/token/', {'username': 'testuser', 'password': 'testpass'}, format='json')
        self.assertEqual(response.status_code, 200, f"JWT token nebyl získán: {response.data}")
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        self.klient1 = Klient.objects.create(jmeno='Jan Novák', datum=date.today(), vyber_banky='KB', navrh_financovani_castka=2000000, user=self.user)
        self.klient2 = Klient.objects.create(jmeno='Petr Svoboda', datum=date.today(), vyber_banky='ČSOB', navrh_financovani_castka=3500000, user=self.user)

    def test_list_klienti(self):
        url = reverse('klient-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_filter_banka(self):
        url = reverse('klient-list')
        response = self.client.get(url, {'banka': 'KB'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['vyber_banky'], 'KB')

    def test_filter_castka_min(self):
        url = reverse('klient-list')
        response = self.client.get(url, {'castka_min': 3000000})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['vyber_banky'], 'ČSOB')

    def test_search_jmeno(self):
        """
        Vyhledávání podle jména není možné, protože pole 'jmeno' je šifrované a nelze jej fulltextově hledat v DB.
        Tento test je zde pouze pro ilustraci bezpečnostního omezení.
        """
        url = reverse('klient-list')
        response = self.client.get(url, {'search': 'Novák'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Očekáváme, že výsledek je prázdný, protože šifrované pole nelze vyhledávat
        self.assertEqual(len(response.data), 0)

    def test_unauthorized_access(self):
        """
        Ověří, že nepřihlášený uživatel nemá přístup k API klientů.
        """
        self.client.credentials()  # Odstraní JWT token
        url = reverse('klient-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_forbidden_for_klient_role(self):
        """
        Ověří, že uživatel s rolí 'klient' nemůže vytvářet ani mazat klienty přes API.
        """
        # Vytvoříme uživatele s rolí 'klient'
        user2 = User.objects.create_user(username='klient', password='testpass')
        profile2 = UserProfile.objects.get(user=user2)
        profile2.role = 'klient'
        profile2.save()
        client2 = APIClient()
        response = client2.post('/api/token/', {'username': 'klient', 'password': 'testpass'}, format='json')
        self.assertEqual(response.status_code, 200)
        token2 = response.data['access']
        client2.credentials(HTTP_AUTHORIZATION='Bearer ' + token2)
        # Pokus o vytvoření klienta
        url = reverse('klient-list')
        data = {'jmeno': 'Test', 'datum': date.today(), 'vyber_banky': 'KB', 'navrh_financovani_castka': 1000000, 'user': user2.pk}
        response = client2.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # Pokus o smazání klienta
        response = client2.delete(url + f'{self.klient1.pk}/')
        self.assertIn(response.status_code, [status.HTTP_403_FORBIDDEN, status.HTTP_404_NOT_FOUND])

    def test_invalid_filter(self):
        """
        Ověří, že API vrací 400 při nevalidním filtru (např. špatný typ hodnoty).
        """
        url = reverse('klient-list')
        response = self.client.get(url, {'castka_min': 'necislo'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patch_partial_update(self):
        """
        Ověří, že PATCH funguje pro poradce a že klient nemůže měnit cizí záznam.
        """
        url = reverse('klient-detail', args=[self.klient1.pk])
        # Poradce může změnit banku
        response = self.client.patch(url, {'vyber_banky': 'Moneta'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['vyber_banky'], 'Moneta')
        # Klient nemůže měnit cizí záznam
        user2 = User.objects.create_user(username='klient2', password='testpass')
        profile2 = UserProfile.objects.get(user=user2)
        profile2.role = 'klient'
        profile2.save()
        client2 = APIClient()
        response = client2.post('/api/token/', {'username': 'klient2', 'password': 'testpass'}, format='json')
        token2 = response.data['access']
        client2.credentials(HTTP_AUTHORIZATION='Bearer ' + token2)
        response = client2.patch(url, {'vyber_banky': 'Raiffeisen'}, format='json')
        self.assertIn(response.status_code, [status.HTTP_403_FORBIDDEN, status.HTTP_404_NOT_FOUND])

    def test_klient_create_unauthorized(self):
        """
        Ověří, že bez autentizace není možné vytvořit klienta (edge-case: neautorizovaný přístup).
        """
        client = APIClient()  # bez tokenu
        url = reverse('klient-list')
        data = {
            'jmeno': 'Neoprávněný',
            'datum': date.today(),
            'vyber_banky': 'KB',
            'navrh_financovani_castka': 1000000
        }
        response = client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_klient_create_invalid_data(self):
        """
        Ověří, že API správně odmítne nevalidní vstup (chybí povinné pole 'datum').
        """
        url = reverse('klient-list')
        data = {
            'jmeno': 'Chybí datum',
            'vyber_banky': 'KB',
            'navrh_financovani_castka': 1000000
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('datum', response.data)

    def test_klient_create_extremni_hodnoty_a_formaty(self):
        """
        Ověří, že API správně odmítne extrémní hodnoty a špatné formáty:
        - příliš dlouhé jméno
        - záporná a extrémně vysoká částka
        - špatný formát data
        - speciální znaky a SQL injection v poli
        """
        url = reverse('klient-list')
        # Příliš dlouhé jméno
        data = {
            'jmeno': 'A' * 300,
            'datum': date.today(),
            'vyber_banky': 'KB',
            'navrh_financovani_castka': 1000000
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Záporná částka
        data = {
            'jmeno': 'Záporná částka',
            'datum': date.today(),
            'vyber_banky': 'KB',
            'navrh_financovani_castka': -500000
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Extrémně vysoká částka
        data = {
            'jmeno': 'Extrémní částka',
            'datum': date.today(),
            'vyber_banky': 'KB',
            'navrh_financovani_castka': 999999999999
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Špatný formát data
        data = {
            'jmeno': 'Špatné datum',
            'datum': 'neplatné datum',
            'vyber_banky': 'KB',
            'navrh_financovani_castka': 1000000
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # SQL injection v poli
        data = {
            'jmeno': "'; DROP TABLE klienti;--",
            'datum': date.today(),
            'vyber_banky': 'KB',
            'navrh_financovani_castka': 1000000
        }
        response = self.client.post(url, data, format='json')
        # Očekáváme odmítnutí nebo bezpečné uložení bez vlivu na DB
        self.assertIn(response.status_code, [status.HTTP_201_CREATED, status.HTTP_400_BAD_REQUEST])
        # Ověř, že DB nebyla poškozena
        self.assertTrue(Klient.objects.exists())
