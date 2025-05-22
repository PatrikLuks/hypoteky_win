from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('klient/pridat/', views.klient_create, name='klient_create'),
    path('klient/<int:pk>/', views.klient_detail, name='klient_detail'),
    path('klient/<int:pk>/editace/', views.klient_edit, name='klient_edit'),
    path('klient/<int:pk>/smazat/', views.klient_delete, name='klient_delete'),
    path('kalkulacka/', views.kalkulacka, name='kalkulacka'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('klient/<int:klient_id>/poznamka/<int:poznamka_id>/smazat/', views.smazat_poznamku, name='smazat_poznamku'),
]
