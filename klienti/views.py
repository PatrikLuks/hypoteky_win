from django.shortcuts import render, redirect, get_object_or_404
from .models import Klient, Poznamka, Zmena, UserProfile
from django import forms
from datetime import timedelta, date
from math import pow
from collections import defaultdict
from django.utils import timezone
import datetime
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User
from .utils import odeslat_notifikaci_email

class KlientForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk and self.instance.cena is not None:
            # Zobrazit cenu jako celé číslo (bez .00)
            self.initial['cena'] = int(self.instance.cena)
        # Přidat text-white ke všem deadline polím
        deadline_fields = [
            'deadline_co_financuje', 'deadline_navrh_financovani', 'deadline_vyber_banky',
            'deadline_priprava_zadosti', 'deadline_kompletace_podkladu', 'deadline_podani_zadosti',
            'deadline_odhad', 'deadline_schvalovani', 'deadline_priprava_uverove_dokumentace',
            'deadline_podpis_uverove_dokumentace', 'deadline_priprava_cerpani', 'deadline_cerpani',
            'deadline_zahajeni_splaceni', 'deadline_podminky_pro_splaceni'
        ]
        for field in deadline_fields:
            if field in self.fields:
                css = self.fields[field].widget.attrs.get('class', '')
                self.fields[field].widget.attrs['class'] = f'{css} text-white'.strip()

    class Meta:
        model = Klient
        fields = [
            'jmeno', 'datum',
            'co_financuje', 'cena', 'deadline_co_financuje', 'splneno_co_financuje',
            'navrh_financovani', 'navrh_financovani_procento', 'deadline_navrh_financovani', 'splneno_navrh_financovani',
            'vyber_banky', 'deadline_vyber_banky', 'splneno_vyber_banky',
            'priprava_zadosti', 'deadline_priprava_zadosti', 'splneno_priprava_zadosti',
            'kompletace_podkladu', 'deadline_kompletace_podkladu', 'splneno_kompletace_podkladu',
            'podani_zadosti', 'deadline_podani_zadosti', 'splneno_podani_zadosti',
            'odhad', 'deadline_odhad', 'splneno_odhad',
            'schvalovani', 'deadline_schvalovani', 'splneno_schvalovani',
            'priprava_uverove_dokumentace', 'deadline_priprava_uverove_dokumentace', 'splneno_priprava_uverove_dokumentace',
            'podpis_uverove_dokumentace', 'deadline_podpis_uverove_dokumentace', 'splneno_podpis_uverove_dokumentace',
            'priprava_cerpani', 'deadline_priprava_cerpani', 'splneno_priprava_cerpani',
            'cerpani', 'deadline_cerpani', 'splneno_cerpani',
            'zahajeni_splaceni', 'deadline_zahajeni_splaceni', 'splneno_zahajeni_splaceni',
            'podminky_pro_splaceni', 'deadline_podminky_pro_splaceni', 'splneno_podminky_pro_splaceni',
        ]
        widgets = {
            'datum': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'cena': forms.TextInput(attrs={'inputmode': 'numeric', 'pattern': '[0-9 ]*', 'placeholder': 'např. 12 200 000', 'class': 'form-control'}),
            'navrh_financovani_procento': forms.NumberInput(attrs={'step': '0.01', 'min': '0', 'max': '100', 'placeholder': 'např. 80', 'class': 'form-control'}),
            'co_financuje': forms.TextInput(attrs={'class': 'form-control'}),
            'navrh_financovani': forms.TextInput(attrs={'class': 'form-control'}),
            'vyber_banky': forms.TextInput(attrs={'class': 'form-control'}),
            'priprava_zadosti': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'poznámka'}),
            'kompletace_podkladu': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'poznámka'}),
            'podani_zadosti': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'poznámka'}),
            'odhad': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'poznámka'}),
            'schvalovani': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'poznámka'}),
            'priprava_uverove_dokumentace': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'poznámka'}),
            'podpis_uverove_dokumentace': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'poznámka'}),
            'priprava_cerpani': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'poznámka'}),
            'cerpani': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'poznámka'}),
            'zahajeni_splaceni': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'poznámka'}),
            'podminky_pro_splaceni': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'poznámka'}),
            'deadline_co_financuje': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'deadline_navrh_financovani': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'deadline_vyber_banky': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'deadline_priprava_zadosti': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'deadline_kompletace_podkladu': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'deadline_podani_zadosti': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'deadline_odhad': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'deadline_schvalovani': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'deadline_priprava_uverove_dokumentace': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'deadline_podpis_uverove_dokumentace': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'deadline_priprava_cerpani': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'deadline_cerpani': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'deadline_zahajeni_splaceni': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'deadline_podminky_pro_splaceni': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'splneno_co_financuje': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'splneno_navrh_financovani': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'splneno_vyber_banky': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'splneno_priprava_zadosti': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'splneno_kompletace_podkladu': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'splneno_podani_zadosti': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'splneno_odhad': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'splneno_schvalovani': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'splneno_priprava_uverove_dokumentace': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'splneno_podpis_uverove_dokumentace': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'splneno_priprava_cerpani': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'splneno_cerpani': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'splneno_zahajeni_splaceni': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'splneno_podminky_pro_splaceni': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def clean_cena(self):
        data = self.cleaned_data['cena']
        if data in (None, ''):
            return None
        if isinstance(data, str):
            data = data.replace(' ', '').replace('\xa0', '').replace(',', '.')
        try:
            return float(data)
        except Exception:
            raise forms.ValidationError('Zadejte částku ve správném formátu, např. 12 200 000')

