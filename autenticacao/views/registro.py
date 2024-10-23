from rest_framework import generics
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from autenticacao.serializers import UsuarioSerializer


class RegistroView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [AllowAny]
