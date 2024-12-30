from flask import Flask, request, render_template, redirect, url_for, jsonify
import os
import xml.etree.ElementTree as ET
from utils.xml_utils import leer_xml, escribir_xml, validar_estructura_xml
import requests

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['PROCESSED_FOLDER'] = os.path.join(os.getcwd(), 'static', 'processed')

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['PROCESSED_FOLDER'], exist_ok=True)



# Ruta del archivo de usuarios
ARCHIVO_USUARIOS = "users.xml"



# Pantalla inicial redirige al login
@app.route('/')
def inicio():
    return redirect(url_for('login'))


# Endpoint para inicio de sesión
@app.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"error": "La solicitud debe ser en formato JSON"}), 400

    datos = request.get_json()
    id_usuario = datos.get("ID")
    contrasena = datos.get("Pwd")

    if not id_usuario or not contrasena:
        return jsonify({"error": "ID de usuario y contraseña son obligatorios"}), 400

    try:
        if id_usuario == "AdminIPC" and contrasena == "ARTIPC2":
            return jsonify({"mensaje": "Inicio de sesión exitoso como administrador", "rol": "administrador"}), 200

        if not os.path.exists(ARCHIVO_USUARIOS):
            return jsonify({"error": "No hay usuarios registrados"}), 404

        with open(ARCHIVO_USUARIOS, "r", encoding="utf-8") as archivo:
            contenido = archivo.read()

        datos_usuarios = leer_xml(contenido)
        usuarios = datos_usuarios.get("Usuarios", {}).get("Usuario", [])

        if not isinstance(usuarios, list):
            usuarios = [usuarios]

        usuario = next((u for u in usuarios if u["ID"] == id_usuario), None)

        if not usuario:
            return jsonify({"error": "Usuario no encontrado"}), 404

        if usuario["Pwd"] != contrasena:
            return jsonify({"error": "Contraseña incorrecta"}), 401

        return jsonify({"mensaje": "Inicio de sesión exitoso", "rol": "usuario"}), 200

    except Exception as e:
        return jsonify({"error": f"Error procesando la solicitud: {str(e)}"}), 500


# Endpoint para cargar usuarios 
@app.route('/admin/cargarUsuarios', methods=['POST'])
def cargar_usuarios():

    if 'file' not in request.files:
        return jsonify({"error": "No se encontró el archivo"}), 400

    archivo = request.files['file']
    if not archivo.filename.endswith('.xml'):
        return jsonify({"error": "El archivo debe ser XML"}), 400

    try:
        contenido = archivo.read().decode('utf-8')
        # Aquí se procesará el contenido XML, se valida y se guarda
        return jsonify({"mensaje": "Usuarios cargados exitosamente"}), 200
    except Exception as e:
        return jsonify({"error": f"Error procesando archivo: {str(e)}"}), 500


# Endpoint para ver usuarios
@app.route('/admin/verUsuarios', methods=['GET'])
def ver_usuarios():
    if not os.path.exists(ARCHIVO_USUARIOS):
        return jsonify({"usuarios": []}), 200  # Respuesta vacía si no hay usuarios registrados

    try:
        with open(ARCHIVO_USUARIOS, "r", encoding="utf-8") as archivo:
            contenido = archivo.read()
        datos_usuarios = leer_xml(contenido)
        usuarios = datos_usuarios.get("Usuarios", {}).get("Usuario", [])

        if not isinstance(usuarios, list):
            usuarios = [usuarios]

        return jsonify({"usuarios": usuarios}), 200
    except Exception as e:
        return jsonify({"error": f"Error al obtener usuarios: {str(e)}"}), 500


#endpoint para ver xml 
@app.route('/admin/verXML', methods=['GET'])
def ver_xml():
    if not os.path.exists(ARCHIVO_USUARIOS):
        return jsonify({"error": "No hay usuarios registrados"}), 404

    try:
        with open(ARCHIVO_USUARIOS, "r", encoding="utf-8") as archivo:
            contenido = archivo.read()
        return jsonify({"xml": contenido}), 200
    except Exception as e:
        return jsonify({"error": f"Error al obtener el XML: {str(e)}"}), 500


