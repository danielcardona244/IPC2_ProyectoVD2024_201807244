import tkinter as tk
from vista.loginVista import IPCArtStudio


from vista.modAdminVista import crear_vista_administrador


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
        # Destruye la vista actual si existe
        if self.current_view:
            for widget in self.root.winfo_children():
                widget.destroy()
        
        # Crea la vista de login
        self.current_view = IPCArtStudio(self.root, self.on_login_success)

    def show_admin_view(self):
        """
        Muestra la vista de administrador después de iniciar sesión.
        """
        # Destruye la vista actual si existe
        if self.current_view:
            for widget in self.root.winfo_children():
                widget.destroy()
        
        # Crea la vista de administrador
        self.current_view = crear_vista_administrador(self.root, self.show_login_view)

    import vista.modAdminVista



    def on_login_success(self, user_type):
        """
        Callback después de un login exitoso.
        """
        if user_type == "Admin":
            self.show_admin_view()
        else:
            print(f"Tipo de usuario no soportado: {user_type}")

    def run(self):
        """
        Ejecuta el bucle principal de la aplicación.
        """
        self.root.mainloop()

if __name__ == "__main__":
    app = MainApp()
    app.run()
