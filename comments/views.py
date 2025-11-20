from rest_framework import viewsets, permissions
from comments.models import Comment
from comments.serializers import CommentSerializer
# Podemos reutilizar el permiso que creamos en la app snippets
from snippets.permissions import IsOwnerOrReadOnly 

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        # Guardamos el dueño automáticamente
        serializer.save(owner=self.request.user)