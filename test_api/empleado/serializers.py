from rest_framework import serializers
from empleado.models import Empleado


class EmpleadoSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Empleado
        fields = '__all__'
