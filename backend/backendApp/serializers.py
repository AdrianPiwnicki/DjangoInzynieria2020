from django.contrib.auth.models import User
from rest_framework import serializers

from backend.backendApp.models import Produkty, Przepisy


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']


class ProduktySerializer(serializers.ModelSerializer):
    class Meta:
        model = Produkty
        fields = '__all__'


class PrzepisySerializer(serializers.ModelSerializer):
    class Meta:
        model = Przepisy
        fields = ['nazwa', 'przygotowanie', 'czas', 'skladniki']