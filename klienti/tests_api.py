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
        self.client = APIClient()
        # Získání JWT tokenu
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
