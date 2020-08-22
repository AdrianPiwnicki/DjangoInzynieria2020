import operator
from functools import reduce

from django.contrib.auth.models import User
from django.db.models import Q, Count
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView
from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from django.http import JsonResponse, HttpResponse
from rest_framework.utils import json
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


def lista_przepisow(request):
    body = json.loads(request.body)
    list1 = body['produkty']
    przepisy = Przepisy.objects.filter(skladniki__in=list1).annotate(num_attr=Count('skladniki')).filter(num_attr=len(list1))
    if przepisy.exists():
        serializer = PrzepisySerializer(przepisy, many=True)
        return JsonResponse(serializer.data, safe=False)
    else:
        return HttpResponse("%s" % "Brak przepisów")


