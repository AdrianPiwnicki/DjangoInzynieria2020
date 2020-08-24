from django.contrib import admin
from .models import Produkty, Przepisy, Skladniki

admin.site.register(Skladniki)


@admin.register(Produkty)
class ProduktyAdmin(admin.ModelAdmin):
    list_display = ['nazwa', 'kategoria']
    list_editable = ['kategoria']


@admin.register(Przepisy)
class PrzepisyAdmin(admin.ModelAdmin):

    def response_add(self, request, obj, post_url_continue=None):
        for i in obj.skladniki.all():
            i.produkt.popularnosc += 1
            i.produkt.save()
        return self.response_post_save_add(request, obj)
