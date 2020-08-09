from django.contrib.auth.models import User
from rest_framework import viewsets, status
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView

from backend.backendApp.models import Produkty, Przepisy
from backend.backendApp.serializers import UserSerializer, ProduktySerializer, PrzepisySerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

class ProduktyViewSet(viewsets.ModelViewSet):
    queryset = Produkty.objects.all()
    serializer_class = ProduktySerializer
    parser_class = (FileUploadParser,)

    def post(self, request, *args, **kwargs):
        file_serializer = ProduktySerializer(data=request.data)
        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PrzepisyViewSet(viewsets.ModelViewSet):
    queryset = Przepisy.objects.all()
    serializer_class = PrzepisySerializer
