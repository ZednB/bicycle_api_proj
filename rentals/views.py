import logging

from django.db import transaction
from django.utils import timezone
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from bicycle.models import Bicycle
from .tasks import calculate_rental_post


from rentals.models import Rental
from rentals.serializers import RentalSerializer


logger = logging.getLogger(__name__)

class RentalViewSet(viewsets.ModelViewSet):
    """
    Эндпоинты для управления арендой велосипедов.
    """
    queryset = Rental.objects.all()
    serializer_class = RentalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Возвращает арендную историю текущего пользователя.
        """
        return Rental.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        """
        Создает новую аренду велосипеда.
        """
        user = request.user
        bicycle_id = request.data.get('bicycle')

        if not bicycle_id:
            return Response({"detail": "Bicycle ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Проверяем, что пользователь не арендует велосипед в данный момент
        active_rental = Rental.objects.filter(user=user, end_time__isnull=True).first()
        if active_rental:
            return Response({"detail": "You already have an active rental."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                bicycle = Bicycle.objects.select_for_update().get(id=bicycle_id, status='available')
                bicycle.status = 'rented'
                bicycle.save()

                rental = Rental.objects.create(user=user, bicycle=bicycle)
                serializer = self.get_serializer(rental)
                logger.info(f"User {user.id} rented bicycle {bicycle.id}. Rental ID: {rental.id}")
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Bicycle.DoesNotExist:
            logger.warning(f"User {user.id} attempted to rent unavailable bicycle {bicycle_id}.")
            return Response({"detail": "Bicycle not available."}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def return_bicycle(self, request, pk=None):
        """
        Возвращает арендованный велосипед и инициирует расчет стоимости аренды.
        """
        user = request.user
        try:
            rental = Rental.objects.get(pk=pk, user=user, end_time__isnull=True)
            logger.info(f"User {user.id} is returning rental {rental.id}.")
        except Rental.DoesNotExist:
            logger.error(f"Active rental not found for user {user.id} with rental ID {pk}.")
            return Response({"detail": "Active rental not found."}, status=status.HTTP_404_NOT_FOUND)

        with transaction.atomic():
            rental.end_time = timezone.now()
            rental.save()

            bicycle = rental.bicycle
            bicycle.status = 'available'
            bicycle.save()

            logger.info(f"Bicycle {bicycle.id} returned by user {user.id}. Rental {rental.id} ended at {rental.end_time}.")

            # Инициация асинхронной задачи для расчета стоимости аренды
            calculate_rental_post.delay(rental.id)
            logger.info(f"Started task to calculate cost for rental {rental.id}.")

            return Response({"detail": "Bicycle returned. Cost is being calculated."}, status=status.HTTP_200_OK)
