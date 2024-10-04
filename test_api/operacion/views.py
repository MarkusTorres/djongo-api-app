from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from operacion.models import Operacion
from operacion.models import Flujo
from operacion.serializers import OperacionSerializer
from operacion.serializers import FlujoSerializer
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework import viewsets, status
from rest_framework import permissions
from rest_framework import renderers
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
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


class OperacionesPagination(PageNumberPagination):
    page_size = 20
    max_page_size = 100
    page_size_query_param = 'page_size'


class OperacionViewSet(viewsets.ModelViewSet):
    queryset = Operacion.objects.all()
    serializer_class = OperacionSerializer
    pagination_class = OperacionesPagination

    @action(detail=True, methods=['get', 'put'], url_path='codigo')
    def codigo(self, request, pk=None):
        serializer_context = {
            'request': request,
        }

        try:
            query_result = Operacion.objects.filter(codigo__exact=pk).get()

            if self.request.method == 'PUT':
                query_result.status = request.data['status']
                query_result.direccion_inicio = request.data['direccion_inicio']
                query_result.direccion_final = request.data['direccion_final']
                query_result.tarifa = request.data['tarifa']
                query_result.fecha_inicio = request.data['fecha_inicio']
                # query_result.fecha_final = request.data['fecha_final']
                query_result.cantidad = request.data['cantidad']
                query_result.comentario = request.data['comentario']
                query_result.precio = request.data['precio']
                query_result.nombre_referencia = request.data['nombre_referencia']
                query_result.numero_referencia = request.data['numero_referencia']
                query_result.repartidor = request.data['repartidor']
                query_result.historial = request.data['historial']
                query_result.peso = request.data['peso']
                query_result.largo = request.data['largo']
                query_result.ancho = request.data['ancho']
                query_result.alto = request.data['alto']
                query_result.devoluciones = request.data['devoluciones']
                query_result.entregas = request.data['entregas']

                query_result.save()


            serializer = OperacionSerializer(query_result, context=serializer_context)

            return Response(serializer.data)
        except ObjectDoesNotExist:
            return Response(data=f'id {pk} not found', status=status.HTTP_400_BAD_REQUEST)

    # for future implementation, custom creation of object depending of data
    # def create(self, request, *args, **kwargs):
    #     tipo_operacion = request.data['id_tipo_operacion']
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'])
    def repartidor(self, request, pk=None):
        queryset = Operacion.objects.filter(repartidor__exact=pk)

        serializer_context = {
            'request': request,
        }
        serializer = OperacionSerializer(queryset, context=serializer_context, many=True)

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
