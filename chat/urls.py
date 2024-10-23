from django.urls import path, include
from rest_framework.routers import DefaultRouter
from chat.views import SalaViewSet, MensagemViewSet

router = DefaultRouter()
router.register(r"salas", SalaViewSet)

message_list = MensagemViewSet.as_view({"get": "list", "post": "create"})

urlpatterns = [
    path("", include(router.urls)),
    path("salas/<int:sala_pk>/mensagens/", message_list, name="mensagens"),
]
