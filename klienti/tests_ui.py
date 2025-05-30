from django.test import TestCase, Client, override_settings
from django.urls import reverse
import difflib
import re

class DashboardUITestCase(TestCase):
    """
    Testuje renderování dashboardu a základní UI prvky.
    """
    def setUp(self):
        self.client = Client()
        # Přihlášení uživatele, pokud je potřeba (předpokládáme, že dashboard je chráněný)
        # Pokud je potřeba, vytvoř uživatele a přihlas ho zde

    def test_dashboard_renderuje(self):
        """
        Ověří, že se dashboard správně načte a obsahuje klíčové prvky.
        """
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        # Ověř přítomnost hlavních sekcí
        self.assertContains(response, 'Dashboard')
        self.assertContains(response, 'Počet klientů')
        self.assertContains(response, 'Objem hypoték')
        self.assertContains(response, 'Urgentní deadliny')
        self.assertContains(response, 'TOP 5 největších hypoték')
        self.assertContains(response, 'Průměrná výše hypotéky')
        self.assertContains(response, 'Poslední změny')

    def test_dashboard_responsivita(self):
        """
        Ověří, že dashboard obsahuje responsivní třídy (Bootstrap).
        """
        response = self.client.get(reverse('dashboard'))
        self.assertContains(response, 'container-fluid')
        self.assertContains(response, 'row')
        self.assertContains(response, 'col-lg-')
        self.assertContains(response, 'card')

    def test_dashboard_snapshot(self):
        """
        Ověří, že HTML dashboardu odpovídá snapshotu (po ošetření dynamických dat).
        Pokud snapshot neexistuje, vytvoří ho.
        """
        response = self.client.get(reverse('dashboard'))
        html = response.content.decode('utf-8')
        # Nahrazení dynamických dat (datum, čísla, ID) zástupnými hodnotami
        html = re.sub(r'\d{2}\.\d{2}\.\d{4}', '__DATUM__', html)  # datum
        html = re.sub(r'Počet klientů.*?<div class="display-4 fw-bold text-warning">(\d+)</div>',
                      'Počet klientů<div class="display-4 fw-bold text-warning">__POCET__</div>', html, flags=re.DOTALL)
        html = re.sub(r'Objem hypoték.*?<div class="display-4 fw-bold text-success"[^>]*>([\d\s]+) Kč</div>',
                      'Objem hypoték<div class="display-4 fw-bold text-success">__OBJEM__ Kč</div>', html, flags=re.DOTALL)
        html = re.sub(r'Urgentní deadliny.*?<div class="display-4 fw-bold text-danger">(\d+)</div>',
                      'Urgentní deadliny<div class="display-4 fw-bold text-danger">__URGENT__</div>', html, flags=re.DOTALL)
        # Další dynamické části lze přidat dle potřeby
        snapshot_path = 'dashboard_snapshot.html'
        try:
            with open(snapshot_path, 'r', encoding='utf-8') as f:
                snapshot = f.read()
            # Porovnání snapshotu s aktuálním HTML
            diff = list(difflib.unified_diff(snapshot.splitlines(), html.splitlines()))
            assert not diff, f"Snapshot neodpovídá!\n{chr(10).join(diff)}"
        except FileNotFoundError:
            # Pokud snapshot neexistuje, vytvoří ho
            with open(snapshot_path, 'w', encoding='utf-8') as f:
                f.write(html)
            print(f"Snapshot uložen do {snapshot_path}")

    # ---
    # Ukázka a11y testu pomocí Playwright a axe-core (vyžaduje Playwright a axe)
    # Tento test je pouze ilustrační, v praxi je vhodné spouštět jej v e2e prostředí
    #
    # from playwright.sync_api import sync_playwright
    # def test_dashboard_accessibility():
    #     with sync_playwright() as p:
    #         browser = p.chromium.launch()
    #         page = browser.new_page()
    #         page.goto('http://localhost:8000/dashboard/')
    #         results = page.evaluate("axe.run()")
    #         assert results['violations'] == []
    #         browser.close()
    # ---

