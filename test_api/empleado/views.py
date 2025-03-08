# from django.shortcuts import render
from empleado.models import Empleado
from empleado.serializers import EmpleadoSerializer
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework import viewsets, status
from rest_framework.response import Response
from tokens.views import auth_check
from utils import base_utils


class EmpleadoViewSet(base_utils.GenericViewSetAuth):
    queryset = Empleado.objects.all()
    serializer_class = EmpleadoSerializer

    @auth_check()
    def create(self, request, *args, **kwargs):
        data = request.data
        id = Empleado.objects.count() + 1
        new_item = Empleado.objects.create(
            id=Empleado.objects.count() + 1,
            id_tipo=data['id_tipo'],
            nombre=data['nombre'],
            posicion=data['posicion'],
            sueldo=data['sueldo'],
            usuario_nombre=data['usuario_nombre'],
            usuario_password=data['usuario_password'],
            fecha_inicio=data['fecha_inicio'],
            fecha_final=data['fecha_final']
        )
        new_item.id = id
        new_item.save()
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

        return Response(serialized_obj, status=status.HTTP_200_OK)


@api_view
def api_root(request, format=None):
    return Response({
        'empleados': reverse('empleado-list', request=request, format=format),
    })
