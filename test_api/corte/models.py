import datetime
from djongo import models


class Corte(models.Model):
    _id = models.ObjectIdField()
    id = models.PositiveIntegerField(default=0, blank=False)
    comentario = models.CharField(max_length=50, default='', blank=True)
    fecha_inicio = models.DateField(auto_now_add=True)
    fecha_final = models.DateField(default=datetime.date.today)
    gastos_fijos = models.JSONField(blank=True, default=[])
    gastos_ocasionales = models.JSONField(blank=True, default=[])
    total_ingresos = models.PositiveIntegerField(default=0, blank=False)
