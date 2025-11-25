from inventario.models import Inventario
from inventario.serializers import InventarioSerializer
from rest_framework.decorators import api_view, action
from rest_framework.reverse import reverse
from rest_framework import viewsets, status
from rest_framework.response import Response
from tokens.views import auth_check
from utils import base_utils
from django.db.models import Q
import json


def update_inventario(json_obj: str):
    items = json.loads(json_obj)
    targets = []
    for item in items:
        id = item['id']
        cantidad = item['cantidad']  # from request

        target = Inventario.objects.get(id=id)
        old_cantidad = target.cantidad
        new_cantidad = old_cantidad - cantidad
        target.cantidad = new_cantidad
        target.save()

    return targets


class InventarioViewSet(base_utils.GenericViewSetAuth):
    queryset = Inventario.objects.all()
    serializer_class = InventarioSerializer

    @auth_check()
    def create(self, request, *args, **kwargs):
        data = request.data
        new_item = Inventario.objects.create(
            id=base_utils.get_model_new_id(Inventario),
            concepto=data['concepto'],
            cantidad=data['cantidad'],
            comentario=data['comentario'],
            id_proveedor= base_utils.value_or_default('id_proveedor', data, data['id_proveedor'])
        )
        serializer = InventarioSerializer(new_item)
        return Response(serializer.data)

    @auth_check()
    def retrieve(self, request, *args, **kwargs):
        pk = request.parser_context['kwargs']['pk']
        queryset = Inventario.objects.filter(id__exact=pk)
        serializer_context = {
            'request': request,
        }
        serializer = InventarioSerializer(queryset, context=serializer_context, many=True)
        return Response(serializer.data)

    @auth_check()
    def destroy(self, request, *args, **kwargs):
        try:
            pk = request.parser_context['kwargs']['pk']
            queryset = Inventario.objects.filter(id__exact=pk)
            queryset.delete()
            return Response(data="object successfully deleted")
        except Inventario.DoesNotExist:
            return Response(data="No object found in DB")
        except Inventario.MultipleObjectsReturned:
            return Response(data="Multiple objects found in DB")

    @auth_check()
    def update(self, request, *args, **kwargs):
        data = request.data
        id_obj = kwargs['pk']
        inventario_obj = Inventario.objects.get(id=id_obj)

        inventario_obj.concepto = base_utils.value_or_default('concepto', data, inventario_obj.concepto)
        inventario_obj.cantidad = base_utils.value_or_default('cantidad', data, inventario_obj.cantidad)
        inventario_obj.comentario = base_utils.value_or_default('comentario', data, inventario_obj.comentario)
        inventario_obj.id_proveedor = base_utils.value_or_default('id_proveedor', data, inventario_obj.id_proveedor)

        inventario_obj.save()
        serialized_obj = InventarioSerializer(inventario_obj)

        return Response(serialized_obj.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    @auth_check()
    def filtro(self, request, pk=None):
        try:
            data = request.data
            q_proveedor = Q(id_proveedor__exact=data['id_proveedor'])
            queryset =Inventario.objects.filter(q_proveedor)

            serializer_context = {
                'request': request,
            }
            serializer = InventarioSerializer(queryset, context=serializer_context, many=True)
            return Response(serializer.data)
        except Inventario.DoesNotExist:
            return Response(data="No se encontraron resultados")
        except Exception:
            return Response(data="Datos erroneos")


    @action(detail=False, methods=['post'])
    @auth_check()
    def like(self, request, pk=None):
        try:
            data = request.data
            q_inventario = Q(nombre__contains=data['nombre'])
            queryset = Inventario.objects.filter(q_inventario)

            serializer_context = {
                'request': request,
            }
            serializer = InventarioSerializer(queryset, context=serializer_context, many=True)
            return Response(serializer.data)
        except Inventario.DoesNotExist:
            return Response(data="No se encontraron resultados")
        except Exception:
            return Response(data="Datos erroneos")


@api_view
def api_root(request, format=None):
    return Response({
        'inventario': reverse('inventario-list', request=request, format=format),
    })
