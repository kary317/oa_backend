from rest_framework.routers import SimpleRouter
from django.urls import path
from .views import InformViewSet, ReadInformView

app_name = 'inform'

router = SimpleRouter()
router.register('inform', InformViewSet, basename='inform')

urlpatterns = [
                  path('inform/read/', ReadInformView.as_view(), name='read_inform')
              ] + router.urls
