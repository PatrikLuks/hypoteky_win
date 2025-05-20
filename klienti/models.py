from django.db import models
from django.utils import timezone

# Create your models here.

class Klient(models.Model):
    jmeno = models.CharField(max_length=100)
    datum = models.DateField(default=timezone.now)
    co_financuje = models.CharField(max_length=255, blank=True)
    cena = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    navrh_financovani = models.CharField(max_length=255, blank=True)
    navrh_financovani_castka = models.DecimalField("Návrh financování částka", max_digits=12, decimal_places=2, blank=True, null=True)
    navrh_financovani_procento = models.DecimalField("Návrh financování v %", max_digits=5, decimal_places=2, blank=True, null=True)
    vyber_banky = models.CharField(max_length=255, blank=True)
    priprava_zadosti = models.CharField(max_length=255, blank=True)
    kompletace_podkladu = models.CharField(max_length=255, blank=True)
    podani_zadosti = models.CharField(max_length=255, blank=True)
    odhad = models.CharField(max_length=255, blank=True)
    schvalovani = models.CharField(max_length=255, blank=True)
    priprava_uverove_dokumentace = models.CharField(max_length=255, blank=True)
    podpis_uverove_dokumentace = models.CharField(max_length=255, blank=True)
    priprava_cerpani = models.CharField(max_length=255, blank=True)
    cerpani = models.CharField(max_length=255, blank=True)
    zahajeni_splaceni = models.CharField(max_length=255, blank=True)
    podminky_pro_splaceni = models.CharField(max_length=255, blank=True)
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
