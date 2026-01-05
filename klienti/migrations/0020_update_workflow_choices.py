# Generated manually to align workflow steps with documentation (15 steps)
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("klienti", "0019_remove_klient_schvalene_cena"),
    ]

    operations = [
        migrations.AlterField(
            model_name="hypotekaworkflow",
            name="krok",
            field=models.PositiveSmallIntegerField(
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
            ),
        ),
    ]
