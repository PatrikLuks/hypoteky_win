from django.contrib import admin
from .models import Klient, HypotekaWorkflow, UserProfile

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
