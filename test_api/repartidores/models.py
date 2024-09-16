from django.db import models


class Repartidor(models.Model):
    nombre = models.CharField(max_length=50, default='', blank=False)
    sueldo = models.DecimalField(max_length=6, decimal_places=2, max_digits=6)
    id_prestamo = models.IntegerField(blank=True, auto_created=True)
