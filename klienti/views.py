# -*- coding: utf-8 -*-
import logging
from collections import defaultdict
from datetime import date, datetime, timedelta

from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .models import Klient, Poznamka, Zmena
from .utils import odeslat_notifikaci_email

logger = logging.getLogger("klienti.views")


class KlientForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk and self.instance.cena is not None:
            # Zobrazit cenu jako celé číslo (bez .00)
            self.initial["cena"] = int(self.instance.cena)
        # Přidat text-white ke všem deadline polím
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
        for field in deadline_fields:
            if field in self.fields:
                css = self.fields[field].widget.attrs.get("class", "")
                self.fields[field].widget.attrs["class"] = f"{css} text-white".strip()
        # Pole splneno_<krok> se již automaticky nepředvyplňuje, zůstává prázdné
        # Pokud chceš předvyplnit, odkomentuj logiku níže
        # if not self.instance or not self.instance.pk:
        #     workflow = [
        #         'co_financuje', 'navrh_financovani', 'vyber_banky', 'priprava_zadosti',
        #         'kompletace_podkladu', 'podani_zadosti', 'odhad', 'schvalovani',
        #         'priprava_uverove_dokumentace', 'podpis_uverove_dokumentace', 'priprava_cerpani',
        #         'cerpani', 'zahajeni_splaceni', 'podminky_pro_splaceni'
        #     ]
        #     for krok in workflow:
        #         deadline_field = f'deadline_{krok}'
        #         splneno_field = f'splneno_{krok}'
        #         if splneno_field in self.fields and deadline_field in self.fields:
        #             if not self.initial.get(splneno_field):
        #                 deadline_value = self.initial.get(deadline_field)
        #                 if deadline_value:
        #                     self.initial[splneno_field] = deadline_value

    class Meta:
        model = Klient
        fields = [
            "jmeno",
            "datum",
            "co_financuje",
            "cena",
            "deadline_co_financuje",
            "splneno_co_financuje",
            "navrh_financovani",
            "navrh_financovani_castka",
            "vlastni_zdroj",
            "navrh_financovani_procento",
            "deadline_navrh_financovani",
            "splneno_navrh_financovani",
            "vyber_banky",
            "deadline_vyber_banky",
            "splneno_vyber_banky",
            "schvalene_financovani",
            "schvalena_hypoetka_castka",
            "schvaleny_vlastni_zdroj",
            "schvaleny_ltv_procento",
            "deadline_schvalene_financovani",
            "splneno_schvalene_financovani",
            "priprava_zadosti",
            "deadline_priprava_zadosti",
            "splneno_priprava_zadosti",
            "kompletace_podkladu",
            "deadline_kompletace_podkladu",
            "splneno_kompletace_podkladu",
            "podani_zadosti",
            "deadline_podani_zadosti",
            "splneno_podani_zadosti",
            "odhad",
            "deadline_odhad",
            "splneno_odhad",
            "schvalovani",
            "deadline_schvalovani",
            "splneno_schvalovani",
            "priprava_uverove_dokumentace",
            "deadline_priprava_uverove_dokumentace",
            "splneno_priprava_uverove_dokumentace",
            "podpis_uverove_dokumentace",
            "deadline_podpis_uverove_dokumentace",
            "splneno_podpis_uverove_dokumentace",
            "priprava_cerpani",
            "deadline_priprava_cerpani",
            "splneno_priprava_cerpani",
            "cerpani",
            "deadline_cerpani",
            "splneno_cerpani",
            "zahajeni_splaceni",
            "deadline_zahajeni_splaceni",
            "splneno_zahajeni_splaceni",
            "podminky_pro_splaceni",
            "deadline_podminky_pro_splaceni",
            "splneno_podminky_pro_splaceni",
            "duvod_zamitnuti",
        ]
        widgets = {
            "jmeno": forms.TextInput(
                attrs={"class": "form-control"}
            ),  # přidáno pro správné barvy
            "datum": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "cena": forms.TextInput(
                attrs={
                    "inputmode": "numeric",
                    "pattern": "[0-9 ]*",
                    "placeholder": "např. 12 200 000",
                    "class": "form-control",
                }
            ),
            "navrh_financovani_castka": forms.NumberInput(
                attrs={
                    "step": "0.01",
                    "min": "0",
                    "placeholder": "Výpočet: cena - vlastní zdroj",
                    "class": "form-control",
                }
            ),
            "vlastni_zdroj": forms.NumberInput(
                attrs={
                    "step": "0.01",
                    "min": "0",
                    "placeholder": "Výpočet: cena - hypotéka",
                    "class": "form-control",
                    "readonly": True,
                }
            ),
            "navrh_financovani_procento": forms.NumberInput(
                attrs={
                    "step": "0.01",
                    "min": "0",
                    "max": "100",
                    "placeholder": "LTV: (hypotéka/cena)*100",
                    "class": "form-control",
                    "readonly": True,
                }
            ),
            "co_financuje": forms.TextInput(attrs={"class": "form-control"}),
            "navrh_financovani": forms.TextInput(attrs={"class": "form-control"}),
            "vyber_banky": forms.TextInput(attrs={"class": "form-control"}),
            "schvalene_financovani": forms.TextInput(attrs={"class": "form-control"}),
            "schvalena_hypoetka_castka": forms.NumberInput(
                attrs={
                    "step": "0.01",
                    "min": "0",
                    "placeholder": "Schválená výše hypotéky",
                    "class": "form-control",
                }
            ),
            "schvaleny_vlastni_zdroj": forms.NumberInput(
                attrs={
                    "step": "0.01",
                    "min": "0",
                    "placeholder": "Výpočet: cena - hypotéka",
                    "class": "form-control",
                    "readonly": True,
                }
            ),
            "schvaleny_ltv_procento": forms.NumberInput(
                attrs={
                    "step": "0.01",
                    "min": "0",
                    "max": "100",
                    "placeholder": "LTV: (hypotéka/cena)*100",
                    "class": "form-control",
                    "readonly": True,
                }
            ),
            "priprava_zadosti": forms.Textarea(
                attrs={"class": "form-control", "rows": 2, "placeholder": "poznámka"}
            ),
            "kompletace_podkladu": forms.Textarea(
                attrs={"class": "form-control", "rows": 2, "placeholder": "poznámka"}
            ),
            "podani_zadosti": forms.Textarea(
                attrs={"class": "form-control", "rows": 2, "placeholder": "poznámka"}
            ),
            "odhad": forms.Textarea(
                attrs={"class": "form-control", "rows": 2, "placeholder": "poznámka"}
            ),
            "schvalovani": forms.Textarea(
                attrs={"class": "form-control", "rows": 2, "placeholder": "poznámka"}
            ),
            "priprava_uverove_dokumentace": forms.Textarea(
                attrs={"class": "form-control", "rows": 2, "placeholder": "poznámka"}
            ),
            "podpis_uverove_dokumentace": forms.Textarea(
                attrs={"class": "form-control", "rows": 2, "placeholder": "poznámka"}
            ),
            "priprava_cerpani": forms.Textarea(
                attrs={"class": "form-control", "rows": 2, "placeholder": "poznámka"}
            ),
            "cerpani": forms.Textarea(
                attrs={"class": "form-control", "rows": 2, "placeholder": "poznámka"}
            ),
            "zahajeni_splaceni": forms.Textarea(
                attrs={"class": "form-control", "rows": 2, "placeholder": "poznámka"}
            ),
            "podminky_pro_splaceni": forms.Textarea(
                attrs={"class": "form-control", "rows": 2, "placeholder": "poznámka"}
            ),
            "deadline_co_financuje": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "deadline_navrh_financovani": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "deadline_vyber_banky": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "deadline_schvalene_financovani": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "deadline_priprava_zadosti": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "deadline_kompletace_podkladu": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "deadline_podani_zadosti": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "deadline_odhad": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "deadline_schvalovani": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "deadline_priprava_uverove_dokumentace": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "deadline_podpis_uverove_dokumentace": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "deadline_priprava_cerpani": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "deadline_cerpani": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "deadline_zahajeni_splaceni": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "deadline_podminky_pro_splaceni": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "splneno_co_financuje": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "splneno_navrh_financovani": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "splneno_vyber_banky": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "splneno_schvalene_financovani": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "splneno_priprava_zadosti": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "splneno_kompletace_podkladu": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "splneno_podani_zadosti": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "splneno_odhad": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "splneno_schvalovani": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "splneno_priprava_uverove_dokumentace": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "splneno_podpis_uverove_dokumentace": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "splneno_priprava_cerpani": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "splneno_cerpani": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "splneno_zahajeni_splaceni": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "splneno_podminky_pro_splaceni": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "duvod_zamitnuti": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 2,
                    "placeholder": "Např. nedostatečný příjem, špatná bonita, chybějící dokumenty...",
                }
            ),
        }

    def clean_cena(self):
        data = self.cleaned_data["cena"]
        if data in (None, ""):
            return None
        if isinstance(data, str):
            data = data.replace(" ", "").replace("\xa0", "").replace(",", ".")
        try:
            return float(data)
        except Exception:
            raise forms.ValidationError(
                "Zadejte částku ve správném formátu, např. 12 200 000"
            )

    def clean(self):
        cleaned_data = super().clean()
        # Definice pořadí workflow kroků podle zadání
        workflow_fields = [
            "co_financuje",
            "navrh_financovani",
            "vyber_banky",
            "schvalene_financovani",
            "priprava_zadosti",
            "kompletace_podkladu",
            "podani_zadosti",
            "odhad",
            "schvalovani",
            "priprava_uverove_dokumentace",
            "podpis_uverove_dokumentace",
            "priprava_cerpani",
            "cerpani",
            "zahajeni_splaceni",
            "podminky_pro_splaceni",
        ]
        # Pro každý krok ověř, že předchozí je vyplněn
        for idx, field in enumerate(workflow_fields[1:], start=1):
            prev_field = workflow_fields[idx - 1]
            if cleaned_data.get(field) and not cleaned_data.get(prev_field):
                self.add_error(
                    field,
                    f'Nelze vyplnit krok "{field}", dokud není vyplněn předchozí krok.',
                )
        return cleaned_data


