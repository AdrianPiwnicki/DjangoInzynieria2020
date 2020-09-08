from django.contrib.auth.models import User
from django.db.models import Count, Max, Q
from rest_framework import viewsets, status, generics
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from django.http import JsonResponse, HttpResponse
from rest_framework.utils import json
from backendApp.models import Products, Recipes, Ingredients
from backendApp.serializers import UserSerializer, ProductsSerializer, RecipesSerializer, MinRecipesSerializer, \
    MinIngredientsSerializer
from django.db.models.functions import Substr


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class ProduktyViewSet(viewsets.ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductsSerializer
    parser_class = (FileUploadParser,)

    def post(self, request, *args, **kwargs):
        file_serializer = ProductsSerializer(data=request.data)
        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProduktyWszystkie(generics.ListAPIView):
    queryset = Products.objects.all().order_by('-popularity')
    serializer_class = ProductsSerializer

    def list(self, request, *arg, **kwargs):
        queryset = self.get_queryset()
        serializer = ProductsSerializer(queryset, many=True)
        return JsonResponse(serializer.data, safe=False)


class ProduktyWarzywa(generics.ListAPIView):
    queryset = Products.objects.filter(category="warzywa").order_by('-popularity')
    serializer_class = ProductsSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = ProductsSerializer(queryset, many=True)
        return JsonResponse(serializer.data, safe=False)


class ProduktyOwoce(generics.ListAPIView):
    queryset = Products.objects.filter(category="owoce").order_by('-popularity')
    serializer_class = ProductsSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = ProductsSerializer(queryset, many=True)
        return JsonResponse(serializer.data, safe=False)


class ProduktyMieso(generics.ListAPIView):
    queryset = Products.objects.filter(category="mięso").order_by('-popularity')
    serializer_class = ProductsSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = ProductsSerializer(queryset, many=True)
        return JsonResponse(serializer.data, safe=False)


class ProduktyNabial(generics.ListAPIView):
    queryset = Products.objects.filter(category="nabiał").order_by('-popularity')
    serializer_class = ProductsSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = ProductsSerializer(queryset, many=True)
        return JsonResponse(serializer.data, safe=False)


class ProduktyInne(generics.ListAPIView):
    queryset = Products.objects.filter(category="inne").order_by('-popularity')
    serializer_class = ProductsSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = ProductsSerializer(queryset, many=True)
        return JsonResponse(serializer.data, safe=False)


class ProduktyRyby(generics.ListAPIView):
    queryset = Products.objects.filter(category="ryby").order_by('-popularity')
    serializer_class = ProductsSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = ProductsSerializer(queryset, many=True)
        return JsonResponse(serializer.data, safe=False)


class ProduktyZboza(generics.ListAPIView):
    queryset = Products.objects.filter(category="zboża").order_by('-popularity')
    serializer_class = ProductsSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = ProductsSerializer(queryset, many=True)
        return JsonResponse(serializer.data, safe=False)


class ProduktyPrzyprawy(generics.ListAPIView):
    queryset = Products.objects.filter(category="przyprawy").order_by('-popularity')
    serializer_class = ProductsSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = ProductsSerializer(queryset, many=True)
        return JsonResponse(serializer.data, safe=False)


class PrzepisyViewSet(viewsets.ModelViewSet):
    queryset = Recipes.objects.all()
    serializer_class = RecipesSerializer


def lista_przepisow(request):
    body = json.loads(request.body)
    list1 = body['products']
    ls_przepisow = list()

    max_skladnikow = Recipes.objects.filter(ingredients__product__in=list1).annotate(
        num_attr=Count('ingredients__product')).filter(num_attr=len(list1))
    max_skladnik = max_skladnikow[0]

    for max_count in max_skladnikow.all():
        if max_count.ingredients.count() > max_skladnik.ingredients.count():
            max_skladnik = max_count
    max_skladnik = max_skladnik.ingredients.count()

    for addition in range(max_skladnik):
        for i in range(len(list1), 0, -1):
            for przepis in Recipes.objects.filter(ingredients__product__in=list1).annotate(
                    num_attr=Count('ingredients__product')).filter(num_attr=i):
                if przepis.ingredients.count() == i + addition:
                    przepis.preparation = przepis.preparation[0:255]
                    if przepis.preparation[254] == "!" or przepis.preparation[254] == "?" or przepis.preparation[
                        254] == " " or przepis.preparation[254] == ",":
                        przepis.preparation = przepis.preparation[0:254] + "..."
                    elif przepis.preparation[254] == ".":
                        przepis.preparation += ".."
                    else:
                        przepis.preparation += "..."
                    ls_przepisow.append(przepis)

    serializer = MinRecipesSerializer(ls_przepisow, many=True, context={'list': list1})
    return JsonResponse(serializer.data, safe=False)
