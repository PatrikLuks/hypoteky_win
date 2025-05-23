from django.contrib import admin
from .models import Klient, HypotekaWorkflow, UserProfile, Zmena, NotifikaceLog

@admin.register(Klient)
class KlientAdmin(admin.ModelAdmin):
    list_display = ('id', 'jmeno', 'user')
    search_fields = ('jmeno',)
    list_filter = ('user',)

@admin.register(HypotekaWorkflow)
class HypotekaWorkflowAdmin(admin.ModelAdmin):
    list_display = ('id', 'klient', 'krok', 'datum')
    list_filter = ('krok', 'datum')
    search_fields = ('klient__jmeno',)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')
    list_filter = ('role',)
    search_fields = ('user__username',)

@admin.register(Zmena)
class ZmenaAdmin(admin.ModelAdmin):
    list_display = ('id', 'klient', 'author', 'created', 'popis')
    list_filter = ('klient', 'author', 'created')
    search_fields = ('klient__jmeno', 'author', 'popis')
    date_hierarchy = 'created'

@admin.register(NotifikaceLog)
class NotifikaceLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'prijemce', 'typ', 'klient', 'datum', 'uspesne')
    list_filter = ('typ', 'uspesne', 'datum')
    search_fields = ('prijemce', 'klient__jmeno', 'obsah')
    date_hierarchy = 'datum'
