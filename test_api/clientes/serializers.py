from rest_framework import serializers
from clientes.models import Cliente


class ClienteSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Cliente
        # nota is not here on purpose
        fields = ['id', 'id_tipo', 'nombre', 'calle', 'num_int', 'num_ext', 'colonia', 'cp',
                  'telefono', 'municipio', 'estado', 'entre_calles', 'desc_fachada', 'referencia', 'tarifa', 'nota']
