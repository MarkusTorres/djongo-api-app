from operacion.models import Operacion
from operacion.models import Flujo
from operacion.serializers import OperacionSerializer
from operacion.serializers import FlujoSerializer
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import renderers
from rest_framework.response import Response
from rest_framework.decorators import action
import json


CREADA = 'Creada'
AGENDADA = 'Agendada'
EN_RUTA = 'En ruta'
CANCELADA = 'Cancelada'
EFECTIVA = 'Efectiva'
TRANSFERENCIA = 'Transferencia'
REAGENDADA = 'Reagendada'
ENTREGADA = 'Entregada'
FINALIZADA = 'Finalizada'

flujo_operacion = {
    CREADA: [AGENDADA],
    AGENDADA: [EN_RUTA, CANCELADA, ENTREGADA],
    EN_RUTA: [EFECTIVA, TRANSFERENCIA, REAGENDADA, CANCELADA],
    EFECTIVA: [REAGENDADA, CANCELADA],
    TRANSFERENCIA: [REAGENDADA, CANCELADA, ENTREGADA],
    CANCELADA: [ENTREGADA, FINALIZADA],
    ENTREGADA: [FINALIZADA],
    FINALIZADA: []
}


class OperacionViewSet(viewsets.ModelViewSet):
    queryset = Operacion.objects.all()
    serializer_class = OperacionSerializer

    @action(detail=True, methods=['get'])
    def codigo(self, request, pk=None):
        queryset = Operacion.objects.get(codigo=pk)

        serializer_context = {
            'request': request,
        }
        serializer = OperacionSerializer(queryset, context=serializer_context)

        return Response(serializer.data)

    @action(detail=True, methods=['get', 'post', 'patch'])
    def repartidor(self, request, pk=None):
        queryset = Operacion.objects.get(repartidor=pk)

        serializer_context = {
            'request': request,
        }
        serializer = OperacionSerializer(queryset, context=serializer_context)

        return Response(serializer.data)


class FlujoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Flujo.objects.all()
    serializer_class = FlujoSerializer

    def list(self, request, *args, **kwargs):
        return Response(flujo_operacion)


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'operaciones': reverse('operacion-list', request=request, format=format),
        'flujo_operaciones': reverse('flujo_operaciones', request=request, format=format),
    })