class ReportingUITestCase(TestCase):
    """
    Testuje renderování a snapshot reportingu (reporting.html).
    """
    def setUp(self):
        self.client = Client()
        # Přihlášení uživatele, pokud je potřeba

    def test_reporting_renderuje(self):
        """
        Ověří, že reporting view se načte a obsahuje klíčové prvky.
        """
        response = self.client.get(reverse('reporting'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Reporting & Statistika hypoték')
        self.assertContains(response, 'Export do PDF')
        self.assertContains(response, 'Úspěšnost podle banky')
        self.assertContains(response, 'Trendy schválených a zamítnutých hypoték')
        self.assertContains(response, 'Heatmapa průměrné doby schválení')
        self.assertContains(response, 'canvas')

    def test_reporting_filtry(self):
        """
        Ověří, že reporting obsahuje filtrační formulář.
        """
        response = self.client.get(reverse('reporting'))
        self.assertContains(response, 'form')
        self.assertContains(response, 'datum_od')
        self.assertContains(response, 'datum_do')
        self.assertContains(response, 'Filtrovat')

    def test_reporting_responsivita(self):
        """
        Ověří, že reporting obsahuje responsivní třídy (Bootstrap, grid, karty).
        """
        response = self.client.get(reverse('reporting'))
        self.assertContains(response, 'container-fluid')
        self.assertContains(response, 'row')
        self.assertContains(response, 'col-')
        self.assertContains(response, 'card')

    def test_reporting_filtr_nevalidni_datum(self):
        """
        Ověří, že při zadání neplatného data ve filtru se zobrazí chybová hláška.
        """
        response = self.client.get(reverse('reporting'), {'datum_od': 'neplatne', 'datum_do': '2025-05-27'})
        self.assertContains(response, 'form')
        # Ověříme, že se v odpovědi vyskytuje chybová hláška o datu (v jakémkoli jazyce)
        self.assertIn('valid date', response.content.decode('utf-8').lower())

    @override_settings(ALLOWED_HOSTS=["testserver", "localhost", "127.0.0.1"])
    def test_reporting_snapshot(self):
        """
        Snapshot test: uloží HTML výstup reportingu a porovná s referenčním snapshotem.
        """
        response = self.client.get(reverse('reporting'))
        html = response.content.decode('utf-8')
        # Nahradíme aktuální datum zástupným textem, aby byl snapshot stabilní
        html = re.sub(r'value="20[0-9]{2}-[0-9]{2}-[0-9]{2}"', 'value="__DATUM__"', html)
        # Nahradíme i případné další datumy v textu
        html = re.sub(r'\d{2}\.\d{2}\.\d{4}', '__DATUM__', html)
        # Nahradíme dynamické počty, částky, atd. (dle potřeby)
        html = re.sub(r'<div class="display-5 fw-bold mb-2"><i class="fa fa-users"></i> (\d+)</div>',
                      '<div class="display-5 fw-bold mb-2"><i class="fa fa-users"></i> __KLIENTU__</div>', html)
        html = re.sub(r'<div class="display-6 fw-bold mb-2"><i class="fa fa-check-circle"></i> (\d+)</div>',
                      '<div class="display-6 fw-bold mb-2"><i class="fa fa-check-circle"></i> __SCHVALENO__</div>', html)
        html = re.sub(r'<div class="display-6 fw-bold mb-2"><i class="fa fa-times-circle"></i> (\d+)</div>',
                      '<div class="display-6 fw-bold mb-2"><i class="fa fa-times-circle"></i> __ZAMITNUTO__</div>', html)
        snapshot_path = 'reporting_snapshot.html'
        try:
            with open(snapshot_path, 'r', encoding='utf-8') as f:
                snapshot = f.read()
            if html != snapshot:
                diff = '\n'.join(difflib.unified_diff(snapshot.splitlines(), html.splitlines(), fromfile='snapshot', tofile='current', lineterm=''))
                self.fail(f"HTML výstup reportingu se změnil oproti snapshotu!\nDiff:\n{diff}")
        except FileNotFoundError:
            with open(snapshot_path, 'w', encoding='utf-8') as f:
                f.write(html)
            # První běh: snapshot vytvořen
            pass

class WorkflowUITestCase(TestCase):
    """
    Testuje průchod klienta všemi 15 kroky workflow a validaci formulářů.
    """
    def setUp(self):
        from django.contrib.auth.models import User
        from klienti.models import UserProfile
        self.user = User.objects.create_user(username='testklient', password='testpass')
        # Nastavíme roli na 'klient'
        profile = UserProfile.objects.get(user=self.user)
        profile.role = 'klient'
        profile.save()
        self.client = Client()
        self.client.login(username='testklient', password='testpass')

    def test_klient_projde_vsechny_kroky_workflow(self):
        """
        Ověří, že klient může projít všemi 15 kroky workflow a validace funguje.
        """
        from klienti.models import Klient
        from django.urls import reverse
        # 1. Vytvoření klienta se všemi povinnými poli
        response = self.client.post(reverse('klient_create'), {
            'jmeno': 'Workflow Tester',
            'datum': '2025-05-27',
            'cena': '5000000',
            'navrh_financovani_procento': '80',
            'co_financuje': 'Byt v Praze',
            'navrh_financovani': 'Hypotéka 80 %',
        })
        print('RESPONSE STATUS:', response.status_code)
        print('RESPONSE BODY:', response.content.decode('utf-8'))
        self.assertEqual(response.status_code, 302)  # redirect po úspěšném vytvoření
        from klienti.models import Klient
        klient = Klient.objects.get(user=self.user)
        # 2. Postupné vyplňování všech kroků workflow
        workflow_fields = [
            ('co_financuje', 'Byt v Praze'),
            ('navrh_financovani', 'Hypotéka 80 %'),
            ('vyber_banky', 'ČSOB'),
            ('priprava_zadosti', 'Připraveno'),
            ('kompletace_podkladu', 'Kompletováno'),
            ('podani_zadosti', 'Podáno'),
            ('odhad', 'Odhad hotov'),
            ('schvalovani', 'Schváleno'),
            ('priprava_uverove_dokumentace', 'Dokumentace připravena'),
            ('podpis_uverove_dokumentace', 'Podepsáno'),
            ('priprava_cerpani', 'Připraveno'),
            ('cerpani', 'Čerpáno'),
            ('zahajeni_splaceni', 'Zahájeno'),
            ('podminky_pro_splaceni', 'Splněno'),
        ]
        for idx, (field, value) in enumerate(workflow_fields, start=2):
            data = {'jmeno': klient.jmeno, 'datum': '2025-05-27'}
            # Vyplníme všechny předchozí kroky, jinak validace neprojde
            for prev_idx, (prev_field, prev_value) in enumerate(workflow_fields[:idx-1]):
                data[prev_field] = prev_value
            # Aktuální krok
            data[field] = value
            response = self.client.post(reverse('klient_edit', args=[klient.pk]), data)
            # Očekáváme redirect po úspěšném uložení
            self.assertEqual(response.status_code, 302, f"Krok {field} neprošel validací!")
            klient.refresh_from_db()
            self.assertEqual(getattr(klient, field), value)
            # Ověříme, že v detailu klienta je zvýrazněn správný krok
            detail = self.client.get(reverse('klient_detail', args=[klient.pk]))
            self.assertEqual(detail.status_code, 200)
            # V HTML by měl být aktivní krok zvýrazněn (border-primary)
            self.assertIn('border-primary', detail.content.decode('utf-8'))
        # 3. Ověření, že po posledním kroku je workflow hotovo
        klient.refresh_from_db()
        # Ověř, že poslední krok je vyplněn a zvýrazněn (dokončený workflow)
        detail = self.client.get(reverse('klient_detail', args=[klient.pk]))
        self.assertEqual(detail.status_code, 200)
        html = detail.content.decode('utf-8')
        # Ověř, že v HTML je poslední krok workflow zvýrazněn (border-primary) a obsahuje text 'Podmínky pro splacení'
        self.assertIn('border-primary', html)
        self.assertIn('Podmínky pro splacení', html)
        # Ověř, že pole podminky_pro_splaceni je opravdu vyplněno
        self.assertEqual(klient.podminky_pro_splaceni, 'Splněno')

    def test_workflow_validace_nelze_preskocit_krok(self):
        """
        Ověří, že nelze přeskočit krok workflow (validace formuláře).
        """
        from klienti.models import Klient
        from django.urls import reverse
        response = self.client.post(reverse('klient_create'), {
            'jmeno': 'Skip Tester',
            'datum': '2025-05-27',
            'cena': '4000000',
            'navrh_financovani_procento': '70',
            'co_financuje': 'Dům v Brně',
            'navrh_financovani': 'Hypotéka 70 %',
        })
        print('RESPONSE STATUS:', response.status_code)
        print('RESPONSE BODY:', response.content.decode('utf-8'))
        self.assertEqual(response.status_code, 302)
        from klienti.models import Klient
        klient = Klient.objects.get(user=self.user)
        # Pokusíme se vyplnit 3. krok bez 2. kroku
        data = {'jmeno': klient.jmeno, 'datum': '2025-05-27', 'navrh_financovani': 'Hypotéka 80 %'}
        response = self.client.post(reverse('klient_edit', args=[klient.pk]), data)
        # Očekáváme, že validace neprojde a stránka se znovu zobrazí s chybou (status 200)
        self.assertEqual(response.status_code, 200)
        html = response.content.decode('utf-8')
        # Ověř, že se zobrazila chybová hláška o workflow (nelze přeskočit krok)
        self.assertIn('Nelze vyplnit krok', html)

class KlientDetailUITestCase(TestCase):
    """
    Testuje správné zobrazení detailu klienta včetně workflow, poznámek a historie změn (auditní log).
    """
    def setUp(self):
        from django.contrib.auth.models import User
        from klienti.models import UserProfile, Klient, Poznamka, Zmena
        # Vytvoř uživatele 'detailklient' s heslem 'testpass' a rolí 'klient'
        self.user = User.objects.create_user(username='detailklient', password='testpass')
        profile = UserProfile.objects.get(user=self.user)
        profile.role = 'klient'
        profile.save()
        self.client = Client()
        self.client.login(username='detailklient', password='testpass')
        # Vytvoření klienta s tímto uživatelem
        self.klient = Klient.objects.create(
            jmeno='Detailní Klient',
            datum='2025-05-27',
            co_financuje='Dům',
            cena=6000000,
            navrh_financovani='Hypotéka 80 %',
            navrh_financovani_procento=80,
            vyber_banky='KB',
            user=self.user
        )
        # Vyčisti poznámky a změny pro jistotu
        Poznamka.objects.filter(klient=self.klient).delete()
        Zmena.objects.filter(klient=self.klient).delete()
        # Přidej základní poznámku s autorem 'detailklient'
        Poznamka.objects.create(klient=self.klient, text='Testovací poznámka', author='detailklient')
        print(f"[DEBUG setUp] Uživatelské jméno: {self.user.username}")

    def test_klient_detail_renderuje_udaje(self):
        """
        Ověří, že detail klienta obsahuje všechny klíčové informace, poznámky a historii změn.
        """
        from django.urls import reverse
        response = self.client.get(reverse('klient_detail', args=[self.klient.pk]))
        self.assertEqual(response.status_code, 200)
        html = response.content.decode('utf-8')
        # Ověření základních údajů
        self.assertIn('Detail klienta', html)
        self.assertIn('Detailní Klient', html)
        self.assertIn('Dům', html)
        self.assertIn('Hypotéka 80 %', html)
        self.assertIn('KB', html)
        # Ověření workflow (výskyt kroků)
        self.assertIn('Výběr banky', html)
        self.assertIn('Návrh financování', html)
        # Ověření poznámky
        self.assertIn('Testovací poznámka', html)
        # Ověření historie změn (audit) – nyní očekáváme prázdný log (žádná změna)
        self.assertIn('Historie změn', html)
        # Ověření, že pokud není žádná změna, zobrazí se správná hláška
        self.assertIn('Žádné změny nejsou evidovány.', html)
        # Ověření přístupnosti (role, aria-label)
        self.assertIn('role="main"', html)
        self.assertIn('aria-label', html)
        # Ověření zvýraznění aktivního kroku (border-primary)
        self.assertIn('border-primary', html)

    def test_audit_log_pribude_polozka_po_editaci(self):
        """
        Ověří, že po editaci klienta se v sekci Historie změn objeví nová položka s popisem změny.
        Test nyní POSTuje změnu ceny z 6 000 000 na 7 000 000, aby byla změna detekována.
        """
        from django.urls import reverse
        from klienti.models import Zmena
        from bs4 import BeautifulSoup
        import datetime
        # Nastav klientovi cenu na 6 000 000 před POSTem
        self.klient.cena = 6000000
        self.klient.save()
        url = reverse('klient_edit', args=[self.klient.pk])
        self.klient.refresh_from_db()
        today = datetime.date.today().strftime('%Y-%m-%d')
        data = {
            'jmeno': self.klient.jmeno,
            'datum': self.klient.datum.strftime('%Y-%m-%d'),
            'co_financuje': self.klient.co_financuje,
            'cena': '7000000',  # změna ceny
            'deadline_co_financuje': today,
            'splneno_co_financuje': '',
            'navrh_financovani': self.klient.navrh_financovani,
            'navrh_financovani_procento': self.klient.navrh_financovani_procento,
            'deadline_navrh_financovani': today,
            'splneno_navrh_financovani': '',
            'vyber_banky': self.klient.vyber_banky,
            'deadline_vyber_banky': today,
            'splneno_vyber_banky': '',
            'priprava_zadosti': '',
            'deadline_priprava_zadosti': today,
            'splneno_priprava_zadosti': '',
            'kompletace_podkladu': '',
            'deadline_kompletace_podkladu': today,
            'splneno_kompletace_podkladu': '',
            'podani_zadosti': '',
            'deadline_podani_zadosti': today,
            'splneno_podani_zadosti': '',
            'odhad': '',
            'deadline_odhad': today,
            'splneno_odhad': '',
            'schvalovani': '',
            'deadline_schvalovani': today,
            'splneno_schvalovani': '',
            'priprava_uverove_dokumentace': '',
            'deadline_priprava_uverove_dokumentace': today,
            'splneno_priprava_uverove_dokumentace': '',
            'podpis_uverove_dokumentace': '',
            'deadline_podpis_uverove_dokumentace': today,
            'splneno_podpis_uverove_dokumentace': '',
            'priprava_cerpani': '',
            'deadline_priprava_cerpani': today,
            'splneno_priprava_cerpani': '',
            'cerpani': '',
            'deadline_cerpani': today,
            'splneno_cerpani': '',
            'zahajeni_splaceni': '',
            'deadline_zahajeni_splaceni': today,
            'splneno_zahajeni_splaceni': '',
            'podminky_pro_splaceni': '',
            'deadline_podminky_pro_splaceni': today,
            'splneno_podminky_pro_splaceni': '',
        }
        response = self.client.post(url, data, follow=True)
        self.klient.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        html = response.content.decode('utf-8')
        self.assertTrue('7000000' in html or '7000000 Kč' in html)
        soup = BeautifulSoup(html, 'html.parser')
        h4 = None
        for tag in soup.find_all('h4'):
            if 'Historie změn' in tag.get_text():
                h4 = tag
                break
        self.assertIsNotNone(h4, 'Nadpis Historie změn nebyl nalezen v HTML.')
        table = h4.find_next('table')
        self.assertIsNotNone(table, 'Tabulka auditního logu nebyla nalezena v HTML.')
        rows = table.find_all('tr')[1:]
        popisy = [row.find_all('td')[2].get_text() for row in rows if len(row.find_all('td')) >= 3]
        nalezeno = any(('cena' in p and '7000000' in p) for p in popisy)
        self.assertTrue(nalezeno, f'V auditním logu nebyla nalezena změna ceny na 7000000.\nPopisy změn: {popisy}')
        # Komentář: Pokud by test selhal na validaci, zkontrolujte, zda pole odpovídají aktuálním fields v KlientForm.

    def test_poznamka_pridani_v_detailu_klienta(self):
        """
        Ověří, že poznámku lze přidat a je viditelná v detailu klienta.
        """
        from django.urls import reverse
        from klienti.models import Poznamka
        self.client.login(username=self.user.username, password='testpass')
        response = self.client.post(reverse('klient_detail', args=[self.klient.pk]), {
            'text': 'Poznámka CRUD test',
            'nova_poznamka': '1',
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        html = response.content.decode('utf-8')
        self.assertIn('Poznámka CRUD test', html)
        pozn_klient = Poznamka.objects.filter(klient=self.klient, author=self.user.username)
        poznamka = pozn_klient.order_by('-id').first()
        self.assertIsNotNone(poznamka, "Poznámka nebyla nalezena!")
        self.klient.refresh_from_db()
        self.assertEqual(poznamka.text, 'Poznámka CRUD test')
        from klienti.models import Zmena
        zmeny = Zmena.objects.filter(klient=self.klient).order_by('-created')
        self.assertGreater(zmeny.count(), 0, 'Nebyl nalezen žádný auditní záznam po přidání poznámky.')
        self.assertIn('Přidána poznámka', zmeny.first().popis)

    def test_poznamka_smazani_audit_v_detailu_klienta(self):
        """
        Ověří, že poznámku lze smazat a že smazání je zaznamenáno v auditním logu.
        """
        from django.urls import reverse
        from klienti.models import Poznamka, Zmena
        self.client.login(username=self.user.username, password='testpass')
        poznamka = Poznamka.objects.create(klient=self.klient, text='Poznámka CRUD test', author=self.user.username)
        url_smazat = reverse('smazat_poznamku', args=[self.klient.pk, poznamka.pk])
        response = self.client.post(url_smazat, follow=True)
        self.assertEqual(response.status_code, 200)
        pozn_klient_po = Poznamka.objects.filter(klient=self.klient)
        self.assertFalse(any('Poznámka CRUD test' in p.text for p in pozn_klient_po), "Poznámka nebyla smazána!")
        self.klient.refresh_from_db()
        zmeny = Zmena.objects.filter(klient=self.klient).order_by('-created')
        zmeny_texts = [z.popis for z in zmeny]
        self.assertTrue(zmeny.exists(), f"Auditní log neobsahuje záznam o smazání poznámky!\nZměny: {zmeny_texts}")
        self.assertIn('Smazána poznámka', zmeny.first().popis)

    def test_klient_detail_snapshot(self):
        """
        Snapshot test: uloží HTML výstup detailu klienta a porovná s referenčním snapshotem.
        """
        from django.urls import reverse
        import re, difflib
        response = self.client.get(reverse('klient_detail', args=[self.klient.pk]))
        html = response.content.decode('utf-8')
        # Nahradíme dynamická data (datumy) zástupným textem
        html = re.sub(r'\d{2}\.\d{2}\.\d{4}', '__DATUM__', html)
        # Nahradíme dynamické ID klienta v odkazech za __ID__
        html = re.sub(r'/klient/\d+/', '/klient/__ID__/', html)
        snapshot_path = 'klient_detail_snapshot.html'
        try:
            with open(snapshot_path, 'r', encoding='utf-8') as f:
                snapshot = f.read()
            if html != snapshot:
                diff = '\n'.join(difflib.unified_diff(snapshot.splitlines(), html.splitlines(), fromfile='snapshot', tofile='current', lineterm=''))
                self.fail(f"HTML výstup klient_detail se změnil oproti snapshotu!\nDiff:\n{diff}")
        except FileNotFoundError:
            with open(snapshot_path, 'w', encoding='utf-8') as f:
                f.write(html)
            # První běh: snapshot vytvořen
            pass

class KalkulackaUITestCase(TestCase):
    """
    Testuje renderování a snapshot kalkulačky hypotéky (kalkulacka.html).
    """
    def setUp(self):
        self.client = Client()

    def test_kalkulacka_snapshot(self):
        """
        Snapshot test: uloží HTML výstup kalkulačky a porovná s referenčním snapshotem.
        """
        from django.urls import reverse
        import re, difflib
        response = self.client.get(reverse('kalkulacka'))
        html = response.content.decode('utf-8')
        # Nahradíme případná dynamická data (např. CSRF token, datumy) zástupným textem
        html = re.sub(r'value="[0-9a-f]{{32,}}"', 'value="__TOKEN__"', html)
        snapshot_path = 'kalkulacka_snapshot.html'
        try:
            with open(snapshot_path, 'r', encoding='utf-8') as f:
                snapshot = f.read()
            if html != snapshot:
                diff = '\n'.join(difflib.unified_diff(snapshot.splitlines(), html.splitlines(), fromfile='snapshot', tofile='current', lineterm=''))
                self.fail(f"HTML výstup kalkulacka se změnil oproti snapshotu!\nDiff:\n{diff}")
        except FileNotFoundError:
            with open(snapshot_path, 'w', encoding='utf-8') as f:
                f.write(html)
            # První běh: snapshot vytvořen
            pass

class KlientFormUITestCase(TestCase):
    """
    Testuje renderování a snapshot formuláře pro přidání klienta (klient_form.html).
    """
    def setUp(self):
        from django.contrib.auth.models import User
        from klienti.models import UserProfile
        self.user = User.objects.create_user(username='formtest', password='testpass')
        profile = UserProfile.objects.get(user=self.user)
        profile.role = 'poradce'
        profile.save()
        self.client = Client()
        self.client.login(username='formtest', password='testpass')

    def test_klient_form_snapshot(self):
        """
        Snapshot test: uloží HTML výstup formuláře pro přidání klienta a porovná s referenčním snapshotem.
        """
        from django.urls import reverse
        import re, difflib
        response = self.client.get(reverse('klient_create'))
        html = response.content.decode('utf-8')
        # Nahradíme případná dynamická data (např. CSRF token, datumy) zástupným textem
        html = re.sub(r'value="[0-9a-f]{{32,}}"', 'value="__TOKEN__"', html)
        html = re.sub(r'\d{2}\.\d{2}\.\d{4}', '__DATUM__', html)
        snapshot_path = 'klient_form_snapshot.html'
        try:
            with open(snapshot_path, 'r', encoding='utf-8') as f:
                snapshot = f.read()
            if html != snapshot:
                diff = '\n'.join(difflib.unified_diff(snapshot.splitlines(), html.splitlines(), fromfile='snapshot', tofile='current', lineterm=''))
                self.fail(f"HTML výstup klient_form se změnil oproti snapshotu!\nDiff:\n{diff}")
        except FileNotFoundError:
            with open(snapshot_path, 'w', encoding='utf-8') as f:
                f.write(html)
            # První běh: snapshot vytvořen
            pass

class LoginUITestCase(TestCase):
    """
    Testuje renderování a snapshot přihlašovací stránky (login.html).
    """
    def setUp(self):
        self.client = Client()

    def test_login_snapshot(self):
        """
        Snapshot test: uloží HTML výstup loginu a porovná s referenčním snapshotem.
        """
        from django.urls import reverse
        import re, difflib
        response = self.client.get(reverse('login'))
        html = response.content.decode('utf-8')
        # Nahradíme případná dynamická data (např. CSRF token) zástupným textem
        html = re.sub(r'value="[0-9a-f]{{32,}}"', 'value="__TOKEN__"', html)
        snapshot_path = 'login_snapshot.html'
        try:
            with open(snapshot_path, 'r', encoding='utf-8') as f:
                snapshot = f.read()
            if html != snapshot:
                diff = '\n'.join(difflib.unified_diff(snapshot.splitlines(), html.splitlines(), fromfile='snapshot', tofile='current', lineterm=''))
                self.fail(f"HTML výstup login se změnil oproti snapshotu!\nDiff:\n{diff}")
        except FileNotFoundError:
            with open(snapshot_path, 'w', encoding='utf-8') as f:
                f.write(html)
            # První běh: snapshot vytvořen
            pass

class HomeUITestCase(TestCase):
    """
    Testuje renderování a snapshot domovské stránky (home.html).
    """
    def setUp(self):
        from django.contrib.auth.models import User
        from klienti.models import UserProfile
        self.user = User.objects.create_user(username='hometest', password='testpass')
        profile = UserProfile.objects.get(user=self.user)
        profile.role = 'klient'
        profile.save()
        self.client = Client()
        self.client.login(username='hometest', password='testpass')

    def test_home_snapshot(self):
        """
        Snapshot test: uloží HTML výstup domovské stránky a porovná s referenčním snapshotem.
        """
        from django.urls import reverse
        import re, difflib
        response = self.client.get(reverse('home'))
        html = response.content.decode('utf-8')
        # Nahradíme případná dynamická data (např. CSRF token, datumy) zástupným textem
        html = re.sub(r'value="[0-9a-f]{{32,}}"', 'value="__TOKEN__"', html)
        html = re.sub(r'\d{2}\.\d{2}\.\d{4}', '__DATUM__', html)
        snapshot_path = 'home_snapshot.html'
        try:
            with open(snapshot_path, 'r', encoding='utf-8') as f:
                snapshot = f.read()
            if html != snapshot:
                diff = '\n'.join(difflib.unified_diff(snapshot.splitlines(), html.splitlines(), fromfile='snapshot', tofile='current', lineterm=''))
                self.fail(f"HTML výstup home se změnil oproti snapshotu!\nDiff:\n{diff}")
        except FileNotFoundError:
            with open(snapshot_path, 'w', encoding='utf-8') as f:
                f.write(html)
            # První běh: snapshot vytvořen
            pass

class KlientConfirmDeleteUITestCase(TestCase):
    """
    Testuje renderování a snapshot potvrzovací stránky smazání klienta (klient_confirm_delete.html).
    """
    def setUp(self):
        from django.contrib.auth.models import User
        from klienti.models import UserProfile, Klient
        self.user = User.objects.create_user(username='deleteuser', password='testpass')
        profile = UserProfile.objects.get(user=self.user)
        profile.role = 'poradce'
        profile.save()
        self.client = Client()
        self.client.login(username='deleteuser', password='testpass')
        self.klient = Klient.objects.create(jmeno='Smazat Test', datum='2025-05-27', user=self.user)

    def test_klient_confirm_delete_snapshot(self):
        """
        Snapshot test: uloží HTML výstup potvrzovací stránky smazání klienta a porovná s referenčním snapshotem.
        """
        from django.urls import reverse
        import re, difflib
        response = self.client.get(reverse('klient_delete', args=[self.klient.pk]))
        html = response.content.decode('utf-8')
        # Nahradíme dynamická data (ID klienta v URL, CSRF token) zástupným textem
        html = re.sub(r'/klient/\d+/', '/klient/__ID__/', html)
        html = re.sub(r'value="[0-9a-f]{{32,}}"', 'value="__TOKEN__"', html)
        snapshot_path = 'klient_confirm_delete_snapshot.html'
        try:
            with open(snapshot_path, 'r', encoding='utf-8') as f:
                snapshot = f.read()
            if html != snapshot:
                diff = '\n'.join(difflib.unified_diff(snapshot.splitlines(), html.splitlines(), fromfile='snapshot', tofile='current', lineterm=''))
                self.fail(f"HTML výstup klient_confirm_delete se změnil oproti snapshotu!\nDiff:\n{diff}")
        except FileNotFoundError:
            with open(snapshot_path, 'w', encoding='utf-8') as f:
                f.write(html)
            # První běh: snapshot vytvořen
            pass
