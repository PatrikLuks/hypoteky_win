from django.db import models
from django.utils import timezone
from django.conf import settings
from encrypted_model_fields.fields import EncryptedCharField, EncryptedTextField

# Signály pro automatické vytváření a aktualizaci UserProfile
try:
    from django.db.models.signals import post_save
    from django.dispatch import receiver
except ImportError:
    post_save = None
    receiver = None

if post_save:
    @receiver(post_save, sender='auth.User')
    def create_or_update_user_profile(sender, instance, created, **kwargs):
        from .models import UserProfile
        if created:
            UserProfile.objects.create(user=instance)
        else:
            try:
                # Nepřepisuj existující profil, pouze ulož
                if hasattr(instance, 'userprofile'):
                    instance.userprofile.save()
                else:
                    UserProfile.objects.create(user=instance)
            except Exception:
                pass  # Pokud profil neexistuje, nevytvářej nový s výchozí rolí

# Create your models here.

class Klient(models.Model):
    jmeno = EncryptedCharField(max_length=100)
    jmeno_index = models.CharField(max_length=100, db_index=True, blank=True)  # Pomocné pole pro rychlé vyhledávání podle jména
    datum = models.DateField(default=timezone.now)
    co_financuje = EncryptedCharField(max_length=255, blank=True)
    cena = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    navrh_financovani = models.CharField(max_length=255, blank=True)
    navrh_financovani_castka = models.DecimalField("Návrh financování částka", max_digits=12, decimal_places=2, blank=True, null=True)
    navrh_financovani_procento = models.DecimalField("Návrh financování v %", max_digits=5, decimal_places=2, blank=True, null=True)
    vyber_banky = models.CharField(max_length=255, blank=True)
    duvod_zamitnuti = EncryptedCharField("Důvod zamítnutí", max_length=255, blank=True, null=True, help_text="Vyplňte pouze v případě zamítnuté hypotéky")
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
    user = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='klienti', help_text='Uživatel (klient), který má přístup ke svému záznamu')

    class Meta:
        pass  # odstraněn unikátní constraint, řeší se na úrovni importu

    def save(self, *args, **kwargs):
        # Synchronizace indexu pro vyhledávání
        self.jmeno_index = self.jmeno
        super().save(*args, **kwargs)

class HypotekaWorkflow(models.Model):
    klient = models.ForeignKey(Klient, on_delete=models.CASCADE, related_name='workflowy')
    krok = models.PositiveSmallIntegerField(choices=[
        (1, 'Jméno klienta'),
        (2, 'Co chce klient financovat'),
        (3, 'Návrh financování'),
        (4, 'Výběr banky'),
        (5, 'Příprava žádosti'),
        (6, 'Kompletace podkladů'),
        (7, 'Podání žádosti'),
        (8, 'Odhad'),
        (9, 'Schvalování'),
        (10, 'Příprava úvěrové dokumentace'),
        (11, 'Podpis úvěrové dokumentace'),
        (12, 'Příprava čerpání'),
        (13, 'Čerpání'),
        (14, 'Zahájení splácení'),
        (15, 'Podmínky pro vyčerpání'),
    ])
    datum = models.DateTimeField(auto_now_add=True)
    poznamka = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Krok workflow hypotéky'
        verbose_name_plural = 'Kroky workflow hypotéky'
        ordering = ['krok', 'datum']

    def __str__(self):
        return f"{self.klient.jmeno} – {self.get_krok_display()}"

class Poznamka(models.Model):
    klient = models.ForeignKey(Klient, on_delete=models.CASCADE, related_name='poznamky')
    text = EncryptedTextField()
    created = models.DateTimeField(auto_now_add=True)
    author = models.CharField(max_length=100, blank=True)  # nebo ForeignKey na User, pokud budeš chtít

    def __str__(self):
        return f"Poznámka ke klientovi {self.klient.jmeno} ({self.created:%d.%m.%Y %H:%M})"

class Zmena(models.Model):
    klient = models.ForeignKey(Klient, on_delete=models.CASCADE, related_name='zmeny')
    popis = EncryptedTextField()
    created = models.DateTimeField(auto_now_add=True)
    author = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"Změna u {self.klient.jmeno} ({self.created:%d.%m.%Y %H:%M})"

class UserProfile(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    ROLE_CHOICES = (
        ('poradce', 'Finanční poradce'),
        ('klient', 'Klient'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='klient')

    def save(self, *args, **kwargs):
        # Pokud je role již nastavena explicitně, neresetuj ji!
        if self.pk is not None and self.role:
            pass  # role již nastavena, neměň
        elif hasattr(self.user, 'groups') and self.user.groups.filter(name='jplservis').exists():
            self.role = 'poradce'
        else:
            self.role = 'klient'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"

class NotifikaceLog(models.Model):
    NOTIF_TYPE_CHOICES = (
        ('deadline', 'Blížící se deadline'),
        ('stav', 'Změna stavu'),
        ('zamítnutí', 'Zamítnutí hypotéky'),
    )
    prijemce = models.EmailField()
    typ = models.CharField(max_length=30, choices=NOTIF_TYPE_CHOICES)
    klient = models.ForeignKey(Klient, on_delete=models.SET_NULL, null=True, blank=True)
    datum = models.DateTimeField(auto_now_add=True)
    obsah = models.TextField(blank=True)
    uspesne = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.get_typ_display()} – {self.prijemce} ({self.datum:%d.%m.%Y %H:%M})"
