from repartidores.models import Repartidor
from repartidores.serializers import RepartidorSerializer
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework import viewsets
from rest_framework.response import Response


class RepartidorViewSet(viewsets.ModelViewSet):
    queryset = Repartidor.objects.all()
    serializer_class = RepartidorSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        id = Repartidor.objects.count() + 1
        new_item = Repartidor.objects.create(
            id=Repartidor.objects.count() + 1,
            nombre=data['nombre'],
            sueldo=data['sueldo'],
            id_prestamo=data['id_prestamo']
        )
        new_item.id = id
        new_item.save()
        serializer = RepartidorSerializer(new_item)
        return Response(serializer.data)

@api_view
def api_root(request, format=None):
    return Response({
        'repartidores': reverse('repartidor-list', request=request, format=format),
    })
