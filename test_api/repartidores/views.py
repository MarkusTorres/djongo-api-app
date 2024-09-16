from repartidores.models import Repartidor
from repartidores.serializers import RepartidorSerializer
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework import viewsets
from rest_framework.response import Response


class RepartidorViewSet(viewsets.ModelViewSet):
    queryset = Repartidor.objects.all()
    serializer_class = RepartidorSerializer

@api_view
def api_root(request, format=None):
    return Response({
        'repartidores': reverse('repartidor-list', request=request, format=format),
    })
