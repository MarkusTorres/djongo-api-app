from django.db import models
from djongo import models
import datetime


class Prestamo(models.Model):
    _id = models.ObjectIdField()
    id = models.PositiveIntegerField(default=0, blank=False)
    id_empleado = models.IntegerField(blank=False, default=0)
    cantidad = models.PositiveIntegerField(blank=False)
    remanente = models.PositiveIntegerField(blank=False)
    fecha = models.DateField(default=datetime.date.today)
    liquidado = models.IntegerField(default=0)
    historial = models.JSONField(blank=True, default=[])

    class Meta:
        ordering = ["id_empleado"]
