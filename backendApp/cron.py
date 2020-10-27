from backendApp.models import Recipes


###############################################################################
# ----------------------------OBLICZANIE RATE---------------------------------#
###############################################################################

def calculation_rate():
    minimal = Recipes.objects.all().order_by('views').first()
    maximum = Recipes.objects.all().order_by('-views').first()
    scale = (maximum.views - minimal.views)/10

    recipes = Recipes.objects.all()
    for recipe in recipes:
        views = recipe.views/scale
        d = 0.5
        k = 1
        while views <= k*scale:
            k += 1
            d += 0.5
        recipe.rate = d
        recipe.save()