#endpoint para ver estadisticas
@app.route('/admin/verEstadisticas', methods=['GET'])
def ver_estadisticas():
    if not os.path.exists(ARCHIVO_USUARIOS):
        return jsonify({"error": "No hay usuarios registrados"}), 404

    try:
        with open(ARCHIVO_USUARIOS, "r", encoding="utf-8") as archivo:
            contenido = archivo.read()
        datos_usuarios = leer_xml(contenido)
        usuarios = datos_usuarios.get("Usuarios", {}).get("Usuario", [])

        if not isinstance(usuarios, list):
            usuarios = [usuarios]

        # Generar estadísticas
        total_usuarios = len(usuarios)
        perfiles = [u["Perfil"] for u in usuarios]
        estadisticas_perfil = {perfil: perfiles.count(perfil) for perfil in set(perfiles)}

        return jsonify({"total_usuarios": total_usuarios, "estadisticas_perfil": estadisticas_perfil}), 200
    except Exception as e:
        return jsonify({"error": f"Error al calcular estadísticas: {str(e)}"}), 500




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
                        "data": [{"x": p["col"], "y": p["fila"]} for p in pixels],
                        "backgroundColor": [p["color"] for p in pixels],
                        "pointRadius": 5  # Tamaño del punto ajustable
                    }
                ]
            },
            "options": {
                "scales": {
                    "x": {"reverse": False},
                    "y": {"reverse": True},  # Invertir eje Y para el diseño correcto
                }
            },
        }
    }
    try:
        response = requests.post(url, json=datos)
        if response.status_code == 200:
            # Usa app.config para resolver el PROCESSED_FOLDER
            image_path = os.path.join(app.config['PROCESSED_FOLDER'], 'imagen_generada.png')
            with open(image_path, 'wb') as f:
                f.write(response.content)
            return f'/static/processed/imagen_generada.png'
        else:
            print("Error en la API de QuickChart:", response.text)
            return None
    except Exception as e:
        print("Error generando gráfico:", str(e))
        return None






# Leer XML y extraer los datos de píxeles
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
        print("Píxeles procesados:", pixels)  # Agrega esta línea
        return pixels
    except Exception as e:
        print("Error procesando el archivo XML:", str(e))
        return None

from flask import send_from_directory

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)


# Ruta para subir imagen
@app.route('/subir_imagen', methods=['GET', 'POST'])
def subir_imagen():
    if request.method == 'POST':
        file = request.files.get('archivo')
        if not file or not file.filename.endswith('.xml'):
            return render_template('subir_imagen.html', error="Debe cargar un archivo XML válido.")

        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        pixels = procesar_archivo_xml(file_path)
        if not pixels:
            return render_template('subir_imagen.html', error="Error procesando el archivo XML.")

        image_path = generar_grafico(pixels)
        if not image_path:
            return render_template('subir_imagen.html', error="No se pudo generar la imagen.")

        return render_template('subir_imagen.html', mensaje="Imagen cargada exitosamente.", imagen=image_path)

    return render_template('subir_imagen.html')

# Ruta para galería
@app.route('/galeria', methods=['GET'])
def galeria():
    imagenes = os.listdir(app.config['PROCESSED_FOLDER'])
    print("Imágenes en la galería:", imagenes)  # Para depuración
    imagenes = [f'/static/processed/{img}' for img in imagenes if img.endswith(('png', 'jpg', 'jpeg'))]
    return render_template('galeria.html', imagenes=imagenes)




# Página inicial redirige a la galería
@app.route('/')
def index():
    return redirect(url_for('galeria'))


if __name__ == '__main__':
    app.run(debug=True)
