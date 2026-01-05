from django import template

from klienti.views import get_user_role

register = template.Library()


@register.filter
def attr(obj, name):
    """Safe access to model attributes in the template."""
    return getattr(obj, name, None)


@register.filter
def thousands_separator(value):
    try:
        return f"{int(value):,}".replace(",", " ")
    except (ValueError, TypeError):
        return value


@register.filter
def index(sequence, position):
    """Vrátí prvek na dané pozici v sekvenci (list, tuple)."""
    try:
        return sequence[position]
    except (IndexError, TypeError, KeyError):
        return ""


def user_role(request):
    """Context processor pro user_role a display_name."""
    user_role = None
    display_name = None
    
    if hasattr(request, "user") and request.user.is_authenticated:
        try:
            user_role = request.user.userprofile.role
        except Exception:
            pass
        
        # Pro klienty zobraz jméno z Klient.jmeno
        if user_role == "klient":
            try:
                klient = request.user.klient_set.first()
                if klient:
                    display_name = klient.jmeno
            except Exception:
                pass
        
        # Fallback na first_name nebo username
        if not display_name:
            display_name = request.user.first_name or request.user.username
    
    return {
        "user_role": user_role,
        "display_name": display_name
    }

