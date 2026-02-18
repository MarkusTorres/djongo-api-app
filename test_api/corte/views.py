from corte.models import Corte
from corte.serializer import CorteSerializer
from gasto_fijo.models import GastoFijo
from operacion.models import Operacion
from django.db.models import Sum, Q
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework import viewsets, status
from rest_framework.response import Response
from tokens.views import auth_check
from utils import base_utils
from rest_framework.decorators import action
import datetime
from django.core.exceptions import ObjectDoesNotExist


class CorteViewSet(base_utils.GenericViewSetAuth):
    queryset = Corte.objects.all()
    serializer_class = CorteSerializer

    @auth_check()
    def create(self, request, *args, **kwargs):
        data = request.data
        new_item = Corte.objects.create(
            id=base_utils.get_model_new_id(Corte),
            comentario=data['comentario'],
            fecha_inicio=data['fecha_inicio'],
            fecha_final=data['fecha_final'],
            gastos_fijos=data['gastos_fijos'],
            gastos_ocasionales=data['gastos_ocasionales'],
            total_ingresos=data['total_ingresos'],
        )
        serializer = CorteSerializer(new_item)
        return Response(serializer.data)

    @auth_check()
    def retrieve(self, request, *args, **kwargs):
        pk = request.parser_context['kwargs']['pk']
        queryset = Corte.objects.filter(id__exact=pk)
        serializer_context = {
            'request': request,
        }
        serializer = CorteSerializer(queryset, context=serializer_context, many=True)
        return Response(serializer.data)

    @auth_check()
    def destroy(self, request, *args, **kwargs):
        try:
            pk = request.parser_context['kwargs']['pk']
            queryset = Corte.objects.filter(id__exact=pk)
            queryset.delete()
            return Response(data="object successfully deleted")
        except Corte.DoesNotExist:
            return Response(data="No object found in DB")
        except Corte.MultipleObjectsReturned:
            return Response(data="Multiple objects found in DB")

    @auth_check()
    def update(self, request, *args, **kwargs):
        data = request.data
        id_obj = kwargs['pk']
        corte_obj = Corte.objects.get(id=id_obj)

        corte_obj.comentario = base_utils.value_or_default('comentario', data, corte_obj.comentario)
        corte_obj.fecha_inicio = base_utils.value_or_default('fecha_inicio', data, corte_obj.fecha_inicio)
        corte_obj.fecha_final = base_utils.value_or_default('fecha_final', data, corte_obj.fecha_final)
        corte_obj.gastos_fijos = base_utils.value_or_default('gastos_fijos', data, corte_obj.gastos_fijos)
        corte_obj.gastos_ocasionales = base_utils.value_or_default('gastos_ocasionales', data, corte_obj.gastos_ocasionales)
        corte_obj.total_ingresos = base_utils.value_or_default('total_ingresos', data, corte_obj.total_ingresos)

        corte_obj.save()
        serialized_obj = CorteSerializer(corte_obj)

        return Response(serialized_obj.data, status=status.HTTP_200_OK)

    @auth_check()
    @action(detail=False, methods=['post'])
    def filtro_fecha(self, request, pk=None):
        try:
            data = request.data
            fecha_1 = datetime.datetime.strptime(data['fecha1'], '%Y-%m-%d') if data['fecha1'] else None
            fecha_2 = datetime.datetime.strptime(data['fecha2'], '%Y-%m-%d') if data['fecha2'] else None

            query_result = Corte.objects.filter(fecha_inicio__range=(fecha_1, fecha_2)) if (fecha_1 and fecha_2) else None

            serializer_context = {
                'request': request,
            }
            serializer = CorteSerializer(query_result, context=serializer_context, many=True)

            return Response(serializer.data)
        except ObjectDoesNotExist:
            return Response([])
        except Exception:
            return Response([])

    @auth_check()
    @action(detail=False, methods=['get'])
    def auto_corte(self, request):
        current_date = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d')
        existing = Corte.objects.filter(fecha_inicio=current_date).first()
        if existing:
            return Response({'message': 'A corte already exists for the current date'}, status=status.HTTP_200_OK)
        today = datetime.date.today()
        # total_gastos_fijos = GastoFijo.objects.aggregate(total=Sum('cantidad'))['total'] or 0
        total_gastos_fijos = list(GastoFijo.objects.all().values())
        total_ingresos = Operacion.objects.filter(
            fecha_inicio=today
        ).filter(
            Q(finalizada__in=[True]) | Q(status='efectiva')
        ).aggregate(total=Sum('precio'))['total'] or 0
        # breakpoint()
        new_item = Corte.objects.create(
            id=base_utils.get_model_new_id(Corte),
            comentario='Corte generado de manera automatica',
            fecha_inicio=current_date,
            fecha_final=current_date,
            gastos_fijos=total_gastos_fijos,
            gastos_ocasionales=[],
            total_ingresos=total_ingresos
        )

        serializer = CorteSerializer(new_item)
        return Response(serializer.data)


@api_view
def api_root(request, format=None):
    return Response({
        'corte': reverse('corte-list', request=request, format=format),
    })
