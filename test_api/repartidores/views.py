from repartidores.models import Repartidor
from repartidores.serializers import RepartidorSerializer
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework import viewsets
from rest_framework.response import Response
from tokens.views import auth_check
from utils import base_utils


class RepartidorViewSet(base_utils.GenericViewSetAuth):
    queryset = Repartidor.objects.all()
    serializer_class = RepartidorSerializer

    @auth_check()
    def create(self, request, *args, **kwargs):
        data = request.data
        new_item = Repartidor.objects.create(
            id=base_utils.get_model_new_id(Repartidor),
            nombre=data['nombre'],
            sueldo=data['sueldo'],
            id_prestamo=data['id_prestamo']
        )
        serializer = RepartidorSerializer(new_item)
        return Response(serializer.data)

    @auth_check()
    def retrieve(self, request, *args, **kwargs):
        pk = request.parser_context['kwargs']['pk']
        queryset = Repartidor.objects.filter(id__exact=pk)
        serializer_context = {
            'request': request,
        }
        serializer = RepartidorSerializer(queryset, context=serializer_context, many=True)
        return Response(serializer.data)

    @auth_check()
    def destroy(self, request, *args, **kwargs):
        try:
            pk = request.parser_context['kwargs']['pk']
            queryset = Repartidor.objects.filter(id__exact=pk)
            queryset.delete()
            return Response(data="object successfully deleted")
        except Repartidor.DoesNotExist:
            return Response(data="No object found in DB")
        except Repartidor.MultipleObjectsReturned:
            return Response(data="Multiple objects found in DB")

@api_view
def api_root(request, format=None):
    return Response({
        'repartidores': reverse('repartidor-list', request=request, format=format),
    })
