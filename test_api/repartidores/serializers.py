from rest_framework import serializers
from repartidores.models import Repartidor


class RepartidorSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Repartidor
        fields = ['nombre', 'sueldo']
