class TipoDTO:
    def __init__(self, id_tipo=None, nombre=None, descripcion=None):
        self.id_tipo = id_tipo
        self.nombre = nombre
        self.descripcion = descripcion

    def __str__(self):
        return f"Tipo: {self.nombre} - {self.descripcion}" 