from django.urls import path, include
from rest_framework.routers import DefaultRouter

from bicycle.views import BicycleViewSet

app_name = 'bicycle'

router = DefaultRouter()
router.register(r'', BicycleViewSet, basename='bicycle')

urlpatterns = [
    path('', include(router.urls)),
]
