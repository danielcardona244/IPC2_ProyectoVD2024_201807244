import xmltodict
import os

# Leer datos desde un archivo XML
def leer_xml(contenido_xml):
    """
    Lee datos desde un contenido XML (como string) y los convierte en un diccionario.
    """
    try:
        # Procesa el contenido como XML
        datos = xmltodict.parse(contenido_xml)
        return datos
    except Exception as e:
        raise ValueError(f"Error procesando el contenido XML: {str(e)}")

# Guardar datos en un archivo XML
def escribir_xml(datos, ruta_archivo):
    """
    Escribe un diccionario como un archivo XML.
    """
    with open(ruta_archivo, "w", encoding="utf-8") as archivo:
        contenido_xml = xmltodict.unparse(datos, pretty=True)
        archivo.write(contenido_xml)

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
