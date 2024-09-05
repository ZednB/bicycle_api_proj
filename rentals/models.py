from django.db import models

from bicycle.models import Bicycle
from users.models import User

NULLABLE = {'blank': True, 'null': True}


class Rental(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    bicycle = models.ForeignKey(Bicycle, on_delete=models.CASCADE, verbose_name='Велосипед')
    start_time = models.DateTimeField(auto_now_add=True, verbose_name='Время начала')
    end_time = models.DateTimeField(**NULLABLE, verbose_name='Время окончания')
    cost = models.DecimalField(max_digits=10, decimal_places=2, **NULLABLE)

    def __str__(self):
        return f'{self.user.email} - {self.bicycle.name}'

    class Meta:
        verbose_name = 'Аренда'
        verbose_name_plural = 'Аренды'
