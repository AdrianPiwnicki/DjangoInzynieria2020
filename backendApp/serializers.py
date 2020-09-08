from django.contrib.auth.models import User
from rest_framework import serializers
from backendApp.models import Products, Recipes, Ingredients


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']


class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ['id', 'name', 'graphics']


class IngredientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredients
        fields = ['quantity', 'converter', 'product']


class MinIngredientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredients
        fields = ['product']


class RecipesSerializer(serializers.ModelSerializer):
    ingredients = IngredientsSerializer(many=True)

    class Meta:
        model = Recipes
        fields = ['name', 'preparation', 'time', 'ingredients']

    def create(self, validated_data):
        ingredients = validated_data["ingredients"]
        del validated_data["ingredients"]

        recipe = Recipes.objects.create(**validated_data)

        for ingredient in ingredients:
            s = Ingredients.objects.create(**ingredient)
            recipe.ingredients.add(s)

        recipe.save()
        return recipe


class MinRecipesSerializer(serializers.ModelSerializer):
    ingredients = MinIngredientsSerializer(many=True)
    additional = serializers.SerializerMethodField('get_additional')

    class Meta:
        model = Recipes
        fields = ['id', 'name', 'preparation', 'photo', 'ingredients', 'additional']

    def get_additional(self, obj):
        list1 = self.context.get("list1")
        string_additional = ""
        for o in obj.ingredients.all():
            if o.product.id not in list1:
                string_additional += o.product.name
                string_additional += ", "
        if string_additional != "":
            lista = list(string_additional)
            lista = lista[:len(lista)-2]
            string_lista = "".join(lista)
            return string_lista
        else:
            return string_additional
