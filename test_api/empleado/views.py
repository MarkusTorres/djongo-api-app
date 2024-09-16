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

@api_view
def api_root(request, format=None):
    return Response({
        'empleados': reverse('empleado-list', request=request, format=format),
    })
