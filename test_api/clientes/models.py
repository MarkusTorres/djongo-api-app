from django.db import models

# Create your models here.
class Cliente(models.Model):
    id_tipo = models.IntegerField(choices=[(1, 'Interno'), (2, 'Externo'), (3, 'Tercero')])
    nombre = models.CharField(max_length=50, default='', blank=False)
    direccion = models.CharField(max_length=100, default='', blank=False)
    tarifa = models.DecimalField(max_length=6, decimal_places=2, max_digits=6)
    nota = models.TextField()

    class Meta:
        ordering = ["nombre"]
