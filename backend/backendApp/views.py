from django.contrib.auth.models import User
from rest_framework import viewsets
from backend.backendApp.models import Produkty, Przepisy
from backend.backendApp.serializers import UserSerializer, ProduktySerializer, PrzepisySerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class ProduktyViewSet(viewsets.ModelViewSet):
    queryset = Produkty.objects.all()
    serializer_class = ProduktySerializer

class PrzepisyViewSet(viewsets.ModelViewSet):
    queryset = Przepisy.objects.all()
    serializer_class = PrzepisySerializer
