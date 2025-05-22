from django.contrib.auth.models import User
from klienti.models import UserProfile

# Hromadné vytvoření UserProfile pro všechny uživatele
for user in User.objects.all():
    profile, created = UserProfile.objects.get_or_create(user=user)
    profile.save()
    print(f"UserProfile for {user.username} ({'created' if created else 'updated'}) - role: {profile.role}")
