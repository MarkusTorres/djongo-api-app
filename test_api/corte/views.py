from corte.models import Corte
from corte.serializer import CorteSerializer
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework import viewsets, status
from rest_framework.response import Response
from tokens.views import auth_check
from utils import base_utils


class CorteViewSet(base_utils.GenericViewSetAuth):
    queryset = Corte.objects.all()
    serializer_class = CorteSerializer

    @auth_check()
    def create(self, request, *args, **kwargs):
        data = request.data
        new_item = Corte.objects.create(
            id=base_utils.get_model_new_id(Corte),
            comentario=data['comentario'],
            fecha_inicio=data['fecha_inicio'],
            fecha_final=data['fecha_final'],
            gastos_fijos=data['gastos_fijos'],
            gastos_ocasionales=data['gastos_ocasionales'],
            total_ingresos=data['total_ingresos'],
        )
        serializer = CorteSerializer(new_item)
        return Response(serializer.data)

    @auth_check()
    def retrieve(self, request, *args, **kwargs):
        pk = request.parser_context['kwargs']['pk']
        queryset = Corte.objects.filter(id__exact=pk)
        serializer_context = {
            'request': request,
        }
        serializer = CorteSerializer(queryset, context=serializer_context, many=True)
        return Response(serializer.data)

    @auth_check()
    def destroy(self, request, *args, **kwargs):
        try:
            pk = request.parser_context['kwargs']['pk']
            queryset = Corte.objects.filter(id__exact=pk)
            queryset.delete()
            return Response(data="object successfully deleted")
        except Corte.DoesNotExist:
            return Response(data="No object found in DB")
        except Corte.MultipleObjectsReturned:
            return Response(data="Multiple objects found in DB")

    def update(self, request, *args, **kwargs):
        data = request.data
        id_obj = kwargs['pk']
        corte_obj = Corte.objects.get(id=id_obj)

        corte_obj.comentario = base_utils.value_or_default('comentario', data, corte_obj.comentario)
        corte_obj.fecha_inicio = base_utils.value_or_default('fecha_inicio', data, corte_obj.fecha_inicio)
        corte_obj.fecha_final = base_utils.value_or_default('fecha_final', data, corte_obj.fecha_final)
        corte_obj.gastos_fijos = base_utils.value_or_default('gastos_fijos', data, corte_obj.gastos_fijos)
        corte_obj.gastos_ocasionales = base_utils.value_or_default('gastos_ocasionales', data, corte_obj.gastos_ocasionales)
        corte_obj.total_ingresos = base_utils.value_or_default('total_ingresos', data, corte_obj.total_ingresos)

        corte_obj.save()
        serialized_obj = CorteSerializer(corte_obj)

        return Response(serialized_obj.data, status=status.HTTP_200_OK)


@api_view
def api_root(request, format=None):
    return Response({
        'corte': reverse('corte-list', request=request, format=format),
    })
