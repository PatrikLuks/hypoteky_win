from rest_framework import viewsets, permissions
from .models import Klient, UserProfile, Poznamka, Zmena
from .serializers import KlientSerializer, PoznamkaSerializer, ZmenaSerializer

class KlientViewSet(viewsets.ModelViewSet):
    queryset = Klient.objects.all()  # <-- přidáno pro DRF router
    serializer_class = KlientSerializer
    permission_classes = [permissions.IsAuthenticated]

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
    permission_classes = [permissions.IsAuthenticated]

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
