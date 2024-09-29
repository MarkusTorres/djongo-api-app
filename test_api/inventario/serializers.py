from rest_framework import serializers
from inventario.models import Inventario


class InventarioSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Inventario
        fields = ['id', 'concepto', 'cantidad', 'comentario']
