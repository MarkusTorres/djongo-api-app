from django.db import models
from djongo import models
from phonenumber_field.modelfields import PhoneNumberField
import datetime

ESTADOS = [
    ('creada', 'creada'),
    ('agendada', 'agendada'),
    ('en ruta', 'Ruta'),
    ('en ruta intento 1', 'Ruta intento 1'),
    ('ruta intento 2', 'Ruta intento 2'),
    ('cancelada', 'Cancelada'),
    ('efectiva', 'Efectiva'),
    ('transferencia', 'Transferencia'),
    ('reagendada', 'Reagendada'),
    ('asignada', 'Asignada'),
    ('Asignada intento 1', 'Asignada intento 1'),
    ('Asignada intento 2', 'Asignada intento 2'),
    ('intento 2', 'Intento 2'),
    ('retorno', 'Retorno'),
]

class Operacion(models.Model):
    _id = models.ObjectIdField()
    id = models.PositiveIntegerField(default=0, blank=False)
    id_tipo_operacion = models.CharField(choices=[("terceros", "terceros"),
                                                  ("interna", "interna"),
                                                  ("producto", "producto")],
                                         default="interna", max_length=20)
    codigo = models.CharField(max_length=50, blank=False)
    status = models.CharField(choices=ESTADOS, default='Agendada', max_length=20)
    direccion_inicio = models.TextField(blank=True)
    direccion_final = models.TextField(blank=True)
    # tarifa = models.DecimalField(max_length=6, decimal_places=2, max_digits=6, default=1)
    tarifa = models.FloatField(blank=False)
    fecha_inicio = models.DateField(auto_now_add=False)
    fecha_final = models.DateField(default=datetime.date.today)
    cantidad = models.PositiveIntegerField(blank=False, default=1)
    comentario = models.TextField(blank=True)
    # precio = models.DecimalField(max_length=20, decimal_places=2, max_digits=12, default=1)
    precio = models.FloatField(blank=False)
    nombre_referencia = models.CharField(max_length=90, blank=True)
    numero_referencia = PhoneNumberField(blank=True)
    repartidor = models.PositiveIntegerField(blank=True, default=0)
    historial = models.JSONField(blank=True, default=[])
    # img = models.ImageField()
    peso = models.PositiveIntegerField(blank=True, default=0)
    largo = models.PositiveIntegerField(blank=True, default=0)
    ancho = models.PositiveIntegerField(blank=True, default=0)
    alto = models.PositiveIntegerField(blank=True, default=0)

    devoluciones = models.PositiveIntegerField(blank=True, default=0)
    entregas = models.PositiveIntegerField(blank=True, default=0)

    inventario_relacion = models.JSONField(blank=True, default=[])
    codigo_postal = models.PositiveIntegerField(blank=False)
    imagen = models.TextField(blank=True)
    imagen_opcional = models.TextField(blank=True)
    monicipio_id = models.IntegerField(blank=True, default=0)
    municipio_nombre = models.TextField(blank=True, default='ninguno')

    # finalizado ahora es un campo
    finalizada = models.BooleanField(blank=True, default=False)
    # pagado will work as a flag on the reports
    pagado = models.BooleanField(blank=True, default=False)
    id_proveedor = models.PositiveIntegerField(blank=False, default=0)
    id_cliente = models.PositiveIntegerField(blank=False, default=0)

    class Meta:
        ordering = ["status"]


class Flujo(models.Model):
    pass

class Flujo2(models.Model):
    pass