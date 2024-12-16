import tkinter as tk

class IPCArtStudio:
    def __init__(self, root, on_login_success):
        self.root = root
        self.on_login_success = on_login_success
        self.create_login_screen()

    def create_login_screen(self):
        # Limpiar la ventana
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Título
        title_label = tk.Label(self.root, text="IPCArt-Studio", font=("Arial", 20))
        title_label.pack(pady=20)
        
        # Etiqueta y campo de usuario
        username_label = tk.Label(self.root, text="Usuario:")
        username_label.pack()
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack()
        
        # Etiqueta y campo de contraseña
        password_label = tk.Label(self.root, text="Contraseña:")
        password_label.pack()
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack()
        
        # Botón de login
        login_button = tk.Button(self.root, text="Iniciar Sesión", command=self.login)
        login_button.pack(pady=20)
    
    def login(self):
        # Lógica de autenticación (por ahora, solo admin)
        username = self.username_entry.get()
        password = self.password_entry.get()
        # Validación de credenciales de prueba
        if username == "AdminIPC" and password == "ARTIPC2":
            self.on_login_success("Admin")
        elif username.startswith("Artista") and password == "ARTISTA123":
            self.on_login_success("Artista")
        elif username.startswith("Solicitante") and password == "SOLICITANTE123":
            self.on_login_success("Solicitante")
        else:
            print("Usuario o contraseña incorrectos")
