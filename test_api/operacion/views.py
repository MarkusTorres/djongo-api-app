from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from django.http import Http404
from operacion.models import Operacion
from inventario.views import update_inventario
from operacion.models import Flujo
from operacion.serializers import OperacionSerializer
from operacion.serializers import FlujoSerializer
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework import viewsets, status
from utils import base_utils
from rest_framework import permissions
from rest_framework import renderers
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
import json
from tokens.views import _header_exists, auth_check


CREADA = 'creada'
AGENDADA = 'agendada'
EN_RUTA = 'en ruta'
CANCELADA = 'cancelada'
EFECTIVA = 'efectiva'
TRANSFERENCIA = 'transferencia'
REAGENDADA = 'reagendada'
ENTREGADA = 'entregada'
FINALIZADA = 'finalizada'

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

#
# def check_if_field_exists(obj, field):
#     if field in obj.__dict__.keys():
#
#

class OperacionesPagination(PageNumberPagination):
    page_size = 20
    max_page_size = 100
    page_size_query_param = 'page_size'


class OperacionViewSet(base_utils.GenericViewSetAuth):
    queryset = Operacion.objects.all()
    serializer_class = OperacionSerializer
    pagination_class = OperacionesPagination

    @action(detail=True, methods=['get', 'put', 'patch'], url_path='codigo')
    @auth_check()
    def codigo(self, request, pk=None):
        serializer_context = {
            'request': request,
        }

        try:
            query_result = Operacion.objects.filter(codigo__exact=pk).get()

            if self.request.method == 'PUT' or self.request.method == 'PATCH':
                for field in request.data.keys():
                    setattr(query_result, field, request.data[field])

                if 'status' in request.data.keys():
                    if request.data['status'] == EFECTIVA:
                        update_inventario(query_result.inventario_relacion)
                # query_result.status = request.data['status']
                # query_result.direccion_inicio = request.data['direccion_inicio']
                # query_result.direccion_final = request.data['direccion_final']
                # query_result.codigo_postal = request.data['codigo_postal']
                # query_result.tarifa = request.data['tarifa']
                # query_result.fecha_inicio = request.data['fecha_inicio']
                # # query_result.fecha_final = request.data['fecha_final']
                # query_result.cantidad = request.data['cantidad']
                # query_result.comentario = request.data['comentario']
                # query_result.precio = request.data['precio']
                # query_result.nombre_referencia = request.data['nombre_referencia']
                # query_result.numero_referencia = request.data['numero_referencia']
                # query_result.repartidor = request.data['repartidor']
                # query_result.historial = request.data['historial']
                # query_result.peso = request.data['peso']
                # query_result.largo = request.data['largo']
                # query_result.ancho = request.data['ancho']
                # query_result.alto = request.data['alto']
                # query_result.devoluciones = request.data['devoluciones']
                # query_result.entregas = request.data['entregas']
                # query_result.inventario_relacion = request.data['inventario_relacion']
                # query_result.imagen = request.data['imagen']
                # workaround for Decimal128 type from pymongo
                query_result.precio = float(str(query_result.precio))
                query_result.tarifa = float(str(query_result.tarifa))
                query_result.save()

            serializer = OperacionSerializer(query_result, context=serializer_context)

            return Response(serializer.data)
        except ObjectDoesNotExist:
            return Response(data=f'id {pk} not found', status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    @auth_check()
    def repartidor(self, request, pk=None):
        queryset = Operacion.objects.filter(repartidor__exact=pk)

        serializer_context = {
            'request': request,
        }
        serializer = OperacionSerializer(queryset, context=serializer_context, many=True)

        return Response(serializer.data)

    @auth_check()
    def create(self, request, *args, **kwargs):
        data = request.data
        if data['id_tipo_operacion'] == 'producto' and data['inventario_relacion'] == '':
            raise ValidationError(detail="Operacion tipo producto debe especificar inventario", code=500)

        new_operacion = insert_operacion(data, Operacion)

        return Response(new_operacion)


def insert_operacion(data, model):

    value_or_default = lambda data_struct, value: value in data_struct.keys()

    id = model.objects.count() + 1
    new_item = model.objects.create(
        id=id,
        id_tipo_operacion=data['id_tipo_operacion'],
        codigo=data['codigo'],
        status=data['status'],
        direccion_inicio=data['direccion_inicio'],
        direccion_final=data['direccion_final'],
        codigo_postal=data['codigo_postal'],
        tarifa=data['tarifa'],
        # fecha_inicio=data['fecha_inicio'],
        fecha_final=data['fecha_final'],
        cantidad=data['cantidad'],
        comentario=data['comentario'],
        precio=data['precio'],
        nombre_referencia=data['nombre_referencia'],
        numero_referencia=data['numero_referencia'],
        repartidor=data['repartidor'],
        historial=data['historial'],
        peso=data['peso'],
        largo=data['largo'],
        ancho=data['ancho'],
        alto=data['alto'],
        devoluciones=data['devoluciones'],
        entregas=data['entregas'],
        inventario_relacion=data['inventario_relacion'],
        imagen=data['imagen'] if value_or_default(data, 'imagen') else '',
        imagen_opcional=data['imagen_opcional'] if value_or_default(data, 'imagen_opcional') else '',
        monicipio_id=data['monicipio_id'] if value_or_default(data, 'monicipio_id') else 0,
        municipio_nombre=data['municipio_nombre'] if value_or_default(data, 'municipio_nombre') else '',
    )
    new_item.id = id
    new_item.save()
    serializer_class = OperacionSerializer(new_item)
    return serializer_class.data


class OperacionBulkViewSet(viewsets.ModelViewSet):
    queryset = Operacion.objects.all()
    serializer_class = OperacionSerializer

    @auth_check()
    def create(self, request, *args, **kwargs):
        data = request.data
        results = [insert_operacion(single_operacion, Operacion) for single_operacion in data]
        serializer = self.get_serializer(data=request.data, many=True)
        headers = self.get_success_headers(results)
        return Response(results, status=status.HTTP_201_CREATED, headers=headers)

    def list(self, request, *args, **kwargs):
        raise Http404

    def destroy(self, request, *args, **kwargs):
        raise Http404

    def update(self, request, *args, **kwargs):
        raise Http404

    def retrieve(self, request, *args, **kwargs):
        raise Http404


class FlujoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Flujo.objects.all()
    serializer_class = FlujoSerializer

    def list(self, request, *args, **kwargs):
        return Response(flujo_operacion)


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'operaciones': reverse('operacion-list', request=request, format=format),
        'operaciones-bulk': reverse('operacion-bulk-list', request=request, format=format),
        'flujo_operaciones': reverse('flujo_operaciones', request=request, format=format),
    })
