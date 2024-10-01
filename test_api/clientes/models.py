from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
class Cliente(models.Model):
    id_tipo = models.IntegerField(choices=[(1, 'Interno'), (2, 'Externo'), (3, 'Tercero')])
    nombre = models.CharField(max_length=50, default='', blank=False)
    calle = models.CharField(max_length=100, default='', blank=False)
    num_int = models.CharField(max_length=8, blank=True)
    num_ext = models.CharField(max_length=8, blank=True)
    colonia = models.CharField(max_length=60, blank=True)
    cp = models.PositiveIntegerField(blank=True)
    telefono = PhoneNumberField(blank=True)
    municipio = models.CharField(max_length=60, blank=True)
    estado = models.CharField(max_length=60, blank=True)
    entre_calles = models.CharField(max_length=90, blank=True)
    desc_fachada = models.TextField()
    referencia = models.TextField()
    tarifa = models.DecimalField(max_length=6, decimal_places=2, max_digits=6)
    nota = models.TextField()

    class Meta:
        ordering = ["nombre"]
