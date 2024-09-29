from rest_framework import serializers
from clientes.models import Cliente


class ClienteSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Cliente
        # nota is not here on purpose
        fields = ['id', 'id_tipo', 'nombre', 'direccion', 'tarifa']
