#!/usr/bin/env python
"""
Test: Kompletní workflow - vytvoření klienta, odeslání emailu, test URL
"""
import os
import sys
import django
import pytest

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hypoteky.settings")
os.environ["EMAIL_BACKEND"] = "django.core.mail.backends.locmem.EmailBackend"
django.setup()

from django.contrib.auth.models import User
from django.core import mail
from django.test import Client
from klienti.models import Klient, UserProfile
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
import re

print("\n" + "="*80)
print("TEST: Kompletní workflow s ověřením URL")
print("="*80 + "\n")

# Cleanup - označíme pro pytest (ale nevoláme zde, voláme v testech)

# 1. Vytvoř poradce
print("📋 FÁZE 1: Vytvoření poradce")
poradce = User.objects.create_user(username="test_complete_poradce", password="test123")
profile, _ = UserProfile.objects.get_or_create(user=poradce)
profile.role = "poradce"
profile.save()
print(f"✅ Poradce vytvořen: {poradce.username}")

# 2. Vyčisti mail outbox
mail.outbox = []

# 3. Vytvoř klienta
print("\n📋 FÁZE 2: Vytvoření klienta s emailem")
klient = Klient.objects.create(
    jmeno="Test Complete Klient",
    email="test_complete@example.com",
    user=None
)
print(f"✅ Klient vytvořen: {klient.jmeno}")
print(f"✅ User vytvořen: {klient.user.username}")
print(f"✅ User ID: {klient.user.pk}")

# 4. Zkontroluj email
print("\n📋 FÁZE 3: Kontrola emailu")
if not mail.outbox:
    print("❌ Email nebyl odeslán!")
    sys.exit(1)

email = mail.outbox[0]
print(f"✅ Email odeslán")
print(f"   Předmět: {email.subject}")
print(f"   Příjemce: {email.to}")

# 5. Extrahuj URL z emailu
print("\n📋 FÁZE 4: Extrakce URL z emailu")
email_body = email.body
url_match = re.search(r'http://[^\s]+/account/reset/[^\s]+', email_body)
if not url_match:
    print("❌ URL nebyla nalezena v emailu!")
    print("Email body:", email_body[:500])
    sys.exit(1)

reset_url = url_match.group(0)
print(f"✅ URL nalezena: {reset_url}")

# 6. Extrahuj uidb64 a token z URL
url_parts = reset_url.split('/')
uidb64 = url_parts[-3]
token = url_parts[-2]
print(f"   UID: {uidb64}")
print(f"   Token: {token}")

# 7. Ověř token manuálně
print("\n📋 FÁZE 5: Ověření tokenu")
user = klient.user
is_valid = default_token_generator.check_token(user, token)
print(f"✅ Token validní: {is_valid}")

if not is_valid:
    print("⚠️  Token není validní!")
    print("   Možné příčiny:")
    print("   - Token byl vygenerován pro jiného uživatele")
    print("   - Token expiroval")
    print("   - Heslo uživatele bylo mezitím změněno")

# 8. Otestuj HTTP request na URL
print("\n📋 FÁZE 6: HTTP GET request na reset URL")
client = Client()
path = f"/account/reset/{uidb64}/{token}/"
response = client.get(path, follow=False)
print(f"✅ HTTP Status: {response.status_code}")
print(f"✅ URL: {path}")

if response.status_code == 302:
    print(f"⚠️  Redirect na: {response.url}")
    if 'login' in response.url:
        print("❌ PROBLÉM: Redirect na login - token pravděpodobně není validní")
    else:
        print("✅ Redirect OK (pravděpodobně na formulář pro nastavení hesla)")
elif response.status_code == 200:
    print("✅ Stránka se načetla (formulář pro nastavení hesla)")
else:
    print(f"⚠️  Neočekávaný status code: {response.status_code}")

# 9. Zkus follow redirects
print("\n📋 FÁZE 7: HTTP request s follow=True")
response_follow = client.get(path, follow=True)
print(f"✅ Finální URL: {response_follow.request['PATH_INFO']}")
print(f"✅ HTTP Status: {response_follow.status_code}")

if 'login' in response_follow.request['PATH_INFO']:
    print("❌ PROBLÉM POTVRZEN: Končí na login page")
else:
    print("✅ Nekončí na login - měl by být formulář pro nastavení hesla")

# Cleanup
print("\n" + "="*80)
print("🧹 Cleanup")
klient.delete()
poradce.delete()
print("✅ Testovací data smazána")
print("="*80 + "\n")
