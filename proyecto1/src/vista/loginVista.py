import tkinter as tk
from tkinter import messagebox
from estructuras.lista_simple.listaSimple import ListaSimple
from estructuras.lista_doble.listaDoble import ListaDoble
from clases.artista import Artista
from clases.solicitante import Solicitante

# Instancias de listas globales para artistas y solicitantes
lista_artistas = ListaSimple()
lista_solicitantes = ListaDoble()

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
        # Lógica de autenticación
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        # Admin fijo
        if username == "AdminIPC" and password == "ARTIPC2":
            self.on_login_success("Admin")
<<<<<<< HEAD
        elif username.startswith("Artista") and password == "ARTISTA123":
            self.on_login_success("Artista")
        elif username.startswith("Solicitante") and password == "SOLICITANTE123":
            self.on_login_success("Solicitante")
        else:
            print("Usuario o contraseña incorrectos")
=======
            return

        # Buscar en la lista de artistas
        actual_artista = lista_artistas.primero
        while actual_artista is not None:
            if actual_artista.valor.id == username and actual_artista.valor.password == password:
                self.on_login_success("Artista")
                return
            actual_artista = actual_artista.siguiente
        
        # Buscar en la lista de solicitantes (usar atributo 'pwd')
        actual_solicitante = lista_solicitantes.primero
        while actual_solicitante is not None:
            if actual_solicitante.valor.id == username and actual_solicitante.valor.pwd == password:
                self.on_login_success("Solicitante")
                return
            actual_solicitante = actual_solicitante.siguiente
        
        # Si no se encuentra ninguna coincidencia
        messagebox.showerror("Error", "Usuario o contraseña incorrectos")

if __name__ == "__main__":
    def on_login_success(role):
        print(f"Login exitoso. Rol: {role}")

    root = tk.Tk()
    app = IPCArtStudio(root, on_login_success)
    root.mainloop()
>>>>>>> develop_201807244
