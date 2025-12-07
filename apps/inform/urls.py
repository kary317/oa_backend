from rest_framework.routers import SimpleRouter

from .views import InformViewSet

app_name = 'inform'

router = SimpleRouter()
router.register('inform', InformViewSet, basename='inform')

urlpatterns = [] + router.urls
