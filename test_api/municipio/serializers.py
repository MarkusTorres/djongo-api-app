from rest_framework import serializers
from municipio.models import Municipio
# from bson.objectid import ObjectId
# from bson.errors import InvalidId
# from django.utils.encoding import smart_str


class MunicipioSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Municipio
        fields = ['id', 'nombre', 'precio']
