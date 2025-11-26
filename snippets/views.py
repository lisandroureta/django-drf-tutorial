from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import renderers
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
from snippets.permissions import IsOwnerOrReadOnly

class SnippetViewSet(viewsets.ModelViewSet):
    """
    Este ViewSet proporciona automáticamente 'list', 'create', 'retrieve',
    'update' y 'destroy'.
    
    Además, proporcionamos una acción extra 'highlight'.
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]

    # @action nos permite crear endpoints personalizados que no son CRUD estándar
    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

    # --- NUEVA ACCIÓN: LIKE ---
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def like(self, request, pk=None):
        snippet = self.get_object() # Obtenemos el snippet por ID (pk)
        user = request.user
        
        # Verificamos si el usuario ya está en la lista de likes
        if user in snippet.likes.all():
            snippet.likes.remove(user) # Lo quitamos
            return Response({'status': 'unliked'}, status=status.HTTP_200_OK)
        else:
            snippet.likes.add(user) # Lo agregamos
            return Response({'status': 'liked'}, status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    # --- NUEVA ACCIÓN: FEED ---
    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def feed(self, request):
        """
        Muestra los snippets de los usuarios a los que sigo.
        """
        # 1. ¿A quién sigo yo?
        # Accedemos al perfil del usuario actual y sacamos la lista 'following'
        following_users = request.user.profile.following.all()
        
        # 2. Filtrar snippets
        # "Trae los snippets cuyo 'owner' esté EN la lista 'following_users'"
        # Y ordénalos por fecha (del más nuevo al más viejo)
        snippets = Snippet.objects.filter(owner__in=following_users).order_by('-created')
        
        # 3. Paginación (¡Muy importante para un feed!)
        page = self.paginate_queryset(snippets)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        # Si no hay paginación configurada, devolvemos todo (fallback)
        serializer = self.get_serializer(snippets, many=True)
        return Response(serializer.data)