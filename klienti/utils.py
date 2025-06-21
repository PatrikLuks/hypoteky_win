from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from .models import NotifikaceLog, Klient
import csv
from typing import IO
import datetime
import openpyxl

def odeslat_notifikaci_email(prijemce, predmet, zprava, html_zprava=None, context=None, template_name=None, typ='deadline', klient=None):
    """
    Odeslání e-mailové notifikace s logováním do NotifikaceLog.
    """
    html_message = html_zprava
    if template_name and context:
        html_message = render_to_string(template_name, context)
    uspesne = True
    try:
        send_mail(
            subject=predmet,
            message=zprava,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[prijemce],
            html_message=html_message,
            fail_silently=False,
        )
    except Exception as e:
        uspesne = False
    NotifikaceLog.objects.create(
        prijemce=prijemce,
        typ=typ,
        klient=klient,
        obsah=zprava,
        uspesne=uspesne
    )

def import_klienti_from_csv(file: IO, encoding: str = 'utf-8') -> int:
    """
    Načte klienty z CSV souboru a uloží je do DB.
    Očekává hlavičku: jmeno,datum,vyber_banky,navrh_financovani_castka,duvod_zamitnuti,co_financuje,navrh_financovani,navrh_financovani_procento,cena
    Vrací počet úspěšně importovaných klientů (nově vytvořených nebo aktualizovaných).
    Robustně ošetřuje poškozené nebo nevalidní CSV soubory – nikdy nespadne, pouze zaloguje chybu a přeskočí řádek.
    """
    import logging
    logger = logging.getLogger("klienti.import")
    try:
        reader = csv.DictReader((line.decode(encoding) if isinstance(line, bytes) else line for line in file))
    except Exception as e:
        logger.error(f"[IMPORT] Chyba při čtení CSV: {e}")
        print(f"[IMPORT] Chyba při čtení CSV: {e}")
        return 0
    count = 0
    imported_keys = set()  # Sada (jmeno, datum) pro detekci duplicit v rámci dávky
    try:
        for idx, row in enumerate(reader):
            try:
                print(f"[IMPORT] Zpracovávám řádek {idx+1}: {row}")
                if not row.get('jmeno'):
                    print(f"[IMPORT] Řádek {idx+1} přeskočen - chybí jméno")
                    continue  # povinné pole
                if not row.get('vyber_banky'):
                    print(f"[IMPORT] Řádek {idx+1} přeskočen - chybí vyber_banky")
                    continue  # povinné pole
                # --- Validace povinného pole datum ---
                jmeno = row['jmeno'].strip() if row.get('jmeno') else ''
                datum_str = row.get('datum', '').strip()
                try:
                    datum = datetime.datetime.strptime(datum_str, '%Y-%m-%d').date()
                except Exception:
                    print(f"[IMPORT] Chyba při převodu datumu: {datum_str}")
                    print(f"[IMPORT] Řádek {idx+1} přeskočen - chybí nebo je nevalidní datum")
                    continue
                key = (jmeno, datum)
                if key in imported_keys:
                    print(f"[IMPORT] Řádek {idx+1} přeskočen - duplicitní klient v dávce (jméno+datum)")
                    continue
                if Klient.objects.filter(jmeno=jmeno, datum=datum).exists():
                    print(f"[IMPORT] Řádek {idx+1} přeskočen - duplicitní klient v DB (jméno+datum)")
                    continue
                imported_keys.add(key)
                castka = None
                if row.get('navrh_financovani_castka'):
                    try:
                        castka = int(row['navrh_financovani_castka'])
                    except Exception as e:
                        print(f"[IMPORT] Chyba při převodu částky: {row['navrh_financovani_castka']} ({e})")
                cena = None
                if row.get('cena'):
                    try:
                        cena = float(row['cena'])
                    except Exception as e:
                        print(f"[IMPORT] Chyba při převodu ceny: {row['cena']} ({e})")
                procento = None
                if row.get('navrh_financovani_procento'):
                    try:
                        procento = float(row['navrh_financovani_procento'])
                    except Exception as e:
                        print(f"[IMPORT] Chyba při převodu procenta: {row['navrh_financovani_procento']} ({e})")
                klient = Klient(
                    jmeno=jmeno,
                    datum=datum,
                    vyber_banky=row.get('vyber_banky'),
                    navrh_financovani_castka=castka,
                    duvod_zamitnuti=row.get('duvod_zamitnuti') or None,
                    co_financuje=row.get('co_financuje') or '',
                    navrh_financovani=row.get('navrh_financovani') or '',
                    navrh_financovani_procento=procento,
                    cena=cena,
                )
                klient.save()
                print(f"[IMPORT] Klient vytvořen: {klient.jmeno}")
                count += 1
            except Exception as e:
                logger.error(f"[IMPORT] Chyba při zpracování řádku {idx+1}: {e}")
                print(f"[IMPORT] Chyba při zpracování řádku {idx+1}: {e}")
                continue
    except Exception as e:
        logger.error(f"[IMPORT] Chyba při čtení CSV v průběhu zpracování: {e}")
        print(f"[IMPORT] Chyba při čtení CSV v průběhu zpracování: {e}")
        return count
    print(f"[IMPORT] Celkem importováno/aktualizováno klientů: {count}")
    print("[IMPORT] Klienti v DB po importu:")
    for k in Klient.objects.all():
        print(f"  - {k.pk}: {k.jmeno}, vyber_banky={getattr(k, 'vyber_banky', None)}, duvod_zamitnuti={getattr(k, 'duvod_zamitnuti', None)}")
    return count

