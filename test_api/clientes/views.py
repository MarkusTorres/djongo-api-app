from clientes.models import Cliente
from clientes.serializers import ClienteSerializer
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework import viewsets
from rest_framework.response import Response
from tokens.views import auth_check
from utils import base_utils


class ClienteViewSet(base_utils.GenericViewSetAuth):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

    @auth_check()
    def create(self, request, *args, **kwargs):
        data = request.data
        new_item = Cliente.objects.create(
            id=base_utils.get_model_new_id(Cliente),
            id_tipo=data['id_tipo'],
            nombre=data['nombre'],
            calle=data['calle'],
            num_int=data['num_int'],
            num_ext=data['num_ext'],
            colonia=data['colonia'],
            cp=data['cp'],
            telefono=data['telefono'],
            municipio=data['municipio'],
            estado=data['estado'],
            entre_calles=data['entre_calles'],
            desc_fachada=data['desc_fachada'],
            referencia=data['referencia'],
            tarifa=data['tarifa'],
            nota=data['nota']
        )
        serializer = ClienteSerializer(new_item)
        return Response(serializer.data)

    @auth_check()
    def retrieve(self, request, *args, **kwargs):
        pk = request.parser_context['kwargs']['pk']
        queryset = Cliente.objects.filter(id__exact=pk)
        serializer_context = {
            'request': request,
        }
        serializer = ClienteSerializer(queryset, context=serializer_context, many=True)
        return Response(serializer.data)

    @auth_check()
    def destroy(self, request, *args, **kwargs):
        try:
            pk = request.parser_context['kwargs']['pk']
            queryset = Cliente.objects.filter(id__exact=pk)
            queryset.delete()
            return Response(data="object successfully deleted")
        except Cliente.DoesNotExist:
            return Response(data="No object found in DB")
        except Cliente.MultipleObjectsReturned:
            return Response(data="Multiple objects found in DB")

@api_view
def api_root(request, format=None):
    return Response({
        'clientes': reverse('cliente-list', request=request, format=format),
    })
