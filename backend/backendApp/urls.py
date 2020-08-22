from django.urls import include, path
from rest_framework import routers
from backend.backendApp import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'produkty', views.ProduktyViewSet)
router.register(r'przepisy', views.PrzepisyViewSet)

urlpatterns = [
    path('lista-przepisow', views.lista_przepisow),
    path('', include(router.urls)),
]
