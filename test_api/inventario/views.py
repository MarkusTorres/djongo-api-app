from inventario.models import Inventario
from inventario.serializers import InventarioSerializer
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework import viewsets
from rest_framework.response import Response


class InventarioViewSet(viewsets.ModelViewSet):
    queryset = Inventario.objects.all()
    serializer_class = InventarioSerializer

@api_view
def api_root(request, format=None):
    return Response({
        'inventario': reverse('inventario-list', request=request, format=format),
    })
