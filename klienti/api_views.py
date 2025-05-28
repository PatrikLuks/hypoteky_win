from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, NumberFilter, CharFilter, DateFilter
from .models import Klient, UserProfile, Poznamka, Zmena, HypotekaWorkflow
from .serializers import KlientSerializer, PoznamkaSerializer, ZmenaSerializer, HypotekaWorkflowSerializer
from .permissions import IsPoradceOrAdmin, IsKlientOrReadOnly

class KlientFilter(FilterSet):
    banka = CharFilter(field_name='vyber_banky', lookup_expr='icontains')
    stav = CharFilter(method='filter_stav')
    castka_min = NumberFilter(field_name='navrh_financovani_castka', lookup_expr='gte')
    castka_max = NumberFilter(field_name='navrh_financovani_castka', lookup_expr='lte')
    datum_od = DateFilter(field_name='datum', lookup_expr='gte')
    datum_do = DateFilter(field_name='datum', lookup_expr='lte')
    zamitnuti = CharFilter(field_name='duvod_zamitnuti', lookup_expr='isnull')

    class Meta:
        model = Klient
        fields = ['banka', 'stav', 'castka_min', 'castka_max', 'datum_od', 'datum_do', 'zamitnuti']

    def filter_stav(self, queryset, name, value):
        # Filtrování podle aktuálního kroku workflow (pole je název kroku)
        if value == 'hotovo':
            for krok in self.Meta.model._meta.get_fields():
                if krok.name.startswith('splneno_') and not krok.name.endswith('hotovo'):
                    queryset = queryset.exclude(**{krok.name: None})
            return queryset
        else:
            return queryset.filter(**{value+'__isnull': True})

class KlientViewSet(viewsets.ModelViewSet):
    queryset = Klient.objects.all()
    serializer_class = KlientSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_class = KlientFilter
    ordering_fields = ['datum', 'navrh_financovani_castka']
    search_fields = ['vyber_banky', 'co_financuje']  # 'jmeno' odstraněno, protože je šifrované a nelze jej vyhledávat

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsPoradceOrAdmin()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        try:
            role = user.userprofile.role
        except Exception:
            role = None
        if role == 'klient':
            return Klient.objects.filter(user=user)
        return Klient.objects.all()

class PoznamkaViewSet(viewsets.ModelViewSet):
    queryset = Poznamka.objects.all()  # <-- přidáno pro DRF router
    serializer_class = PoznamkaSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsPoradceOrAdmin()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        try:
            role = user.userprofile.role
        except Exception:
            role = None
        if role == 'klient':
            return Poznamka.objects.filter(klient__user=user)
        return Poznamka.objects.all()

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
        if role == 'klient':
            return Zmena.objects.filter(klient__user=user)
        return Zmena.objects.all()

class HypotekaWorkflowViewSet(viewsets.ModelViewSet):
    queryset = HypotekaWorkflow.objects.all()  # <-- přidáno pro DRF router
    serializer_class = HypotekaWorkflowSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsPoradceOrAdmin()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        try:
            role = user.userprofile.role
        except Exception:
            role = None
        if role == 'klient':
            return HypotekaWorkflow.objects.filter(klient__user=user)
        return HypotekaWorkflow.objects.all()
