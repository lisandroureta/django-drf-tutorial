from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

# Importamos las vistas de JWT
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Esta es la línea que recuperamos para el Login/Logout
    path('api-auth/', include('rest_framework.urls')), 
    
    # Tu API de snippets
    path('', include('snippets.urls')),

    # --- RUTAS DE JWT ---
    # Para pedir el token inicial (Login)
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # Para refrescar el token cuando caduca (seguridad)
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # --- DOCUMENTACIÓN (SWAGGER) ---
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]