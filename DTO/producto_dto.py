"""
DTO para la entidad Producto.
Implementa validaciones y métodos de utilidad para el manejo de productos.
"""

class ProductoDTO:
    def __init__(self, id=None, nombre=None, descripcion=None, precio=None, cantidad_en_stock=None, categoria_id=None):
        self._id = id
        self._nombre = nombre
        self._descripcion = descripcion
        self._precio = precio
        self._cantidad_en_stock = cantidad_en_stock
        self._categoria_id = categoria_id
        self.validar()

    @property
    def id(self):
        return self._id

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        if not valor or not valor.strip():
            raise ValueError("El nombre no puede estar vacío")
        self._nombre = valor.strip()

    @property
    def descripcion(self):
        return self._descripcion

    @descripcion.setter
    def descripcion(self, valor):
        self._descripcion = valor.strip() if valor else None

    @property
    def precio(self):
        return self._precio

    @precio.setter
    def precio(self, valor):
        if valor is not None and valor <= 0:
            raise ValueError("El precio debe ser mayor que 0")
        self._precio = valor

    @property
    def cantidad_en_stock(self):
        return self._cantidad_en_stock

    @cantidad_en_stock.setter
    def cantidad_en_stock(self, valor):
        if valor is not None and valor < 0:
            raise ValueError("El stock no puede ser negativo")
        self._cantidad_en_stock = valor

    @property
    def categoria_id(self):
        return self._categoria_id

    @categoria_id.setter
    def categoria_id(self, valor):
        self._categoria_id = valor

    def validar(self):
        """Valida que los datos del producto sean correctos."""
        if self._nombre is not None:
            self.nombre = self._nombre
        if self._precio is not None:
            self.precio = self._precio
        if self._cantidad_en_stock is not None:
            self.cantidad_en_stock = self._cantidad_en_stock

    def necesita_reposicion(self, nivel_alerta):
        """Determina si el producto necesita reposición."""
        return self._cantidad_en_stock <= nivel_alerta

    def calcular_valor_inventario(self):
        """Calcula el valor total del inventario para este producto."""
        return self._precio * self._cantidad_en_stock if self._precio and self._cantidad_en_stock else 0

    def to_dict(self):
        """Convierte el DTO a un diccionario."""
        return {
            'id': self._id,
            'nombre': self._nombre,
            'descripcion': self._descripcion,
            'precio': self._precio,
            'cantidad_en_stock': self._cantidad_en_stock,
            'categoria_id': self._categoria_id
        }

    def __str__(self):
        """Representación en string del producto."""
        return f"Producto(id={self._id}, nombre='{self._nombre}', stock={self._cantidad_en_stock}, precio=${self._precio})" 