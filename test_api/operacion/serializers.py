from rest_framework import serializers
from operacion.models import Operacion


class OperacionSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Operacion
        fields = ['id', 'id_tipo_operacion', 'codigo', 'status', 'direccion_inicio', 'direccion_final', 'tarifa',
                  'fecha_inicio', 'fecha_final', 'cantidad', 'comentario', 'precio', 'nombre_referencia',
                  'repartidor', 'historial', 'peso', 'largo', 'ancho', 'alto', 'devoluciones', 'entregas']


class FlujoSerializer(serializers.HyperlinkedModelSerializer):
    pass
