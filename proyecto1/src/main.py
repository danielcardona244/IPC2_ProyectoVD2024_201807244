import tkinter as tk
from vista.loginVista import IPCArtStudio
from vista.modAdminVista import crear_vista_administrador
from vista.modArtistaVista import ModuloArtistaVista
from vista.modSolicitanteVista import ModuloSolicitanteVista


class MainApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("IPCArt-Studio")
        self.current_view = None  # Vista actual

        # Inicia con la pantalla de login
        self.show_login_view()

    def show_login_view(self):
        """
        Muestra la pantalla de login.
        """
        self.clean_view()
        self.current_view = IPCArtStudio(self.root, self.on_login_success)

    def show_admin_view(self):
        """
        Muestra la vista de administrador después de iniciar sesión.
        """
        self.clean_view()
        self.current_view = crear_vista_administrador(self.root, self.show_login_view)

    def show_artista_view(self):
        """
        Muestra la vista del módulo de artista.
        """
        self.clean_view()
        self.current_view = ModuloArtistaVista(self.root, self.show_login_view)

    def show_solicitante_view(self):
        """
        Muestra la vista del módulo de solicitantes.
        """
        self.clean_view()
        self.current_view = ModuloSolicitanteVista(self.root, self.show_login_view)

    def on_login_success(self, user_type):
        """
        Callback después de un login exitoso.
        """
        if user_type == "Admin":
            self.show_admin_view()
        elif user_type == "Artista":
            self.show_artista_view()
        elif user_type == "Solicitante":
            self.show_solicitante_view()
        else:
            print(f"Tipo de usuario no soportado: {user_type}")

    def clean_view(self):
        """
        Elimina la vista actual de la ventana.
        """
        if self.current_view:
            for widget in self.root.winfo_children():
                widget.destroy()

    def run(self):
        """
        Ejecuta el bucle principal de la aplicación.
        """
        self.root.mainloop()


if __name__ == "__main__":
    app = MainApp()
    app.run()
