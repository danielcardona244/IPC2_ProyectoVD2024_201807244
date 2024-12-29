from flask import Flask, request, jsonify, redirect, url_for
import os
from utils.xml_utils import leer_xml, escribir_xml, validar_estructura_xml

app = Flask(__name__)

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




if __name__ == '__main__':
    app.run(debug=True)
