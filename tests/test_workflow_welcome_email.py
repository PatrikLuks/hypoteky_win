#!/usr/bin/env python
"""
Test workflow: Smazání a znovu vytvoření klienta - ověření welcome emailu
"""
import os
import sys
import django
import pytest

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hypoteky.settings_test")
django.setup()


@pytest.mark.django_db
def test_delete_and_recreate_client_sends_welcome_email():
    """
    Test workflow:
    1. Vytvoř klienta Patrik Luks s emailem
    2. Smaž klienta
    3. Vytvoř znovu klienta Patrik Luks se stejným emailem
    4. Ověř, že welcome email byl odeslán i podruhé
    """
    from django.contrib.auth.models import User
    from django.core import mail
    from klienti.models import Klient

    print("\n" + "=" * 80)
    print("TEST: Smazání a znovu vytvoření klienta - welcome email")
    print("=" * 80)

    # KROK 1: Vytvoř prvního klienta
    print("\n📋 KROK 1: Vytvoření prvního klienta")
    mail.outbox = []
    klient1 = Klient.objects.create(
        jmeno="Patrik Luks",
        email="patrik.luks@example.com",
        user=None
    )
    print(f"   ✅ Vytvořen klient: {klient1.jmeno}")
    print(f"   User ID: {klient1.user.id}")
    print(f"   Username: {klient1.user.username}")
    
    # Ověř první welcome email
    assert len(mail.outbox) == 1, "První welcome email nebyl odeslán"
    print(f"   ✅ První welcome email odeslán")
    first_email = mail.outbox[0]
    print(f"   Předmět: {first_email.subject}")

    # KROK 2: Smazání klienta
    print("\n📋 KROK 2: Smazání klienta")
    user_id = klient1.user.id
    username = klient1.user.username
    klient1.delete()
    print(f"   ✅ Klient smazán")
    
    # Zkontroluj zda User stále existuje
    user_still_exists = User.objects.filter(id=user_id).exists()
    if user_still_exists:
        print(f"   ℹ️  User stále existuje v DB (id={user_id})")
        orphaned_user = User.objects.get(id=user_id)
        has_clients = Klient.objects.filter(user=orphaned_user).exists()
        print(f"   ℹ️  User má klienty: {has_clients}")
    else:
        print(f"   ℹ️  User byl smazán (id={user_id})")

    # KROK 3: Vytvoř znovu klienta se stejným emailem
    print("\n📋 KROK 3: Vytvoření nového klienta se stejným emailem")
    mail.outbox = []  # Vyčisti mailbox
    klient2 = Klient.objects.create(
        jmeno="Patrik Luks",
        email="patrik.luks@example.com",
        user=None
    )
    print(f"   ✅ Vytvořen nový klient: {klient2.jmeno}")
    print(f"   User ID: {klient2.user.id}")
    print(f"   Username: {klient2.user.username}")

    # KROK 4: Ověř druhý welcome email
    print("\n📋 KROK 4: Ověření druhého welcome emailu")
    if len(mail.outbox) == 0:
        print(f"   ❌ CHYBA: Žádný email nebyl odeslán!")
        print(f"   Mail.outbox je prázdný")
        assert False, "Druhý welcome email nebyl odeslán"
    else:
        print(f"   ✅ Druhý welcome email byl odeslán")
        second_email = mail.outbox[0]
        print(f"   Předmět: {second_email.subject}")
        print(f"   Příjemce: {second_email.to}")
        
        # Ověř že email obsahuje reset link
        assert "account/reset/" in second_email.body, "Email neobsahuje reset link"
        print(f"   ✅ Email obsahuje password reset link")

    # Cleanup
    klient2.delete()

    print("\n" + "=" * 80)
    print("✅ Test úspěšný - welcome email funguje i po smazání a vytvoření")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