@login_required
def klient_create(request):
    if request.method == "POST":
        klient_form = KlientForm(request.POST)
        if klient_form.is_valid():
            klient = klient_form.save(commit=False)
            # Výpočet částky hypotečního úvěru
            cena = klient_form.cleaned_data.get("cena")
            procento = klient_form.cleaned_data.get("navrh_financovani_procento")
            if cena and procento:
                klient.navrh_financovani_castka = round(
                    float(cena) * float(procento) / 100, 2
                )
            else:
                klient.navrh_financovani_castka = None
            # Nastavení pole user pouze pokud je role klient
            try:
                profile = request.user.userprofile
                if profile.role == "klient":
                    klient.user = request.user
                else:
                    klient.user = None
            except Exception:
                klient.user = None
            # Nastavení deadline podle zadaného data
            zadane_datum = klient_form.cleaned_data.get("datum")
            if zadane_datum:
                base_date = zadane_datum
            else:
                base_date = date.today()
            klient.deadline_co_financuje = base_date + timedelta(days=7)
            klient.deadline_navrh_financovani = base_date + timedelta(days=14)
            klient.deadline_vyber_banky = base_date + timedelta(days=21)
            klient.deadline_schvalene_financovani = base_date + timedelta(days=28)
            klient.deadline_priprava_zadosti = base_date + timedelta(days=35)
            klient.deadline_kompletace_podkladu = base_date + timedelta(days=42)
            klient.deadline_podani_zadosti = base_date + timedelta(days=49)
            klient.deadline_odhad = base_date + timedelta(days=56)
            klient.deadline_schvalovani = base_date + timedelta(days=63)
            klient.deadline_priprava_uverove_dokumentace = base_date + timedelta(
                days=70
            )
            klient.deadline_podpis_uverove_dokumentace = base_date + timedelta(days=77)
            klient.deadline_priprava_cerpani = base_date + timedelta(days=84)
            klient.deadline_cerpani = base_date + timedelta(days=91)
            klient.deadline_zahajeni_splaceni = base_date + timedelta(days=98)
            klient.deadline_podminky_pro_splaceni = base_date + timedelta(days=105)
            klient.save()
            # Audit log - vytvoření klienta
            from .models import Zmena

            popis = f"Vytvořen klient: {klient.jmeno} (ID {klient.pk})"
            Zmena.objects.create(
                klient=klient,
                popis=popis,
                author=request.user.username if request.user.is_authenticated else "",
            )
            return redirect("home")
    else:
        today = date.today()
        initial = {
            "datum": today,
            "deadline_co_financuje": today + timedelta(days=7),
            "deadline_navrh_financovani": today + timedelta(days=14),
            "deadline_vyber_banky": today + timedelta(days=21),
            "deadline_schvalene_financovani": today + timedelta(days=28),
            "deadline_priprava_zadosti": today + timedelta(days=35),
            "deadline_kompletace_podkladu": today + timedelta(days=42),
            "deadline_podani_zadosti": today + timedelta(days=49),
            "deadline_odhad": today + timedelta(days=56),
            "deadline_schvalovani": today + timedelta(days=63),
            "deadline_priprava_uverove_dokumentace": today + timedelta(days=70),
            "deadline_podpis_uverove_dokumentace": today + timedelta(days=77),
            "deadline_priprava_cerpani": today + timedelta(days=84),
            "deadline_cerpani": today + timedelta(days=91),
            "deadline_zahajeni_splaceni": today + timedelta(days=98),
            "deadline_podminky_pro_splaceni": today + timedelta(days=105),
        }
        klient_form = KlientForm(initial=initial)
    return render(request, "klienti/klient_form.html", {"form": klient_form})


