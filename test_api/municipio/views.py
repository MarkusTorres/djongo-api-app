from municipio.models import Municipio
from municipio.serializers import MunicipioSerializer
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework import viewsets
from rest_framework.response import Response


class MunicipioViewSet(viewsets.ModelViewSet):
    queryset = Municipio.objects.all()
    serializer_class = MunicipioSerializer

@api_view
def api_root(request, format=None):
    return Response({
        'municipios': reverse('municipio-list', request=request, format=format),
    })
