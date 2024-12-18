import tkinter as tk
from tkinter import filedialog, messagebox
import xml.etree.ElementTree as ET
from estructuras.lista_doble import ListaDoble
from clases.solicitante import Solicitante

lista_solicitantes = ListaDoble()

def cargar_solicitantes():
    """
    Carga los solicitantes desde un archivo XML.
    """
    file_path = filedialog.askopenfilename(title="Seleccionar archivo XML", filetypes=[("Archivos XML", "*.xml")])
    if not file_path:
        return

    try:
        tree = ET.parse(file_path)
        root = tree.getroot()

        for solicitante in root.findall("solicitante"):
            id = solicitante.get("id")
            pwd = solicitante.get("pwd")
            nombre = solicitante.find("NombreCompleto").text
            correo = solicitante.find("CorreoElectronico").text
            telefono = solicitante.find("NumeroTelefono").text
            direccion = solicitante.find("Direccion").text

            # Validar que no exista el ID
            if lista_solicitantes.buscar(id):
                print(f"ID duplicado: {id}")
                continue

            nuevo_solicitante = Solicitante(id, pwd, nombre, correo, telefono, direccion)
            lista_solicitantes.insertar(nuevo_solicitante)

        messagebox.showinfo("Éxito", "Solicitantes cargados correctamente.")
        print("Lista actualizada:")
        lista_solicitantes.imprimirListaHaciaAdelante()

    except Exception as e:
        messagebox.showerror("Error", f"Error al cargar XML: {e}")

def ver_solicitantes():
    """
    Genera y abre un reporte gráfico de la lista de solicitantes.
    """
    if len(lista_solicitantes) == 0:
        messagebox.showinfo("Información", "La lista de solicitantes está vacía.")
    else:
        lista_solicitantes.graficar()

def crear_vista_administrador(root, on_logout):
    """
    Crea la vista de administrador.
    """
    # Limpiar la ventana
    for widget in root.winfo_children():
        widget.destroy()

    # Crear los marcos
    marco_solicitantes = tk.Frame(root)
    marco_artistas = tk.Frame(root)
    marco_reporte = tk.Frame(root)

    # Crear los botones y etiquetas
    boton_cargar_solicitantes = tk.Button(marco_solicitantes, text="Cargar Solicitantes", command=cargar_solicitantes)
    boton_ver_solicitantes = tk.Button(marco_solicitantes, text="Ver Solicitantes", command=ver_solicitantes)
    boton_cargar_artistas = tk.Button(marco_artistas, text="Cargar Artistas")
    boton_ver_artistas = tk.Button(marco_artistas, text="Ver Artistas")
    etiqueta_reporte = tk.Label(marco_reporte, text="Reporte")
    boton_cerrar_sesion = tk.Button(root, text="Cerrar Sesión", command=on_logout)

    # Organizar los elementos en la ventana
    marco_solicitantes.grid(row=0, column=0, padx=10, pady=10)
    marco_artistas.grid(row=0, column=1, padx=10, pady=10)
    marco_reporte.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
    boton_cerrar_sesion.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    boton_cargar_solicitantes.grid(row=0, column=0, pady=5)
    boton_ver_solicitantes.grid(row=1, column=0, pady=5)
    boton_cargar_artistas.grid(row=0, column=0, pady=5)
    boton_ver_artistas.grid(row=1, column=0, pady=5)
    etiqueta_reporte.grid(row=0, column=0, pady=5)