@login_required
def klient_edit(request, pk):
    klient = get_object_or_404(Klient, pk=pk)
    # Ulož původní hodnoty z DB před inicializací formuláře
    puvodni = {}
    for field in KlientForm().fields:
        puvodni[field] = getattr(klient, field)
    if request.method == "POST":
        form = KlientForm(request.POST, instance=klient)
        if form.is_valid():
            klient = form.save(commit=False)
            cena = form.cleaned_data.get("cena")
            procento = form.cleaned_data.get("navrh_financovani_procento")
            if cena and procento:
                klient.navrh_financovani_castka = round(
                    float(cena) * float(procento) / 100, 2
                )
            else:
                klient.navrh_financovani_castka = None
            klient.save()
            # Audit log - detailní změny
            from .models import Zmena

            zmeny = []
            for field in form.fields:
                nova = getattr(klient, field)
                stara = puvodni[field]
                if stara != nova:
                    zmeny.append(f"{field}: '{stara}' → '{nova}'")
            if zmeny:
                popis = "Upraven klient: " + klient.jmeno + "\n" + "\n".join(zmeny)
                Zmena.objects.create(
                    klient=klient,
                    popis=popis,
                    author=(
                        request.user.username if request.user.is_authenticated else ""
                    ),
                )
            return redirect("klient_detail", pk=klient.pk)
    else:
        form = KlientForm(instance=klient)
    return render(
        request,
        "klienti/klient_form.html",
        {"form": form, "editace": True, "klient": klient},
    )


