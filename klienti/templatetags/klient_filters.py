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
    return {"user_role": get_user_role(request)}
