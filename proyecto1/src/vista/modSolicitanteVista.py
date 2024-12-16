import tkinter as tk

class ModuloSolicitanteVista:
    def __init__(self, root, on_logout):
        self.root = root
        self.on_logout = on_logout
        self.crear_interfaz_galeria()

    def crear_interfaz_galeria(self):
        # Limpiar la ventana
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.title("IPCArt-Studio - Galería de Imágenes")

        # Botón de Cerrar Sesión
        btn_cerrar_sesion = tk.Button(self.root, text="Cerrar Sesión", command=self.on_logout)
        btn_cerrar_sesion.pack(anchor="ne", padx=10, pady=10)

        # Botones de navegación
        frame_navegacion = tk.Frame(self.root)
        frame_navegacion.pack(pady=10)
        btn_anterior = tk.Button(frame_navegacion, text="Anterior", width=15)
        btn_anterior.pack(side="left", padx=20)
        btn_siguiente = tk.Button(frame_navegacion, text="Siguiente", width=15)
        btn_siguiente.pack(side="right", padx=20)

        # Marco de imagen
        frame_imagen = tk.Frame(self.root, width=400, height=300, bg="gray")
        frame_imagen.pack(pady=20)

    def crear_interfaz_solicitar(self):
        # Limpiar la ventana
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.title("IPCArt-Studio - Solicitar")

        # Botón de Cerrar Sesión
        btn_cerrar_sesion = tk.Button(self.root, text="Cerrar Sesión", command=self.on_logout)
        btn_cerrar_sesion.pack(anchor="ne", padx=10, pady=10)

        # Botones para Solicitar
        frame_solicitar = tk.Frame(self.root)
        frame_solicitar.pack(pady=20)
        lbl_solicitar = tk.Label(frame_solicitar, text="Solicitar", font=("Arial", 16, "bold"))
        lbl_solicitar.grid(row=0, column=0, columnspan=2, pady=10)

        btn_cargar_figura = tk.Button(frame_solicitar, text="Cargar Figura", width=20)
        btn_cargar_figura.grid(row=1, column=0, padx=20, pady=5)
        btn_solicitar = tk.Button(frame_solicitar, text="Solicitar", width=20)
        btn_solicitar.grid(row=2, column=0, padx=20, pady=5)

        # Botones de Reportes
        btn_ver_pila = tk.Button(frame_solicitar, text="Ver Pila", width=20)
        btn_ver_pila.grid(row=1, column=1, padx=20, pady=5)
        btn_ver_lista = tk.Button(frame_solicitar, text="Ver Lista", width=20)
        btn_ver_lista.grid(row=2, column=1, padx=20, pady=5)

        # Marco de imagen
        frame_imagen = tk.Frame(self.root, width=400, height=300, bg="gray")
        frame_imagen.pack(pady=20)