@login_required
def klient_delete(request, pk):
    klient = get_object_or_404(Klient, pk=pk)
    if request.method == "POST":
        from .models import Zmena

        popis = f"Smazán klient: {klient.jmeno} (ID {klient.pk})"
        Zmena.objects.create(
            klient=klient,
            popis=popis,
            author=request.user.username if request.user.is_authenticated else "",
        )
        klient.delete()
        return redirect("home")
    return render(request, "klienti/klient_confirm_delete.html", {"klient": klient})


@login_required
def klient_detail(request, pk):
    klient = get_object_or_404(Klient, pk=pk)
    user = request.user
    try:
        profile = user.userprofile
        role = profile.role
    except Exception:
        role = None
    # Oprávnění: klient může vidět jen svůj záznam
    if user.is_authenticated and role == "klient" and klient.user != user:
        return redirect("home")
    poznamky = klient.poznamky.order_by("-created")
    zmeny = klient.zmeny.order_by("-created")
    if request.method == "POST" and "nova_poznamka" in request.POST:
        text = request.POST.get("text", "").strip()
        if text:
            from .models import Poznamka, Zmena

            Poznamka.objects.create(
                klient=klient,
                text=text,
                author=request.user.username if request.user.is_authenticated else "",
            )
            popis = f"Přidána poznámka: '{text[:50]}{'...' if len(text) > 50 else ''}'"
            Zmena.objects.create(
                klient=klient,
                popis=popis,
                author=request.user.username if request.user.is_authenticated else "",
            )
            return redirect("klient_detail", pk=pk)
    # Nová logika: použij pouze get_workflow_progress
    progress = klient.get_workflow_progress
    workflow_steps = progress["kroky"]
    aktivni_krok = progress["posledni_splneny_krok_index"]
    return render(
        request,
        "klienti/klient_detail.html",
        {
            "klient": klient,
            "poznamky": poznamky,
            "zmeny": zmeny,
            "workflow_steps": workflow_steps,
            "aktivni_krok": aktivni_krok,
        },
    )


