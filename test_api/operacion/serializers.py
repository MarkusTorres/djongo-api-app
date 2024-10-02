from rest_framework import serializers
from operacion.models import Operacion


class OperacionSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Operacion
        fields = '__all__'


class FlujoSerializer(serializers.HyperlinkedModelSerializer):
    pass
