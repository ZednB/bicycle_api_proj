from django.utils import timezone
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .tasks import calculate_rental_post


from rentals.models import Rental
from rentals.serializers import RentalSerializer


class RentalViewSet(viewsets.ModelViewSet):
    queryset = Rental.objects.all()
    serializer_class = RentalSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'])
    def return_bicycle(self, request, pk=None):
        rental = self.get_object()
        if rental.end_time is not None:
            return Response({'detail': 'Велосипед свободен'})

        rental.end_time = timezone.now()
        rental.save()
        calculate_rental_post.delay(rental.id)
        return Response({'detail': 'Велосипед свободен. Стоимость расчитывается'})
