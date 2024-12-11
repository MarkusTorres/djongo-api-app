from tokens.models import Tokens
from tokens.serializers import TokensSerializer
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.http import Http404
from rest_framework.decorators import action
import hashlib


# Create your views here.
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
        # shall create the token and add it to the table
        # hashlib.sha256(b"Nobody inspects the spammish repetition").hexdigest() -> hash to use
        print("\ntoken log-in\n")
        # breakpoint()
        # request.META.get('HTTP_USER')
        # request.META['HTTP_USER']
        user = request.META['HTTP_USER']
        gen_hash = hashlib.sha256(user).hexdigest()
        print(gen_hash)


    @action(detail=True, methods=['post'])
    def log_out(self, request):
        # retrieve the token from header, validate it and delete the register
        # for header use request.META.get('attribute')
        pass

@api_view
def api_root(request, format=None):
    return Response({
        'token': reverse('token', request=request, format=format),
    })
