from django.urls import path

from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .api_views import (
    HypotekaWorkflowViewSet,
    KlientViewSet,
    PoznamkaViewSet,
    ZmenaViewSet,
)

router = routers.DefaultRouter()
router.register(r"klienti", KlientViewSet)
router.register(r"poznamky", PoznamkaViewSet)
router.register(r"zmeny", ZmenaViewSet)
router.register(r"workflow", HypotekaWorkflowViewSet)

urlpatterns = router.urls

urlpatterns += [
    # JWT autentizace
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
