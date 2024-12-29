from rest_framework import serializers
from tokens.models import Tokens


class TokensSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Tokens
        fields = ['id', 'user_id', 'token', 'created']
