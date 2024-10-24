import json
from channels.generic.websocket import AsyncWebsocketConsumer
from chat.models import Sala, Mensagem
from django.contrib.auth.models import User
from django.contrib.auth.models import AnonymousUser
from channels.exceptions import DenyConnection
from channels.db import database_sync_to_async


class ChatConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super(ChatConsumer, self).__init__(*args, **kwargs)
        self.nome_sala = None
        self.grupo_nome_sala = None

    async def connect(self):
        if self.scope["user"] == AnonymousUser():
            await self.close()
            raise DenyConnection("Usuário não autenticado")
        self.nome_sala = self.scope["url_route"]["kwargs"]["nome_sala"]
        self.grupo_nome_sala = f"chat_{self.nome_sala}"

        await self.channel_layer.group_add(self.grupo_nome_sala, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        await self.close(close_code)

    async def receive(self, text_data):

        data = json.loads(text_data)
        mensagem = data["mensagem"]
        username = data["username"]

        usuario = await database_sync_to_async(User.objects.get)(username=username)
        sala = await database_sync_to_async(Sala.objects.get)(nome=self.nome_sala)
        await database_sync_to_async(Mensagem.objects.create)(
            usuario=usuario, sala=sala, conteudo=mensagem
        )

        await self.channel_layer.group_send(
            self.grupo_nome_sala,
            {"type": "chat_message", "mensagem": mensagem, "username": username},
        )

    async def chat_message(self, event):
        mensagem = event["mensagem"]
        username = event["username"]

        await self.send(
            text_data=json.dumps({"mensagem": mensagem, "username": username})
        )
