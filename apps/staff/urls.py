from django.urls import path
from rest_framework.routers import SimpleRouter

from . import views

app_name = 'staff'

router = SimpleRouter()
router.register('staff', views.StaffViewSet, basename='staff')

urlpatterns = [
    path('departments/', views.DepartmentListView.as_view(), name='departments'),
    # path('staff/', views.StaffView.as_view(), name='staff_view'),
    path('active/', views.ActiveStaffView.as_view(), name='active_staff'),
    path('test/celery/', views.TestCeleryView.as_view(), name='test_celery'),
]

urlpatterns += router.urls
