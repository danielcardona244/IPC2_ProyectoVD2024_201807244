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

# Endpoint para cargar usuarios (solo accesible para administrador)
@app.route('/admin/cargarUsuarios', methods=['POST'])
def cargar_usuarios():
    # Validar si las credenciales son del administrador
    if not request.headers.get('Rol') == 'administrador':
        return jsonify({"error": "Acceso denegado. Solo el administrador puede cargar usuarios."}), 403

    if 'file' not in request.files:
        return jsonify({"error": "No se encontró el archivo"}), 400

    archivo = request.files['file']
    if not archivo.filename.endswith('.xml'):
        return jsonify({"error": "El archivo debe ser XML"}), 400

    try:
        # Leer el contenido del archivo XML cargado
        contenido = archivo.read().decode('utf-8')
        datos = leer_xml(contenido)
        usuarios = datos.get("Usuarios", {}).get("Usuario", [])

        # Asegurarnos de que los usuarios estén en formato lista
        if not isinstance(usuarios, list):
            usuarios = [usuarios]

        # Validar y procesar usuarios
        claves_requeridas = ["ID", "Pwd", "Nombre", "Correo", "Telefono", "Direccion", "Perfil"]
        usuarios_validos = []
        for usuario in usuarios:
            errores = validar_estructura_xml(usuario, claves_requeridas)
            if errores:
                return jsonify({"error": f"Errores en los datos del usuario: {errores}"}), 400
            usuarios_validos.append(usuario)

        # Leer usuarios existentes y actualizar con los nuevos
        if os.path.exists(ARCHIVO_USUARIOS):
            with open(ARCHIVO_USUARIOS, "r", encoding="utf-8") as f:
                datos_existentes = leer_xml(f.read())
            usuarios_existentes = datos_existentes.get("Usuarios", {}).get("Usuario", [])
            if not isinstance(usuarios_existentes, list):
                usuarios_existentes = [usuarios_existentes]
            usuarios_validos = usuarios_existentes + usuarios_validos

        # Guardar los usuarios actualizados en el archivo XML
        escribir_xml({"Usuarios": {"Usuario": usuarios_validos}}, ARCHIVO_USUARIOS)
        return jsonify({"mensaje": "Usuarios cargados exitosamente"}), 200

    except Exception as e:
        return jsonify({"error": f"Error procesando archivo: {str(e)}"}), 500


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
        # Validar si las credenciales corresponden al administrador
        if id_usuario == "AdminIPC" and contrasena == "ARTIPC2":
            return jsonify({"mensaje": "Inicio de sesión exitoso como administrador", "rol": "administrador"}), 200

        # Leer los usuarios del archivo XML
        if not os.path.exists(ARCHIVO_USUARIOS):
            return jsonify({"error": "No hay usuarios registrados"}), 404

        with open(ARCHIVO_USUARIOS, "r", encoding="utf-8") as archivo:
            contenido = archivo.read()

        datos_usuarios = leer_xml(contenido)
        usuarios = datos_usuarios.get("Usuarios", {}).get("Usuario", [])

        # Asegurarse de que los usuarios estén en formato lista
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


if __name__ == '__main__':
    app.run(debug=True)
