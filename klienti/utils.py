from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from .models import NotifikaceLog, Klient

def odeslat_notifikaci_email(prijemce, predmet, zprava, html_zprava=None, context=None, template_name=None, typ='deadline', klient=None):
    """
    Odeslání e-mailové notifikace s logováním do NotifikaceLog.
    """
    html_message = html_zprava
    if template_name and context:
        html_message = render_to_string(template_name, context)
    uspesne = True
    try:
        send_mail(
            subject=predmet,
            message=zprava,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[prijemce],
            html_message=html_message,
            fail_silently=False,
        )
    except Exception as e:
        uspesne = False
    NotifikaceLog.objects.create(
        prijemce=prijemce,
        typ=typ,
        klient=klient,
        obsah=zprava,
        uspesne=uspesne
    )
