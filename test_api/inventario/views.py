from inventario.models import Inventario
from inventario.serializers import InventarioSerializer
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework import viewsets
from rest_framework.response import Response


class InventarioViewSet(viewsets.ModelViewSet):
    queryset = Inventario.objects.all()
    serializer_class = InventarioSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        id = Inventario.objects.count()
        new_item = Inventario.objects.create(
            id=Inventario.objects.count(),
            concepto=data['concepto'],
            cantidad=data['cantidad'],
            comentario=data['comentario']
        )
        new_item.id = id
        new_item.save()
        serializer = InventarioSerializer(new_item)
        return Response(serializer.data)


@api_view
def api_root(request, format=None):
    return Response({
        'inventario': reverse('inventario-list', request=request, format=format),
    })
