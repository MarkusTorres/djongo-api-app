from django.db import models
from djongo import models
from djongo import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Inventario(models.Model):
    _id = models.ObjectIdField()
    id = models.PositiveIntegerField(default=0, blank=False)
    concepto = models.CharField(max_length=50, default='', blank=False)
    # cantidad = models.IntegerField(blank=False, validators=[MinValueValidator(1), MaxValueValidator(1000)])
    cantidad = models.IntegerField(blank=False)
    comentario = models.TextField(blank=True)
    id_proveedor = models.PositiveIntegerField(blank=False, default=0)

