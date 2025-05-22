from django.shortcuts import render, redirect, get_object_or_404
from .models import Klient
from django import forms
from datetime import timedelta, date
from math import pow
from collections import defaultdict
from django.utils import timezone
import datetime

class KlientForm(forms.ModelForm):
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
        if isinstance(data, str):
            data = data.replace(' ', '').replace('\xa0', '')
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
            klient.save()
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
            klient = form.save(commit=False)
            cena = form.cleaned_data.get('cena')
            procento = form.cleaned_data.get('navrh_financovani_procento')
            if cena and procento:
                klient.navrh_financovani_castka = round(float(cena) * float(procento) / 100, 2)
            else:
                klient.navrh_financovani_castka = None
            klient.save()
            return redirect('klient_detail', pk=klient.pk)
    else:
        form = KlientForm(instance=klient)
    return render(request, 'klienti/klient_form.html', {'form': form, 'editace': True, 'klient': klient})

def klient_delete(request, pk):
    klient = get_object_or_404(Klient, pk=pk)
    if request.method == 'POST':
        klient.delete()
        return redirect('home')
    return render(request, 'klienti/klient_confirm_delete.html', {'klient': klient})

def klient_detail(request, pk):
    klient = get_object_or_404(Klient, pk=pk)
    return render(request, 'klienti/klient_detail.html', {'klient': klient})

def home(request):
    klienti = Klient.objects.all().order_by('-datum')
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
