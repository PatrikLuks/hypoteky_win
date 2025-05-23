from rest_framework import serializers
from .models import Klient, Poznamka, Zmena, HypotekaWorkflow

class KlientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Klient
        fields = '__all__'

class PoznamkaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poznamka
        fields = '__all__'

class ZmenaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zmena
        fields = '__all__'

class HypotekaWorkflowSerializer(serializers.ModelSerializer):
    klient_jmeno = serializers.CharField(source='klient.jmeno', read_only=True)
    krok_display = serializers.CharField(source='get_krok_display', read_only=True)
    class Meta:
        model = HypotekaWorkflow
        fields = '__all__'
