from clientes.models import Cliente
from clientes.serializers import ClienteSerializer
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework import viewsets
from rest_framework.response import Response


class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        id = Cliente.objects.count() + 1
        new_item = Cliente.objects.create(
            id=Cliente.objects.count() + 1,
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
        new_item.id = id
        new_item.save()
        serializer = ClienteSerializer(new_item)
        return Response(serializer.data)

@api_view
def api_root(request, format=None):
    return Response({
        'clientes': reverse('cliente-list', request=request, format=format),
    })
