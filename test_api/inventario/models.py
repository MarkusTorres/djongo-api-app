from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Inventario(models.Model):
    concepto = models.CharField(max_length=50, default='', blank=False)
    cantidad = models.IntegerField(blank=False, validators=[MinValueValidator(1), MaxValueValidator(1000)])
    comentario = models.TextField(blank=True)

