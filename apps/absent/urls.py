from django.urls import path
from rest_framework.routers import SimpleRouter
from .views import AbsentViewSet, AbsentTypeView, ResponderView

app_name = 'absent'

router = SimpleRouter()
router.register('absent', AbsentViewSet, basename='absent')

urlpatterns = [
                  path('type/', AbsentTypeView.as_view(), name='absenttypes'),
                  path('responder/', ResponderView.as_view(), name='getresponder'),
              ] + router.urls
