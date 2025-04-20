from rest_framework import serializers
from proveedores.models import Proveedor


class ProveedorSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Proveedor
        fields = ['id', 'nombre', 'tarifa', 'tarifa_foraneo', 'tarifa_local']
