from django.contrib import admin
from .models import Klient, HypotekaWorkflow

@admin.register(Klient)
class KlientAdmin(admin.ModelAdmin):
    list_display = ('id', 'jmeno')
    search_fields = ('jmeno',)

@admin.register(HypotekaWorkflow)
class HypotekaWorkflowAdmin(admin.ModelAdmin):
    list_display = ('id', 'klient', 'krok', 'datum')
    list_filter = ('krok', 'datum')
    search_fields = ('klient__jmeno',)