def import_klienti_from_xlsx(file: IO) -> int:
    """
    Načte klienty z XLSX souboru a uloží je do DB.
    Očekává hlavičku: jmeno,datum,vyber_banky,navrh_financovani_castka,duvod_zamitnuti,co_financuje,navrh_financovani,navrh_financovani_procento,cena
    Vrací počet úspěšně importovaných klientů (nově vytvořených nebo aktualizovaných).
    """
    wb = openpyxl.load_workbook(file)
    ws = wb.active
    headers = [cell.value for cell in next(ws.iter_rows(min_row=1, max_row=1))]
    count = 0
    imported_keys = set()  # Sada (jmeno, datum) pro detekci duplicit v rámci dávky
    for idx, row in enumerate(ws.iter_rows(min_row=2), start=2):
        row_data = {headers[i]: (cell.value if cell.value is not None else '') for i, cell in enumerate(row)}
        print(f"[IMPORT XLSX] Zpracovávám řádek {idx}: {row_data}")
        if not row_data.get('jmeno'):
            print(f"[IMPORT XLSX] Řádek {idx} přeskočen - chybí jméno")
            continue
        jmeno = row_data['jmeno'].strip()
        # Validace délky jména podle modelu (max_length=100)
        if len(jmeno) > 100:
            print(f"[IMPORT XLSX] VAROVÁNÍ: Jméno je delší než 100 znaků, bude zkráceno. Původní: {jmeno}")
            jmeno = jmeno[:100]
        datum = None
        if row_data.get('datum'):
            try:
                datum = row_data['datum']
                if isinstance(datum, str):
                    datum = datetime.datetime.strptime(datum, '%Y-%m-%d').date()
                elif isinstance(datum, datetime.datetime):
                    datum = datum.date()
            except Exception as e:
                print(f"[IMPORT XLSX] Chyba při převodu datumu: {row_data['datum']} ({e})")
        if not datum:
            print(f"[IMPORT XLSX] Řádek {idx} přeskočen - chybí nebo je nevalidní datum")
            continue
        key = (jmeno, datum)
        if key in imported_keys:
            print(f"[IMPORT XLSX] Řádek {idx} přeskočen - duplicitní klient v dávce (jméno+datum)")
            continue
        if Klient.objects.filter(jmeno=jmeno, datum=datum).exists():
            print(f"[IMPORT XLSX] Řádek {idx} přeskočen - duplicitní klient v DB (jméno+datum)")
            continue
        imported_keys.add(key)
        castka = None
        if row_data.get('navrh_financovani_castka'):
            try:
                castka = int(row_data['navrh_financovani_castka'])
            except Exception as e:
                print(f"[IMPORT XLSX] Chyba při převodu částky: {row_data['navrh_financovani_castka']} ({e})")
        # Oprava: správně rozpoznat nulu i prázdné hodnoty pro pole cena
        cena = None
        if row_data.get('cena') is not None and row_data.get('cena') != '':
            try:
                cena = float(row_data['cena'])
            except Exception as e:
                print(f"[IMPORT XLSX] Chyba při převodu ceny: {row_data['cena']} ({e})")
        procento = None
        if row_data.get('navrh_financovani_procento'):
            try:
                procento = float(row_data['navrh_financovani_procento'])
            except Exception as e:
                print(f"[IMPORT XLSX] Chyba při převodu procenta: {row_data['navrh_financovani_procento']} ({e})")
        klient, created = Klient.objects.get_or_create(
            jmeno=jmeno,
            defaults={
                'datum': datum,
                'vyber_banky': row_data.get('vyber_banky'),
                'navrh_financovani_castka': castka,
                'duvod_zamitnuti': row_data.get('duvod_zamitnuti') or None,
                'co_financuje': row_data.get('co_financuje') or '',
                'navrh_financovani': row_data.get('navrh_financovani') or '',
                'navrh_financovani_procento': procento,
                'cena': cena if cena is not None else 0,
            }
        )
        if not created:
            klient.datum = datum or klient.datum
            klient.vyber_banky = row_data.get('vyber_banky') or klient.vyber_banky
            klient.navrh_financovani_castka = castka if castka is not None else klient.navrh_financovani_castka
            klient.duvod_zamitnuti = row_data.get('duvod_zamitnuti') or klient.duvod_zamitnuti
            klient.co_financuje = row_data.get('co_financuje') or klient.co_financuje
            klient.navrh_financovani = row_data.get('navrh_financovani') or klient.navrh_financovani
            klient.navrh_financovani_procento = procento if procento is not None else klient.navrh_financovani_procento
            klient.cena = cena if cena is not None else klient.cena
            klient.save()
            print(f"[IMPORT XLSX] Klient aktualizován: {klient.jmeno}")
        else:
            print(f"[IMPORT XLSX] Klient vytvořen: {klient.jmeno}")
        count += 1
    print(f"[IMPORT XLSX] Celkem importováno/aktualizováno klientů: {count}")
    return count
