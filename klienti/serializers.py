from rest_framework import serializers

from .models import HypotekaWorkflow, Klient, Poznamka, Zmena


class KlientSerializer(serializers.ModelSerializer):
    # Povinná pole a základní validace
    jmeno = serializers.CharField(max_length=100, required=False, allow_blank=False)
    datum = serializers.DateField(required=False)
    vyber_banky = serializers.CharField(
        max_length=255, required=False, allow_blank=False
    )
    navrh_financovani_castka = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
        required=False,
        min_value=10000,
        max_value=100000000,
    )

    def validate_jmeno(self, value):
        if value is not None and not value.strip():
            raise serializers.ValidationError("Jméno klienta nesmí být prázdné.")
        if value is not None and len(value) > 100:
            raise serializers.ValidationError(
                "Jméno klienta je příliš dlouhé (max 100 znaků)."
            )
        return value

    def validate_navrh_financovani_castka(self, value):
        if value is not None and value < 10000:
            raise serializers.ValidationError("Minimální částka je 10 000 Kč.")
        if value is not None and value > 100_000_000:
            raise serializers.ValidationError("Maximální částka je 100 000 000 Kč.")
        return value

    def validate(self, data):
        # Pokud je partial update (PATCH), nevyžaduj povinná pole
        if not self.partial:
            if not data.get("jmeno") or not data["jmeno"].strip():
                raise serializers.ValidationError(
                    {"jmeno": "Jméno klienta je povinné."}
                )
            if not data.get("vyber_banky") or not data["vyber_banky"].strip():
                raise serializers.ValidationError({"vyber_banky": "Vyberte banku."})
            if not data.get("datum"):
                raise serializers.ValidationError({"datum": "Datum je povinné."})
            if not data.get("navrh_financovani_castka"):
                raise serializers.ValidationError(
                    {"navrh_financovani_castka": "Zadejte částku návrhu financování."}
                )
        return data

    class Meta:
        model = Klient
        fields = "__all__"


class PoznamkaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poznamka
        fields = "__all__"


class ZmenaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zmena
        fields = "__all__"


class HypotekaWorkflowSerializer(serializers.ModelSerializer):
    klient_jmeno = serializers.CharField(source="klient.jmeno", read_only=True)
    krok_display = serializers.CharField(source="get_krok_display", read_only=True)

    class Meta:
        model = HypotekaWorkflow
        fields = "__all__"
