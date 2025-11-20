from django.db import models

class Comment(models.Model):
    # Relación 1: ¿Quién escribió esto? (Viene de la app 'auth' o 'accounts')
    owner = models.ForeignKey('auth.User', related_name='comments', on_delete=models.CASCADE)
    
    # Relación 2: ¿A qué snippet pertenece? (Viene de la app 'snippets')
    # Importante: Como el modelo Snippet está en otra app, usamos 'nombre_app.NombreModelo'
    snippet = models.ForeignKey('snippets.Snippet', related_name='comments', on_delete=models.CASCADE)
    
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created']