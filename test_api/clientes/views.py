from clientes.models import Cliente
from clientes.serializers import ClienteSerializer
from rest_framework.decorators import api_view, action
from rest_framework.reverse import reverse
from rest_framework import viewsets, status
from rest_framework.response import Response
from tokens.views import auth_check
from utils import base_utils
from django.db.models import Q


class ClienteViewSet(base_utils.GenericViewSetAuth):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

    @auth_check()
    def create(self, request, *args, **kwargs):
        data = request.data
        new_item = Cliente.objects.create(
            id=base_utils.get_model_new_id(Cliente),
            id_tipo=data['id_tipo'],
            nombre=data['nombre'],
            calle=data['calle'],
            num_int=data['num_int'],
            num_ext=data['num_ext'],
            colonia=data['colonia'],
            cp=data['cp'],
            telefono=data['telefono'],
            municipio=data['municipio'],
            estado=data['estado'],
            entre_calles=data['entre_calles'],
            desc_fachada=data['desc_fachada'],
            referencia=data['referencia'],
            tarifa=data['tarifa'],
            nota=data['nota']
        )
        serializer = ClienteSerializer(new_item)
        return Response(serializer.data)

    @auth_check()
    def retrieve(self, request, *args, **kwargs):
        pk = request.parser_context['kwargs']['pk']
        queryset = Cliente.objects.filter(id__exact=pk)
        serializer_context = {
            'request': request,
        }
        serializer = ClienteSerializer(queryset, context=serializer_context, many=True)
        return Response(serializer.data)

    @auth_check()
    def destroy(self, request, *args, **kwargs):
        try:
            pk = request.parser_context['kwargs']['pk']
            queryset = Cliente.objects.filter(id__exact=pk)
            queryset.delete()
            return Response(data="object successfully deleted")
        except Cliente.DoesNotExist:
            return Response(data="No object found in DB")
        except Cliente.MultipleObjectsReturned:
            return Response(data="Multiple objects found in DB")

    @auth_check()
    def update(self, request, *args, **kwargs):
        data = request.data
        cliente_obj = Cliente.objects.filter(id__exact=data['id']).get()

        cliente_obj.id_tipo = base_utils.value_or_default('id_tipo', data, cliente_obj.id_tipo)
        cliente_obj.nombre = base_utils.value_or_default('nombre', data, cliente_obj.nombre)
        cliente_obj.calle = base_utils.value_or_default('calle', data, cliente_obj.calle)
        cliente_obj.num_int = base_utils.value_or_default('num_int', data, cliente_obj.num_int)
        cliente_obj.num_ext = base_utils.value_or_default('num_ext', data, cliente_obj.num_ext)
        cliente_obj.colonia = base_utils.value_or_default('colonia', data, cliente_obj.colonia)
        cliente_obj.cp = base_utils.value_or_default('cp', data, cliente_obj.cp)
        cliente_obj.telefono = base_utils.value_or_default('telefono', data, cliente_obj.telefono)
        cliente_obj.municipio = base_utils.value_or_default('municipio', data, cliente_obj.municipio)
        cliente_obj.estado = base_utils.value_or_default('estado', data, cliente_obj.estado)
        cliente_obj.entre_calles = base_utils.value_or_default('entre_calles', data, cliente_obj.entre_calles)
        cliente_obj.desc_fachada = base_utils.value_or_default('desc_fachada', data, cliente_obj.desc_fachada)
        cliente_obj.referencia = base_utils.value_or_default('referencia', data, cliente_obj.referencia)
        cliente_obj.tarifa = base_utils.value_or_default('tarifa', data, cliente_obj.tarifa)
        cliente_obj.nota = base_utils.value_or_default('nota', data, cliente_obj.nota)

        cliente_obj.save()
        serialized_obj = ClienteSerializer(cliente_obj)

        return Response(serialized_obj.data, status=status.HTTP_200_OK)


    @action(detail=False, methods=['post'])
    @auth_check()
    def filtro(self, request, pk=None):
        try:
            data = request.data
            q_cliente = Q(id__exact=data['cliente_id'])
            queryset = Cliente.objects.filter(q_cliente)

            serializer_context = {
                'request': request,
            }
            serializer = ClienteSerializer(queryset, context=serializer_context, many=True)
            return Response(serializer.data)
        except Cliente.DoesNotExist:
            return Response(data="No se encontraron resultados")
        except Exception:
            return Response(data="Datos erroneos")


@api_view
def api_root(request, format=None):
    return Response({
        'clientes': reverse('cliente-list', request=request, format=format),
    })
