import os
import xml.etree.ElementTree as ET
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.conf import settings
import requests
import json


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



# Logout
def logout_view(request):
    request.session.flush()  # Limpia la sesión actual
    return redirect('login')






# Dashboard del administrador
def admin_dashboard(request):
    rol = request.session.get('rol')
    if rol != 'administrador':
        return redirect('login')  # Redirigir al login si no es administrador
    return render(request, 'admin_dashboard.html')


# carga masiva
def cargar_usuarios(request):
    if request.method == 'POST' and 'archivo' in request.FILES:
        archivo = request.FILES['archivo']
        files = {'file': archivo}

        try:
            # Enviar archivo al backend
            response = requests.post(f'{FLASK_BACKEND_URL}/admin/cargarUsuarios', files=files)
            respuesta = response.json()

            # Estado 200: Todo se procesó correctamente
            if response.status_code == 200:
                mensaje = respuesta.get('mensaje', 'Archivo cargado exitosamente.')
                errores = respuesta.get('errores', [])  # Puede haber errores parciales
                return render(request, 'cargar_usuarios.html', {
                    'mensaje': mensaje,
                    'errores': errores
                })

            # Estado 400: Algunos errores ocurrieron
            elif response.status_code == 400:
                mensaje = respuesta.get('mensaje', 'Error al cargar el archivo.')
                errores = respuesta.get('errores', [])
                return render(request, 'cargar_usuarios.html', {
                    'mensaje': mensaje,
                    'errores': errores
                })

            # Otros estados: Error inesperado
            else:
                error = respuesta.get('error', 'Error al cargar el archivo.')
                return render(request, 'cargar_usuarios.html', {'error': error})

        except Exception as e:
            # Manejo de errores de conexión u otros problemas
            return render(request, 'cargar_usuarios.html', {'error': f"Error al comunicarse con el backend: {str(e)}"})

    # Si no es POST o no hay archivo
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






# Dashboard del usuario
def usuario_dashboard(request):
    rol = request.session.get('rol')
    if rol != 'usuario':
        return redirect('login')  # Redirige al login si no es usuario.
    return render(request, 'usuario_dashboard.html')


# Rutas para guardar las imágenes
UPLOAD_FOLDER = os.path.join(settings.BASE_DIR, 'frontend', 'static', 'uploads')
PROCESSED_FOLDER = os.path.join(settings.BASE_DIR, 'frontend', 'static', 'processed')

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

# Función para procesar el XML
def procesar_archivo_xml(file_path):
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        pixels = []
        for pixel in root.findall("./diseño/pixel"):
            fila = int(pixel.attrib['fila'])
            col = int(pixel.attrib['col'])
            color = pixel.text.strip()
            pixels.append({"fila": fila, "col": col, "color": color})
        return pixels
    except Exception as e:
        print("Error procesando el archivo XML:", str(e))
        return None

# QuickChart API
def generar_grafico(pixels):
    url = "https://quickchart.io/chart"
    datos = {
        "chart": {
            "type": "scatter",
            "data": {
                "datasets": [
                    {
                        "label": "Pixels",
                        "data": [{"x": p["col"], "y": p["fila"], "r": 5} for p in pixels],
                        "backgroundColor": [p["color"] for p in pixels],
                    }
                ]
            }
        }
    }
    try:
        response = requests.post(url, json=datos)
        if response.status_code == 200:
            image_path = os.path.join(PROCESSED_FOLDER, 'imagen_generada.png')
            with open(image_path, 'wb') as f:
                f.write(response.content)
            return os.path.relpath(image_path, settings.BASE_DIR)
        else:
            print("Error en la API de QuickChart:", response.text)
            return None
    except Exception as e:
        print("Error generando gráfico:", str(e))
        return None

# Vista para cargar imagen
def subir_imagen(request):
    if request.method == 'POST':
        file = request.FILES.get('archivo')
        if not file or not file.name.endswith('.xml'):
            return render(request, 'subir_imagen.html', {'error': "Debe cargar un archivo XML válido."})

        # Guarda el archivo XML
        file_path = os.path.join(UPLOAD_FOLDER, file.name)
        with open(file_path, 'wb') as f:
            for chunk in file.chunks():
                f.write(chunk)

        # Procesa el archivo XML
        pixels = procesar_archivo_xml(file_path)
        if not pixels:
            return render(request, 'subir_imagen.html', {'error': "Error procesando el archivo XML."})

        # Genera la imagen
        image_path = generar_grafico(pixels)
        if not image_path:
            return render(request, 'subir_imagen.html', {'error': "No se pudo generar la imagen."})

        # Lee el contenido del XML para mostrarlo en la interfaz
        with open(file_path, 'r', encoding='utf-8') as f:
            xml_content = f.read()

        # Renderiza la plantilla con los datos del XML y la imagen generada
        return render(request, 'subir_imagen.html', {
            'mensaje': "Imagen cargada exitosamente.",
            'xml': xml_content,
            'imagen': image_path,
        })

    return render(request, 'subir_imagen.html')

# Vista para galería
def galeria(request):
    processed_path = os.path.join(settings.BASE_DIR, 'frontend', 'static', 'processed')
    imagenes = [
        f'/static/processed/{archivo}' 
        for archivo in os.listdir(processed_path) 
        if archivo.endswith(('png', 'jpg', 'jpeg'))
    ]
    return render(request, 'galeria.html', {'imagenes': imagenes})


#editor de imagenes
def editor_imagenes(request):
    if request.method == "GET":
        # Simulación de diseño: matriz 25x25 con colores blancos
        diseño = [["#FFFFFF" for _ in range(25)] for _ in range(25)]
        return render(request, "editor_imagenes.html", {"design": json.dumps(diseño)})
    

def guardar_diseno(request):
    if request.method == "POST":
        data = json.loads(request.body)
        design = data.get("design", [])
        # Aquí se procesa y guarda el nuevo diseño como XML
        with open("nuevo_diseño.xml", "w") as file:
            file.write("<figura>\n")
            for fila_idx, fila in enumerate(design):
                for col_idx, color in enumerate(fila):
                    file.write(
                        f'<pixel fila="{fila_idx}" col="{col_idx}">{color}</pixel>\n'
                    )
            file.write("</figura>")
        return JsonResponse({"mensaje": "Diseño guardado exitosamente"})

#ayuda
from django.shortcuts import render

def ayuda(request):
    return render(request, 'ayuda.html')
