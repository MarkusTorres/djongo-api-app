from django.db import models
import datetime


class Prestamo(models.Model):
    id_empleado = models.IntegerField(blank=False, default=0)
    cantidad = models.PositiveIntegerField(blank=False)
    remanente = models.PositiveIntegerField(blank=False)
    fecha = models.DateField(default=datetime.date.today)
    liquidado = models.IntegerField(default=0)
    historial = models.JSONField(blank=True, default="[]")

    class Meta:
        ordering = ["id_empleado"]
