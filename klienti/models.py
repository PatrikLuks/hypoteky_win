# -*- coding: utf-8 -*-
import unicodedata

from django.db import models
from django.utils import timezone

from encrypted_model_fields.fields import EncryptedCharField, EncryptedTextField

# Signály pro automatické vytváření a aktualizaci UserProfile
try:
    from django.db.models.signals import post_save
    from django.dispatch import receiver
except ImportError:
    post_save = None
    receiver = None

if post_save:

    @receiver(post_save, sender="auth.User")
    def create_or_update_user_profile(sender, instance, created, **kwargs):
        from .models import UserProfile

        if created:
            UserProfile.objects.create(user=instance)
        else:
            try:
                # Vždy aktualizuj roli podle skupin při každém uložení uživatele
                if hasattr(instance, "userprofile"):
                    profile = instance.userprofile
                    if (
                        hasattr(instance, "groups")
                        and instance.groups.filter(name="jplservis").exists()
                    ):
                        profile.role = "poradce"
                    else:
                        profile.role = "klient"
                    profile.save()
                else:
                    UserProfile.objects.create(user=instance)
            except Exception:
                pass  # Pokud profil neexistuje, nevytvářej nový s výchozí rolí


# Create your models here.


class Klient(models.Model):
    jmeno = EncryptedCharField(max_length=100)
    jmeno_index = models.CharField(
        max_length=100, db_index=True, blank=True
    )  # Pomocné pole pro rychlé vyhledávání podle jména
    datum = models.DateField(default=timezone.now)
    co_financuje = EncryptedCharField(max_length=255, blank=True)
    cena = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    navrh_financovani = models.CharField(max_length=255, blank=True)
    navrh_financovani_castka = models.DecimalField(
        "Návrh financování částka",
        max_digits=12,
        decimal_places=2,
        blank=True,
        null=True,
    )
    vlastni_zdroj = models.DecimalField(
        "Vlastní zdroj",
        max_digits=12,
        decimal_places=2,
        blank=True,
        null=True,
    )
    navrh_financovani_procento = models.DecimalField(
        "Návrh financování v %", max_digits=5, decimal_places=2, blank=True, null=True
    )
    vyber_banky = models.CharField(max_length=255, blank=True)
    schvalene_financovani = models.CharField(
        "Schválené financování",
        max_length=255,
        blank=True,
        help_text="Schválené parametry hypotéky po schválení",
    )
    schvalena_hypoteka_castka = models.DecimalField(
        "Schválená výše hypotéky",
        max_digits=12,
        decimal_places=2,
        blank=True,
        null=True,
    )
    schvaleny_vlastni_zdroj = models.DecimalField(
        "Schválený vlastní zdroj",
        max_digits=12,
        decimal_places=2,
        blank=True,
        null=True,
    )
    schvaleny_ltv_procento = models.DecimalField(
        "Schválené LTV (%)",
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
    )
    duvod_zamitnuti = EncryptedCharField(
        "Důvod zamítnutí",
        max_length=255,
        blank=True,
        null=True,
        help_text="Vyplňte pouze v případě zamítnuté hypotéky",
    )
    priprava_zadosti = EncryptedTextField(blank=True, default="")
    kompletace_podkladu = EncryptedTextField(blank=True, default="")
    podani_zadosti = EncryptedTextField(blank=True, default="")
    odhad = EncryptedTextField(blank=True, default="")
    schvalovani = EncryptedTextField(blank=True, default="")
    priprava_uverove_dokumentace = EncryptedTextField(blank=True, default="")
    podpis_uverove_dokumentace = EncryptedTextField(blank=True, default="")
    priprava_cerpani = EncryptedTextField(blank=True, default="")
    cerpani = EncryptedTextField(blank=True, default="")
    zahajeni_splaceni = EncryptedTextField(blank=True, default="")
    podminky_pro_splaceni = EncryptedTextField(blank=True, default="")
    deadline_co_financuje = models.DateField(blank=True, null=True)
    deadline_navrh_financovani = models.DateField(blank=True, null=True)
    deadline_vyber_banky = models.DateField(blank=True, null=True)
    deadline_schvalene_financovani = models.DateField(blank=True, null=True)
    deadline_priprava_zadosti = models.DateField(blank=True, null=True)
    deadline_kompletace_podkladu = models.DateField(blank=True, null=True)
    deadline_podani_zadosti = models.DateField(blank=True, null=True)
    deadline_odhad = models.DateField(blank=True, null=True)
    deadline_schvalovani = models.DateField(blank=True, null=True)
    deadline_priprava_uverove_dokumentace = models.DateField(blank=True, null=True)
    deadline_podpis_uverove_dokumentace = models.DateField(blank=True, null=True)
    deadline_priprava_cerpani = models.DateField(blank=True, null=True)
    deadline_cerpani = models.DateField(blank=True, null=True)
    deadline_zahajeni_splaceni = models.DateField(blank=True, null=True)
    deadline_podminky_pro_splaceni = models.DateField(blank=True, null=True)
    splneno_co_financuje = models.DateField(blank=True, null=True)
    splneno_navrh_financovani = models.DateField(blank=True, null=True)
    splneno_vyber_banky = models.DateField(blank=True, null=True)
    splneno_schvalene_financovani = models.DateField(blank=True, null=True)
    splneno_priprava_zadosti = models.DateField(blank=True, null=True)
    splneno_kompletace_podkladu = models.DateField(blank=True, null=True)
    splneno_podani_zadosti = models.DateField(blank=True, null=True)
    splneno_odhad = models.DateField(blank=True, null=True)
    splneno_schvalovani = models.DateField(blank=True, null=True)
    splneno_priprava_uverove_dokumentace = models.DateField(blank=True, null=True)
    splneno_podpis_uverove_dokumentace = models.DateField(blank=True, null=True)
    splneno_priprava_cerpani = models.DateField(blank=True, null=True)
    splneno_cerpani = models.DateField(blank=True, null=True)
    splneno_zahajeni_splaceni = models.DateField(blank=True, null=True)
    splneno_podminky_pro_splaceni = models.DateField(blank=True, null=True)
    email = models.EmailField(
        "E-mail klienta",
        max_length=255,
        blank=True,
        help_text="E-mailová adresa pro odeslání přihlašovacích údajů",
    )
    user = models.ForeignKey(
        "auth.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="klienti",
        help_text="Uživatel (klient), který má přístup ke svému záznamu",
    )

    class Meta:
        pass  # odstraněn unikátní constraint, řeší se na úrovni importu

    def save(self, *args, **kwargs):
        # Před uložením si načti původní hodnoty pro audit/notifikace
        prev = None
        prev_duvod = None
        is_new_user = False  # Flag pro sledování nově vytvořeného uživatele
        new_user_email = None  # Email pro welcome email
        new_user_username = None  # Username pro welcome email
        
        splneno_fields = [
            "splneno_co_financuje",
            "splneno_navrh_financovani",
            "splneno_vyber_banky",
            "splneno_schvalene_financovani",
            "splneno_priprava_zadosti",
            "splneno_kompletace_podkladu",
            "splneno_podani_zadosti",
            "splneno_odhad",
            "splneno_schvalovani",
            "splneno_priprava_uverove_dokumentace",
            "splneno_podpis_uverove_dokumentace",
            "splneno_priprava_cerpani",
            "splneno_cerpani",
            "splneno_zahajeni_splaceni",
            "splneno_podminky_pro_splaceni",
        ]
        prev_splneno = {}
        if self.pk:
            try:
                prev = Klient.objects.get(pk=self.pk)
                prev_duvod = prev.duvod_zamitnuti
                prev_splneno = {f: getattr(prev, f) for f in splneno_fields}
            except Klient.DoesNotExist:
                prev = None
        self.jmeno_index = self.jmeno
        if not self.user:
            from django.contrib.auth.models import User
            from django.core.exceptions import ValidationError

            existing_user = None  # Inicializace proměnné
            username = None  # Inicializace proměnné
            
            # Pro klienty používáme email jako username (pokud je k dispozici)
            # Jinak generujeme z jména jako fallback
            if hasattr(self, "email") and self.email:
                # Zkontroluj zda email už není použit
                existing_user = User.objects.filter(username=self.email).first()
                
                if existing_user:
                    # Email již existuje jako username
                    # Zkontroluj zda má přiřazeného klienta (kromě aktuální instance)
                    existing_klienti = self.__class__.objects.filter(user=existing_user)
                    # Pokud se edituje existující klient, vyfiltruj ho
                    if self.pk:
                        existing_klienti = existing_klienti.exclude(pk=self.pk)
                    
                    if existing_klienti.exists():
                        raise ValidationError(
                            f"Email {self.email} je již používán jiným klientem. "
                            "Každý email může být použit pouze jednou."
                        )
                    else:
                        # User existuje, ale nemá klienta - můžeme ho použít
                        self.user = existing_user
                        # Aktualizuj jméno
                        existing_user.first_name = self.jmeno
                        existing_user.email = self.email
                        existing_user.save()
                        import logging
                        logger = logging.getLogger("klienti.models")
                        logger.info(f"Použit existující uživatel {self.email} pro nového klienta {self.jmeno}")
                else:
                    # Email je volný - vytvoř nového uživatele
                    username = self.email
            else:
                # Fallback - normalizuj jméno pokud není email
                def normalize_username(name):
                    name = (
                        unicodedata.normalize("NFKD", name)
                        .encode("ascii", "ignore")
                        .decode("ascii")
                    )
                    return "".join(
                        c for c in name.lower().replace(" ", "_") if c.isalnum() or c == "_"
                    )
                base_username = normalize_username(self.jmeno)
                username = base_username
                i = 1
                while User.objects.filter(username=username).exists():
                    username = f"{base_username}{i}"
                    i += 1
            
            # Vytvoř nového uživatele pouze pokud self.user nebyl nastaven výše
            if not self.user:
                # Generování bezpečného náhodného hesla
                import secrets
                import string
                alphabet = string.ascii_letters + string.digits + string.punctuation
                temp_password = ''.join(secrets.choice(alphabet) for _ in range(16))
                user = User.objects.create_user(username=username, password=temp_password)
                user.first_name = self.jmeno
                if hasattr(self, "email") and self.email:
                    user.email = self.email
                user.save()
                self.user = user
            # Bezpečnostní logování bez hesla
            import logging
            logger = logging.getLogger('klienti')
            # Loguj pouze pokud byl vytvořen nový uživatel (ne při znovupoužití)
            if self.user and not existing_user:
                logger.info(f"Vytvořen uživatel: {self.user.username} pro klienta {self.jmeno}")
            
            # Welcome email posíláme vždy pro nového klienta
            # (i když se znovupoužil existující User po smazání předchozího klienta)
            is_new_user = True
            new_user_email = self.user.email if self.user else None
            new_user_username = self.user.username if self.user else None
        
        # DŮLEŽITÉ: Nejdřív ulož Klient objekt do DB, pak teprve posílej email
        super().save(*args, **kwargs)
        
        # Odeslání welcome emailu AŽ PO uložení do DB (pouze pro nově vytvořené uživatele)
        if is_new_user and new_user_email:
            try:
                from django.contrib.auth.tokens import default_token_generator
                from django.utils.http import urlsafe_base64_encode
                from django.utils.encoding import force_bytes
                from django.template import loader
                from django.core.mail import send_mail
                from django.conf import settings
                import logging
                logger = logging.getLogger('klienti')
                
                # Znovu načti uživatele z DB pro jistotu, že má správné heslo v DB
                from django.contrib.auth.models import User
                user = User.objects.get(pk=self.user.pk)
                
                # Vygeneruj token
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                
                # Určení domény
                if settings.DEBUG:
                    domain = 'localhost:8000'
                else:
                    domain = settings.ALLOWED_HOSTS[0] if settings.ALLOWED_HOSTS else 'localhost'
                
                # Načti šablony
                subject = loader.render_to_string('registration/welcome_subject.txt').strip()
                message = loader.render_to_string(
                    'registration/welcome_email.html',
                    {
                        'username': new_user_username,
                        'uid': uid,
                        'token': token,
                        'protocol': 'https' if settings.SECURE_SSL_REDIRECT else 'http',
                        'domain': domain,
                        'user': user,
                    }
                )
                
                # Odešli email
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [new_user_email],
                    fail_silently=False,
                )
                logger.info(f"Welcome email odeslán na {new_user_email} pro uživatele {new_user_username}")
            except Exception as e:
                logger.error(f"Chyba při odesílání welcome emailu: {str(e)}")
        
        # --- Notifikace po uložení ---
        try:
            from django.contrib.auth.models import User
            from .utils import odeslat_notifikaci_email
        except Exception:
            odeslat_notifikaci_email = None
        if odeslat_notifikaci_email:
            poradci_qs = User.objects.filter(userprofile__role="poradce").exclude(email="")
            poradci_emails = [u.email for u in poradci_qs if u.email]
            klient_email = self.user.email if self.user and self.user.email else None
            # Zamítnutí hypotéky – nově vyplněný důvod
            if self.duvod_zamitnuti and (self.duvod_zamitnuti != (prev_duvod or "")):
                predmet = "Zamítnutí hypotéky"
                zprava = (
                    f"U klienta {self.jmeno} byl zadán důvod zamítnutí: {self.duvod_zamitnuti}.\n"
                    "Přihlaste se do systému pro detailní informace."
                )
                for prijemce in poradci_emails:
                    odeslat_notifikaci_email(
                        prijemce=prijemce,
                        predmet=predmet,
                        zprava=zprava,
                        typ="zamítnutí",
                        klient=self,
                    )
                if klient_email:
                    odeslat_notifikaci_email(
                        prijemce=klient_email,
                        predmet=predmet,
                        zprava=zprava,
                        typ="zamítnutí",
                        klient=self,
                    )
            # Změna stavu – nový splněný krok
            changed_kroky = [
                f
                for f in splneno_fields
                if getattr(self, f) is not None and not prev_splneno.get(f)
            ]
            if changed_kroky:
                label_map = {
                    "splneno_co_financuje": "Co chce klient financovat",
                    "splneno_navrh_financovani": "Návrh financování",
                    "splneno_vyber_banky": "Výběr banky",
                    "splneno_schvalene_financovani": "Schválené financování",
                    "splneno_priprava_zadosti": "Příprava žádosti",
                    "splneno_kompletace_podkladu": "Kompletace podkladů",
                    "splneno_podani_zadosti": "Podání žádosti",
                    "splneno_odhad": "Odhad",
                    "splneno_schvalovani": "Schvalování",
                    "splneno_priprava_uverove_dokumentace": "Příprava úvěrové dokumentace",
                    "splneno_podpis_uverove_dokumentace": "Podpis úvěrové dokumentace",
                    "splneno_priprava_cerpani": "Příprava čerpání",
                    "splneno_cerpani": "Čerpání",
                    "splneno_zahajeni_splaceni": "Zahájení splácení",
                    "splneno_podminky_pro_splaceni": "Podmínky pro splacení",
                }
                kroky_popis = ", ".join(label_map.get(f, f) for f in changed_kroky)
                predmet = "Změna stavu hypotéky"
                zprava = (
                    f"U klienta {self.jmeno} byl označen jako splněný krok/kroky: {kroky_popis}.\n"
                    "Přihlaste se do systému pro detailní informace."
                )
                for prijemce in poradci_emails:
                    odeslat_notifikaci_email(
                        prijemce=prijemce,
                        predmet=predmet,
                        zprava=zprava,
                        typ="stav",
                        klient=self,
                    )
                if klient_email:
                    odeslat_notifikaci_email(
                        prijemce=klient_email,
                        predmet=predmet,
                        zprava=zprava,
                        typ="stav",
                        klient=self,
                    )

    @property
    def is_hotovo(self):
        progress = self.get_workflow_progress
        vse_splneno = all(k["splneno"] for k in progress["kroky"])
        return self.duvod_zamitnuti in (None, "") and vse_splneno

    @property
    def get_workflow_progress(self):
        """
        Vrací průběh workflow na základě polí splneno_... jako slovník:
        {
            'posledni_splneny_krok_index': int or None,
            'posledni_splneny_krok_nazev': str or None,
            'prvni_nesplneny_krok_index': int or None,
            'prvni_nesplneny_krok_nazev': str or None,
            'procenta_dokonceni': float, # procento dokončení (0-100)
            'kroky': [
                {'nazev': str, 'splneno': bool, 'datum': date or None},
                ...
            ]
        }
        """
        workflow_kroky = [
            ("Co chce klient financovat", self.splneno_co_financuje),
            ("Návrh financování", self.splneno_navrh_financovani),
            ("Výběr banky", self.splneno_vyber_banky),
            ("Schválené financování", self.splneno_schvalene_financovani),
            ("Příprava žádosti", self.splneno_priprava_zadosti),
            ("Kompletace podkladů", self.splneno_kompletace_podkladu),
            ("Podání žádosti", self.splneno_podani_zadosti),
            ("Odhad", self.splneno_odhad),
            ("Schvalování", self.splneno_schvalovani),
            ("Příprava úvěrové dokumentace", self.splneno_priprava_uverove_dokumentace),
            ("Podpis úvěrové dokumentace", self.splneno_podpis_uverove_dokumentace),
            ("Příprava čerpání", self.splneno_priprava_cerpani),
            ("Čerpání", self.splneno_cerpani),
            ("Zahájení splácení", self.splneno_zahajeni_splaceni),
            ("Podmínky pro splacení", self.splneno_podminky_pro_splaceni),
        ]
        kroky = []
        posledni_splneny_krok_index = None
        prvni_nesplneny_krok_index = None
        for idx, (nazev, datum) in enumerate(workflow_kroky):
            splneno = datum is not None
            kroky.append({"nazev": nazev, "splneno": splneno, "datum": datum})
            if splneno:
                posledni_splneny_krok_index = idx
            elif prvni_nesplneny_krok_index is None:
                prvni_nesplneny_krok_index = idx
        procenta_dokonceni = (
            100
            * sum(1 for _, d in workflow_kroky if d is not None)
            / len(workflow_kroky)
        )
        return {
            "posledni_splneny_krok_index": posledni_splneny_krok_index,
            "posledni_splneny_krok_nazev": (
                workflow_kroky[posledni_splneny_krok_index][0]
                if posledni_splneny_krok_index is not None
                else None
            ),
            "prvni_nesplneny_krok_index": prvni_nesplneny_krok_index,
            "prvni_nesplneny_krok_nazev": (
                workflow_kroky[prvni_nesplneny_krok_index][0]
                if prvni_nesplneny_krok_index is not None
                else None
            ),
            "procenta_dokonceni": round(procenta_dokonceni, 1),
            "kroky": kroky,
        }

    # Příklad použití v šabloně nebo view:
    # progress = klient.get_workflow_progress
    # progress['aktualni_krok_nazev'], progress['procenta_dokonceni'], ...
    # Pro zobrazení všech kroků a jejich splnění:
    # for krok in progress['kroky']:
    #     print(krok['nazev'], krok['splneno'], krok['datum'])
    # ...