@login_required
def home(request):
    user = request.user
    try:
        profile = user.userprofile
        role = profile.role
    except Exception:
        role = None
    if user.is_authenticated and role == "klient":
        klienti = Klient.objects.filter(user=user)
    elif user.is_authenticated and role == "poradce":
        klienti = Klient.objects.all().order_by("-datum")
    else:
        klienti = Klient.objects.none()
    # Filtrování podle jména (pouze jednou, před stránkováním)
    q = request.GET.get("q", "").strip()
    if q:
        klienti = klienti.filter(jmeno_index__icontains=q)
    # Stránkování pro výkon
    paginator = Paginator(klienti, 20)  # 20 klientů na stránku
    page_number = request.GET.get("page")
    klienti_page = paginator.get_page(page_number)
    today = date.today()
    deadline_fields = [
        ("co_financuje", "deadline_co_financuje", "splneno_co_financuje"),
        (
            "navrh_financovani",
            "deadline_navrh_financovani",
            "splneno_navrh_financovani",
        ),
        ("vyber_banky", "deadline_vyber_banky", "splneno_vyber_banky"),
        (
            "schvalene_financovani",
            "deadline_schvalene_financovani",
            "splneno_schvalene_financovani",
        ),
        ("priprava_zadosti", "deadline_priprava_zadosti", "splneno_priprava_zadosti"),
        (
            "kompletace_podkladu",
            "deadline_kompletace_podkladu",
            "splneno_kompletace_podkladu",
        ),
        ("podani_zadosti", "deadline_podani_zadosti", "splneno_podani_zadosti"),
        ("odhad", "deadline_odhad", "splneno_odhad"),
        ("schvalovani", "deadline_schvalovani", "splneno_schvalovani"),
        (
            "priprava_uverove_dokumentace",
            "deadline_priprava_uverove_dokumentace",
            "splneno_priprava_uverove_dokumentace",
        ),
        (
            "podpis_uverove_dokumentace",
            "deadline_podpis_uverove_dokumentace",
            "splneno_podpis_uverove_dokumentace",
        ),
        ("priprava_cerpani", "deadline_priprava_cerpani", "splneno_priprava_cerpani"),
        ("cerpani", "deadline_cerpani", "splneno_cerpani"),
        (
            "zahajeni_splaceni",
            "deadline_zahajeni_splaceni",
            "splneno_zahajeni_splaceni",
        ),
        (
            "podminky_pro_splaceni",
            "deadline_podminky_pro_splaceni",
            "splneno_podminky_pro_splaceni",
        ),
    ]
    klienti_deadlines = []
    for klient in klienti_page:
        nejblizsi_deadline = None
        nejblizsi_krok = None
        for krok, deadline_field, splneno_field in deadline_fields:
            deadline = getattr(klient, deadline_field)
            splneno = getattr(klient, splneno_field)
            if deadline and (not splneno) and deadline >= today:
                if not nejblizsi_deadline or deadline < nejblizsi_deadline:
                    nejblizsi_deadline = deadline
                    nejblizsi_krok = krok
        if nejblizsi_deadline:
            days_left = (nejblizsi_deadline - today).days
            klienti_deadlines.append(
                {
                    "klient": klient,
                    "deadline": nejblizsi_deadline,
                    "krok": nejblizsi_krok,
                    "days_left": days_left,
                    "po_termínu": days_left < 0,
                }
            )
    klienti_deadlines = sorted(klienti_deadlines, key=lambda x: x["deadline"])

    workflow_counts = [0] * 17
    workflow_sums = [0] * 17
    for k in klienti_page:
        progress = k.get_workflow_progress
        idx = (
            progress["prvni_nesplneny_krok_index"] + 1
            if progress["prvni_nesplneny_krok_index"] is not None
            else 16
        )
        workflow_counts[idx] += 1
        workflow_sums[idx] += float(k.navrh_financovani_castka or 0)
    months = []
    for i in range(6, -1, -1):
        m = (today.replace(day=1) - timedelta(days=30 * i)).replace(day=1)
        months.append(m.strftime("%Y-%m"))
    months = sorted(list(set(months)))
    klienti_timeline = defaultdict(int)
    objem_timeline = defaultdict(float)
    # OPRAVA: počítej timeline ze všech klientů, ne jen z klienti_page
    for klient in klienti:  # původně klienti_page
        m = klient.datum.strftime("%Y-%m")
        klienti_timeline[m] += 1
        objem_timeline[m] += float(klient.navrh_financovani_castka or 0)
    klientiTimeline = [klienti_timeline.get(m, 0) for m in months]
    objemTimeline = [objem_timeline.get(m, 0) for m in months]
    banky_vyber = list(
        Klient.objects.exclude(vyber_banky__isnull=True)
        .exclude(vyber_banky="")
        .values_list("vyber_banky", flat=True)
        .distinct()
    )

    return render(
        request,
        "klienti/home.html",
        {
            "klienti": klienti_page,
            "klienti_deadlines": klienti_deadlines,
            "today": today,
            "workflow_counts": workflow_counts,
            "workflow_sums": workflow_sums,
            "months": months,
            "klientiTimeline": klientiTimeline,
            "objemTimeline": objemTimeline,
            "banky_vyber": banky_vyber,
            "user_role": role,  # <--- přidáno pro správné větvení šablony
        },
    )


