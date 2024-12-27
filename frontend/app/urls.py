from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),  # Esto sigue siendo el panel de administración de Django
    path('', views.login, name='login'),  # Login por defecto
    path('login/', views.login, name='login'),
    path('cargarUsuarios/', views.cargar_usuarios, name='cargar_usuarios'),  # Ruta personalizada
]
