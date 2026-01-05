#!/usr/bin/env python
"""
Test unikátnosti emailů pro klienty
"""
import os
import sys
import django
import pytest

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hypoteky.settings_test")
django.setup()


@pytest.mark.django_db
def test_email_must_be_unique():
    """
    Test že email musí být unikátní - nelze vytvořit dva klienty se stejným emailem
    """
    from django.contrib.auth.models import User
    from django.core.exceptions import ValidationError
    from klienti.models import Klient

    print("\n" + "=" * 80)
    print("TEST: Unikátnost emailu pro klienty")
    print("=" * 80)

    # KROK 1: Vytvoř prvního klienta s emailem
    print("\n📋 KROK 1: Vytvoření prvního klienta")
    klient1 = Klient.objects.create(
        jmeno="Jan Novák",
        email="test@example.com",
        user=None
    )
    print(f"   ✅ Vytvořen klient 1: {klient1.jmeno}")
    print(f"   Username: {klient1.user.username}")
    assert klient1.user.username == "test@example.com", "Username by měl být email"

    # KROK 2: Pokus o vytvoření druhého klienta se stejným emailem
    print("\n📋 KROK 2: Pokus o vytvoření druhého klienta se stejným emailem")
    try:
        klient2 = Klient.objects.create(
            jmeno="Petr Svoboda",
            email="test@example.com",
            user=None
        )
        print(f"   ❌ CHYBA: Povedlo se vytvořit druhého klienta!")
        print(f"   Username klient2: {klient2.user.username}")
        assert False, "Nemělo by být možné vytvořit klienta s duplicitním emailem"
    except ValidationError as e:
        print(f"   ✅ Správně vyvolána ValidationError: {e}")
        assert "již používán" in str(e).lower()

    # KROK 3: Smazání prvního klienta
    print("\n📋 KROK 3: Smazání prvního klienta")
    user1_id = klient1.user.id
    klient1.delete()
    print(f"   ✅ Klient 1 smazán")

    # Zkontroluj zda byl smazán i User (pokud používáme CASCADE)
    user_exists = User.objects.filter(id=user1_id).exists()
    if user_exists:
        print(f"   ⚠️  User stále existuje (id={user1_id})")
    else:
        print(f"   ✅ User byl také smazán (id={user1_id})")

    # KROK 4: Vytvoření nového klienta se stejným emailem po smazání
    print("\n📋 KROK 4: Vytvoření nového klienta po smazání prvního")
    klient3 = Klient.objects.create(
        jmeno="Marie Nová",
        email="test@example.com",
        user=None
    )
    print(f"   ✅ Vytvořen klient 3: {klient3.jmeno}")
    print(f"   Username: {klient3.user.username}")
    assert klient3.user.username == "test@example.com", "Username by měl být email (bez _1)"

    # Cleanup
    klient3.delete()

    print("\n" + "=" * 80)
    print("✅ Test úspěšný - email je unikátní a po smazání znovu použitelný")
    print("=" * 80 + "\n")


@pytest.mark.django_db
def test_reuse_orphaned_user():
    """
    Test že pokud existuje User bez klienta, použije se pro nového klienta
    """
    from django.contrib.auth.models import User
    from klienti.models import Klient

    print("\n" + "=" * 80)
    print("TEST: Znovupoužití osiřelého User účtu")
    print("=" * 80)

    # KROK 1: Vytvoř User bez klienta
    print("\n📋 KROK 1: Vytvoření User bez klienta")
    orphaned_user = User.objects.create_user(
        username="orphan@example.com",
        email="orphan@example.com",
        first_name="Starý uživatel"
    )
    print(f"   ✅ Vytvořen User: {orphaned_user.username}")

    # KROK 2: Vytvoř klienta se stejným emailem
    print("\n📋 KROK 2: Vytvoření klienta se stejným emailem")
    klient = Klient.objects.create(
        jmeno="Nový klient",
        email="orphan@example.com",
        user=None
    )
    print(f"   ✅ Vytvořen klient: {klient.jmeno}")
    print(f"   User ID klienta: {klient.user.id}")
    print(f"   Orphaned User ID: {orphaned_user.id}")

    # Ověř že se použil existující User
    assert klient.user.id == orphaned_user.id, "Měl se použít existující User"
    print(f"   ✅ Použit existující User (id={orphaned_user.id})")

    # Ověř že se aktualizovalo jméno
    klient.user.refresh_from_db()
    assert klient.user.first_name == "Nový klient", "Mělo se aktualizovat jméno"
    print(f"   ✅ Jméno aktualizováno: {klient.user.first_name}")

    # Cleanup
    klient.delete()

    print("\n" + "=" * 80)
    print("✅ Test úspěšný - osiřelý User se znovu použil")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
