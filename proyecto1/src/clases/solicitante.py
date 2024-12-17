class Solicitante:
    def __init__(self, id, pwd, nombre, correo, telefono, direccion):
        self.id = id
        self.password = pwd
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono
        self.direccion = direccion

    def __str__(self):
        return f"ID: {self.id} | Nombre: {self.nombre} | Correo: {self.correo} | Teléfono: {self.telefono}"
