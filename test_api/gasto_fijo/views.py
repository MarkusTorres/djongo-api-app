from gasto_fijo.models import GastoFijo
from gasto_fijo.serializer import GastoFijoSerializer
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework import viewsets, status
from rest_framework.response import Response
from tokens.views import auth_check
from utils import base_utils


class GastoFijoViewSet(base_utils.GenericViewSetAuth):
    queryset = GastoFijo.objects.all()
    serializer_class = GastoFijoSerializer

    @auth_check()
    def create(self, request, *args, **kwargs):
        data = request.data
        new_item = GastoFijo.objects.create(
            id=base_utils.get_model_new_id(GastoFijo),
            concepto=data['concepto'],
            cantidad=data['cantidad'],
            habilitado=data['habilitado']
        )
        serializer = GastoFijoSerializer(new_item)
        return Response(serializer.data)

    @auth_check()
    def retrieve(self, request, *args, **kwargs):
        pk = request.parser_context['kwargs']['pk']
        queryset = GastoFijo.objects.filter(id__exact=pk)
        serializer_context = {
            'request': request,
        }
        serializer = GastoFijoSerializer(queryset, context=serializer_context, many=True)
        return Response(serializer.data)

    @auth_check()
    def destroy(self, request, *args, **kwargs):
        try:
            pk = request.parser_context['kwargs']['pk']
            queryset = GastoFijo.objects.filter(id__exact=pk)
            queryset.delete()
            return Response(data="object successfully deleted")
        except GastoFijo.DoesNotExist:
            return Response(data="No object found in DB")
        except GastoFijo.MultipleObjectsReturned:
            return Response(data="Multiple objects found in DB")

    def update(self, request, *args, **kwargs):
        data = request.data
        id_obj = kwargs['pk']
        gasto_fijo_obj = GastoFijo.objects.get(id=id_obj)

        gasto_fijo_obj.concepto = base_utils.value_or_default('concepto', data, gasto_fijo_obj.concepto)
        gasto_fijo_obj.cantidad = base_utils.value_or_default('cantidad', data, gasto_fijo_obj.cantidad)
        gasto_fijo_obj.habilitado = base_utils.value_or_default('habilitado', data, gasto_fijo_obj.habilitado)

        gasto_fijo_obj.save()
        serialized_obj = GastoFijoSerializer(gasto_fijo_obj)

        return Response(serialized_obj.data, status=status.HTTP_200_OK)


@api_view
def api_root(request, format=None):
    return Response({
        'gasto_fijo': reverse('gasto-fijo-list', request=request, format=format),
    })
