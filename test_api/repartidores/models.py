from django.db import models
from djongo import models


class Repartidor(models.Model):
    _id = models.ObjectIdField()
    id = models.PositiveIntegerField(default=0, blank=False)
    nombre = models.CharField(max_length=50, default='', blank=False)
    sueldo = models.FloatField(blank=False, default=1)
    id_prestamo = models.IntegerField(blank=True, auto_created=True)
