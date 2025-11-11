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
    navrh_financovani_procento = models.DecimalField(
        "Návrh financování v %", max_digits=5, decimal_places=2, blank=True, null=True
    )
    vyber_banky = models.CharField(max_length=255, blank=True)
    duvod_zamitnuti = EncryptedCharField(
        "Důvod zamítnutí",
        max_length=255,
        blank=True,
        null=True,
        help_text="Vyplňte pouze v případě zamítnuté hypotéky",
    )
    priprava_zadosti = EncryptedTextField(blank=True)
    kompletace_podkladu = EncryptedTextField(blank=True)
    podani_zadosti = EncryptedTextField(blank=True)
    odhad = EncryptedTextField(blank=True)
    schvalovani = EncryptedTextField(blank=True)
    priprava_uverove_dokumentace = EncryptedTextField(blank=True)
    podpis_uverove_dokumentace = EncryptedTextField(blank=True)
    priprava_cerpani = EncryptedTextField(blank=True)
    cerpani = EncryptedTextField(blank=True)
    zahajeni_splaceni = EncryptedTextField(blank=True)
    podminky_pro_splaceni = EncryptedTextField(blank=True)
    deadline_co_financuje = models.DateField(blank=True, null=True)
    deadline_navrh_financovani = models.DateField(blank=True, null=True)
    deadline_vyber_banky = models.DateField(blank=True, null=True)
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
        self.jmeno_index = self.jmeno
        if not self.user:
            from django.contrib.auth.models import User

            # Odstranění diakritiky a speciálních znaků
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
            temp_password = username
            user = User.objects.create_user(username=username, password=temp_password)
            user.first_name = self.jmeno
            if hasattr(self, "email") and self.email:
                user.email = self.email
            user.save()
            self.user = user
            print(f"[DEBUG] Vytvoren uzivatel: {username} / heslo: {temp_password}")
        super().save(*args, **kwargs)

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
            ("Podmínky pro vyčerpání", self.splneno_podminky_pro_splaceni),
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
            (1, "Jméno klienta"),
            (2, "Co chce klient financovat"),
            (3, "Návrh financování"),
            (4, "Výběr banky"),
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
            (15, "Podmínky pro vyčerpání"),
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
