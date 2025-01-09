class ProductoService:
    def __init__(self, producto_dao):
        self.producto_dao = producto_dao

    def eliminar_producto(self, producto_id):
        try:
            return self.producto_dao.eliminar(producto_id)
        except Exception as e:
            raise Exception(f"Error al eliminar el producto: {str(e)}") 

    def eliminar_producto_con_movimientos(self, producto_id, confirmar_eliminacion=False):
        try:
            if not confirmar_eliminacion:
                if self.producto_dao.tiene_movimientos(producto_id):
                    return False, "El producto tiene movimientos y/o pedidos asociados. ¿Desea eliminar el producto y todos sus registros relacionados?"
            
            self.producto_dao.eliminar(producto_id)
            return True, "Producto y todos sus registros relacionados eliminados correctamente"
            
        except Exception as e:
            raise Exception(f"Error al eliminar el producto: {str(e)}") 