@login_required
def dashboard(request):
    klienti = Klient.objects.all()
    pocet_klientu = klienti.count()
    objem_hypotek = sum([k.navrh_financovani_castka or 0 for k in klienti])
    urgent_deadlines = []
    today = date.today()
    klienti_po_termínu = []
    for k in klienti:
        for field in [
            "deadline_co_financuje",
            "deadline_navrh_financovani",
            "deadline_vyber_banky",
            "deadline_schvalene_financovani",
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
        ]:
            deadline = getattr(k, field)
            splneno = getattr(k, field.replace("deadline_", "splneno_"), None)
            if deadline and not splneno:
                if (deadline - today).days < 0:
                    klienti_po_termínu.append(
                        {
                            "klient": k,
                            "krok": field,
                            "deadline": deadline,
                            "days_left": (deadline - today).days,
                        }
                    )
                elif (deadline - today).days <= 3 and (deadline - today).days >= 0:
                    urgent_deadlines.append(
                        {
                            "klient": k,
                            "krok": field,
                            "deadline": deadline,
                            "days_left": (deadline - today).days,
                        }
                    )
    # --- E-mailové notifikace pro poradce ---
    poradci = User.objects.filter(userprofile__role="poradce")
    from .models import NotifikaceLog

    for poradce in poradci:
        if poradce.email:
            urgent_klienti = [ud for ud in urgent_deadlines]
            for ud in urgent_klienti:
                # Kontrola, zda už dnes byla notifikace pro tohoto poradce a klienta odeslána
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
                        logger.error(f"Chyba při odesílání e-mailu: {e}")
    # Workflow rozložení
    workflow_labels = [
        "jmeno_klienta",
        "co_financuje",
        "navrh_financovani",
        "vyber_banky",
        "schvalene_financovani",
        "priprava_zadosti",
        "kompletace_podkladu",
        "podani_zadosti",
        "odhad",
        "schvalovani",
        "priprava_uverove_dokumentace",
        "podpis_uverove_dokumentace",
        "priprava_cerpani",
        "cerpani",
        "zahajeni_splaceni",
        "podminky_pro_splaceni",
        "hotovo",
    ]
    workflow_counts = [0] * 17
    workflow_sums = [0] * 17
    for k in klienti:
        progress = k.get_workflow_progress
        idx = (
            progress["prvni_nesplneny_krok_index"] + 1
            if progress["prvni_nesplneny_krok_index"] is not None
            else 16
        )
        workflow_counts[idx] += 1
        workflow_sums[idx] += float(k.navrh_financovani_castka or 0)
    posledni_klienti = klienti.order_by("-datum")[:5]
    top_hypoteky = klienti.order_by("-navrh_financovani_castka")[:5]
    # Log posledních změn
    from .models import Zmena

    posledni_zmeny = Zmena.objects.select_related("klient").order_by("-created")[:5]
    # Průměrná výše hypotéky
    prumerna_hypoteka = objem_hypotek / pocet_klientu if pocet_klientu else 0

    return render(
        request,
        "klienti/dashboard.html",
        {
            "pocet_klientu": pocet_klientu,
            "objem_hypotek": objem_hypotek,
            "urgent_deadlines": urgent_deadlines,
            "workflow_labels": workflow_labels,
            "workflow_counts": workflow_counts,
            "posledni_klienti": posledni_klienti,
            "top_hypoteky": top_hypoteky,
            "klienti_po_termínu": klienti_po_termínu,
            "posledni_zmeny": posledni_zmeny,
            "prumerna_hypoteka": prumerna_hypoteka,
        },
    )


@login_required
def smazat_poznamku(request, klient_id, poznamka_id):
    klient = get_object_or_404(Klient, pk=klient_id)
    poznamka = get_object_or_404(Poznamka, pk=poznamka_id, klient=klient)
    if request.method == "POST":
        text = poznamka.text
        poznamka.delete()
        popis = f"Smazána poznámka: '{text[:50]}{'...' if len(text) > 50 else ''}'"
        Zmena.objects.create(
            klient=klient,
            popis=popis,
            author=request.user.username if request.user.is_authenticated else "",
        )
        return redirect("klient_detail", pk=klient_id)
    return redirect("klient_detail", pk=klient_id)


def get_user_role(request):
    if hasattr(request, "user") and request.user.is_authenticated:
        try:
            return request.user.userprofile.role
        except Exception:
            return None
    return None


@login_required
def export_klient_ical(request, pk):
    klient = get_object_or_404(Klient, pk=pk)
    # Sestavení iCal souboru s deadliny workflow
    ical_lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//Hypoteky//CZ",
        f"X-WR-CALNAME:Deadliny klienta {klient.jmeno}",
    ]
    workflow_kroky = [
        ("Co chce klient financovat", klient.deadline_co_financuje),
        ("Návrh financování", klient.deadline_navrh_financovani),
        ("Výběr banky", klient.deadline_vyber_banky),
        ("Schválené financování", klient.deadline_schvalene_financovani),
        ("Příprava žádosti", klient.deadline_priprava_zadosti),
        ("Kompletace podkladů", klient.deadline_kompletace_podkladu),
        ("Podání žádosti", klient.deadline_podani_zadosti),
        ("Odhad", klient.deadline_odhad),
        ("Schvalování", klient.deadline_schvalovani),
        ("Příprava úvěrové dokumentace", klient.deadline_priprava_uverove_dokumentace),
        ("Podpis úvěrové dokumentace", klient.deadline_podpis_uverove_dokumentace),
        ("Příprava čerpání", klient.deadline_priprava_cerpani),
        ("Čerpání", klient.deadline_cerpani),
        ("Zahájení splácení", klient.deadline_zahajeni_splaceni),
        ("Podmínky pro splacení", klient.deadline_podminky_pro_splaceni),
    ]
    for krok, deadline in workflow_kroky:
        if deadline:
            dt = deadline.strftime("%Y%m%d")
            ical_lines += [
                "BEGIN:VEVENT",
                f"SUMMARY:{krok} – {klient.jmeno}",
                f"DTSTART;VALUE=DATE:{dt}",
                f"DTEND;VALUE=DATE:{dt}",
                f"DESCRIPTION:Deadline pro krok {krok} klienta {klient.jmeno}",
                f'UID:{pk}-{krok.replace(" ", "_")}@hypoteky.cz',
                "END:VEVENT",
            ]
    ical_lines.append("END:VCALENDAR")
    ical_content = "\r\n".join(ical_lines)
    response = HttpResponse(ical_content, content_type="text/calendar")
    response["Content-Disposition"] = f"attachment; filename=klient_{pk}_deadliny.ics"
    return response


