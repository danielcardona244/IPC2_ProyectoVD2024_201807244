import tkinter as tk

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
    boton_cargar_solicitantes = tk.Button(marco_solicitantes, text="Cargar Solicitantes")
    boton_cargar_artistas = tk.Button(marco_artistas, text="Cargar Artistas")
    boton_ver_solicitantes = tk.Button(marco_solicitantes, text="Ver Solicitantes")
    boton_ver_artistas = tk.Button(marco_artistas, text="Ver Artistas")
    etiqueta_reporte = tk.Label(marco_reporte, text="Reporte")
    boton_cerrar_sesion = tk.Button(root, text="Cerrar Sesión", command=on_logout)

    # Organizar los elementos en la ventana
    marco_solicitantes.grid(row=0, column=0, padx=10, pady=10)
    marco_artistas.grid(row=0, column=1, padx=10, pady=10)
    marco_reporte.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
    boton_cerrar_sesion.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    boton_cargar_solicitantes.grid(row=0, column=0, pady=5)
    boton_cargar_artistas.grid(row=0, column=0, pady=5)
    boton_ver_solicitantes.grid(row=1, column=0, pady=5)
    boton_ver_artistas.grid(row=1, column=0, pady=5)
    etiqueta_reporte.grid(row=0, column=0, pady=5)
