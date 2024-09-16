from django.db import models


class Proveedor(models.Model):
    nombre = models.CharField(max_length=50, default='', blank=False)

    class Meta:
        ordering = ["nombre"]