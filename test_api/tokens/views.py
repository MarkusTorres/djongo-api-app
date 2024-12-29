from tokens.models import Tokens
from empleado.models import Empleado
from tokens.serializers import TokensSerializer
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.http import Http404
from rest_framework.decorators import action
import hashlib
from django.core.exceptions import ObjectDoesNotExist
import jwt
import time
import datetime as dt
from test_api.settings import SECRET_KEY


# Create your views here.
def _header_exists(headers, value):
    if value not in headers.keys():
        return None
    return headers[value]


def auth_check():
    def decorator(func):
        def wrapper(*args, **kwargs):
            # breakpoint()
            token_data = _header_exists(args[1].META, 'HTTP_TOKEN')
            # add return for None on token_data
            token_exists = list(Tokens.objects.filter(token=token_data))
            if not token_exists:
                return Response(data="Token is not valid", status=status.HTTP_400_BAD_REQUEST)
            return func(*args, **kwargs)
        return wrapper
    return decorator


class AuthViewSet(viewsets.ModelViewSet):
    queryset = Tokens.objects.all()
    serializer_class = TokensSerializer

    def create(self, request, *args, **kwargs):
        raise Http404

    def list(self, request, *args, **kwargs):
        return Response("Not allowed", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, *args, **kwargs):
        raise Http404

    def update(self, request, *args, **kwargs):
        raise Http404

    def retrieve(self, request, *args, **kwargs):
        raise Http404

    @action(detail=False, methods=['get'])
    def log_in(self, request, pk=None):
        user_data = _header_exists(request.META, 'HTTP_USER')
        pass_data = _header_exists(request.META, 'HTTP_PASS')
        users = None
        if not user_data or not pass_data:
            return Response(data="Credentials not specified", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        # check if user exists
        try:
            users = Empleado.objects.filter(nombre__exact=user_data).get()
        except ObjectDoesNotExist:
            return Response(data="User not found", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        token_exists = Tokens.objects.filter(user_id__exact=user_data).exists()
        # if it does not exist create the token entry and return the token data
        # if it does indeed exist return Error
        if token_exists:
            return Response(data="Token for user already created", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        # create the entry on DB
        data = request.data
        id = Tokens.objects.count() + 1
        user_encoded_token = jwt.encode({"user": user_data}, SECRET_KEY + str(time.time()), algorithm="HS256")
        new_token = Tokens.objects.create(
            id=id,
            user_id=user_data,
            token=user_encoded_token,
            created=dt.datetime.now().strftime('%Y-%m-%d')
        )
        new_token.id = id
        new_token.save()
        serializer = TokensSerializer(new_token)
        # TODO: add cp on 'operacion', delete dates on 'empleado' and create and endpoint
        #  for checking if a code is already created on operacion
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def log_out(self, request):
        token_data = _header_exists(request.META, 'HTTP_TOKEN')
        token_exists = Tokens.objects.get(token=token_data)
        if token_exists is None:
            return Response(data="Token is not valid", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        token_obj = Tokens.objects.filter(token__exact=token_data).get()
        token_obj.delete()
        return Response(data="Token successfully deleted", status=status.HTTP_200_OK)


@api_view
def api_root(request, format=None):
    return Response({
        'token': reverse('token', request=request, format=format),
    })