@login_required
def reporting(request):
    today = timezone.now().date()
    # ZOBRAZIT VŠECHNY KLIENTY BEZ FILTRU NA DATUM
    klienti = Klient.objects.all()
    # Připravíme pro každého klienta stav podle workflow a zamítnutí
    klienti_with_status = []
    for k in klienti:
        if k.duvod_zamitnuti and str(k.duvod_zamitnuti).strip():
            stav = "zamítnuto"
        else:
            progress = k.get_workflow_progress
            if all(krok["splneno"] for krok in progress["kroky"]):
                stav = "schvaleno"
            else:
                stav = "in_process"
        klienti_with_status.append(
            {
                "obj": k,
                "stav": stav,
            }
        )
    # Najdi všechny unikátní banky (bez prázdných a mezer)
    banky_labels = sorted(
        set(
            k.vyber_banky.strip()
            for k in klienti
            if k.vyber_banky and k.vyber_banky.strip()
        )
    )
    schvalenost = []
    zamitnutost = []
    prumery = []
    for banka in banky_labels:
        klienti_banka = [
            k
            for k in klienti_with_status
            if k["obj"].vyber_banky and k["obj"].vyber_banky.strip() == banka
        ]
        schv = [k for k in klienti_banka if k["stav"] == "schvaleno"]
        zam = [k for k in klienti_banka if k["stav"] == "zamítnuto"]
        schvalenost.append(len(schv))
        zamitnutost.append(len(zam))
        # Průměrná doba schválení (jen pro schválené)
        doby = []
        for k in schv:
            try:
                schv_date = k["obj"].schvalovani
                pod_date = k["obj"].podani_zadosti
                if isinstance(schv_date, str):
                    schv_date = datetime.datetime.strptime(schv_date, "%Y-%m-%d").date()
                if isinstance(pod_date, str):
                    pod_date = datetime.datetime.strptime(pod_date, "%Y-%m-%d").date()
                if schv_date and pod_date:
                    doby.append((schv_date - pod_date).days)
            except Exception:
                continue
        prumery.append(round(sum(doby) / len(doby), 1) if doby else None)
    # Trendy schválených a zamítnutých hypoték (timeline)
    months = []
    schvaleneTimeline = []
    zamitnuteTimeline = []
    # Vždy zobraz posledních 12 měsíců (i když nejsou data)
    today = timezone.now().date()
    for i in range(11, -1, -1):
        m = (today.replace(day=1) - timedelta(days=30 * i)).replace(day=1)
        months.append(m.strftime("%Y-%m"))
    for m in months:
        schv = 0
        zam = 0
        for k in klienti_with_status:
            if k["obj"].datum.strftime("%Y-%m") == m:
                if k["stav"] == "schvaleno":
                    schv += 1
                elif k["stav"] == "zamítnuto":
                    zam += 1
        schvaleneTimeline.append(schv)
        zamitnuteTimeline.append(zam)
    # Pokud jsou všechna data nulová, zobrazit info v šabloně
    graf_trendy_prazdny = all(x == 0 for x in schvaleneTimeline + zamitnuteTimeline)
    # Statistika pro boxy nahoře
    klientu_celkem = len(klienti)
    schvaleno_celkem = sum(schvalenost)
    zamitnuto_celkem = sum(zamitnutost)
    # Předání do šablony
    context = {
        "banky_labels": banky_labels,
        "schvalenost": schvalenost,
        "zamitnutost": zamitnutost,
        "prumery": prumery,
        "months": months,
        "schvaleneTimeline": schvaleneTimeline,
        "zamitnuteTimeline": zamitnuteTimeline,
        "graf_trendy_prazdny": graf_trendy_prazdny,
        "klienti": klienti_with_status,
        "klientu_celkem": klientu_celkem,
        "schvaleno_celkem": schvaleno_celkem,
        "zamitnuto_celkem": zamitnuto_celkem,
    }
    return render(request, "klienti/reporting.html", context)


