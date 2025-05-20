from django.shortcuts import render, redirect, get_object_or_404
from .models import Klient
from django import forms
from datetime import timedelta, date

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
            'datum': forms.DateInput(attrs={'type': 'date'}),
            'cena': forms.TextInput(attrs={'inputmode': 'numeric', 'pattern': '[0-9 ]*', 'placeholder': 'např. 12 200 000'}),
            'navrh_financovani_procento': forms.NumberInput(attrs={'step': '0.01', 'min': '0', 'max': '100', 'placeholder': 'např. 80'}),
            'deadline_co_financuje': forms.DateInput(attrs={'type': 'date'}),
            'deadline_navrh_financovani': forms.DateInput(attrs={'type': 'date'}),
            'deadline_vyber_banky': forms.DateInput(attrs={'type': 'date'}),
            'deadline_priprava_zadosti': forms.DateInput(attrs={'type': 'date'}),
            'deadline_kompletace_podkladu': forms.DateInput(attrs={'type': 'date'}),
            'deadline_podani_zadosti': forms.DateInput(attrs={'type': 'date'}),
            'deadline_odhad': forms.DateInput(attrs={'type': 'date'}),
            'deadline_schvalovani': forms.DateInput(attrs={'type': 'date'}),
            'deadline_priprava_uverove_dokumentace': forms.DateInput(attrs={'type': 'date'}),
            'deadline_podpis_uverove_dokumentace': forms.DateInput(attrs={'type': 'date'}),
            'deadline_priprava_cerpani': forms.DateInput(attrs={'type': 'date'}),
            'deadline_cerpani': forms.DateInput(attrs={'type': 'date'}),
            'deadline_zahajeni_splaceni': forms.DateInput(attrs={'type': 'date'}),
            'deadline_podminky_pro_splaceni': forms.DateInput(attrs={'type': 'date'}),
            'splneno_co_financuje': forms.DateInput(attrs={'type': 'date'}),
            'splneno_navrh_financovani': forms.DateInput(attrs={'type': 'date'}),
            'splneno_vyber_banky': forms.DateInput(attrs={'type': 'date'}),
            'splneno_priprava_zadosti': forms.DateInput(attrs={'type': 'date'}),
            'splneno_kompletace_podkladu': forms.DateInput(attrs={'type': 'date'}),
            'splneno_podani_zadosti': forms.DateInput(attrs={'type': 'date'}),
            'splneno_odhad': forms.DateInput(attrs={'type': 'date'}),
            'splneno_schvalovani': forms.DateInput(attrs={'type': 'date'}),
            'splneno_priprava_uverove_dokumentace': forms.DateInput(attrs={'type': 'date'}),
            'splneno_podpis_uverove_dokumentace': forms.DateInput(attrs={'type': 'date'}),
            'splneno_priprava_cerpani': forms.DateInput(attrs={'type': 'date'}),
            'splneno_cerpani': forms.DateInput(attrs={'type': 'date'}),
            'splneno_zahajeni_splaceni': forms.DateInput(attrs={'type': 'date'}),
            'splneno_podminky_pro_splaceni': forms.DateInput(attrs={'type': 'date'}),
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
    return render(request, 'klienti/home.html', {'klienti': klienti, 'klienti_deadlines': klienti_deadlines, 'today': today})
