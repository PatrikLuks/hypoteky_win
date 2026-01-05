#!/usr/bin/env python
"""
Jednoduchý test: Vytvoř uživatele, vygeneruj token, ověř token
"""
import os
import sys
import django

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hypoteky.settings")
django.setup()

from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str

# Vytvoř testovacího uživatele
User.objects.filter(username="token_test").delete()
user = User.objects.create_user(username="token_test", password="test123", email="test@example.com")
print(f"✅ User vytvořen: {user.username} (ID: {user.pk})")

# Vygeneruj token
token = default_token_generator.make_token(user)
uid = urlsafe_base64_encode(force_bytes(user.pk))
print(f"✅ Token vygenerován: {token}")
print(f"✅ UID: {uid}")

# Ověř token IHNED
is_valid_immediate = default_token_generator.check_token(user, token)
print(f"✅ Token validní (ihned): {is_valid_immediate}")

# Dekóduj UID a znovu načti uživatele
try:
    uid_decoded = force_str(urlsafe_base64_decode(uid))
    user_from_db = User.objects.get(pk=uid_decoded)
    print(f"✅ User načten z DB: {user_from_db.username}")
    
    # Ověř token s user z DB
    is_valid_from_db = default_token_generator.check_token(user_from_db, token)
    print(f"✅ Token validní (user z DB): {is_valid_from_db}")
except Exception as e:
    print(f"❌ Chyba: {e}")

# Cleanup
user.delete()
print("✅ Cleanup dokončen")
