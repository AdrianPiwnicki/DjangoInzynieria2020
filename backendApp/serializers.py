from django.contrib.auth.models import User
from rest_framework import serializers
from backendApp.models import Produkty, Przepisy, Skladniki


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']


class ProduktySerializer(serializers.ModelSerializer):
    class Meta:
        model = Produkty
        fields = ['id', 'nazwa', 'grafika']


class SkladnikiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skladniki
        fields = ['ilosc', 'przelicznik', 'produkt']


class PrzepisySerializer(serializers.ModelSerializer):
    skladniki = SkladnikiSerializer(many=True)

    class Meta:
        model = Przepisy
        fields = ['nazwa', 'przygotowanie', 'czas', 'skladniki']

    def create(self, validated_data):
        skladniki = validated_data["skladniki"]
        del validated_data["skladniki"]

        przepis = Przepisy.objects.create(**validated_data)

        for skladnik in skladniki:
            s = Skladniki.objects.create(**skladnik)
            przepis.skladniki.add(s)

        przepis.save()
        return przepis


class MinPrzepisySerializer(serializers.ModelSerializer):

    class Meta:
        model = Przepisy
        fields = ['id', 'nazwa', 'przygotowanie']