def klient_create(request):
    if request.method == 'POST':
        klient_form = KlientForm(request.POST)
        if klient_form.is_valid():
            klient = klient_form.save(commit=False)
            # Výpočet částky hypotečního úvěru
            cena = klient_form.cleaned_data.get('cena')
            procento = klient_form.cleaned_data.get('navrh_financovani_procento')
            if cena and procento:
                klient.navrh_financovani_castka = round(float(cena) * float(procento) / 100, 2)
            else:
                klient.navrh_financovani_castka = None
            # Nastavení pole user pouze pokud je role klient
            try:
                profile = request.user.userprofile
                if profile.role == 'klient':
                    klient.user = request.user
                else:
                    klient.user = None
            except Exception:
                klient.user = None
            klient.save()
            # Audit log - vytvoření klienta
            from .models import Zmena
            popis = f"Vytvořen klient: {klient.jmeno} (ID {klient.pk})"
            Zmena.objects.create(
                klient=klient,
                popis=popis,
                author=request.user.username if request.user.is_authenticated else ''
            )
            return redirect('home')
    else:
        today = date.today()
        initial = {
            'datum': today,
            'deadline_co_financuje': today + timedelta(days=7),
            'deadline_navrh_financovani': today + timedelta(days=14),
            'deadline_vyber_banky': today + timedelta(days=21),
            'deadline_priprava_zadosti': today + timedelta(days=28),
            'deadline_kompletace_podkladu': today + timedelta(days=35),
            'deadline_podani_zadosti': today + timedelta(days=42),
            'deadline_odhad': today + timedelta(days=49),
            'deadline_schvalovani': today + timedelta(days=56),
            'deadline_priprava_uverove_dokumentace': today + timedelta(days=63),
            'deadline_podpis_uverove_dokumentace': today + timedelta(days=70),
            'deadline_priprava_cerpani': today + timedelta(days=77),
            'deadline_cerpani': today + timedelta(days=84),
            'deadline_zahajeni_splaceni': today + timedelta(days=91),
            'deadline_podminky_pro_splaceni': today + timedelta(days=98),
        }
        klient_form = KlientForm(initial=initial)
    return render(request, 'klienti/klient_form.html', {'form': klient_form})

def klient_edit(request, pk):
    klient = get_object_or_404(Klient, pk=pk)
    if request.method == 'POST':
        form = KlientForm(request.POST, instance=klient)
        if form.is_valid():
            # Uchovej původní hodnoty
            puvodni = {}
            for field in form.fields:
                puvodni[field] = getattr(klient, field)
            klient = form.save(commit=False)
            cena = form.cleaned_data.get('cena')
            procento = form.cleaned_data.get('navrh_financovani_procento')
            if cena and procento:
                klient.navrh_financovani_castka = round(float(cena) * float(procento) / 100, 2)
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
                    author=request.user.username if request.user.is_authenticated else ''
                )
            return redirect('klient_detail', pk=klient.pk)
    else:
        form = KlientForm(instance=klient)
    return render(request, 'klienti/klient_form.html', {'form': form, 'editace': True, 'klient': klient})

