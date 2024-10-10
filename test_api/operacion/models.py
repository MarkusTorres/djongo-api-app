from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
import datetime

ESTADOS = [
    ('creada', 'Creada'),
    ('agendada', 'Agendada'),
    ('en ruta', 'Ruta'),
    ('efectiva', 'Efectiva'),
    ('transferencia', 'Transferencia'),
    ('reagendada', 'Reagendada'),
    ('cancelada', 'Cancelada'),
    ('entregada', 'Entregada'),
    ('finalizada', 'Finalizada'),
]


class Operacion(models.Model):
    id_tipo_operacion = models.CharField(choices=[("terceros", "terceros"),
                                                  ("interna", "interna"),
                                                  ("producto", "producto")],
                                         default="interna", max_length=20)
    codigo = models.CharField(max_length=50, blank=False)
    status = models.CharField(choices=ESTADOS, default='Agendada', max_length=20)
    direccion_inicio = models.TextField(blank=True)
    direccion_final = models.TextField(blank=True)
    tarifa = models.DecimalField(max_length=6, decimal_places=2, max_digits=6, default=1)
    fecha_inicio = models.DateField(auto_now_add=True)
    fecha_final = models.DateField(default=datetime.date.today)
    cantidad = models.PositiveIntegerField(blank=False, default=1)
    comentario = models.TextField(blank=True)
    precio = models.DecimalField(max_length=20, decimal_places=2, max_digits=12, default=1)
    nombre_referencia = models.CharField(max_length=90, blank=True)
    numero_referencia = PhoneNumberField(blank=True)
    repartidor = models.PositiveIntegerField(blank=True, default=0)
    historial = models.JSONField(blank=True)
    # img = models.ImageField()
    peso = models.PositiveIntegerField(blank=True, default=0)
    largo = models.PositiveIntegerField(blank=True, default=0)
    ancho = models.PositiveIntegerField(blank=True, default=0)
    alto = models.PositiveIntegerField(blank=True, default=0)

    devoluciones = models.PositiveIntegerField(blank=True, default=0)
    entregas = models.PositiveIntegerField(blank=True, default=0)

    class Meta:
        ordering = ["status"]


class Flujo(models.Model):
    pass
