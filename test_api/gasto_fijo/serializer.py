from rest_framework import serializers
from gasto_fijo.models import GastoFijo


class GastoFijoSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = GastoFijo
        habilidato = serializers.BooleanField(default=True)
        fields = ['id', 'concepto', 'cantidad', 'habilitado']