def klient_delete(request, pk):
    klient = get_object_or_404(Klient, pk=pk)
    if request.method == 'POST':
        from .models import Zmena
        popis = f"Smazán klient: {klient.jmeno} (ID {klient.pk})"
        Zmena.objects.create(
            klient=klient,
            popis=popis,
            author=request.user.username if request.user.is_authenticated else ''
        )
        klient.delete()
        return redirect('home')
    return render(request, 'klienti/klient_confirm_delete.html', {'klient': klient})

def klient_detail(request, pk):
    klient = get_object_or_404(Klient, pk=pk)
    user = request.user
    try:
        profile = user.userprofile
        role = profile.role
    except Exception:
        role = None
    # Oprávnění: klient může vidět jen svůj záznam
    if user.is_authenticated and role == 'klient' and klient.user != user:
        return redirect('home')
    poznamky = klient.poznamky.order_by('-created')
    zmeny = klient.zmeny.order_by('-created')
    if request.method == 'POST' and 'nova_poznamka' in request.POST:
        text = request.POST.get('text', '').strip()
        if text:
            from .models import Poznamka, Zmena
            Poznamka.objects.create(klient=klient, text=text, author=request.user.username if request.user.is_authenticated else '')
            popis = f"Přidána poznámka: '{text[:50]}{'...' if len(text) > 50 else ''}'"
            Zmena.objects.create(
                klient=klient,
                popis=popis,
                author=request.user.username if request.user.is_authenticated else ''
            )
            return redirect('klient_detail', pk=pk)
    # Definice kroků workflow pro timeline
    from datetime import date
    today = date.today()
    workflow_steps = [
        {
            'pole': 'co_financuje',
            'popis': 'Co chce klient financovat',
            'deadline': klient.deadline_co_financuje,
            'splneno': klient.splneno_co_financuje,
            'stav_deadlinu': (
                'po_termínu' if klient.deadline_co_financuje and klient.splneno_co_financuje is None and klient.deadline_co_financuje < today else
                'blizi_se' if klient.deadline_co_financuje and klient.splneno_co_financuje is None and (klient.deadline_co_financuje - today).days <= 3 and (klient.deadline_co_financuje - today).days >= 0 else
                'ok'
            ),
            'poznamky': [p for p in poznamky if getattr(p, 'krok', None) == 'co_financuje'] if poznamky and hasattr(poznamky[0], 'krok') else []
        },
        {
            'pole': 'navrh_financovani',
            'popis': 'Návrh financování',
            'deadline': klient.deadline_navrh_financovani,
            'splneno': klient.splneno_navrh_financovani,
            'stav_deadlinu': (
                'po_termínu' if klient.deadline_navrh_financovani and klient.splneno_navrh_financovani is None and klient.deadline_navrh_financovani < today else
                'blizi_se' if klient.deadline_navrh_financovani and klient.splneno_navrh_financovani is None and (klient.deadline_navrh_financovani - today).days <= 3 and (klient.deadline_navrh_financovani - today).days >= 0 else
                'ok'
            ),
            'poznamky': [p for p in poznamky if getattr(p, 'krok', None) == 'navrh_financovani'] if poznamky and hasattr(poznamky[0], 'krok') else []
        },
        {
            'pole': 'vyber_banky',
            'popis': 'Výběr banky',
            'deadline': klient.deadline_vyber_banky,
            'splneno': klient.splneno_vyber_banky,
            'stav_deadlinu': (
                'po_termínu' if klient.deadline_vyber_banky and klient.splneno_vyber_banky is None and klient.deadline_vyber_banky < today else
                'blizi_se' if klient.deadline_vyber_banky and klient.splneno_vyber_banky is None and (klient.deadline_vyber_banky - today).days <= 3 and (klient.deadline_vyber_banky - today).days >= 0 else
                'ok'
            ),
            'poznamky': [p for p in poznamky if getattr(p, 'krok', None) == 'vyber_banky'] if poznamky and hasattr(poznamky[0], 'krok') else []
        },
        {
            'pole': 'priprava_zadosti',
            'popis': 'Příprava žádosti',
            'deadline': klient.deadline_priprava_zadosti,
            'splneno': klient.splneno_priprava_zadosti,
            'stav_deadlinu': (
                'po_termínu' if klient.deadline_priprava_zadosti and klient.splneno_priprava_zadosti is None and klient.deadline_priprava_zadosti < today else
                'blizi_se' if klient.deadline_priprava_zadosti and klient.splneno_priprava_zadosti is None and (klient.deadline_priprava_zadosti - today).days <= 3 and (klient.deadline_priprava_zadosti - today).days >= 0 else
                'ok'
            ),
            'poznamky': [p for p in poznamky if getattr(p, 'krok', None) == 'priprava_zadosti'] if poznamky and hasattr(poznamky[0], 'krok') else []
        },
        {
            'pole': 'kompletace_podkladu',
            'popis': 'Kompletace podkladů',
            'deadline': klient.deadline_kompletace_podkladu,
            'splneno': klient.splneno_kompletace_podkladu,
            'stav_deadlinu': (
                'po_termínu' if klient.deadline_kompletace_podkladu and klient.splneno_kompletace_podkladu is None and klient.deadline_kompletace_podkladu < today else
                'blizi_se' if klient.deadline_kompletace_podkladu and klient.splneno_kompletace_podkladu is None and (klient.deadline_kompletace_podkladu - today).days <= 3 and (klient.deadline_kompletace_podkladu - today).days >= 0 else
                'ok'
            ),
            'poznamky': [p for p in poznamky if getattr(p, 'krok', None) == 'kompletace_podkladu'] if poznamky and hasattr(poznamky[0], 'krok') else []
        },
        {
            'pole': 'podani_zadosti',
            'popis': 'Podání žádosti',
            'deadline': klient.deadline_podani_zadosti,
            'splneno': klient.splneno_podani_zadosti,
            'stav_deadlinu': (
                'po_termínu' if klient.deadline_podani_zadosti and klient.splneno_podani_zadosti is None and klient.deadline_podani_zadosti < today else
                'blizi_se' if klient.deadline_podani_zadosti and klient.splneno_podani_zadosti is None and (klient.deadline_podani_zadosti - today).days <= 3 and (klient.deadline_podani_zadosti - today).days >= 0 else
                'ok'
            ),
            'poznamky': [p for p in poznamky if getattr(p, 'krok', None) == 'podani_zadadosti'] if poznamky and hasattr(poznamky[0], 'krok') else []
        },
        {
            'pole': 'odhad',
            'popis': 'Odhad',
            'deadline': klient.deadline_odhad,
            'splneno': klient.splneno_odhad,
            'stav_deadlinu': (
                'po_termínu' if klient.deadline_odhad and klient.splneno_odhad is None and klient.deadline_odhad < today else
                'blizi_se' if klient.deadline_odhad and klient.splneno_odhad is None and (klient.deadline_odhad - today).days <= 3 and (klient.deadline_odhad - today).days >= 0 else
                'ok'
            ),
            'poznamky': [p for p in poznamky if getattr(p, 'krok', None) == 'odhad'] if poznamky and hasattr(poznamky[0], 'krok') else []
        },
        {
            'pole': 'schvalovani',
            'popis': 'Schvalování',
            'deadline': klient.deadline_schvalovani,
            'splneno': klient.splneno_schvalovani,
            'stav_deadlinu': (
                'po_termínu' if klient.deadline_schvalovani and klient.splneno_schvalovani is None and klient.deadline_schvalovani < today else
                'blizi_se' if klient.deadline_schvalovani and klient.splneno_schvalovani is None and (klient.deadline_schvalovani - today).days <= 3 and (klient.deadline_schvalovani - today).days >= 0 else
                'ok'
            ),
            'poznamky': [p for p in poznamky if getattr(p, 'krok', None) == 'schvalovani'] if poznamky and hasattr(poznamky[0], 'krok') else []
        },
        {
            'pole': 'priprava_uverove_dokumentace',
            'popis': 'Příprava úvěrové dokumentace',
            'deadline': klient.deadline_priprava_uverove_dokumentace,
            'splneno': klient.splneno_priprava_uverove_dokumentace,
            'stav_deadlinu': (
                'po_termínu' if klient.deadline_priprava_uverove_dokumentace and klient.splneno_priprava_uverove_dokumentace is None and klient.deadline_priprava_uverove_dokumentace < today else
                'blizi_se' if klient.deadline_priprava_uverove_dokumentace and klient.splneno_priprava_uverove_dokumentace is None and (klient.deadline_priprava_uverove_dokumentace - today).days <= 3 and (klient.deadline_priprava_uverove_dokumentace - today).days >= 0 else
                'ok'
            ),
            'poznamky': [p for p in poznamky if getattr(p, 'krok', None) == 'priprava_uverove_dokumentace'] if poznamky and hasattr(poznamky[0], 'krok') else []
        },
        {
            'pole': 'podpis_uverove_dokumentace',
            'popis': 'Podpis úvěrové dokumentace',
            'deadline': klient.deadline_podpis_uverove_dokumentace,
            'splneno': klient.splneno_podpis_uverove_dokumentace,
            'stav_deadlinu': (
                'po_termínu' if klient.deadline_podpis_uverove_dokumentace and klient.splneno_podpis_uverove_dokumentace is None and klient.deadline_podpis_uverove_dokumentace < today else
                'blizi_se' if klient.deadline_podpis_uverove_dokumentace and klient.splneno_podpis_uverove_dokumentace is None and (klient.deadline_podpis_uverove_dokumentace - today).days <= 3 and (klient.deadline_podpis_uverove_dokumentace - today).days >= 0 else
                'ok'
            ),
            'poznamky': [p for p in poznamky if getattr(p, 'krok', None) == 'podpis_uverove_dokumentace'] if poznamky and hasattr(poznamky[0], 'krok') else []
        },
        {
            'pole': 'priprava_cerpani',
            'popis': 'Příprava čerpání',
            'deadline': klient.deadline_priprava_cerpani,
            'splneno': klient.splneno_priprava_cerpani,
            'stav_deadlinu': (
                'po_termínu' if klient.deadline_priprava_cerpani and klient.splneno_priprava_cerpani is None and klient.deadline_priprava_cerpani < today else
                'blizi_se' if klient.deadline_priprava_cerpani and klient.splneno_priprava_cerpani is None and (klient.deadline_priprava_cerpani - today).days <= 3 and (klient.deadline_priprava_cerpani - today).days >= 0 else
                'ok'
            ),
            'poznamky': [p for p in poznamky if getattr(p, 'krok', None) == 'priprava_cerpani'] if poznamky and hasattr(poznamky[0], 'krok') else []
        },
        {
            'pole': 'cerpani',
            'popis': 'Čerpání',
            'deadline': klient.deadline_cerpani,
            'splneno': klient.splneno_cerpani,
            'stav_deadlinu': (
                'po_termínu' if klient.deadline_cerpani and klient.splneno_cerpani is None and klient.deadline_cerpani < today else
                'blizi_se' if klient.deadline_cerpani and klient.splneno_cerpani is None and (klient.deadline_cerpani - today).days <= 3 and (klient.deadline_cerpani - today).days >= 0 else
                'ok'
            ),
            'poznamky': [p for p in poznamky if getattr(p, 'krok', None) == 'cerpani'] if poznamky and hasattr(poznamky[0], 'krok') else []
        },
        {
            'pole': 'zahajeni_splaceni',
            'popis': 'Zahájení splácení',
            'deadline': klient.deadline_zahajeni_splaceni,
            'splneno': klient.splneno_zahajeni_splaceni,
            'stav_deadlinu': (
                'po_termínu' if klient.deadline_zahajeni_splaceni and klient.splneno_zahajeni_splaceni is None and klient.deadline_zahajeni_splaceni < today else
                'blizi_se' if klient.deadline_zahajeni_splaceni and klient.splneno_zahajeni_splaceni is None and (klient.deadline_zahajeni_splaceni - today).days <= 3 and (klient.deadline_zahajeni_splaceni - today).days >= 0 else
                'ok'
            ),
            'poznamky': [p for p in poznamky if getattr(p, 'krok', None) == 'zahajeni_splaceni'] if poznamky and hasattr(poznamky[0], 'krok') else []
        },
    ]
    # Určení aktuálního kroku klienta pro zvýraznění v timeline
    aktivni_krok = None
    for idx, step in enumerate(workflow_steps):
        if not getattr(klient, step['pole']):
            aktivni_krok = idx
            break
    else:
        aktivni_krok = len(workflow_steps) - 1  # vše splněno
    return render(request, 'klienti/klient_detail.html', {
        'klient': klient,
        'poznamky': poznamky,
        'zmeny': zmeny,
        'workflow_steps': workflow_steps,
        'aktivni_krok': aktivni_krok,
    })

