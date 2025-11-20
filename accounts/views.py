from django.contrib.auth.models import User
from rest_framework import viewsets
from accounts.serializers import UserSerializer
from rest_framework import generics
from rest_framework.permissions import AllowAny
from accounts.serializers import RegisterSerializer

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Este ViewSet proporciona automáticamente las acciones 'list' y 'retrieve'.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,) # Permitir acceso a cualquiera (público)
    serializer_class = RegisterSerializer