from datetime import date

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils import timezone

from klienti.models import Klient, NotifikaceLog
from klienti.utils import odeslat_notifikaci_email


class Command(BaseCommand):
    help = "Odešle e-mailové notifikace poradcům o blížících se deadlinách (do 3 dnů)"

    def handle(self, *args, **options):
        today = date.today()
        poradci = User.objects.filter(userprofile__role="poradce")
        deadline_fields = [
            "deadline_co_financuje",
            "deadline_navrh_financovani",
            "deadline_vyber_banky",
            "deadline_priprava_zadosti",
            "deadline_kompletace_podkladu",
            "deadline_podani_zadosti",
            "deadline_odhad",
            "deadline_schvalovani",
            "deadline_priprava_uverove_dokumentace",
            "deadline_podpis_uverove_dokumentace",
            "deadline_priprava_cerpani",
            "deadline_cerpani",
            "deadline_zahajeni_splaceni",
            "deadline_podminky_pro_splaceni",
        ]
        klienti = Klient.objects.all()
        urgent_deadlines = []
        for k in klienti:
            for field in deadline_fields:
                deadline = getattr(k, field)
                splneno = getattr(k, field.replace("deadline_", "splneno_"), None)
                if deadline and not splneno:
                    if (deadline - today).days <= 3 and (deadline - today).days >= 0:
                        urgent_deadlines.append(
                            {
                                "klient": k,
                                "krok": field,
                                "deadline": deadline,
                                "days_left": (deadline - today).days,
                            }
                        )
        for poradce in poradci:
            if poradce.email:
                for ud in urgent_deadlines:
                    existuje = NotifikaceLog.objects.filter(
                        prijemce=poradce.email,
                        typ="deadline",
                        klient=ud["klient"],
                        datum__date=timezone.now().date(),
                    ).exists()
                    if not existuje:
                        predmet = "Upozornění: Blíží se deadline u klientů"
                        zprava = f"Dobrý den,\n\nU klienta {ud['klient'].jmeno} se blíží deadline ({ud['krok'].replace('deadline_', '').replace('_', ' ').title()}): {ud['deadline'].strftime('%d.%m.%Y')}\n\nPřihlaste se do systému pro detailní informace.\n\nTým hypoteční aplikace"
                        try:
                            odeslat_notifikaci_email(
                                prijemce=poradce.email,
                                predmet=predmet,
                                zprava=zprava,
                                context={"urgent_klienti": [ud]},
                                template_name="email_deadline_notifikace.html",
                                typ="deadline",
                                klient=ud["klient"],
                            )
                        except Exception as e:
                            self.stdout.write(
                                self.style.ERROR(f"Chyba při odesílání e-mailu: {e}")
                            )
        self.stdout.write(self.style.SUCCESS("Notifikace odeslány."))