@login_required
def home(request):
    user = request.user
    try:
        profile = user.userprofile
        role = profile.role
    except Exception:
        role = None
    if user.is_authenticated and role == 'klient':
        klienti = Klient.objects.filter(user=user)
    elif user.is_authenticated and role == 'poradce':
        klienti = Klient.objects.all().order_by('-datum')
    else:
        klienti = Klient.objects.none()
    today = date.today()
    deadline_fields = [
        ('co_financuje', 'deadline_co_financuje', 'splneno_co_financuje'),
        ('navrh_financovani', 'deadline_navrh_financovani', 'splneno_navrh_financovani'),
        ('vyber_banky', 'deadline_vyber_banky', 'splneno_vyber_banky'),
        ('priprava_zadosti', 'deadline_priprava_zadosti', 'splneno_priprava_zadosti'),
        ('kompletace_podkladu', 'deadline_kompletace_podkladu', 'splneno_kompletace_podkladu'),
        ('podani_zadosti', 'deadline_podani_zadosti', 'splneno_podani_zadosti'),
        ('odhad', 'deadline_odhad', 'splneno_odhad'),
        ('schvalovani', 'deadline_schvalovani', 'splneno_schvalovani'),
        ('priprava_uverove_dokumentace', 'deadline_priprava_uverove_dokumentace', 'splneno_priprava_uverove_dokumentace'),
        ('podpis_uverove_dokumentace', 'deadline_podpis_uverove_dokumentace', 'splneno_podpis_uverove_dokumentace'),
        ('priprava_cerpani', 'deadline_priprava_cerpani', 'splneno_priprava_cerpani'),
        ('cerpani', 'deadline_cerpani', 'splneno_cerpani'),
        ('zahajeni_splaceni', 'deadline_zahajeni_splaceni', 'splneno_zahajeni_splaceni'),
        ('podminky_pro_splaceni', 'deadline_podminky_pro_splaceni', 'splneno_podminky_pro_splaceni'),
    ]
    # --- Filtrování a vyhledávání ---
    q = request.GET.get('q', '').strip()
    stav = request.GET.get('stav', '').strip()
    if q:
        klienti = klienti.filter(jmeno__icontains=q)
    if stav:
        # stav je číslo kroku 1-15 (string), převedeme na int
        try:
            stav = int(stav)
            workflow_labels = [
                'co_financuje', 'navrh_financovani', 'vyber_banky', 'priprava_zadosti',
                'kompletace_podkladu', 'podani_zadadosti', 'odhad', 'schvalovani',
                'priprava_uverove_dokumentace', 'podpis_uverove_dokumentace',
                'priprava_cerpani', 'cerpani', 'zahajeni_splaceni', 'podminky_pro_splaceni',
            ]
            if stav == 1:
                klienti = klienti.filter(co_financuje__isnull=True)
            elif stav <= len(workflow_labels):
                predchozi = workflow_labels[stav-2] if stav > 1 else None
                aktualni = workflow_labels[stav-1]
                if predchozi:
                    klienti = klienti.filter(**{predchozi+'__isnull': False, aktualni+'__isnull': True})
                else:
                    klienti = klienti.filter(**{aktualni+'__isnull': True})
        except Exception:
            pass
    klienti_deadlines = []
    for klient in klienti:
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
            klienti_deadlines.append({
                'klient': klient,
                'deadline': nejblizsi_deadline,
                'krok': nejblizsi_krok,
                'days_left': days_left,
                'po_termínu': days_left < 0,
            })
    klienti_deadlines = sorted(klienti_deadlines, key=lambda x: x['deadline'])

    # --- Data pro grafy ---
    workflow_labels = [
        'co_financuje', 'navrh_financovani', 'vyber_banky', 'priprava_zadosti',
        'kompletace_podkladu', 'podani_zadosti', 'odhad', 'schvalovani',
        'priprava_uverove_dokumentace', 'podpis_uverove_dokumentace',
        'priprava_cerpani', 'cerpani', 'zahajeni_splaceni', 'podminky_pro_splaceni', 'hotovo'
    ]
    workflow_counts = [0]*15
    workflow_sums = [0]*15
    # --- Časové řady ---
    # Získat posledních 7 měsíců
    today = timezone.now().date()
    months = []
    for i in range(6, -1, -1):
        m = (today.replace(day=1) - datetime.timedelta(days=30*i)).replace(day=1)
        months.append(m.strftime('%Y-%m'))
    months = sorted(list(set(months)))
    klienti_timeline = defaultdict(int)
    objem_timeline = defaultdict(float)
    for klient in klienti:
        m = klient.datum.strftime('%Y-%m')
        klienti_timeline[m] += 1
        objem_timeline[m] += float(klient.navrh_financovani_castka or 0)
    klientiTimeline = [klienti_timeline.get(m, 0) for m in months]
    objemTimeline = [objem_timeline.get(m, 0) for m in months]
    # workflow stav
    for klient in klienti:
        stav = 0
        for idx, krok in enumerate(workflow_labels[:-1]):
            if not getattr(klient, krok):
                stav = idx
                break
        else:
            stav = 14  # hotovo
        workflow_counts[stav] += 1
        workflow_sums[stav] += float(klient.navrh_financovani_castka or 0)
    # ---
    return render(request, 'klienti/home.html', {
        'klienti': klienti,
        'klienti_deadlines': klienti_deadlines,
        'today': today,
        'workflow_counts': workflow_counts,
        'workflow_sums': workflow_sums,
        'months': months,
        'klientiTimeline': klientiTimeline,
        'objemTimeline': objemTimeline,
    })

