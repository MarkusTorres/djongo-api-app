from clientes.models import Cliente
from clientes.serializers import ClienteSerializer
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework import viewsets
from rest_framework.response import Response


class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

@api_view
def api_root(request, format=None):
    return Response({
        'clientes': reverse('cliente-list', request=request, format=format),
    })
