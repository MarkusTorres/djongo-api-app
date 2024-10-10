from django.db import models


class Municipio(models.Model):
    # id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, default='', blank=False)
    precio = models.DecimalField(max_length=10, decimal_places=2, max_digits=12)

    class Meta:
        ordering = ["nombre"]
