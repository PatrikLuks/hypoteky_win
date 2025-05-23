from rest_framework import routers
from .api_views import KlientViewSet, PoznamkaViewSet, ZmenaViewSet, HypotekaWorkflowViewSet

router = routers.DefaultRouter()
router.register(r'klienti', KlientViewSet)
router.register(r'poznamky', PoznamkaViewSet)
router.register(r'zmeny', ZmenaViewSet)
router.register(r'workflow', HypotekaWorkflowViewSet)

urlpatterns = router.urls
