from django.contrib.auth.models import User
from django.db.models import Count
from rest_framework import viewsets, status, generics
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from django.http import JsonResponse, HttpResponse
from rest_framework.utils import json
from backendApp.models import Produkty, Przepisy
from backendApp.serializers import UserSerializer, ProduktySerializer, PrzepisySerializer


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


class ProduktyWszystkie(generics.ListAPIView):
    queryset = Produkty.objects.all().order_by('-popularnosc')
    serializer_class = ProduktySerializer

    def list(self, request, *arg, **kwargs):
        queryset = self.get_queryset()
        serializer = ProduktySerializer(queryset, many=True)
        return JsonResponse(serializer.data, safe=False)


class ProduktyWarzywa(generics.ListAPIView):
    queryset = Produkty.objects.filter(kategoria="warzywa").order_by('-popularnosc')
    serializer_class = ProduktySerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = ProduktySerializer(queryset, many=True)
        return JsonResponse(serializer.data, safe=False)


class ProduktyOwoce(generics.ListAPIView):
    queryset = Produkty.objects.filter(kategoria="owoce").order_by('-popularnosc')
    serializer_class = ProduktySerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = ProduktySerializer(queryset, many=True)
        return JsonResponse(serializer.data, safe=False)


class ProduktyMieso(generics.ListAPIView):
    queryset = Produkty.objects.filter(kategoria="mięso").order_by('-popularnosc')
    serializer_class = ProduktySerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = ProduktySerializer(queryset, many=True)
        return JsonResponse(serializer.data, safe=False)


class ProduktyNabial(generics.ListAPIView):
    queryset = Produkty.objects.filter(kategoria="nabiał").order_by('-popularnosc')
    serializer_class = ProduktySerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = ProduktySerializer(queryset, many=True)
        return JsonResponse(serializer.data, safe=False)


class ProduktyInne(generics.ListAPIView):
    queryset = Produkty.objects.filter(kategoria="inne").order_by('-popularnosc')
    serializer_class = ProduktySerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = ProduktySerializer(queryset, many=True)
        return JsonResponse(serializer.data, safe=False)


class ProduktyRyby(generics.ListAPIView):
    queryset = Produkty.objects.filter(kategoria="ryby").order_by('-popularnosc')
    serializer_class = ProduktySerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = ProduktySerializer(queryset, many=True)
        return JsonResponse(serializer.data, safe=False)


class ProduktyZboza(generics.ListAPIView):
    queryset = Produkty.objects.filter(kategoria="zboża").order_by('-popularnosc')
    serializer_class = ProduktySerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = ProduktySerializer(queryset, many=True)
        return JsonResponse(serializer.data, safe=False)


class ProduktyPrzyprawy(generics.ListAPIView):
    queryset = Produkty.objects.filter(kategoria="przyprawy").order_by('-popularnosc')
    serializer_class = ProduktySerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = ProduktySerializer(queryset, many=True)
        return JsonResponse(serializer.data, safe=False)


class PrzepisyViewSet(viewsets.ModelViewSet):
    queryset = Przepisy.objects.all()
    serializer_class = PrzepisySerializer


# def lista_przepisow(request):
#     body = json.loads(request.body)
#     list1 = body['produkty']
#     ls_przepisow = []
#     przepisy = Przepisy.objects.filter(skladniki__in=list1).annotate(num_attr=Count('skladniki')).filter(num_attr=len(list1))
#     if przepisy.exists():
#         for przepis in przepisy:
#             if str(przepis.skladniki.count) == str(len(list1)):
#                 ls_przepisow.append(przepis)
#         serializer = PrzepisySerializer(ls_przepisow, many=True)
#         return JsonResponse(serializer.data, safe=False)
#     else:
#         return HttpResponse("%s" % "Brak przepisów")


def lista_przepisow(request):
    body = json.loads(request.body)
    list1 = body['produkty']
    ls_przepisow = list()
    for przepis in Przepisy.objects.filter(skladniki__produkt__in=list1).annotate(
            num_attr=Count('skladniki__produkt')).filter(num_attr=len(list1)):
        if przepis.skladniki.count() == len(list1):
            ls_przepisow.append(przepis)
    serializer = PrzepisySerializer(ls_przepisow, many=True)
    return JsonResponse(serializer.data, safe=False)
