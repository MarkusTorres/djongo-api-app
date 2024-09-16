from proveedores.models import Proveedor
from proveedores.serializers import ProveedorSerializer
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework import viewsets
from rest_framework.response import Response


class ProveedorViewSet(viewsets.ModelViewSet):
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer

@api_view
def api_root(request, format=None):
    return Response({
        'proveedores': reverse('proveedor-list', request=request, format=format),
    })
