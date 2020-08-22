from django.contrib import admin

from .models import Produkty, Przepisy, Skladniki

admin.site.register(Produkty)
admin.site.register(Skladniki)
admin.site.register(Przepisy)

