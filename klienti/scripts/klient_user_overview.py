from django.apps import apps

Klient = apps.get_model('klienti', 'Klient')
User = apps.get_model('auth', 'User')
UserProfile = apps.get_model('klienti', 'UserProfile')

print("Přehled klientů přiřazených uživatelům s rolí 'klient':\n")

for user in User.objects.filter(userprofile__role='klient'):
    klienti_count = Klient.objects.filter(user=user).count()
    print(f"{user.username}: {klienti_count} klient(ů)")

print("\nHotovo. Pokud některý uživatel nemá přiřazeného klienta, můžete upravit sample_data.py nebo přiřadit ručně v adminu.")
