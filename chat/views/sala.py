from rest_framework import viewsets, permissions
from django.contrib.auth.models import User
from chat.models import Sala
from chat.serializers import SalaSerializer


class SalaViewSet(viewsets.ModelViewSet):
    queryset = Sala.objects.all()
    serializer_class = SalaSerializer
    permission_classes = [permissions.IsAuthenticated]
