from django.urls import include, path
from rest_framework import routers
from backendApp import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'przepisy', views.PrzepisyViewSet)
router.register(r'produkty', views.ProduktyViewSet)

urlpatterns = [
    path('recipe-detail/<int:pk>', views.RecipeDetail.as_view()),
    path('lista-przepisow', views.lista_przepisow),
    path('lista-wybrane', views.wybrane),
    path('lista-all-wybrane-dodatkowe', views.all_wybrane_dodatkowe),
    path('lista-dodatkowe', views.lista_dodatkowe),
    path('produkty-inne', views.ProduktyInne.as_view()),
    path('produkty-owoce', views.ProduktyOwoce.as_view()),
    path('produkty-warzywa', views.ProduktyWarzywa.as_view()),
    path('produkty-zboza', views.ProduktyZboza.as_view()),
    path('produkty-nabial', views.ProduktyNabial.as_view()),
    path('produkty-mieso', views.ProduktyMieso.as_view()),
    path('produkty-ryby', views.ProduktyRyby.as_view()),
    path('produkty-przyprawy', views.ProduktyPrzyprawy.as_view()),
    path('produkty-all', views.ProduktyWszystkie.as_view()),
    path('', include(router.urls)),
]
