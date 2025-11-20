from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from snippets.models import Snippet

class SnippetTests(APITestCase):
    
    # 1. Preparación (setUp): Se ejecuta ANTES de cada test.
    # Aquí creamos los datos "falsos" que necesitamos para probar.
    def setUp(self):
        # Creamos un usuario de prueba
        self.user = User.objects.create_user(username='tester', password='password123')
        
        # Obtenemos la URL de la lista de snippets por su nombre (definido en el router)
        self.url = reverse('snippet-list') 
        
        # Datos que vamos a intentar enviar
        self.data = {'code': 'print("Hello World")', 'title': 'Test Snippet'}

    # 2. Test: Crear un snippet estando logueado (Debería funcionar)
    def test_create_snippet_authenticated(self):
        """
        Asegura que un usuario autenticado pueda crear un snippet.
        """
        # Simulamos que el usuario se loguea (magia de DRF)
        self.client.force_authenticate(user=self.user)
        
        # Hacemos una petición POST (como si fuera un formulario)
        response = self.client.post(self.url, self.data, format='json')
        
        # ASERCIONES: Las "preguntas" que determinan si el test pasa o falla
        
        # ¿El servidor respondió 201 CREATED?
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # ¿La base de datos ahora tiene 1 snippet?
        self.assertEqual(Snippet.objects.count(), 1)
        
        # ¿El dueño del snippet es el usuario 'tester'?
        self.assertEqual(Snippet.objects.get().owner, self.user)

    # 3. Test: Crear un snippet SIN estar logueado (Debería fallar)
    def test_create_snippet_unauthenticated(self):
        """
        Asegura que un usuario anónimo NO pueda crear un snippet.
        """
        # NO nos autenticamos aquí (self.client es anónimo)
        
        response = self.client.post(self.url, self.data, format='json')
        
        # Esperamos un error 401 (No autorizado)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # La base de datos debe seguir vacía
        self.assertEqual(Snippet.objects.count(), 0)