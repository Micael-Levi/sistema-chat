import pytest
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken
from channels.db import database_sync_to_async
from channels.layers import get_channel_layer
from channels.testing import WebsocketCommunicator
from sistema_chat.asgi import application
from chat.models import Sala


@pytest.mark.django_db
def test_criar_sala():
    usuario = User.objects.create_user(username="usuarioteste", password="usuarioteste")

    client = APIClient()
    client.force_authenticate(user=usuario)

    response = client.post("/api/salas/", {"nome": "Sala de Teste"})

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["nome"] == "Sala de Teste"


@pytest.mark.django_db
def test_listar_salas():
    usuario = User.objects.create_user(username="testuser", password="testpass123")

    client = APIClient()
    client.force_authenticate(user=usuario)

    client.post("/api/salas/", {"nome": "Sala 1"})
    client.post("/api/salas/", {"nome": "Sala 2"})

    response = client.get("/api/salas/")

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2
    assert response.data[0]["nome"] == "Sala 1"
    assert response.data[1]["nome"] == "Sala 2"


from chat.models import Sala, Mensagem


@pytest.mark.django_db
def test_historico_mensagens_sala():
    usuario = User.objects.create_user(username="testuser", password="testpass123")

    client = APIClient()
    client.force_authenticate(user=usuario)

    response = client.post("/api/salas/", {"nome": "Sala de Teste"})
    sala_id = response.data["id"]

    Mensagem.objects.create(
        sala_id=sala_id, usuario=usuario, conteudo="Primeira mensagem"
    )
    Mensagem.objects.create(
        sala_id=sala_id, usuario=usuario, conteudo="Segunda mensagem"
    )

    # Consultar o histórico de mensagens da sala
    response = client.get(f"/api/salas/{sala_id}/mensagens/")

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2
    assert response.data[0]["conteudo"] == "Primeira mensagem"
    assert response.data[1]["conteudo"] == "Segunda mensagem"


@database_sync_to_async
def criar_usuario(username, password):
    return User.objects.create_user(username=username, password=password)


@database_sync_to_async
def criar_sala(nome):
    return Sala.objects.create(nome=nome)


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_conexao_valida():
    usuario = await criar_usuario(username="usuarioteste", password="senhateste")
    sala = await criar_sala(nome="salateste")
    access_token = str(AccessToken.for_user(usuario))

    communicator = WebsocketCommunicator(
        application, f"/ws/chat/{sala.nome}/?token={access_token}"
    )
    connected, _ = await communicator.connect()

    assert connected is True
    await communicator.disconnect()


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_conexao_invalida():
    communicator = WebsocketCommunicator(application, "/ws/chat/salateste/")
    connected, _ = await communicator.connect()

    assert connected is False
    await communicator.disconnect()


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_envio_mensagem():
    usuario = await criar_usuario(username="usuarioteste2", password="senhateste2")
    sala = await criar_sala(nome="salateste2")
    access_token = str(AccessToken.for_user(usuario))

    communicator = WebsocketCommunicator(
        application, f"/ws/chat/{sala.nome}/?token={access_token}"
    )
    connected, _ = await communicator.connect()

    assert connected is True

    await communicator.send_json_to(
        {"mensagem": "Olá, esta é uma mensagem de teste!", "username": "usuarioteste2"}
    )

    response = await communicator.receive_json_from()
    assert response["mensagem"] == "Olá, esta é uma mensagem de teste!"
    assert response["username"] == usuario.username

    await communicator.disconnect()
