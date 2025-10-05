from rest_framework import serializers
from corte.models import Corte


class CorteSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Corte
        fields = ['id', 'comentario', 'fecha_inicio', 'fecha_final', 'gastos_fijos', 'gastos_ocasionales', 'total_ingresos']
