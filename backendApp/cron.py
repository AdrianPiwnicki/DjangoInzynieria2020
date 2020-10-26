from backendApp.models import Recipes


def calculation_rate():
    recipes = Recipes.objects.all()
    for recipe in recipes:
        recipe.rate += 1
        recipe.save()