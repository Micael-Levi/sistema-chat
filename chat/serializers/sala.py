from rest_framework import serializers
from django.contrib.auth.models import User
from chat.models import Sala


class SalaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sala
        fields = ["id", "nome"]
