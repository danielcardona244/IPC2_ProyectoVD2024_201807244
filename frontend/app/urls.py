from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.login, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Rutas módulo admin
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('cargar_usuarios/', views.cargar_usuarios, name='cargar_usuarios'),
    path('ver_usuarios/', views.ver_usuarios, name='ver_usuarios'),
    path('ver_xml/', views.ver_xml, name='ver_xml'),
    path('ver_estadisticas/', views.ver_estadisticas, name='ver_estadisticas'),

    # Rutas módulo usuario
    path('usuario_dashboard/', views.usuario_dashboard, name='usuario_dashboard'),
    path('galeria/', views.galeria, name='galeria'),
    path('subir_imagen/', views.subir_imagen, name='subir_imagen'),
    path("editor_imagenes/", views.editor_imagenes, name="editor_imagenes"),
    path("guardar_diseno/", views.guardar_diseno, name="guardar_diseno"),
    path('ayuda/', views.ayuda, name='ayuda'),
]

# Agregar rutas para archivos estáticos
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
