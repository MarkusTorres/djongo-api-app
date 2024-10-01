from rest_framework import serializers
from operacion.models import Operacion


class OperacionSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Operacion
        fields = ['id', 'url', 'id_tipo_operacion', 'status',
                  'direccion_inicio', 'direccion_final', 'tarifa',
                  'fecha_inicio', 'cantidad', 'nombre_referencia', 'numero_referencia', 'comentario']


class FlujoSerializer(serializers.HyperlinkedModelSerializer):
    pass
