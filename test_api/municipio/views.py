from municipio.models import Municipio
from municipio.serializers import MunicipioSerializer
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework import viewsets
from rest_framework.response import Response


class MunicipioViewSet(viewsets.ModelViewSet):
    queryset = Municipio.objects.all()
    serializer_class = MunicipioSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        id = Municipio.objects.count() + 1
        new_item = Municipio.objects.create(
            id=Municipio.objects.count()+1,
            nombre=data['nombre'],
            precio=data['precio']
        )
        new_item.id = id
        # breakpoint()
        new_item.save()
        serializer = MunicipioSerializer(new_item)
        return Response(serializer.data)

@api_view
def api_root(request, format=None):
    return Response({
        'municipios': reverse('municipio-list', request=request, format=format),
    })
