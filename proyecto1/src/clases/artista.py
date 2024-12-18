class Artista:
    def __init__(self, id, password, nombre_completo, correo, telefono, especialidades, notas_adicionales):
        self.id = id
        self.password = password
        self.nombre_completo = nombre_completo
        self.correo = correo
        self.telefono = telefono
        self.especialidades = especialidades
        self.notas_adicionales = notas_adicionales

    def __str__(self):
        return (f"ID: {self.id}\\n"
                f"Nombre: {self.nombre_completo}\\n"
                f"Correo: {self.correo}\\n"
                f"Teléfono: {self.telefono}\\n"
                f"Especialidades: {self.especialidades}\\n"
                f"Notas: {self.notas_adicionales}")
