from djongo import models


class GastoFijo(models.Model):
    _id = models.ObjectIdField()
    id = models.PositiveIntegerField(default=0, blank=False)
    concepto = models.CharField(max_length=50, default='', blank=False)
    cantidad = models.IntegerField(blank=False)
    habilitado = models.BinaryField(default=True, null=False)