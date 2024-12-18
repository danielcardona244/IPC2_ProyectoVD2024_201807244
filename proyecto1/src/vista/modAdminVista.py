import tkinter as tk
from tkinter import filedialog, messagebox
import xml.etree.ElementTree as ET
from estructuras.lista_simple.listaSimple import ListaSimple  # Lista simplemente enlazada
from clases.artista import Artista  # Clase Artista
from estructuras.lista_doble.listaDoble import ListaDoble
from clases.solicitante import Solicitante

lista_solicitantes = ListaDoble()
lista_artistas = ListaSimple()

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

def cargar_artistas():
    """
    Carga artistas desde un archivo XML.
    """
    file_path = filedialog.askopenfilename(title="Seleccionar archivo XML", filetypes=[("Archivos XML", "*.xml")])
    if not file_path:
        return

    try:
        tree = ET.parse(file_path)
        root = tree.getroot()

        for artista in root.findall("Artista"):
            id = artista.get("id")
            pwd = artista.get("pwd")
            nombre = artista.find("NombreCompleto").text
            correo = artista.find("CorreoElectronico").text
            telefono = artista.find("NumeroTelefono").text
            especialidades = artista.find("Especialidades").text
            notas = artista.find("NotasAdicionales").text

            # Validar que no exista el ID
            if not id.startswith("ART-"):
                print(f"ID no valido: {id}")
                continue
            if lista_artistas.validarExiste(id):
                print(f"ID duplicado: {id}")
                continue

            # Crear y agregar el artista
            nuevo_artista = Artista(id, pwd, nombre, correo, telefono, especialidades, notas)
            lista_artistas.insertar(nuevo_artista)

        messagebox.showinfo("Éxito", "Artistas cargados correctamente.")
        print("Lista actualizada de artistas:")
        lista_artistas.imprimirLista()

    except Exception as e:
        messagebox.showerror("Error", f"Error al cargar XML: {e}")

def ver_artistas():
    """
    Genera y abre un reporte gráfico de la lista de artistas.
    """
    if len(lista_artistas) == 0:
        messagebox.showinfo("Información", "La lista de artistas está vacía.")
    else:
        lista_artistas.graficar()

def crear_vista_administrador(root, on_logout):
    """
    Crea la vista de administrador con un diseño mejorado.
    """
    # Limpiar la ventana
    for widget in root.winfo_children():
        widget.destroy()

    root.title("IPCArt-Studio")

    # Configuración de la interfaz
    root.configure(bg="white")

    # Título
    titulo = tk.Label(root, text="IPCArt-Studio", font=("Arial", 16, "bold"), bg="white")
    titulo.grid(row=0, column=0, columnspan=3, pady=10)

    # Marcos
    marco_solicitantes = tk.LabelFrame(root, text="Solicitantes", bg="white", font=("Arial", 10, "bold"))
    marco_artistas = tk.LabelFrame(root, text="Artistas", bg="white", font=("Arial", 10, "bold"))
    marco_reporte = tk.LabelFrame(root, text="Reporte", bg="white", font=("Arial", 10, "bold"))

    # Botones de solicitantes
    boton_cargar_solicitantes = tk.Button(marco_solicitantes, text="Cargar Solicitanes", command=cargar_solicitantes, width=20)
    boton_ver_solicitantes = tk.Button(marco_solicitantes, text="Ver Solicitanes", command=ver_solicitantes, width=20)
    boton_cargar_solicitantes.pack(pady=5)
    boton_ver_solicitantes.pack(pady=5)

    # Botones de artistas
    boton_cargar_artistas = tk.Button(marco_artistas, text="Cargar Artistas", command=cargar_artistas, width=20)
    boton_ver_artistas = tk.Button(marco_artistas, text="Ver Artistas", command=ver_artistas, width=20)
    boton_cargar_artistas.pack(pady=5)
    boton_ver_artistas.pack(pady=5)

    # Reporte
    etiqueta_reporte = tk.Label(marco_reporte, text="Aquí se mostrarán los reportes", bg="white")
    etiqueta_reporte.pack(pady=20, padx=20)

    # Botón cerrar sesión
    boton_cerrar_sesion = tk.Button(root, text="Cerrar Sesión", command=on_logout, width=20)

    # Ubicar marcos
    marco_solicitantes.grid(row=1, column=0, padx=20, pady=10)
    marco_artistas.grid(row=1, column=1, padx=20, pady=10)
    marco_reporte.grid(row=2, column=0, columnspan=3, pady=20, padx=20, ipadx=50, ipady=50)
    boton_cerrar_sesion.grid(row=3, column=0, columnspan=3, pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    crear_vista_administrador(root, root.quit)
    root.mainloop()
