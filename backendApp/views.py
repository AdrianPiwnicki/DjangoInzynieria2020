from django.contrib.auth.models import User
from django.db.models import Count, Max
from rest_framework import viewsets, status, generics
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from django.http import JsonResponse, HttpResponse
from rest_framework.utils import json
from backendApp.models import Produkty, Przepisy
from backendApp.serializers import UserSerializer, ProduktySerializer, PrzepisySerializer, MinPrzepisySerializer
from django.db.models.functions import Substr


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


def lista_przepisow(request):
    body = json.loads(request.body)
    list1 = body['produkty']
    ls_przepisow = list()
    max_skladnikow = Przepisy.objects.filter(skladniki__produkt__in=list1).annotate(
        num_attr=Count('skladniki__produkt')).filter(num_attr=len(list1))
    max_skladnik = max_skladnikow[0]

    for max_count in max_skladnikow.all():
        if max_count.skladniki.count() > max_skladnik.skladniki.count():
            max_skladnik = max_count
    max_skladnik = max_skladnik.skladniki.count()

    for addition in range(max_skladnik):
        for i in range(len(list1), 0, -1):
            for przepis in Przepisy.objects.filter(skladniki__produkt__in=list1).annotate(
                    num_attr=Count('skladniki__produkt')).filter(num_attr=i):
                if przepis.skladniki.count() == i + addition:
                    przepis.przygotowanie = przepis.przygotowanie[0:255]
                    if przepis.przygotowanie[254] == "!" or przepis.przygotowanie[254] == "?" or przepis.przygotowanie[254] == " " or przepis.przygotowanie[254] == ",":
                        przepis.przygotowanie = przepis.przygotowanie[0:254]+"..."
                    elif przepis.przygotowanie[254] == ".":
                        przepis.przygotowanie += ".."
                    else:
                        przepis.przygotowanie += "..."
                    ls_przepisow.append(przepis)

    serializer = MinPrzepisySerializer(ls_przepisow, many=True)
    return JsonResponse(serializer.data, safe=False)
