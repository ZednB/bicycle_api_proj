from django.shortcuts import render
from rest_framework import viewsets

from bicycle.models import Bicycle
from bicycle.serializers import BicycleSerializer


class BicycleViewSet(viewsets.ModelViewSet):
    queryset = Bicycle.objects.all()
    serializer_class = BicycleSerializer

    def get_queryset(self):
        return super().get_queryset().filter(status='available')
