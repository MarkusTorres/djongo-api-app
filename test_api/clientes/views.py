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

@api_view
def api_root(request, format=None):
    return Response({
        'clientes': reverse('cliente-list', request=request, format=format),
    })
