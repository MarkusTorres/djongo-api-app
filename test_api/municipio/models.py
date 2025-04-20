from django.db import models
from djongo import models


class Municipio(models.Model):
    # id = models.AutoField(primary_key=True)
    _id = models.ObjectIdField()
    id = models.PositiveIntegerField(default=0, blank=False)
    nombre = models.CharField(max_length=50, default='', blank=False)
    precio = models.FloatField(blank=False, default=1)
    tarifa_internas = models.FloatField(blank=False, default=1)
    tarifa_producto = models.FloatField(blank=False, default=1)

    class Meta:
        ordering = ["nombre"]
