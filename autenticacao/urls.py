from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import RegistroView, LoginView

urlpatterns = [
    path("registrar/", RegistroView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
