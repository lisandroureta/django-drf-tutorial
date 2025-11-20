from django.urls import path, include
from rest_framework.routers import DefaultRouter
from snippets import views

# Crea un router y registra nuestros viewsets
router = DefaultRouter()
router.register(r'snippets', views.SnippetViewSet, basename='snippet')
router.register(r'users', views.UserViewSet, basename='user')

# Las URLs de la API ahora son determinadas automáticamente por el router.
urlpatterns = [
    path('', include(router.urls)),
]