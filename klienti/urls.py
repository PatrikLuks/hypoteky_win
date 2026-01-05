from django.contrib.auth import views as auth_views
from django.urls import path

from . import views
from .views import reporting, reporting_export_pdf, reporting_export_xlsx

urlpatterns = [
    path("", views.home, name="home"),
    path("klient/pridat/", views.klient_create, name="klient_create"),
    path("klient/<int:pk>/", views.klient_detail, name="klient_detail"),
    path("klient/<int:pk>/editace/", views.klient_edit, name="klient_edit"),
    path("klient/<int:pk>/smazat/", views.klient_delete, name="klient_delete"),
    # Alias pro snapshot testy a kompatibilitu
    path(
        "klient/<int:pk>/potvrdit-smazani/",
        views.klient_delete,
        name="klient_confirm_delete",
    ),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="registration/login.html"),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(next_page="/"), name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path(
        "klient/<int:klient_id>/poznamka/<int:poznamka_id>/smazat/",
        views.smazat_poznamku,
        name="smazat_poznamku",
    ),
    path("klienti/", views.home, name="klient_list"),
    path("klient/<int:pk>/ical/", views.export_klient_ical, name="export_klient_ical"),
]

urlpatterns += [
    path("reporting/", reporting, name="reporting"),
    path("reporting/export/pdf/", reporting_export_pdf, name="reporting_export_pdf"),
    path("reporting/export/xlsx/", reporting_export_xlsx, name="reporting_export_xlsx"),
]
