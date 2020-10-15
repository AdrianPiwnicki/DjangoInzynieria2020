from django.contrib import admin
from .models import Products, Recipes, Ingredients, Graphics

admin.site.register(Ingredients)
admin.site.register(Graphics)


@admin.register(Products)
class ProduktyAdmin(admin.ModelAdmin):
    list_display = ['name', 'category']
    list_editable = ['category']
    search_fields = ['name']


@admin.register(Recipes)
class PrzepisyAdmin(admin.ModelAdmin):

    def response_add(self, request, obj, post_url_continue=None):
        for i in obj.ingredients.all():
            i.product.popularity += 1
            i.product.save()
        return self.response_post_save_add(request, obj)
