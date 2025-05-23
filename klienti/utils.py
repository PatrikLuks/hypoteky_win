from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string

def odeslat_notifikaci_email(prijemce, predmet, zprava, html_zprava=None, context=None, template_name=None):
    """
    Odeslání e-mailové notifikace. Pokud je html_zprava nebo template_name vyplněna, odešle i HTML verzi.
    """
    html_message = html_zprava
    if template_name and context:
        html_message = render_to_string(template_name, context)
    send_mail(
        subject=predmet,
        message=zprava,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[prijemce],
        html_message=html_message,
        fail_silently=False,
    )
