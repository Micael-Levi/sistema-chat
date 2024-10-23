import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status


@pytest.mark.django_db
def test_usuario_registro():
    client = APIClient()
    data = {
        "username": "usuarioteste",
        "password": "usuarioteste",
        "email": "usuarioteste@examplo.com",
    }
    response = client.post("/api/auth/registrar/", data)

    assert response.status_code == status.HTTP_201_CREATED
    assert User.objects.filter(username="usuarioteste").exists()


@pytest.mark.django_db
def test_usuario_login():
    user = User.objects.create_user(username="usuarioteste", password="usuarioteste")

    client = APIClient()
    data = {"username": "usuarioteste", "password": "usuarioteste"}
    response = client.post("/api/auth/login/", data)

    assert response.status_code == status.HTTP_200_OK
    assert "access" in response.data
    assert "refresh" in response.data
