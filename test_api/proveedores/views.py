from proveedores.models import Proveedor
from proveedores.serializers import ProveedorSerializer
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework import viewsets
from rest_framework.response import Response


class ProveedorViewSet(viewsets.ModelViewSet):
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        id = Proveedor.objects.count() + 1
        new_item = Proveedor.objects.create(
            id=Proveedor.objects.count() + 1,
            nombre=data['nombre']
        )
        new_item.id = id
        new_item.save()
        serializer = ProveedorSerializer(new_item)
        return Response(serializer.data)

@api_view
def api_root(request, format=None):
    return Response({
        'proveedores': reverse('proveedor-list', request=request, format=format),
    })
