from municipio.models import Municipio
from municipio.serializers import MunicipioSerializer
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework import viewsets, status
from rest_framework.response import Response
from tokens.views import auth_check
from utils import base_utils


class MunicipioViewSet(base_utils.GenericViewSetAuth):
    queryset = Municipio.objects.all()
    serializer_class = MunicipioSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        max_id = base_utils.get_model_new_id(Municipio)
        new_item = Municipio.objects.create(
            id=max_id,
            nombre=data['nombre'],
            precio=data['precio'],
            tarifa_internas=data['tarifa_internas'],
            tarifa_producto=data['tarifa_producto']
        )
        serializer = MunicipioSerializer(new_item)
        return Response(serializer.data)

    @auth_check()
    def retrieve(self, request, *args, **kwargs):
        pk = request.parser_context['kwargs']['pk']
        queryset = Municipio.objects.filter(id__exact=pk)
        serializer_context = {
            'request': request,
        }
        serializer = MunicipioSerializer(queryset, context=serializer_context, many=True)
        return Response(serializer.data)

    @auth_check()
    def destroy(self, request, *args, **kwargs):
        try:
            pk = request.parser_context['kwargs']['pk']
            queryset = Municipio.objects.filter(id__exact=pk)
            queryset.delete()
            return Response(data="object successfully deleted")
        except Municipio.DoesNotExist:
            return Response(data="No object found in DB")
        except Municipio.MultipleObjectsReturned:
            return Response(data="Multiple objects found in DB")

    @auth_check()
    def update(self, request, *args, **kwargs):
        data = request.data
        municipio_obj = Municipio.objects.filter(id__exact=data['id']).get()
        municipio_obj.nombre = base_utils.value_or_default('nombre', data, municipio_obj.nombre)
        municipio_obj.precio = base_utils.value_or_default('precio', data, municipio_obj.precio)
        municipio_obj.tarifa_internas = base_utils.value_or_default('tarifa_internas', data, municipio_obj.tarifa_internas)
        municipio_obj.tarifa_producto = base_utils.value_or_default('tarifa_producto', data, municipio_obj.tarifa_producto)

        municipio_obj.save()
        serialized_obj = MunicipioSerializer(municipio_obj)
        return Response(serialized_obj.data, status=status.HTTP_200_OK)


@api_view
def api_root(request, format=None):
    return Response({
        'municipios': reverse('municipio-list', request=request, format=format),
    })
