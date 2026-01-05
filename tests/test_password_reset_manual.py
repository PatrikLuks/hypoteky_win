#!/usr/bin/env python
"""
Test manuálního password reset flow pro existující uživatele
"""
import os
import sys
import django
import pytest

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hypoteky.settings_test")
django.setup()


@pytest.mark.django_db
def test_password_reset_for_existing_user():
    """
    Test kompletního password reset flow:
    1. GET na /account/password_reset/
    2. POST s emailem
    3. Ověření odeslání emailu
    4. Extrakce tokenu z emailu
    5. GET na reset URL (s tokenem)
    6. POST nového hesla
    7. Ověření změny hesla
    """
    from django.contrib.auth.models import User
    from django.core import mail
    from django.test import Client
    import re

    print("\n" + "=" * 80)
    print("TEST: Password reset pro existujícího uživatele")
    print("=" * 80)

    # Vytvoř testovacího uživatele
    test_user = User.objects.create_user(
        username="reset_test@example.com",
        email="reset_test@example.com",
        password="OldPassword123",
        first_name="Test User"
    )
    print(f"✅ Vytvořen uživatel: {test_user.username}")

    client = Client()

    # KROK 1: GET na password reset form
    print("\n📋 KROK 1: GET /account/password_reset/")
    response = client.get("/account/password_reset/")
    assert response.status_code == 200, f"Chyba GET: {response.status_code}"
    print(f"   ✅ Status: {response.status_code}")

    # KROK 2: POST s emailem
    print("\n📋 KROK 2: POST s emailem")
    mail.outbox = []
    response = client.post(
        "/account/password_reset/",
        {"email": "reset_test@example.com"},
        follow=True
    )
    assert response.status_code == 200, f"Chyba POST: {response.status_code}"
    print(f"   ✅ Status: {response.status_code}")

    # KROK 3: Ověření emailu
    print("\n📋 KROK 3: Ověření odeslání emailu")
    assert len(mail.outbox) > 0, "Email nebyl odeslán"
    email = mail.outbox[0]
    print(f"   ✅ Email odeslán")
    print(f"   Předmět: {email.subject}")
    print(f"   Příjemce: {email.to}")

    # KROK 4: Extrakce tokenu
    print("\n📋 KROK 4: Extrakce tokenu z emailu")
    body = email.body
    match = re.search(r"/account/reset/([^/]+)/([^/]+)/", body)
    assert match, "Token nebyl nalezen v emailu"
    uid = match.group(1)
    token = match.group(2)
    print(f"   ✅ Token nalezen: {token[:10]}...")

    # KROK 5: GET na reset URL
    reset_url = f"/account/reset/{uid}/{token}/"
    print(f"\n📋 KROK 5: GET {reset_url}")
    response = client.get(reset_url)
    print(f"   Status: {response.status_code}")

    # Django dělá redirect na /account/reset/<uidb64>/set-password/
    if response.status_code == 302:
        redirect_url = response["Location"]
        print(f"   Redirect na: {redirect_url}")
        response = client.get(redirect_url)
        print(f"   Status po redirectu: {response.status_code}")
        assert response.status_code == 200, f"Chyba při redirectu: {response.status_code}"
    else:
        redirect_url = reset_url

    # KROK 6: POST nového hesla
    print(f"\n📋 KROK 6: POST nového hesla")
    response = client.post(
        redirect_url,
        {
            "new_password1": "NewSecurePass123",
            "new_password2": "NewSecurePass123"
        }
    )
    print(f"   Status: {response.status_code}")

    # KROK 7: Ověření změny hesla
    print(f"\n📋 KROK 7: Ověření změny hesla")
    test_user.refresh_from_db()
    assert test_user.check_password("NewSecurePass123"), "Heslo nebylo změněno!"
    print("   ✅ Heslo bylo úspěšně změněno!")

    # Cleanup
    test_user.delete()

    print("\n" + "=" * 80)
    print("✅ Test úspěšný - password reset funguje správně")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
