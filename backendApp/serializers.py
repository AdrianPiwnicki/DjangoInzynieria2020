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
    name = serializers.SerializerMethodField('get_name')

    class Meta:
        model = Ingredients
        fields = ['quantity', 'converter', 'product', 'name']

    def get_name(self, obj):
        name = Products.objects.get(id=obj.product.id)
        return name.name


class MinIngredientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredients
        fields = ['product']


class RecipesSerializer(serializers.ModelSerializer):
    ingredients = IngredientsSerializer(many=True)

    class Meta:
        model = Recipes
        fields = ['name', 'preparation', 'time', 'ingredients', 'photo', 'rate']

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
    additional = serializers.SerializerMethodField('get_additional')
    quantity_additional = serializers.SerializerMethodField('get_quantity_additional')
    category_additional = serializers.SerializerMethodField('get_category_additional')

    class Meta:
        model = Recipes
        fields = ['id', 'name', 'preparation', 'photo', 'additional', 'quantity_additional', 'category_additional']

    def get_additional(self, obj):
        list1 = self.context.get("list1")
        string_additional = ""
        for o in obj.ingredients.all():
            if o.product.id not in list1:
                string_additional += o.product.name
                string_additional += ", "
        if string_additional != "":
            lista = list(string_additional)
            lista = lista[:len(lista) - 2]
            string_lista = "".join(lista)
            return string_lista
        else:
            return string_additional

    def get_quantity_additional(self, obj):
        products = self.context.get("list1")
        product = 0
        for o in obj.ingredients.all():
            if o.product.id in products:
                product += 1
        quantity = obj.ingredients.count() - product
        return quantity

    def get_category_additional(self, obj):
        products = self.context.get("list1")
        category = []
        for o in obj.ingredients.all():
            if o.product.id not in products:
                product = Products.objects.get(id=o.product.id)
                if product.category not in category:
                    category.append(product.category)
        return category
