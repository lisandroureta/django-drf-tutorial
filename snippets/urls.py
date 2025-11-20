from django.urls import path, include
from rest_framework.routers import DefaultRouter
from snippets import views as snippet_views
from accounts import views as account_views
from comments import views as comment_views

router = DefaultRouter()
# Registramos los snippets
router.register(r'snippets', snippet_views.SnippetViewSet, basename='snippet')
# Registramos los usuarios
router.register(r'users', account_views.UserViewSet, basename='user')
# Registramos los comentarios
router.register(r'comments', comment_views.CommentViewSet, basename='comment')

urlpatterns = [
    path('', include(router.urls)),
]