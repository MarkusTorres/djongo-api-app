from rest_framework import serializers
from prestamos.models import Prestamo


class PrestamoSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Prestamo
        fields = ['id', 'id_empleado', 'cantidad', 'remanente', 'fecha', 'liquidado', 'historial']
