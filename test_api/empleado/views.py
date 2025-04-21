# from django.shortcuts import render
from empleado.models import Empleado
from empleado.serializers import EmpleadoSerializer
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework import viewsets, status
from rest_framework.response import Response
from tokens.views import auth_check
from utils import base_utils


def repartidor_info(id):
    try:
        result = Empleado.objects.get(id__exact=id)
        return result.nombre
    except Empleado.DoesNotExist:
        return None


def get_repartidores():
    queryset = Empleado.objects.filter(id_tipo=1)
    return {empleado.id: empleado.nombre for empleado in queryset}


class EmpleadoViewSet(base_utils.GenericViewSetAuth):
    queryset = Empleado.objects.all()
    serializer_class = EmpleadoSerializer

    @auth_check()
    def create(self, request, *args, **kwargs):
        data = request.data
        new_item = Empleado.objects.create(
            id=base_utils.get_model_new_id(Empleado),
            id_tipo=data['id_tipo'],
            nombre=data['nombre'],
            posicion=data['posicion'],
            sueldo=data['sueldo'],
            usuario_nombre=data['usuario_nombre'],
            usuario_password=data['usuario_password'],
            fecha_inicio=data['fecha_inicio'],
            fecha_final=data['fecha_final']
        )
        serializer = EmpleadoSerializer(new_item)
        return Response(serializer.data)

    @auth_check()
    def update(self, request, *args, **kwargs):
        data = request.data
        id_obj = kwargs['pk']
        empleado_obj = Empleado.objects.get(id=id_obj)

        empleado_obj.id_tipo = base_utils.value_or_default('id_tipo', data, empleado_obj.id_tipo)
        empleado_obj.nombre = base_utils.value_or_default('nombre', data, empleado_obj.nombre)
        empleado_obj.posicion = base_utils.value_or_default('posicion', data, empleado_obj.posicion)
        empleado_obj.sueldo = base_utils.value_or_default('sueldo', data, empleado_obj.sueldo)
        empleado_obj.usuario_nombre = base_utils.value_or_default('usuario_nombre', data, empleado_obj.usuario_nombre)
        empleado_obj.usuario_password = base_utils.value_or_default('usuario_password', data, empleado_obj.usuario_password)
        empleado_obj.fecha_inicio = base_utils.value_or_default('fecha_inicio', data, empleado_obj.fecha_inicio)
        empleado_obj.fecha_final = base_utils.value_or_default('fecha_final', data, empleado_obj.fecha_final)

        empleado_obj.save()
        serialized_obj = EmpleadoSerializer(empleado_obj)

        return Response(serialized_obj.data, status=status.HTTP_200_OK)

    @auth_check()
    def retrieve(self, request, *args, **kwargs):
        pk = request.parser_context['kwargs']['pk']
        queryset = Empleado.objects.filter(id__exact=pk)
        serializer_context = {
            'request': request,
        }
        serializer = EmpleadoSerializer(queryset, context=serializer_context, many=True)
        return Response(serializer.data)

    @auth_check()
    def destroy(self, request, *args, **kwargs):
        try:
            pk = request.parser_context['kwargs']['pk']
            queryset = Empleado.objects.filter(id__exact=pk)
            queryset.delete()
            return Response(data="object successfully deleted")
        except Empleado.DoesNotExist:
            return Response(data="No object found in DB")
        except Empleado.MultipleObjectsReturned:
            return Response(data="Multiple objects found in DB")


@api_view
def api_root(request, format=None):
    return Response({
        'empleados': reverse('empleado-list', request=request, format=format),
    })
