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
    #non_field = serializers.CharField(max_length=500)

    class Meta:
        model = Recipes
        fields = ['id', 'name', 'preparation', 'photo']
