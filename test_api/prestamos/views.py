import datetime
import json
from utils import base_utils
from rest_framework import viewsets
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from prestamos.models import Prestamo
from prestamos.serializers import PrestamoSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from tokens.views import auth_check


# class PrestamosViewSet(base_utils.GenericViewSetAuth):
class PrestamosViewSet(viewsets.ModelViewSet):
    queryset = Prestamo.objects.all()
    serializer_class = PrestamoSerializer

    # @auth_check()
    def create(self, request, *args, **kwargs):
        data = request.data
        new_item = Prestamo.objects.create(
            id=base_utils.get_model_new_id(Prestamo),
            id_empleado=data['id_empleado'],
            cantidad=data['cantidad'],
            remanente=data['cantidad'],
            fecha=str(datetime.date.today()),
            liquidado=False,
            historial={}    # default historial value
        )
        # serializer = self.get_serializer(data=request.data, many=True)
        serializer = PrestamoSerializer(new_item)
        headers = self.get_success_headers(new_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    # list operation can be default behaviour

    # @auth_check()
    @action(detail=False, methods=['get'])
    def filtro(self, request, pk=None):
        filter_val = request.GET.get('liquidado')
        value = 1 if filter_val == 'true' else 0
        queryset = Prestamo.objects.filter(liquidado=value)

        serializer_context = {
            'request': request,
        }
        serializer = PrestamoSerializer(queryset, context=serializer_context, many=True)

        return Response(serializer.data)

    # def destroy(self, request, *args, **kwargs):
    #     raise Http404

    @staticmethod
    def create_abono_str(abono_cantidad):
        json_str = f'{{"cantidad":{str(abono_cantidad)},"fecha":"{str(datetime.datetime.now())}"}}'
        return json.loads(json_str)

    @staticmethod
    def add_json_entry(json_list, json_object):
        json_list = json_list if json_list else []
        json_list.append(json_object)

        return json_list

    def update(self, request, *args, **kwargs):
        data = request.data
        target_id = data['id']

        try:
            target_prestamo = Prestamo.objects.filter(id__exact=target_id).get()
            abono = data['abono']
            # remanente se actualiza con el abono
            cantidad = target_prestamo.remanente
            nuevo_remanente = cantidad - abono
            if nuevo_remanente < 0:
                return Response(data='El abono implica remanente negativo', status=status.HTTP_400_BAD_REQUEST)
            if nuevo_remanente == 0:
                target_prestamo.liquidado = True
            # se agrega un entry al historial con cantidad y fecha
            historial = target_prestamo.historial
            new_entry = self.create_abono_str(abono)
            target_prestamo.historial = self.add_json_entry(historial, new_entry)

            target_prestamo.remanente = nuevo_remanente
            target_prestamo.fecha = str(target_prestamo.fecha)

            target_prestamo.save()
            serializer_class = PrestamoSerializer(target_prestamo)
            result = serializer_class.data
            headers = self.get_success_headers(result)
            return Response(result, status=status.HTTP_201_CREATED, headers=headers)
        except ObjectDoesNotExist:
            return Response(data=f'id {target_id} not found', status=status.HTTP_400_BAD_REQUEST)

    @auth_check()
    def retrieve(self, request, *args, **kwargs):
        pk = request.parser_context['kwargs']['pk']
        queryset = Prestamo.objects.filter(id__exact=pk)
        serializer_context = {
            'request': request,
        }
        serializer = PrestamoSerializer(queryset, context=serializer_context, many=True)
        return Response(serializer.data)

    @auth_check()
    def destroy(self, request, *args, **kwargs):
        try:
            pk = request.parser_context['kwargs']['pk']
            queryset = Prestamo.objects.filter(id__exact=pk)
            queryset.delete()
            return Response(data="object successfully deleted")
        except Prestamo.DoesNotExist:
            return Response(data="No object found in DB")
        except Prestamo.MultipleObjectsReturned:
            return Response(data="Multiple objects found in DB")
