from rest_framework import serializers
from proveedores.models import Proveedor


class ProveedorSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Proveedor
        fields = ['nombre']