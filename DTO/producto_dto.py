class ProductoDTO:
    def __init__(self, id=None, nombre=None, descripcion=None, precio=None, cantidad_en_stock=None, categoria_id=None):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio
        self.cantidad_en_stock = cantidad_en_stock
        self.categoria_id = categoria_id

    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'precio': self.precio,
            'cantidad_en_stock': self.cantidad_en_stock,
            'categoria_id': self.categoria_id
        } 