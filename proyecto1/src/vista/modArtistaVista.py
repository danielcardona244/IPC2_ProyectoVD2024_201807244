import tkinter as tk

class ModuloArtistaVista:
    def __init__(self, root, on_logout):
        self.root = root
        self.on_logout = on_logout
        self.crear_interfaz()

    def crear_interfaz(self):
        # Limpiar la ventana
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.title("IPCArt-Studio - Módulo Artista")

        # Botón de Cerrar Sesión
        btn_cerrar_sesion = tk.Button(self.root, text="Cerrar Sesión", command=self.on_logout)
        btn_cerrar_sesion.pack(anchor="ne", padx=10, pady=10)

        # Marco principal
        frame_principal = tk.Frame(self.root)
        frame_principal.pack(pady=20)

        # Botón Aceptar
        btn_aceptar = tk.Button(frame_principal, text="Aceptar", width=15)
        btn_aceptar.grid(row=0, column=0, padx=20, pady=10)

        # Información del solicitante
        frame_info = tk.Frame(frame_principal, bd=1, relief="solid")
        frame_info.grid(row=0, column=1, padx=20, pady=10)
        lbl_solicitante = tk.Label(frame_info, text="Solicitante: IPC-001\nImagen: Kirby", justify="left")
        lbl_solicitante.pack(padx=10, pady=10)

        # Botones de Reportes
        btn_ver_cola = tk.Button(frame_principal, text="Ver Cola", width=15)
        btn_ver_cola.grid(row=1, column=0, padx=20, pady=5)
        btn_imagenes_solicitadas = tk.Button(frame_principal, text="Imagenes Solicitadas", width=15)
        btn_imagenes_solicitadas.grid(row=2, column=0, padx=20, pady=5)

        # Marco para Reportes
        lbl_reportes = tk.Label(self.root, text="Reportes", font=("Arial", 12, "bold"))
        lbl_reportes.pack(pady=10)
        frame_reportes = tk.Frame(self.root, bd=1, relief="solid", width=400, height=200)
        frame_reportes.pack()

