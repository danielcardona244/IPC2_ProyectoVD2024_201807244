from django.shortcuts import render, redirect
from django.http import JsonResponse
import requests

# Ruta del backend Flask
FLASK_BACKEND_URL = 'http://127.0.0.1:5000'

# Login
def login(request):
    if request.method == 'POST':
        id_usuario = request.POST.get('ID')
        pwd = request.POST.get('Pwd')
        data = {'ID': id_usuario, 'Pwd': pwd}
        response = requests.post(f'{FLASK_BACKEND_URL}/login', json=data)

        if response.status_code == 200:
            rol = response.json().get('rol')
            if rol == 'administrador':
                # Redirige al cargador de usuarios
                return redirect('cargar_usuarios')
            elif rol == 'usuario':
                # Redirige al dashboard del usuario regular
                return render(request, 'usuario_dashboard.html', {"mensaje": "Bienvenido al sistema"})
        else:
            return render(request, 'login.html', {'error': response.json().get('error')})
    return render(request, 'login.html')

# Cargar usuarios (solo administrador)
def cargar_usuarios(request):
    if request.method == 'POST' and 'archivo' in request.FILES:
        archivo = request.FILES['archivo']
        files = {'file': archivo}
        headers = {'Rol': 'administrador'}  # Encabezado para validar rol
        response = requests.post(f'{FLASK_BACKEND_URL}/admin/cargarUsuarios', files=files, headers=headers)
        return JsonResponse(response.json(), safe=False)
    return render(request, 'cargar_usuarios.html')
