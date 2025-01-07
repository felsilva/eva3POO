class MovimientoInventarioDTO:
    def __init__(self, id=None, producto_id=None, cantidad=None, fecha=None, tipo_movimiento=None):
        self.id = id
        self.producto_id = producto_id
        self.cantidad = cantidad
        self.fecha = fecha
        self.tipo_movimiento = tipo_movimiento  # 'entrada' o 'salida'

    def to_dict(self):
        return {
            'id': self.id,
            'producto_id': self.producto_id,
            'cantidad': self.cantidad,
            'fecha': self.fecha,
            'tipo_movimiento': self.tipo_movimiento
        } 