@login_required
def reporting_export_pdf(request):
    """
    View pro export reportingu do PDF včetně grafů a tabulky.
    Využívá matplotlib pro generování grafů a reportlab pro PDF.
    """
    import io
    import tempfile
    from collections import Counter

    from django.utils import timezone

    from matplotlib import pyplot as plt
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.utils import ImageReader
    from reportlab.pdfgen import canvas

    from .models import Klient

    # --- Filtrování podle období ---
    today = timezone.now().date()
    first_day = today.replace(day=1)
    datum_od = request.GET.get("datum_od")
    datum_do = request.GET.get("datum_do")
    klienti = Klient.objects.all()
    if datum_od:
        klienti = klienti.filter(datum__gte=datum_od)
    else:
        klienti = klienti.filter(datum__gte=first_day)
    if datum_do:
        klienti = klienti.filter(datum__lte=datum_do)
    # --- Statistika podle banky ---
    banky = [k.vyber_banky for k in klienti if k.vyber_banky]
    rozlozeni_banky = Counter(banky)
    schvalene = klienti.filter(duvod_zamitnuti__isnull=True, vyber_banky__isnull=False)
    zamitnute = klienti.filter(duvod_zamitnuti__isnull=False, vyber_banky__isnull=False)
    banky_labels = list(rozlozeni_banky.keys())
    schvalenost = [schvalene.filter(vyber_banky=b).count() for b in banky_labels]
    zamitnutost = [zamitnute.filter(vyber_banky=b).count() for b in banky_labels]
    prumery = []
    for banka in banky_labels:
        klienti_banka = klienti.filter(
            vyber_banky=banka, podani_zadosti__isnull=False, schvalovani__isnull=False
        )
        doby = []
        for k in klienti_banka:
            schv = k.schvalovani
            pod = k.podani_zadosti
            # Pokud je hodnota typu str, převedeme na date
            if isinstance(schv, str):
                try:
                    schv = datetime.strptime(schv, "%Y-%m-%d").date()
                except Exception:
                    continue
            if isinstance(pod, str):
                try:
                    pod = datetime.strptime(pod, "%Y-%m-%d").date()
                except Exception:
                    continue
            if schv and pod:
                doby.append((schv - pod).days)
        prumery.append(round(sum(doby) / len(doby), 1) if doby else None)
    # --- trendy ---
    months = []
    schvaleneTimeline = []
    zamitnuteTimeline = []
    # Vždy zobraz posledních 12 měsíců (i když nejsou data)
    today = timezone.now().date()
    for i in range(11, -1, -1):
        m = (today.replace(day=1) - timedelta(days=30 * i)).replace(day=1)
        months.append(m.strftime("%Y-%m"))
    for m in months:
        schv = 0
        zam = 0
        for k in klienti:
            if k.datum.strftime("%Y-%m") == m:
                if not (k.duvod_zamitnuti and str(k.duvod_zamitnuti).strip()):
                    schv += 1
                else:
                    zam += 1
        schvaleneTimeline.append(schv)
        zamitnuteTimeline.append(zam)
    # Oprava: zajistit, že timeline mají vždy stejnou délku jako months
    if len(schvaleneTimeline) != len(months):
        schvaleneTimeline = [0] * len(months)
    if len(zamitnuteTimeline) != len(months):
        zamitnuteTimeline = [0] * len(months)
    # --- generování grafů ---
    tempfiles = []
    # Bar chart úspěšnost podle banky
    if banky_labels:
        fig1, ax1 = plt.subplots(figsize=(6, 3))
        x = range(len(banky_labels))
        ax1.bar(x, schvalenost, label="Schváleno", color="#198754")
        ax1.bar(x, zamitnutost, bottom=schvalenost, label="Zamítnuto", color="#dc3545")
        ax1.set_xticks(x)
        ax1.set_xticklabels(banky_labels, rotation=30, ha="right")
        ax1.set_ylabel("Počet případů")
        ax1.set_title("Úspěšnost podle banky")
        ax1.legend()
        f1 = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
        fig1.tight_layout()
        fig1.savefig(f1.name, dpi=120)
        tempfiles.append(f1)
        plt.close(fig1)
    # Line chart trendy
    if months:
        fig2, ax2 = plt.subplots(figsize=(6, 3))
        ax2.plot(
            months, schvaleneTimeline, marker="o", label="Schváleno", color="#198754"
        )
        ax2.plot(
            months, zamitnuteTimeline, marker="o", label="Zamítnuto", color="#dc3545"
        )
        ax2.set_ylabel("Počet případů")
        ax2.set_title("Trendy schválených a zamitnutých hypoték")
        ax2.legend()
        fig2.tight_layout()
        f2 = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
        fig2.savefig(f2.name, dpi=120)
        tempfiles.append(f2)
        plt.close(fig2)
    # --- PDF ---
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    p.setFont("Helvetica-Bold", 16)
    p.drawString(40, 800, "Reporting – úspěšnost podle banky")
    y = 770
    # Vložit grafy
    for tf in tempfiles:
        p.drawImage(ImageReader(tf.name), 40, y - 180, width=500, height=120)
        y -= 200
    p.setFont("Helvetica", 11)
    # Tabulka
    p.drawString(40, y, "Banka")
    y -= 20
    for i in range(len(banky_labels)):
        banka = banky_labels[i]
        p.drawString(40, y, banka)
        p.drawString(180, y, str(schvalenost[i]))
        p.drawString(270, y, str(zamitnutost[i]))
        p.drawString(370, y, str(prumery[i]) if prumery[i] is not None else "-")
        y += 15
    p.showPage()
    p.save()
    buffer.seek(0)
    response = HttpResponse(buffer, content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="reporting.pdf"'
    return response
