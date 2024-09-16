from operacion.models import Operacion
from operacion.serializers import OperacionSerializer
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import renderers
from rest_framework.response import Response
from rest_framework.decorators import action


class OperacionViewSet(viewsets.ModelViewSet):
    queryset = Operacion.objects.all()
    serializer_class = OperacionSerializer


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'operaciones': reverse('operacion-list', request=request, format=format),
    })
