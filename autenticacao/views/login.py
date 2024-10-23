from rest_framework_simplejwt.views import TokenObtainPairView
from autenticacao.serializers import LoginSerializer


class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer
