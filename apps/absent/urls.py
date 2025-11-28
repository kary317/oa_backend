from django.urls import path
from rest_framework.routers import SimpleRouter
from .views import AbsentViewSet

app_name = 'absent'

router = SimpleRouter()
router.register('absent', AbsentViewSet, basename='absent')

urlpatterns = [] + router.urls
