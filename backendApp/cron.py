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
        d = 0.5
        k = 1
        while recipe.views > k*scale:
            k += 1
            if d < 5:
                d += 0.5
        recipe.rate = d
        recipe.save()
