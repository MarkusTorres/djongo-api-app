# from django.shortcuts import render
from empleado.models import Empleado
from empleado.serializers import EmpleadoSerializer
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework import viewsets
from rest_framework.response import Response


class EmpleadoViewSet(viewsets.ModelViewSet):
    queryset = Empleado.objects.all()
    serializer_class = EmpleadoSerializer

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

@api_view
def api_root(request, format=None):
    return Response({
        'empleados': reverse('empleado-list', request=request, format=format),
    })
