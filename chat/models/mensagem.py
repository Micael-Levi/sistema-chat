from django.db import models
from django.contrib.auth.models import User
from chat.models import Sala


class Mensagem(models.Model):
    sala = models.ForeignKey(Sala, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    conteudo = models.TextField()
    data = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "mensagem"

    def __str__(self):
        return f"{self.usuario.username}: {self.conteudo[:20]}..."
