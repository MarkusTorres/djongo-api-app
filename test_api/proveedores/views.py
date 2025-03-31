from proveedores.models import Proveedor
from proveedores.serializers import ProveedorSerializer
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework import viewsets
from rest_framework.response import Response
from tokens.views import auth_check
from utils import base_utils


class ProveedorViewSet(base_utils.GenericViewSetAuth):
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        new_item = Proveedor.objects.create(
            id=base_utils.get_model_new_id(Proveedor),
            nombre=data['nombre'],
            tarifa=data['tarifa']
        )
        serializer = ProveedorSerializer(new_item)
        return Response(serializer.data)

@api_view
def api_root(request, format=None):
    return Response({
        'proveedores': reverse('proveedor-list', request=request, format=format),
    })
