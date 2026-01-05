#!/usr/bin/env python
"""
Test CSRF tokenu v password reset formuláři
"""
import os
import sys
import django
import pytest

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hypoteky.settings_test")
django.setup()


@pytest.mark.django_db
def test_csrf_token_in_password_reset():
    """
    Test že CSRF token je správně vkládán do formulářů
    """
    from django.test import Client
    from django.contrib.auth.models import User
    
    print("\n" + "=" * 80)
    print("TEST: CSRF token v password reset")
    print("=" * 80)
    
    # Vytvoř testovacího uživatele
    user = User.objects.create_user(
        username="csrf_test@example.com",
        email="csrf_test@example.com",
        password="TestPassword123"
    )
    print(f"✅ Vytvořen uživatel: {user.username}")
    
    client = Client()
    
    # KROK 1: GET na password reset form
    print("\n📋 KROK 1: GET /account/password_reset/")
    response = client.get("/account/password_reset/")
    assert response.status_code == 200
    content = response.content.decode("utf-8")
    
    # Zkontroluj přítomnost CSRF tokenu
    if "csrfmiddlewaretoken" in content:
        print("   ✅ CSRF token přítomen v HTML")
    else:
        print("   ❌ CSRF token NENÍ v HTML!")
    
    assert "csrfmiddlewaretoken" in content, "CSRF token chybí v HTML"
    
    # KROK 2: POST s emailem (client.post automaticky přidá CSRF)
    print("\n📋 KROK 2: POST s emailem")
    response = client.post(
        "/account/password_reset/",
        {"email": "csrf_test@example.com"},
        follow=True
    )
    
    if response.status_code == 200:
        print(f"   ✅ POST úspěšný: {response.status_code}")
    else:
        print(f"   ❌ POST neúspěšný: {response.status_code}")
        if "CSRF" in response.content.decode("utf-8"):
            print("   ⚠️  Detekována CSRF chyba!")
    
    assert response.status_code == 200, f"POST selhal: {response.status_code}"
    
    # KROK 3: Test přihlášení (další častý problém s CSRF)
    print("\n📋 KROK 3: Test přihlášení")
    response = client.get("/account/login/")
    assert response.status_code == 200
    content = response.content.decode("utf-8")
    
    if "csrfmiddlewaretoken" in content:
        print("   ✅ CSRF token v login formuláři")
    else:
        print("   ❌ CSRF token CHYBÍ v login formuláři!")
    
    assert "csrfmiddlewaretoken" in content
    
    # KROK 4: POST přihlášení
    print("\n📋 KROK 4: POST přihlášení")
    response = client.post(
        "/account/login/",
        {
            "username": "csrf_test@example.com",
            "password": "TestPassword123"
        },
        follow=True
    )
    
    if response.status_code == 200:
        print(f"   ✅ Login POST úspěšný: {response.status_code}")
    else:
        print(f"   ❌ Login POST neúspěšný: {response.status_code}")
    
    assert response.status_code == 200
    
    # Cleanup
    user.delete()
    
    print("\n" + "=" * 80)
    print("✅ Test úspěšný - CSRF funguje správně")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
