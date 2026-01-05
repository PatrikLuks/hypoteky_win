#!/usr/bin/env python
"""
Test export deadlinů do kalendáře (iCal formát)
"""
import os
import sys
import django
import pytest

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hypoteky.settings_test")
django.setup()


@pytest.mark.django_db
def test_export_klient_ical_with_deadlines():
    """
    Test export deadlinů klienta do iCal formátu
    """
    from django.test import Client
    from django.contrib.auth.models import User
    from klienti.models import Klient, UserProfile
    from datetime import date, timedelta
    import re

    print("\n" + "=" * 80)
    print("TEST: Export deadlinů do kalendáře (iCal)")
    print("=" * 80)

    # KROK 1: Vytvoř poradce
    print("\n📋 KROK 1: Vytvoření poradce")
    poradce = User.objects.create_user(username="poradce_test", password="test123")
    profile, _ = UserProfile.objects.get_or_create(user=poradce)
    profile.role = "poradce"
    profile.save()
    print(f"   ✅ Poradce vytvořen: {poradce.username}")

    # KROK 2: Vytvoř klienta s deadliny
    print("\n📋 KROK 2: Vytvoření klienta s deadliny")
    today = date.today()
    klient = Klient.objects.create(
        jmeno="Test Klient",
        email="test@example.com",
        deadline_co_financuje=today + timedelta(days=7),
        deadline_navrh_financovani=today + timedelta(days=14),
        deadline_vyber_banky=today + timedelta(days=21),
        deadline_schvalene_financovani=today + timedelta(days=30),
        user=None
    )
    print(f"   ✅ Klient vytvořen: {klient.jmeno}")
    print(f"   Počet deadlinů: 4")

    # KROK 3: Přihlásit se a stáhnout iCal
    print("\n📋 KROK 3: Přihlášení a stažení iCal souboru")
    client = Client()
    login_success = client.login(username="poradce_test", password="test123")
    assert login_success, "Přihlášení se nezdařilo"
    print(f"   ✅ Přihlášen jako poradce")

    # KROK 4: GET na export URL
    print("\n📋 KROK 4: Stažení iCal souboru")
    response = client.get(f"/klient/{klient.pk}/ical/")
    print(f"   Status: {response.status_code}")
    assert response.status_code == 200, f"Chyba: {response.status_code}"
    print(f"   ✅ iCal soubor stažen")

    # KROK 5: Kontrola Content-Type
    print("\n📋 KROK 5: Kontrola Content-Type")
    content_type = response.get("Content-Type")
    print(f"   Content-Type: {content_type}")
    assert "text/calendar" in content_type, f"Špatný Content-Type: {content_type}"
    print(f"   ✅ Content-Type je správný (text/calendar)")

    # KROK 6: Kontrola Content-Disposition
    print("\n📋 KROK 6: Kontrola Content-Disposition")
    disposition = response.get("Content-Disposition")
    print(f"   Disposition: {disposition}")
    assert "attachment" in disposition, f"Není attachment: {disposition}"
    assert ".ics" in disposition, f"Není .ics: {disposition}"
    print(f"   ✅ Soubor je attachment s .ics")

    # KROK 7: Kontrola obsahu iCal
    print("\n📋 KROK 7: Kontrola obsahu iCal")
    content = response.content.decode("utf-8")
    
    # Kontrola základní struktury
    assert "BEGIN:VCALENDAR" in content, "Chybí BEGIN:VCALENDAR"
    assert "END:VCALENDAR" in content, "Chybí END:VCALENDAR"
    assert "BEGIN:VEVENT" in content, "Chybí BEGIN:VEVENT"
    assert "END:VEVENT" in content, "Chybí END:VEVENT"
    print(f"   ✅ iCal má správnou strukturu")

    # KROK 8: Kontrola počtu eventů
    print("\n📋 KROK 8: Kontrola počtu eventů")
    event_count = content.count("BEGIN:VEVENT")
    print(f"   Počet eventů: {event_count}")
    # Máme 4 deadliny, takže 4 eventy
    assert event_count == 4, f"Očekáváno 4 eventy, bylo {event_count}"
    print(f"   ✅ Počet eventů je správný")

    # KROK 9: Kontrola obsahu eventů
    print("\n📋 KROK 9: Kontrola obsahu eventů")
    assert "Co chce klient financovat" in content, "Chybí první deadline"
    assert "Návrh financování" in content, "Chybí druhý deadline"
    assert "Výběr banky" in content, "Chybí třetí deadline"
    assert "Schválené financování" in content, "Chybí čtvrtý deadline"
    print(f"   ✅ Všechny deadliny jsou v iCal")

    # KROK 10: Kontrola UID
    print("\n📋 KROK 10: Kontrola UID")
    uid_pattern = r"UID:[^@]+@hypoteky\.cz"
    uids = re.findall(uid_pattern, content)
    print(f"   Počet UID: {len(uids)}")
    assert len(uids) == 4, f"Očekáváno 4 UID, bylo {len(uids)}"
    print(f"   ✅ UID jsou správně generovány")

    # Cleanup
    klient.delete()
    poradce.delete()

    print("\n" + "=" * 80)
    print("✅ Test úspěšný - export do kalendáře funguje")
    print("=" * 80 + "\n")


@pytest.mark.django_db
def test_export_klient_ical_bez_deadlinu():
    """
    Test export klienta bez deadlinů (měl by být prázdný iCal)
    """
    from django.test import Client
    from django.contrib.auth.models import User
    from klienti.models import Klient, UserProfile

    print("\n" + "=" * 80)
    print("TEST: Export klienta bez deadlinů")
    print("=" * 80)

    # Vytvoř poradce
    poradce = User.objects.create_user(username="poradce_test2", password="test123")
    profile, _ = UserProfile.objects.get_or_create(user=poradce)
    profile.role = "poradce"
    profile.save()

    # Vytvoř klienta BEZ deadlinů
    print("\n📋 Vytvoření klienta bez deadlinů")
    klient = Klient.objects.create(
        jmeno="Test Klient Bez Deadline",
        email="test2@example.com",
        user=None
    )
    print(f"   ✅ Klient vytvořen bez deadlinů")

    # Přihlášení
    client = Client()
    client.login(username="poradce_test2", password="test123")

    # GET na export URL
    print("\n📋 Stažení iCal souboru")
    response = client.get(f"/klient/{klient.pk}/ical/")
    assert response.status_code == 200
    content = response.content.decode("utf-8")
    
    # Ověř že iCal je validní, ale bez eventů
    print("\n📋 Kontrola obsahu")
    assert "BEGIN:VCALENDAR" in content, "Chybí VCALENDAR"
    assert "END:VCALENDAR" in content, "Chybí END:VCALENDAR"
    
    event_count = content.count("BEGIN:VEVENT")
    print(f"   Počet eventů: {event_count}")
    assert event_count == 0, f"Očekáváno 0 eventů, bylo {event_count}"
    print(f"   ✅ iCal je validní, ale bez eventů")

    # Cleanup
    klient.delete()
    poradce.delete()

    print("\n" + "=" * 80)
    print("✅ Test úspěšný - export bez deadlinů funguje")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
