from rest_framework import serializers
from municipio.models import Municipio


class MunicipioSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Municipio
        fields = ['id', 'nombre', 'precio']
