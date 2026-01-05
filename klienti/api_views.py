import logging

from django_filters.rest_framework import (
    CharFilter,
    DateFilter,
    DjangoFilterBackend,
    FilterSet,
    NumberFilter,
)
from rest_framework import filters, permissions, viewsets

from .models import HypotekaWorkflow, Klient, Poznamka, Zmena
from .permissions import IsPoradceOrAdmin

logger = logging.getLogger("klienti.api")
from .serializers import (
    HypotekaWorkflowSerializer,
    KlientSerializer,
    PoznamkaSerializer,
    ZmenaSerializer,
)


class KlientFilter(FilterSet):
    banka = CharFilter(field_name="vyber_banky", lookup_expr="icontains")
    stav = CharFilter(method="filter_stav")
    castka_min = NumberFilter(field_name="navrh_financovani_castka", lookup_expr="gte")
    castka_max = NumberFilter(field_name="navrh_financovani_castka", lookup_expr="lte")
    datum_od = DateFilter(field_name="datum", lookup_expr="gte")
    datum_do = DateFilter(field_name="datum", lookup_expr="lte")
    zamitnuti = CharFilter(field_name="duvod_zamitnuti", lookup_expr="isnull")

    class Meta:
        model = Klient
        fields = [
            "banka",
            "stav",
            "castka_min",
            "castka_max",
            "datum_od",
            "datum_do",
            "zamitnuti",
        ]

    def filter_stav(self, queryset, name, value):
        # Filtrování podle aktuálního kroku workflow (pole je název kroku)
        if value == "hotovo":
            for krok in self.Meta.model._meta.get_fields():
                if krok.name.startswith("splneno_") and not krok.name.endswith(
                    "hotovo"
                ):
                    queryset = queryset.exclude(**{krok.name: None})
            return queryset
        else:
            return queryset.filter(**{value + "__isnull": True})


class KlientViewSet(viewsets.ModelViewSet):
    permission_classes = [IsPoradceOrAdmin]
    queryset = Klient.objects.all()
    serializer_class = KlientSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    filterset_class = KlientFilter
    ordering_fields = ["datum", "navrh_financovani_castka"]
    search_fields = [
        "vyber_banky",
        "co_financuje",
    ]  # 'jmeno' odstraněno, protože je šifrované a nelze jej vyhledávat

    def get_object(self):
        # Umožní poradci upravovat všechny klienty, klientovi jen své
        obj = super().get_object()
        user = self.request.user
        try:
            role = user.userprofile.role
        except Exception:
            role = None
        if role == "klient" and obj.user != user:
            from rest_framework.exceptions import PermissionDenied

            raise PermissionDenied("Klient může upravovat pouze své záznamy.")
        return obj

    def get_queryset(self):
        user = self.request.user
        try:
            role = user.userprofile.role
        except Exception:
            role = None
        if role == "klient":
            return Klient.objects.filter(user=user)
        return Klient.objects.all()

    def get_permissions(self):
        # Pro zápisové operace (POST, PUT, PATCH, DELETE) pouze poradce/admin, pro čtení stačí přihlášení
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsPoradceOrAdmin()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        """Auditní log při vytvoření klienta přes API."""
        instance = serializer.save()
        author = self.request.user.username if self.request.user.is_authenticated else "API"
        Zmena.objects.create(
            klient=instance,
            popis=f"[API] Vytvořen klient: {instance.jmeno} (ID {instance.pk})",
            author=author,
        )
        logger.info(f"[API AUDIT] Klient vytvořen: {instance.pk} uživatelem {author}")

    def perform_update(self, serializer):
        """Auditní log při aktualizaci klienta přes API."""
        instance = serializer.save()
        author = self.request.user.username if self.request.user.is_authenticated else "API"
        Zmena.objects.create(
            klient=instance,
            popis=f"[API] Aktualizován klient: {instance.jmeno} (ID {instance.pk})",
            author=author,
        )
        logger.info(f"[API AUDIT] Klient aktualizován: {instance.pk} uživatelem {author}")

    def perform_destroy(self, instance):
        """Auditní log při smazání klienta přes API."""
        author = self.request.user.username if self.request.user.is_authenticated else "API"
        klient_jmeno = instance.jmeno
        klient_pk = instance.pk
        # Vytvoř log před smazáním (klient už nebude existovat)
        Zmena.objects.create(
            klient=instance,
            popis=f"[API] Smazán klient: {klient_jmeno} (ID {klient_pk})",
            author=author,
        )
        logger.info(f"[API AUDIT] Klient smazán: {klient_pk} uživatelem {author}")
        instance.delete()


