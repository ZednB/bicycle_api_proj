from rest_framework import serializers

from bicycle.models import Bicycle


class BicycleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Bicycle
        fields = ('id', 'name', 'status',)
        read_only_fields = ['id', 'status',]
