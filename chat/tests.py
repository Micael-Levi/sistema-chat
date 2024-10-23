import pytest
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User


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
