from django.urls import path
from app import views

urlpatterns = [
    path('', views.login, name='login'),  # Login como raíz
    path('usuario_dashboard/', views.usuario_dashboard, name='usuario_dashboard'), 
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('cargar_usuarios/', views.cargar_usuarios, name='cargar_usuarios'),
    path('ver_usuarios/', views.ver_usuarios, name='ver_usuarios'),
    path('ver_xml/', views.ver_xml, name='ver_xml'),
    path('ver_estadisticas/', views.ver_estadisticas, name='ver_estadisticas'),
    path('logout/', views.logout_view, name='logout'),
]
