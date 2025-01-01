import xmltodict
import os

# Leer datos desde un archivo XML
def leer_xml(contenido_xml):
    try:
        return xmltodict.parse(contenido_xml)
    except Exception as e:
        raise ValueError(f"Error procesando el contenido XML: {str(e)}")

# Escribir datos en un archivo XML
def escribir_xml(datos, ruta_archivo):
    try:
        with open(ruta_archivo, "w", encoding="utf-8") as archivo:
            contenido_xml = xmltodict.unparse(datos, pretty=True)
            archivo.write(contenido_xml)
    except Exception as e:
        raise ValueError(f"Error escribiendo XML: {str(e)}")

# Validar si un archivo tiene contenido válido antes de leerlo
def validar_xml_existente(ruta_archivo):
    if not os.path.exists(ruta_archivo):
        return False
    try:
        with open(ruta_archivo, "r", encoding="utf-8") as archivo:
            contenido = archivo.read().strip()
            if not contenido:
                return False
            leer_xml(contenido)  # Valida si es XML válido
        return True
    except Exception:
        return False

# Validar estructura de usuarios
def validar_usuarios_xml(usuarios):
    errores = []
    for idx, usuario in enumerate(usuarios):
        if not usuario.get("@id") or not usuario.get("@id").startswith("IPC-"):
            errores.append(f"Usuario {idx + 1}: ID inválido")
        if not usuario.get("@pwd"):
            errores.append(f"Usuario {idx + 1}: Contraseña no proporcionada")
        if not usuario.get("CorreoElectronico") or "@" not in usuario["CorreoElectronico"]:
            errores.append(f"Usuario {idx + 1}: Correo inválido")
    return errores

# Validar si un archivo tiene una estructura XML válida
def validar_estructura_xml(datos, claves_requeridas):
    """
    Valida que un diccionario (convertido desde XML) contenga claves requeridas.
    """
    errores = []
    for clave in claves_requeridas:
        if clave not in datos:
            errores.append(f"Falta la clave requerida: {clave}")
    return errores