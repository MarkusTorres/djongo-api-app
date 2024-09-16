from django.db import models


class Empleado(models.Model):
    id_tipo = models.IntegerField(choices=[(1, 'Repartidor'), (2, 'Empleado'), (3, 'Analista'), (4, 'Maistro')])
    nombre = models.CharField(max_length=50, default='', blank=False)
    sueldo = models.DecimalField(max_length=6, decimal_places=2, max_digits=6)
    fecha_inicio = models.DateField()
    fecha_final = models.DateField()

    class Meta:
        ordering = ["nombre"]