class KalkulackaForm(forms.Form):
    castka = forms.DecimalField(label="Výše úvěru", max_digits=12, decimal_places=2, min_value=10000)
    urok = forms.DecimalField(label="Úroková sazba (%)", max_digits=5, decimal_places=2, min_value=0.01)
    doba = forms.IntegerField(label="Doba splatnosti (roky)", min_value=1, max_value=40)
    fixace = forms.IntegerField(label="Doba fixace (roky)", min_value=1, max_value=40, required=False)
    mimoradne_splatky = forms.DecimalField(label="Mimořádná splátka (Kč)", max_digits=12, decimal_places=2, required=False)


def kalkulacka(request):
    vysledek = None
    if request.method == 'POST':
        form = KalkulackaForm(request.POST)
        if form.is_valid():
            castka = float(form.cleaned_data['castka'])
            urok = float(form.cleaned_data['urok']) / 100 / 12
            doba = int(form.cleaned_data['doba']) * 12
            splatka = castka * urok * pow(1 + urok, doba) / (pow(1 + urok, doba) - 1)
            celkem = splatka * doba
            urok_celkem = celkem - castka
            vysledek = {
                'splatka': round(splatka, 2),
                'celkem': round(celkem, 2),
                'urok_celkem': round(urok_celkem, 2),
            }
    else:
        form = KalkulackaForm()
    return render(request, 'klienti/kalkulacka.html', {'form': form, 'vysledek': vysledek})

