from rest_framework import viewsets
from tokens.views import auth_check


class GenericViewSetAuth(viewsets.ModelViewSet):

    @auth_check()
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @auth_check()
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @auth_check()
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @auth_check()
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @auth_check()
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


def value_or_default(key, data_struct, default):
    if key not in data_struct.keys():
        return default
    else:
        return data_struct[key]
