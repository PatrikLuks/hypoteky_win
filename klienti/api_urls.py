from rest_framework import routers
from .api_views import KlientViewSet, PoznamkaViewSet, ZmenaViewSet

router = routers.DefaultRouter()
router.register(r'klienti', KlientViewSet)
router.register(r'poznamky', PoznamkaViewSet)
router.register(r'zmeny', ZmenaViewSet)

urlpatterns = router.urls