def dashboard(request):
    klienti = Klient.objects.all()
    pocet_klientu = klienti.count()
    objem_hypotek = sum([k.navrh_financovani_castka or 0 for k in klienti])
    urgent_deadlines = []
    today = date.today()
    klienti_po_termínu = []
    for k in klienti:
        for field in [
            'deadline_co_financuje', 'deadline_navrh_financovani', 'deadline_vyber_banky',
            'deadline_priprava_zadosti', 'deadline_kompletace_podkladu', 'deadline_podani_zadosti',
            'deadline_odhad', 'deadline_schvalovani', 'deadline_priprava_uverove_dokumentace',
            'deadline_podpis_uverove_dokumentace', 'deadline_priprava_cerpani', 'deadline_cerpani',
            'deadline_zahajeni_splaceni', 'deadline_podminky_pro_splaceni']:
            deadline = getattr(k, field)
            splneno = getattr(k, field.replace('deadline_', 'splneno_'), None)
            if deadline and not splneno:
                if (deadline - today).days < 0:
                    klienti_po_termínu.append({'klient': k, 'krok': field, 'deadline': deadline, 'days_left': (deadline-today).days})
                elif (deadline - today).days <= 3 and (deadline - today).days >= 0:
                    urgent_deadlines.append({'klient': k, 'krok': field, 'deadline': deadline, 'days_left': (deadline-today).days})
    # --- E-mailové notifikace pro poradce ---
    poradci = User.objects.filter(userprofile__role='poradce')
    for poradce in poradci:
        if poradce.email:
            urgent_klienti = [ud for ud in urgent_deadlines]
            if urgent_klienti:
                predmet = "Upozornění: Blíží se deadline u klientů"
                zprava = "Dobrý den,\n\nU následujících klientů se blíží deadline (do 3 dnů):\n"
                for ud in urgent_klienti:
                    zprava += f"- {ud['klient'].jmeno} ({ud['krok'].replace('deadline_', '').replace('_', ' ').title()}): {ud['deadline'].strftime('%d.%m.%Y')}\n"
                zprava += "\nPřihlaste se do systému pro detailní informace.\n\nTým hypoteční aplikace"
                try:
                    odeslat_notifikaci_email(
                        prijemce=poradce.email,
                        predmet=predmet,
                        zprava=zprava,
                        context={'urgent_klienti': urgent_klienti},
                        template_name='email_deadline_notifikace.html'
                    )
                except Exception as e:
                    print(f"Chyba při odesílání e-mailu: {e}")
    # Workflow rozložení
    workflow_labels = [
        'co_financuje', 'navrh_financovani', 'vyber_banky', 'priprava_zadosti',
        'kompletace_podkladu', 'podani_zadosti', 'odhad', 'schvalovani',
        'priprava_uverove_dokumentace', 'podpis_uverove_dokumentace',
        'priprava_cerpani', 'cerpani', 'zahajeni_splaceni', 'podminky_pro_splaceni', 'hotovo'
    ]
    workflow_counts = [0]*15
    for k in klienti:
        stav = 0
        for idx, krok in enumerate(workflow_labels[:-1]):
            if not getattr(k, krok):
                stav = idx
                break
        else:
            stav = 14
        workflow_counts[stav] += 1
    posledni_klienti = klienti.order_by('-datum')[:5]
    top_hypoteky = klienti.order_by('-navrh_financovani_castka')[:5]
    # Log posledních změn
    from .models import Zmena
    posledni_zmeny = Zmena.objects.select_related('klient').order_by('-created')[:5]
    # Průměrná výše hypotéky
    prumerna_hypoteka = objem_hypotek / pocet_klientu if pocet_klientu else 0

    # --- NOVÉ AGREGACE ---
    # Rozložení podle bank
    from collections import Counter
    banky = [k.vyber_banky for k in klienti if k.vyber_banky]
    rozlozeni_banky = Counter(banky)
    banky_labels = list(rozlozeni_banky.keys())
    banky_counts = list(rozlozeni_banky.values())
    # Nejčastější důvody zamítnutí
    duvody = [k.duvod_zamitnuti for k in klienti if k.duvod_zamitnuti]
    duvody_zamitnuti = Counter(duvody).most_common(5)
    # Notifikace (např. klienti po termínu, urgentní deadliny)
    notifikace = []
    if urgent_deadlines:
        notifikace.append(f"{len(urgent_deadlines)} urgentních deadline během 3 dnů")
    if klienti_po_termínu:
        notifikace.append(f"{len(klienti_po_termínu)} klientů po termínu")
    # ...další notifikace lze přidat zde...

    return render(request, 'klienti/dashboard.html', {
        'pocet_klientu': pocet_klientu,
        'objem_hypotek': objem_hypotek,
        'urgent_deadlines': urgent_deadlines,
        'workflow_labels': workflow_labels,
        'workflow_counts': workflow_counts,
        'posledni_klienti': posledni_klienti,
        'top_hypoteky': top_hypoteky,
        'klienti_po_termínu': klienti_po_termínu,
        'posledni_zmeny': posledni_zmeny,
        'prumerna_hypoteka': prumerna_hypoteka,
        'rozlozeni_banky': dict(rozlozeni_banky),
        'banky_labels': banky_labels,
        'banky_counts': banky_counts,
        'duvody_zamitnuti': duvody_zamitnuti,
        'notifikace': notifikace,
    })

def smazat_poznamku(request, klient_id, poznamka_id):
    klient = get_object_or_404(Klient, pk=klient_id)
    poznamka = get_object_or_404(Poznamka, pk=poznamka_id, klient=klient)
    if request.method == 'POST':
        text = poznamka.text
        poznamka.delete()
        popis = f"Smazána poznámka: '{text[:50]}{'...' if len(text) > 50 else ''}'"
        Zmena.objects.create(
            klient=klient,
            popis=popis,
            author=request.user.username if request.user.is_authenticated else ''
        )
        return redirect('klient_detail', pk=klient_id)
    return redirect('klient_detail', pk=klient_id)

def get_user_role(request):
    if request.user.is_authenticated:
        try:
            return request.user.userprofile.role
        except Exception:
            return None
    return None
