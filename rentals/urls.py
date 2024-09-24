from django.urls import path, include
from rest_framework.routers import DefaultRouter

from rentals.views import RentalViewSet

app_name = 'rentals'

router = DefaultRouter()
router.register(r'', RentalViewSet, basename='rentals')

urlpatterns = [
    path('', include(router.urls)),
]