class PoznamkaViewSet(viewsets.ModelViewSet):
    queryset = Poznamka.objects.all()  # <-- přidáno pro DRF router
    serializer_class = PoznamkaSerializer

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsPoradceOrAdmin()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        try:
            role = user.userprofile.role
        except Exception:
            role = None
        if role == "klient":
            return Poznamka.objects.filter(klient__user=user)
        return Poznamka.objects.all()

    def perform_create(self, serializer):
        """Auditní log při vytvoření poznámky přes API."""
        instance = serializer.save()
        author = self.request.user.username if self.request.user.is_authenticated else "API"
        Zmena.objects.create(
            klient=instance.klient,
            popis=f"[API] Přidána poznámka (ID {instance.pk})",
            author=author,
        )
        logger.info(f"[API AUDIT] Poznámka vytvořena: {instance.pk} uživatelem {author}")

    def perform_update(self, serializer):
        """Auditní log při aktualizaci poznámky přes API."""
        instance = serializer.save()
        author = self.request.user.username if self.request.user.is_authenticated else "API"
        Zmena.objects.create(
            klient=instance.klient,
            popis=f"[API] Aktualizována poznámka (ID {instance.pk})",
            author=author,
        )
        logger.info(f"[API AUDIT] Poznámka aktualizována: {instance.pk} uživatelem {author}")

    def perform_destroy(self, instance):
        """Auditní log při smazání poznámky přes API."""
        author = self.request.user.username if self.request.user.is_authenticated else "API"
        klient = instance.klient
        poznamka_pk = instance.pk
        Zmena.objects.create(
            klient=klient,
            popis=f"[API] Smazána poznámka (ID {poznamka_pk})",
            author=author,
        )
        logger.info(f"[API AUDIT] Poznámka smazána: {poznamka_pk} uživatelem {author}")
        instance.delete()


class ZmenaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Zmena.objects.all()  # <-- přidáno pro DRF router
    serializer_class = ZmenaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        try:
            role = user.userprofile.role
        except Exception:
            role = None
        if role == "klient":
            return Zmena.objects.filter(klient__user=user)
        return Zmena.objects.all()


class HypotekaWorkflowViewSet(viewsets.ModelViewSet):
    queryset = HypotekaWorkflow.objects.all()  # <-- přidáno pro DRF router
    serializer_class = HypotekaWorkflowSerializer

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsPoradceOrAdmin()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        try:
            role = user.userprofile.role
        except Exception:
            role = None
        if role == "klient":
            return HypotekaWorkflow.objects.filter(klient__user=user)
        return HypotekaWorkflow.objects.all()

    def perform_create(self, serializer):
        """Auditní log při vytvoření workflow kroku přes API."""
        instance = serializer.save()
        author = self.request.user.username if self.request.user.is_authenticated else "API"
        Zmena.objects.create(
            klient=instance.klient,
            popis=f"[API] Přidán workflow krok {instance.get_krok_display()} (ID {instance.pk})",
            author=author,
        )
        logger.info(f"[API AUDIT] Workflow krok vytvořen: {instance.pk} uživatelem {author}")

    def perform_update(self, serializer):
        """Auditní log při aktualizaci workflow kroku přes API."""
        instance = serializer.save()
        author = self.request.user.username if self.request.user.is_authenticated else "API"
        Zmena.objects.create(
            klient=instance.klient,
            popis=f"[API] Aktualizován workflow krok {instance.get_krok_display()} (ID {instance.pk})",
            author=author,
        )
        logger.info(f"[API AUDIT] Workflow krok aktualizován: {instance.pk} uživatelem {author}")

    def perform_destroy(self, instance):
        """Auditní log při smazání workflow kroku přes API."""
        author = self.request.user.username if self.request.user.is_authenticated else "API"
        klient = instance.klient
        krok_display = instance.get_krok_display()
        workflow_pk = instance.pk
        Zmena.objects.create(
            klient=klient,
            popis=f"[API] Smazán workflow krok {krok_display} (ID {workflow_pk})",
            author=author,
        )
        logger.info(f"[API AUDIT] Workflow krok smazán: {workflow_pk} uživatelem {author}")
        instance.delete()
