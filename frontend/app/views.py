from django.shortcuts import render, redirect
from django.http import JsonResponse
import requests

FLASK_BACKEND_URL = 'http://127.0.0.1:5000'


# Login
def login(request):
    if request.method == 'POST':
        id_usuario = request.POST.get('ID')
        pwd = request.POST.get('Pwd')
        data = {'ID': id_usuario, 'Pwd': pwd}

        try:
            response = requests.post(f'{FLASK_BACKEND_URL}/login', json=data)
            # Imprimir la respuesta para verificar el contenido
            print("Respuesta del backend:", response.json())
            if response.status_code == 200:
                rol = response.json().get('rol')
                # Guardar rol en la sesión para autorización en otras vistas
                request.session['rol'] = rol
                if rol == 'administrador':
                    return redirect('admin_dashboard')
                elif rol == 'usuario':
                    return redirect('usuario_dashboard')  # Redirigir al nuevo dashboard del usuario
            else:
                # Si no es un 200, mostrar el error en la página
                error = response.json().get('error', 'Error desconocido')
                return render(request, 'login.html', {'error': error})
        except Exception as e:
            return render(request, 'login.html', {'error': f"Error al comunicarse con el backend: {str(e)}"})
    return render(request, 'login.html')


# Dashboard del administrador
def admin_dashboard(request):
    rol = request.session.get('rol')
    if rol != 'administrador':
        return redirect('login')  # Redirigir al login si no es administrador
    return render(request, 'admin_dashboard.html')


# Dashboard del usuario
def usuario_dashboard(request):
    rol = request.session.get('rol')
    if rol != 'usuario':
        return redirect('login')  # Redirigir al login si no es un usuario regular
    return render(request, 'usuario_dashboard.html', {'mensaje': 'Bienvenido al Dashboard de Usuario'})


# Logout
def logout_view(request):
    request.session.flush()  # Limpia la sesión actual
    return redirect('login')


# carga masiva
def cargar_usuarios(request):
    if request.method == 'POST' and 'archivo' in request.FILES:
        archivo = request.FILES['archivo']
        files = {'file': archivo}

        try:
            response = requests.post(f'{FLASK_BACKEND_URL}/admin/cargarUsuarios', files=files)
            if response.status_code == 200:
                mensaje = response.json().get('mensaje', 'Archivo cargado exitosamente.')
                return render(request, 'cargar_usuarios.html', {'mensaje': mensaje})
            else:
                error = response.json().get('error', 'Error al cargar el archivo.')
                return render(request, 'cargar_usuarios.html', {'error': error})
        except Exception as e:
            return render(request, 'cargar_usuarios.html', {'error': f"Error al comunicarse con el backend: {str(e)}"})
    return render(request, 'cargar_usuarios.html')



# Ver usuarios
def ver_usuarios(request):
    try:
        response = requests.get(f'{FLASK_BACKEND_URL}/admin/verUsuarios')
        if response.status_code == 200:
            usuarios = response.json().get('usuarios', [])
            if not usuarios:
                return render(request, 'ver_usuarios.html', {'mensaje': 'No hay usuarios registrados.'})
            return render(request, 'ver_usuarios.html', {'usuarios': usuarios})
        else:
            error = response.json().get('error', 'Error desconocido.')
            return render(request, 'ver_usuarios.html', {'error': error})
    except Exception as e:
        return render(request, 'ver_usuarios.html', {'error': f"Error al comunicarse con el backend: {str(e)}"})


#ver xml
def ver_xml(request):
    try:
        response = requests.get(f'{FLASK_BACKEND_URL}/admin/verXML')
        if response.status_code == 200:
            xml_contenido = response.json().get('xml', '')
            return render(request, 'ver_xml.html', {'xml': xml_contenido})
        else:
            error = response.json().get('error', 'Error desconocido.')
            return render(request, 'ver_xml.html', {'error': error})
    except Exception as e:
        return render(request, 'ver_xml.html', {'error': f"Error al comunicarse con el backend: {str(e)}"})


#ver estadistica
def ver_estadisticas(request):
    try:
        response = requests.get(f'{FLASK_BACKEND_URL}/admin/verEstadisticas')
        if response.status_code == 200:
            data = response.json()
            total_usuarios = data.get("total_usuarios", 0)
            estadisticas_perfil = data.get("estadisticas_perfil", {})
            return render(request, 'ver_estadisticas.html', {
                'total_usuarios': total_usuarios,
                'estadisticas_perfil': estadisticas_perfil
            })
        else:
            error = response.json().get('error', 'Error desconocido.')
            return render(request, 'ver_estadisticas.html', {'error': error})
    except Exception as e:
        return render(request, 'ver_estadisticas.html', {'error': f"Error al comunicarse con el backend: {str(e)}"})


