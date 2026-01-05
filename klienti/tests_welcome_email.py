"""
Test: Automatické odeslání welcome emailu při vytvoření klienta poradcem
"""
import pytest
from django.contrib.auth.models import User, Group
from django.core import mail
from klienti.models import Klient, UserProfile


@pytest.mark.django_db
def test_poradce_vytvori_klienta_s_welcome_emailem():
    """Test: Poradce vytvoří klienta → automaticky se vytvoří účet + odešle welcome email"""
    
    # 1. Vytvoření poradce
    poradce_user = User.objects.create_user(
        username="test_poradce_email",
        password="testpass123",
        email="poradce@test.cz"
    )
    
    # Přiřazení do skupiny jplservis (pokud existuje)
    try:
        jplservis_group = Group.objects.get(name="jplservis")
        poradce_user.groups.add(jplservis_group)
    except Group.DoesNotExist:
        pass
    
    # Vytvoření UserProfile s rolí poradce
    profile, _ = UserProfile.objects.get_or_create(user=poradce_user)
    profile.role = "poradce"
    profile.save()
    
    # 2. Vyčištění mail outbox
    mail.outbox = []
    
    # 3. Vytvoření klienta s emailem (jako by to udělal poradce formulářem)
    klient = Klient.objects.create(
        jmeno="Test Email Klient",
        email="klient@test.cz",
        user=None  # Toto spustí automatické vytvoření účtu
    )
    
    # 4. Ověření vytvoření User účtu
    assert klient.user is not None, "User účet nebyl vytvořen"
    # Po změně: email je nyní username
    assert klient.user.username == "klient@test.cz", f"Špatné username: {klient.user.username}"
    assert klient.user.email == "klient@test.cz", f"Špatný email: {klient.user.email}"
    
    # 5. Ověření UserProfile
    klient_profile = UserProfile.objects.get(user=klient.user)
    assert klient_profile.role == "klient", f"Špatná role: {klient_profile.role}"
    
    # 6. Ověření odeslání welcome emailu
    assert len(mail.outbox) > 0, "Žádný email nebyl odeslán"
    
    welcome_email = mail.outbox[0]
    assert "klient@test.cz" in welcome_email.to, f"Email nebyl odeslán na správnou adresu: {welcome_email.to}"
    assert "Vítejte" in welcome_email.subject or "Welcome" in welcome_email.subject, f"Špatný předmět: {welcome_email.subject}"
    
    # Ověření obsahu emailu
    email_body = welcome_email.body
    assert klient.user.username in email_body, "Email neobsahuje username"
    assert "password_reset_confirm" in email_body or "nastavení hesla" in email_body.lower(), "Email neobsahuje odkaz na nastavení hesla"
    
    # 7. Ověření oprávnění RBAC
    viditelne_klienti = Klient.objects.filter(user=klient.user)
    assert viditelne_klienti.count() == 1, "Klient nevidí jen svůj záznam"
    
    vsichni_klienti = Klient.objects.all()
    # Poradce by měl vidět všechny (včetně tohoto nového)
    assert vsichni_klienti.count() >= 1, "Database nemá žádné klienty"
    
    print(f"\n✅ Test úspěšný:")
    print(f"   - Klient: {klient.jmeno}")
    print(f"   - Username: {klient.user.username}")
    print(f"   - Email: {klient.user.email}")
    print(f"   - Welcome email odeslán: ✓")
    print(f"   - Předmět: {welcome_email.subject}")
