#!/usr/bin/env python
"""
Test: Kontrola URL v welcome emailu
"""
import os
import sys
import django

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hypoteky.settings")
# Force console email backend for testing
os.environ["EMAIL_BACKEND"] = "django.core.mail.backends.locmem.EmailBackend"
django.setup()

from django.contrib.auth.models import User, Group
from django.core import mail
from klienti.models import Klient, UserProfile

# Cleanup
User.objects.filter(username__startswith="test_url").delete()
Klient.objects.filter(jmeno__startswith="Test URL").delete()

# Vytvoř poradce
poradce = User.objects.create_user(username="test_url_poradce", password="test123")
profile, _ = UserProfile.objects.get_or_create(user=poradce)
profile.role = "poradce"
profile.save()

# Vyčisti mail outbox
mail.outbox = []

# Vytvoř klienta s emailem
print("📧 Vytváření klienta s emailem...")
klient = Klient.objects.create(
    jmeno="Test URL Klient",
    email="test@example.com",
    user=None
)

print(f"✅ Klient vytvořen: {klient.jmeno}")
print(f"✅ User vytvořen: {klient.user.username}")

# Zkontroluj email
if mail.outbox:
    print(f"\n✅ Email odeslán: {len(mail.outbox)} emailů")
    email = mail.outbox[0]
    print(f"📧 Předmět: {email.subject}")
    print(f"📧 Příjemce: {email.to}")
    print(f"\n📧 Obsah emailu:")
    print("=" * 80)
    for line in email.body.split('\n'):
        if 'localhost' in line or 'password_reset' in line or 'http' in line:
            print(f"🔗 {line}")
    print("=" * 80)
else:
    print("❌ Email nebyl odeslán!")

# Cleanup
klient.delete()
poradce.delete()
print("\n✅ Cleanup dokončen")
