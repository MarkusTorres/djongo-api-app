from rest_framework import serializers
from operacion.models import Operacion


class OperacionSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Operacion
        fields = ['url', 'id', 'id_tipo_operacion', 'status',
                  'direccion_inicio', 'direccion_final', 'tarifa',
                  'fecha_inicio', 'cantidad', 'comentario']
