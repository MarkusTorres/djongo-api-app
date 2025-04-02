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

    @auth_check()
    def retrieve(self, request, *args, **kwargs):
        pk = request.parser_context['kwargs']['pk']
        queryset = Proveedor.objects.filter(id__exact=pk)
        serializer_context = {
            'request': request,
        }
        serializer = ProveedorSerializer(queryset, context=serializer_context, many=True)
        return Response(serializer.data)

    @auth_check()
    def destroy(self, request, *args, **kwargs):
        try:
            pk = request.parser_context['kwargs']['pk']
            queryset = Proveedor.objects.filter(id__exact=pk)
            queryset.delete()
            return Response(data="object successfully deleted")
        except Proveedor.DoesNotExist:
            return Response(data="No object found in DB")
        except Proveedor.MultipleObjectsReturned:
            return Response(data="Multiple objects found in DB")

@api_view
def api_root(request, format=None):
    return Response({
        'proveedores': reverse('proveedor-list', request=request, format=format),
    })
