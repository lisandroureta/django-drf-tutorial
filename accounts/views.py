from django.contrib.auth.models import User
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
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

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def follow(self, request, pk=None):
        target_user = self.get_object() # El usuario al que queremos seguir
        current_user = request.user     # Yo (el que hace la petición)

        # Evitar seguirse a uno mismo (opcional, pero buena práctica)
        if target_user == current_user:
             return Response({'error': 'No te puedes seguir a ti mismo'}, status=status.HTTP_400_BAD_REQUEST)

        # Accedemos al perfil del usuario actual
        my_profile = current_user.profile

        # Verificamos si ya lo sigo
        if my_profile.following.filter(pk=target_user.pk).exists():
            my_profile.following.remove(target_user) # Dejar de seguir (Unfollow)
            return Response({'status': 'unfollowed', 'count': target_user.followers.count()}, status=status.HTTP_200_OK)
        else:
            my_profile.following.add(target_user) # Seguir (Follow)
            return Response({'status': 'followed', 'count': target_user.followers.count()}, status=status.HTTP_200_OK)

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,) # Permitir acceso a cualquiera (público)
    serializer_class = RegisterSerializer