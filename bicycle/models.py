from django.db import models


class Bicycle(models.Model):
    STATUS_CHOICES = (
        ('available', 'Available'),
        ('rented', 'Rented'),
    )
    name = models.CharField(max_length=50, verbose_name='Имя')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available', verbose_name='Статус')

    def __str__(self):
        return f'{self.name} - {self.status}'

    class Meta:
        verbose_name = 'Велосипед'
        verbose_name_plural = 'Велосипеды'
