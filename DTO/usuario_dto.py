class UsuarioDTO:
    def __init__(self, id_usuario=None, username=None, password_hash=None, nombres=None, 
                 apellidos=None, email=None, tipo_usuario=None, fecha_registro=None):
        self.id_usuario = id_usuario
        self.username = username
        self.password_hash = password_hash
        self.nombres = nombres
        self.apellidos = apellidos
        self.email = email
        self.tipo_usuario = tipo_usuario
        self.fecha_registro = fecha_registro

    def __str__(self):
        return f"Usuario: {self.username} - {self.nombres} {self.apellidos}" 