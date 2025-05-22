from django.apps import apps

Klient = apps.get_model('klienti', 'Klient')
User = apps.get_model('auth', 'User')
UserProfile = apps.get_model('klienti', 'UserProfile')

# Najdi všechny uživatele s rolí 'klient'
klient_users = list(User.objects.filter(userprofile__role='klient'))
if not klient_users:
    print('Nebyli nalezeni žádní uživatelé s rolí klient!')
    exit(1)

# Najdi všechny klienty bez přiřazeného uživatele
nezarazeni_klienti = list(Klient.objects.filter(user__isnull=True))

if not nezarazeni_klienti:
    print('Všichni klienti již mají přiřazeného uživatele.')
else:
    for idx, klient in enumerate(nezarazeni_klienti):
        user = klient_users[idx % len(klient_users)]
        klient.user = user
        klient.save()
        print(f"Klient {klient.jmeno} přiřazen uživateli {user.username}")
    print(f"Hotovo! Přiřazeno {len(nezarazeni_klienti)} klientů {len(klient_users)} uživatelům.")
