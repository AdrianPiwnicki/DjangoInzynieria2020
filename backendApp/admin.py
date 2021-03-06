from django.contrib import admin
from .models import Products, Recipes, Ingredients

admin.site.register(Ingredients)


@admin.register(Products)
class ProduktyAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'graphics']
    list_editable = ['category','graphics']
    search_fields = ['name']


@admin.register(Recipes)
class PrzepisyAdmin(admin.ModelAdmin):

    def response_add(self, request, obj, post_url_continue=None):
        for i in obj.ingredients.all():
            i.product.popularity += 1
            i.product.save()
        return self.response_post_save_add(request, obj)
