"""
DTO para la entidad Producto.
Implementa validaciones y métodos de utilidad para el manejo de productos.
"""

class ProductoDTO:
    def __init__(self, id=None, nombre=None, descripcion=None, precio=None, 
                 cantidad_en_stock=None, categoria_id=None):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = float(precio) if precio is not None else None
        self.cantidad_en_stock = int(cantidad_en_stock) if cantidad_en_stock is not None else None
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

    @staticmethod
    def from_dict(data):
        return ProductoDTO(
            id=data.get('id'),
            nombre=data.get('nombre'),
            descripcion=data.get('descripcion'),
            precio=data.get('precio'),
            cantidad_en_stock=data.get('cantidad_en_stock'),
            categoria_id=data.get('categoria_id')
        )

    def validar(self):
        if not self.nombre:
            raise ValueError("El nombre del producto es obligatorio")
        if self.precio is not None and self.precio < 0:
            raise ValueError("El precio no puede ser negativo")
        if self.cantidad_en_stock is not None and self.cantidad_en_stock < 0:
            raise ValueError("La cantidad en stock no puede ser negativa") 