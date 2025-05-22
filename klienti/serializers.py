from rest_framework import serializers
from .models import Klient, Poznamka, Zmena

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