class HypotekaWorkflow(models.Model):
    klient = models.ForeignKey(
        Klient, on_delete=models.CASCADE, related_name="workflowy"
    )
    krok = models.PositiveSmallIntegerField(
        choices=[
            (1, "Co chce klient financovat"),
            (2, "Návrh financování"),
            (3, "Výběr banky"),
            (4, "Schválené financování"),
            (5, "Příprava žádosti"),
            (6, "Kompletace podkladů"),
            (7, "Podání žádosti"),
            (8, "Odhad"),
            (9, "Schvalování"),
            (10, "Příprava úvěrové dokumentace"),
            (11, "Podpis úvěrové dokumentace"),
            (12, "Příprava čerpání"),
            (13, "Čerpání"),
            (14, "Zahájení splácení"),
            (15, "Podmínky pro splacení"),
        ]
    )
    datum = models.DateTimeField(auto_now_add=True)
    poznamka = models.TextField(blank=True)

    class Meta:
        verbose_name = "Krok workflow hypotéky"
        verbose_name_plural = "Kroky workflow hypotéky"
        ordering = ["krok", "datum"]

    def __str__(self):
        return f"{self.klient.jmeno} – {self.get_krok_display()}"


class Poznamka(models.Model):
    klient = models.ForeignKey(
        Klient, on_delete=models.CASCADE, related_name="poznamky"
    )
    text = EncryptedTextField()
    created = models.DateTimeField(auto_now_add=True)
    author = models.CharField(
        max_length=100, blank=True
    )  # nebo ForeignKey na User, pokud budeš chtít

    def __str__(self):
        return (
            f"Poznámka ke klientovi {self.klient.jmeno} ({self.created:%d.%m.%Y %H:%M})"
        )


