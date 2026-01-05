#!/usr/bin/env python
"""
Test zobrazení jména klienta v horní liště
"""
import os
import sys
import django
import pytest

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hypoteky.settings_test")
django.setup()


@pytest.mark.django_db
def test_klient_vidi_sve_jmeno_v_horni_liste():
    """
    Test že klient vidí své skutečné jméno (s diakritikou a mezerami)
    v horní liště místo emailu nebo normalizovaného jména.
    """
    from django.contrib.auth.models import User
    from django.test import Client
    from klienti.models import Klient, UserProfile

    print("\n" + "=" * 80)
    print("TEST: Klient vidí své jméno v horní liště")
    print("=" * 80)

    # Vytvoř klienta s diakritikou a mezerami
    print("\n📋 KROK 1: Vytvoření klienta")
    klient = Klient.objects.create(
        jmeno="Patrik Lukš",  # Jméno s diakritikou
        email="patrik.luks@example.com",
        user=None
    )
    
    print(f"   ✅ Vytvořen klient: {klient.jmeno}")
    print(f"   User username: {klient.user.username}")
    print(f"   User first_name: {klient.user.first_name}")
    
    # Přihlásit se jako klient
    print("\n📋 KROK 2: Přihlášení jako klient")
    client = Client()
    klient.user.set_password("TestHeslo123")
    klient.user.save()
    
    login_success = client.login(
        username=klient.user.username,
        password="TestHeslo123"
    )
    assert login_success, "Přihlášení se nezdařilo"
    print(f"   ✅ Přihlášen jako: {klient.user.username}")
    
    # Načti hlavní stránku
    print("\n📋 KROK 3: Načtení hlavní stránky")
    response = client.get("/")
    assert response.status_code == 200, f"Chyba: {response.status_code}"
    print(f"   ✅ Status: {response.status_code}")
    
    # Zkontroluj že stránka obsahuje skutečné jméno
    print("\n📋 KROK 4: Kontrola zobrazení jména")
    content = response.content.decode("utf-8")
    
    if "Patrik Lukš" in content:
        print(f"   ✅ ÚSPĚCH: Jméno 'Patrik Lukš' je zobrazeno v HTML!")
    else:
        print(f"   ❌ CHYBA: Jméno 'Patrik Lukš' NENÍ zobrazeno")
        print(f"   Hledám v HTML...")
        
        # Zkontroluj co je zobrazeno místo toho
        if klient.user.username in content:
            print(f"   ⚠️  Zobrazeno username: {klient.user.username}")
        if klient.user.first_name in content:
            print(f"   ⚠️  Zobrazeno first_name: {klient.user.first_name}")
    
    assert "Patrik Lukš" in content, "Skutečné jméno klienta není zobrazeno v horní liště"
    
    # Cleanup
    klient.delete()
    
    print("\n" + "=" * 80)
    print("✅ Test úspěšný - klient vidí své skutečné jméno")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
