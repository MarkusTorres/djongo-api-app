from proveedores.models import Proveedor
from proveedores.serializers import ProveedorSerializer
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework import viewsets, status
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
            tarifa=data['tarifa'],
            tarifa_contacto_efectivo=data['tarifa_contacto_efectivo'],
            tarifa_repartidor=data['tarifa_repartidor']
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

    @auth_check()
    def update(self, request, *args, **kwargs):
        data = request.data
        proveedor_obj = Proveedor.objects.filter(id__exact=data['id']).get()
        proveedor_obj.nombre = base_utils.value_or_default('nombre', data, proveedor_obj.nombre)
        proveedor_obj.tarifa = base_utils.value_or_default('tarifa', data, proveedor_obj.tarifa)
        proveedor_obj.tarifa_contacto_efectivo = base_utils.value_or_default('tarifa_contacto_efectivo', data, proveedor_obj.tarifa_foraneo)
        proveedor_obj.tarifa_repartidor = base_utils.value_or_default('tarifa_repartidor', data, proveedor_obj.tarifa_local)

        proveedor_obj.save()
        serialized_obj = ProveedorSerializer(proveedor_obj)
        return Response(serialized_obj.data, status=status.HTTP_200_OK)


@api_view
def api_root(request, format=None):
    return Response({
        'proveedores': reverse('proveedor-list', request=request, format=format),
    })
