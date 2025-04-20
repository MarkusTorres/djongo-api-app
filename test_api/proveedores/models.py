from django.db import models
from djongo import models


class Proveedor(models.Model):
    _id = models.ObjectIdField()
    id = models.PositiveIntegerField(default=0, blank=False)
    nombre = models.CharField(max_length=50, default='', blank=False)
    tarifa = models.PositiveIntegerField(blank=False)
    tarifa_foraneo = models.FloatField(blank=False, default=1)
    tarifa_local = models.FloatField(blank=False, default=1)

    class Meta:
        ordering = ["nombre"]
