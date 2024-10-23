from rest_framework import serializers
from django.contrib.auth.models import User
from chat.models import Mensagem
from autenticacao.serializers import UsuarioSerializer


class MensagemSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer(read_only=True)

    class Meta:
        model = Mensagem
        fields = ["id", "sala", "usuario", "conteudo", "data"]
