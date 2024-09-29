from django.db import models

ESTADOS = [
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
    id_tipo_operacion = models.CharField(choices=[("terceros", "terceros"), ("interna", "interna")], default="interna", max_length=20)
    status = models.CharField(choices=ESTADOS, default='Agendada', max_length=20)
    direccion_inicio = models.TextField()
    direccion_final = models.TextField()
    tarifa = models.DecimalField(max_length=6, decimal_places=2, max_digits=6)
    fecha_inicio = models.DateField(auto_created=True)
    fecha_final = models.DateField(auto_now_add=True)
    cantidad = models.IntegerField()
    comentario = models.TextField(blank=True)
    precio = models.DecimalField(max_length=6, decimal_places=2, max_digits=6)
    # img = models.ImageField()

    class Meta:
        ordering = ["status"]


class Flujo(models.Model):
    pass
