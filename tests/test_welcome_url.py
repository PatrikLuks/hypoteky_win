#!/usr/bin/env python
"""
Test: URL z welcome emailu funguje správně
"""
import os
import sys
import django

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hypoteky.settings")
os.environ["EMAIL_BACKEND"] = "django.core.mail.backends.locmem.EmailBackend"
django.setup()

from django.contrib.auth.models import User
from django.core import mail
from django.test import Client
from klienti.models import Klient, UserProfile
import re

print("\n" + "="*80)
print("TEST: Ověření URL z welcome emailu")
print("="*80 + "\n")

# Cleanup
User.objects.filter(username__startswith="test_welcome_url").delete()
Klient.objects.filter(jmeno__startswith="Test Welcome URL").delete()

# Vytvoř poradce
poradce = User.objects.create_user(username="test_welcome_url_poradce", password="test123")
profile, _ = UserProfile.objects.get_or_create(user=poradce)
profile.role = "poradce"
profile.save()

# Vyčisti mail
mail.outbox = []

# Vytvoř klienta
klient = Klient.objects.create(
    jmeno="Test Welcome URL Klient",
    email="test@example.com",
    user=None
)

print(f"✅ Klient vytvořen: {klient.jmeno}")
print(f"✅ User: {klient.user.username} (ID: {klient.user.pk})")

# Zkontroluj email
if not mail.outbox:
    print("❌ Žádný email!")
    sys.exit(1)

# Najdi welcome email (ne password_reset email)
welcome_email = None
for email in mail.outbox:
    if "Vítejte" in email.subject or "Welcome" in email.subject:
        welcome_email = email
        break

if not welcome_email:
    print(f"❌ Welcome email nenalezen! Počet emailů: {len(mail.outbox)}")
    for i, email in enumerate(mail.outbox):
        print(f"   Email {i+1}: {email.subject}")
    sys.exit(1)

print(f"✅ Welcome email nalezen: {welcome_email.subject}")

# Extrahuj URL
url_match = re.search(r'/account/reset/[^/]+/[^/\s]+/', welcome_email.body)
if not url_match:
    print("❌ URL nebyla nalezena!")
    print("Email body:", welcome_email.body[:500])
    sys.exit(1)

reset_path = url_match.group(0)
print(f"✅ URL path: {reset_path}")

# Test HTTP GET
client = Client()
response = client.get(reset_path, follow=False)
print(f"\n📋 HTTP GET {reset_path}")
print(f"   Status: {response.status_code}")

if response.status_code == 302:
    print(f"   Redirect: {response.url}")
    if 'login' in response.url:
        print("   ❌ PROBLÉM: Redirectuje na login!")
    elif 'reset' in response.url:
        print("   ✅ OK: Redirectuje na reset confirm form")
    else:
        print(f"   ⚠️  Neočekávaný redirect: {response.url}")
elif response.status_code == 200:
    print("   ✅ OK: Vrátila se stránka (pravděpodobně formulář)")
    if 'Nastavení nového hesla'.encode('utf-8') in response.content or b'new_password' in response.content:
        print("   ✅ Formulář pro nastavení hesla nalezen!")
    else:
        print("   ⚠️  Formulář nenalezen v odpovědi")

# Test s follow
response_follow = client.get(reset_path, follow=True)
final_path = response_follow.request['PATH_INFO']
print(f"\n📋 HTTP GET s follow=True")
print(f"   Finální path: {final_path}")
print(f"   Status: {response_follow.status_code}")

if 'login' in final_path:
    print("   ❌ CHYBA: Končí na login!")
elif 'reset' in final_path:
    print("   ✅ OK: Reset formulář")
    # Zkontroluj, jestli je to formulář pro nastavení hesla
    if b'new_password1' in response_follow.content:
        print("   ✅ Formulář pro nastavení hesla přítomen!")
    else:
        print("   ⚠️  Formulář nenalezen")
else:
    print(f"   ⚠️  Neočekávaný path: {final_path}")

# Cleanup
print("\n🧹 Cleanup")
klient.delete()
poradce.delete()
print("✅ Done")
print("="*80 + "\n")
