from rest_framework import viewsets, permissions
from django.contrib.auth.models import User
from chat.models import Mensagem
from chat.serializers import MensagemSerializer


class MensagemViewSet(viewsets.ModelViewSet):
    queryset = Mensagem.objects.all()
    serializer_class = MensagemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        sala_id = self.kwargs["sala_pk"]
        return Mensagem.objects.filter(sala__id=sala_id)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