class Zmena(models.Model):
    klient = models.ForeignKey(Klient, on_delete=models.CASCADE, related_name="zmeny")
    popis = EncryptedTextField()
    created = models.DateTimeField(auto_now_add=True)
    author = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"Změna u {self.klient.jmeno} ({self.created:%d.%m.%Y %H:%M})"


class UserProfile(models.Model):
    user = models.OneToOneField("auth.User", on_delete=models.CASCADE)
    ROLE_CHOICES = (
        ("poradce", "Finanční poradce"),
        ("klient", "Klient"),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="klient")

    def save(self, *args, **kwargs):
        # Pokud je role již nastavena explicitně, neresetuj ji!
        if self.pk is not None and self.role:
            pass  # role již nastavena, neměň
        elif (
            hasattr(self.user, "groups")
            and self.user.groups.filter(name="jplservis").exists()
        ):
            self.role = "poradce"
        else:
            self.role = "klient"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"


class NotifikaceLog(models.Model):
    NOTIF_TYPE_CHOICES = (
        ("deadline", "Blížící se deadline"),
        ("stav", "Změna stavu"),
        ("zamítnutí", "Zamítnutí hypotéky"),
    )
    prijemce = models.EmailField()
    typ = models.CharField(max_length=30, choices=NOTIF_TYPE_CHOICES)
    klient = models.ForeignKey(Klient, on_delete=models.SET_NULL, null=True, blank=True)
    datum = models.DateTimeField(auto_now_add=True)
    obsah = models.TextField(blank=True)
    uspesne = models.BooleanField(default=True)

    def __str__(self):
        return (
            f"{self.get_typ_display()} – {self.prijemce} ({self.datum:%d.%m.%Y %H:%M})"
        )
