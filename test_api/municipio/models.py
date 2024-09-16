from django.db import models


class Municipio(models.Model):
    nombre = models.CharField(max_length=50, default='', blank=False)
    precio = models.DecimalField(max_length=6, decimal_places=2, max_digits=6)
