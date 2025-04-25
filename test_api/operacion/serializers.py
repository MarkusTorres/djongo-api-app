from rest_framework import serializers
from operacion.models import Operacion


class OperacionSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Operacion
        fields = ['id', 'id_tipo_operacion', 'codigo', 'status', 'direccion_inicio',
                  'direccion_final', 'codigo_postal', 'tarifa', 'fecha_inicio', 'fecha_final',
                  'cantidad', 'comentario', 'precio', 'nombre_referencia',
                  'numero_referencia', 'repartidor', 'historial', 'peso',
                  'largo', 'ancho', 'alto', 'devoluciones', 'entregas', 'inventario_relacion', 'imagen', 
                  'imagen_opcional', 'monicipio_id', 'municipio_nombre', 'finalizada', 'pagado', 'id_proveedor']


class FlujoSerializer(serializers.HyperlinkedModelSerializer):
    pass
