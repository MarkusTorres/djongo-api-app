from django.db import models
from djongo import models
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
class Cliente(models.Model):
    _id = models.ObjectIdField()
    id = models.PositiveIntegerField(default=0, blank=False)
    id_tipo = models.IntegerField(choices=[(1, 'Interno'), (2, 'Externo'), (3, 'Tercero'), (4, 'Externo')])
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
    tarifa = models.FloatField(blank=False, default=1)
    nota = models.TextField()

    class Meta:
        ordering = ["nombre"]
