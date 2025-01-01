from flask import Flask, request, render_template, redirect, url_for, jsonify
import os
import xml.etree.ElementTree as ET
from utils.xml_utils import leer_xml, validar_estructura_xml, validar_usuarios_xml, escribir_xml, validar_xml_existente
import requests
import matplotlib
matplotlib.use('Agg')  # Usar backend no interactivo


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
        usuarios, error = leer_usuarios_desde_xml(contenido)

        if error:
            return jsonify({"error": error}), 400

        # Validaciones de los usuarios
        errores = []
        usuarios_validos = []
        for usuario in usuarios:
            if not usuario['id'] or not usuario['id'].startswith('IPC-'):
                errores.append(f"ID inválido: {usuario['id']}")
                continue
            if not usuario['telefono'].isdigit() or len(usuario['telefono']) != 8:
                errores.append(f"Teléfono inválido: {usuario['telefono']}")
                continue
            if '@' not in usuario['correo']:
                errores.append(f"Correo inválido: {usuario['correo']}")
                continue

            # Usuario válido
            usuarios_validos.append(usuario)

        # Guardar usuarios válidos en el archivo users.xml
        if usuarios_validos:
            # Validar si existe un archivo válido
            if validar_xml_existente(ARCHIVO_USUARIOS):
                with open(ARCHIVO_USUARIOS, "r", encoding="utf-8") as archivo:
                    contenido_actual = archivo.read()
                datos_actuales = leer_xml(contenido_actual).get("Usuarios", {}).get("Usuario", [])
                if not isinstance(datos_actuales, list):
                    datos_actuales = [datos_actuales]
            else:
                datos_actuales = []

            # Convertir usuarios válidos al formato esperado y agregar
            for usuario in usuarios_validos:
                datos_actuales.append({
                    "ID": usuario["id"],
                    "Pwd": usuario["password"],
                    "Nombre": usuario["nombre"],
                    "Correo": usuario["correo"],
                    "Telefono": usuario["telefono"],
                    "Direccion": usuario["direccion"],
                    "Perfil": usuario["perfil"],
                })

            nuevos_datos = {"Usuarios": {"Usuario": datos_actuales}}
            escribir_xml(nuevos_datos, ARCHIVO_USUARIOS)

        if errores:
            return jsonify({
                "mensaje": "Usuarios procesados con algunos errores.",
                "errores": errores
            }), 400

        return jsonify({"mensaje": "Usuarios cargados exitosamente"}), 200
    except Exception as e:
        return jsonify({"error": f"Error procesando archivo: {str(e)}"}), 500


def leer_usuarios_desde_xml(contenido):
    """
    Lee y valida usuarios desde el contenido XML proporcionado.
    """
    try:
        datos = leer_xml(contenido)
        solicitantes = datos.get("solicitantes", {}).get("solicitante", [])

        if not isinstance(solicitantes, list):
            solicitantes = [solicitantes]  # Convertir a lista si es un solo solicitante

        usuarios = []
        for solicitante in solicitantes:
            usuario = {
                "id": solicitante.get("@id"),
                "password": solicitante.get("@pwd"),
                "nombre": solicitante.get("NombreCompleto"),
                "correo": solicitante.get("CorreoElectronico"),
                "telefono": solicitante.get("NumeroTelefono"),
                "direccion": solicitante.get("Direccion"),
                "perfil": solicitante.get("perfil"),
            }
            usuarios.append(usuario)

        return usuarios, None
    except ValueError as ve:
        return None, str(ve)
    except Exception as e:
        return None, f"Error procesando el XML: {str(e)}"



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
    try:
        # Validar si el archivo de usuarios existe
        if not os.path.exists(ARCHIVO_USUARIOS):
            return jsonify({"error": "No hay usuarios registrados"}), 404

        with open(ARCHIVO_USUARIOS, "r", encoding="utf-8") as archivo:
            contenido = archivo.read()

        datos_usuarios = leer_xml(contenido)
        usuarios = datos_usuarios.get("Usuarios", {}).get("Usuario", [])
        if not isinstance(usuarios, list):
            usuarios = [usuarios]

        # 1. Leer imágenes procesadas desde la carpeta `static/processed`
        imagenes_procesadas = os.listdir(app.config['PROCESSED_FOLDER'])

        estadisticas = {}
        for usuario in usuarios:
            user_id = usuario.get("ID")
            estadisticas[user_id] = sum(user_id in img for img in imagenes_procesadas)

        # 2. Calcular Top 3 usuarios con más imágenes cargadas
        top_usuarios = sorted(estadisticas.items(), key=lambda x: x[1], reverse=True)[:3]

        # 3. Generar gráficos con matplotlib
        import matplotlib.pyplot as plt

        # Gráfico 1: Top 3 usuarios con más imágenes cargadas
        usuarios_top = [user[0] for user in top_usuarios]
        imagenes_top = [user[1] for user in top_usuarios]

        plt.bar(usuarios_top, imagenes_top, color='blue')
        plt.title("Top 3 Usuarios con Más Imágenes Cargadas")
        plt.xlabel("Usuarios")
        plt.ylabel("Cantidad de Imágenes")
        top_chart_path = os.path.join(app.config['PROCESSED_FOLDER'], "top_usuarios.png")
        plt.savefig(top_chart_path)
        plt.clf()

        # Gráfico 2: Cantidad de imágenes procesadas por usuario
        plt.bar(estadisticas.keys(), estadisticas.values(), color='green')
        plt.title("Imágenes Procesadas por Usuario")
        plt.xlabel("Usuarios")
        plt.ylabel("Cantidad de Imágenes")
        total_chart_path = os.path.join(app.config['PROCESSED_FOLDER'], "imagenes_procesadas.png")
        plt.savefig(total_chart_path)
        plt.clf()

        return jsonify({
            "mensaje": "Estadísticas generadas correctamente",
            "top_chart": "/static/processed/top_usuarios.png",
            "total_chart": "/static/processed/imagenes_procesadas.png"
        }), 200

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
