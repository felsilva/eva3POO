from DTO.producto_dto import ProductoDTO
from .conexion import Conexion
import pymysql

class ProductoDAO:
    def __init__(self):
        self.conexion = Conexion()

    def crear(self, producto_dto):
        conn = None
        try:
            conn = self.conexion.get_connection()
            cursor = conn.cursor()
            
            # Insertar el producto
            sql = """INSERT INTO productos (nombre, descripcion, precio, cantidad_en_stock, categoria_id) 
                     VALUES (%s, %s, %s, %s, %s)"""
            valores = (producto_dto.nombre, producto_dto.descripcion, 
                      producto_dto.precio, producto_dto.cantidad_en_stock,
                      producto_dto.categoria_id)
            cursor.execute(sql, valores)
            
            # Registrar el precio inicial en el historial
            producto_id = cursor.lastrowid
            sql_historial = """INSERT INTO historial_precios 
                             (producto_id, precio_anterior, precio_nuevo) 
                             VALUES (%s, %s, %s)"""
            cursor.execute(sql_historial, (producto_id, producto_dto.precio, producto_dto.precio))
            
            conn.commit()
            return producto_id
        except pymysql.Error as error:
            print(f"Error al crear producto: {error}")
            raise
        finally:
            if conn and conn.open:
                cursor.close()
                conn.close()

    def actualizar(self, producto_dto):
        conn = None
        try:
            conn = self.conexion.get_connection()
            cursor = conn.cursor()
            
            # Obtener precio actual
            cursor.execute("SELECT precio FROM productos WHERE id = %s", (producto_dto.id,))
            resultado = cursor.fetchone()
            if not resultado:
                raise ValueError("Producto no encontrado")
            
            precio_anterior = resultado['precio']
            
            # Actualizar producto
            sql = """UPDATE productos 
                     SET nombre = %s, 
                         descripcion = %s, 
                         precio = %s, 
                         cantidad_en_stock = %s
                     WHERE id = %s"""
            valores = (
                producto_dto.nombre,
                producto_dto.descripcion,
                producto_dto.precio,
                producto_dto.cantidad_en_stock,
                producto_dto.id
            )
            cursor.execute(sql, valores)
            
            # Registrar cambio de precio si hubo cambio
            if precio_anterior != producto_dto.precio:
                sql_historial = """INSERT INTO historial_precios 
                                 (producto_id, precio_anterior, precio_nuevo, usuario_id) 
                                 VALUES (%s, %s, %s, %s)"""
                cursor.execute(sql_historial, (
                    producto_dto.id,
                    precio_anterior,
                    producto_dto.precio,
                    1  # ID del usuario por defecto
                ))
            
            conn.commit()
            return True
            
        except pymysql.Error as error:
            if conn:
                conn.rollback()
            print(f"Error al actualizar producto: {error}")
            raise
        finally:
            if conn and conn.open:
                cursor.close()
                conn.close()

    def obtener_por_id(self, id):
        conn = None
        try:
            conn = self.conexion.get_connection()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            sql = """SELECT p.*, c.nombre as categoria_nombre
                     FROM productos p
                     LEFT JOIN categorias_productos c ON p.categoria_id = c.id
                     WHERE p.id = %s"""
            cursor.execute(sql, (id,))
            resultado = cursor.fetchone()
            if resultado:
                categoria_nombre = resultado.pop('categoria_nombre', None)
                return ProductoDTO(**resultado)
            return None
        except pymysql.Error as error:
            print(f"Error al obtener producto: {error}")
            raise
        finally:
            if conn and conn.open:
                cursor.close()
                conn.close()

    def listar_todos(self):
        conn = None
        try:
            conn = self.conexion.get_connection()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            sql = """SELECT p.*, c.nombre as categoria_nombre
                     FROM productos p
                     LEFT JOIN categorias_productos c ON p.categoria_id = c.id"""
            cursor.execute(sql)
            resultados = cursor.fetchall()
            productos = []
            for producto in resultados:
                categoria_nombre = producto.pop('categoria_nombre', None)
                productos.append(ProductoDTO(**producto))
            return productos
        except pymysql.Error as error:
            print(f"Error al listar productos: {error}")
            raise
        finally:
            if conn and conn.open:
                cursor.close()
                conn.close()

    def listar_por_categoria(self, categoria_id):
        conn = None
        try:
            conn = self.conexion.get_connection()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            sql = """SELECT p.*, c.nombre as categoria_nombre
                     FROM productos p
                     LEFT JOIN categorias_productos c ON p.categoria_id = c.id
                     WHERE p.categoria_id = %s"""
            cursor.execute(sql, (categoria_id,))
            resultados = cursor.fetchall()
            return [ProductoDTO(**producto) for producto in resultados]
        except pymysql.Error as error:
            print(f"Error al listar productos por categoría: {error}")
            raise
        finally:
            if conn and conn.open:
                cursor.close()
                conn.close()

    def verificar_stock_bajo(self):
        conn = None
        try:
            conn = self.conexion.get_connection()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            sql = """SELECT p.*, c.nombre as categoria_nombre, a.nivel_alerta 
                     FROM productos p 
                     LEFT JOIN categorias_productos c ON p.categoria_id = c.id
                     JOIN alertas_inventario a ON p.id = a.producto_id 
                     WHERE p.cantidad_en_stock <= a.nivel_alerta"""
            cursor.execute(sql)
            return cursor.fetchall()
        except pymysql.Error as error:
            print(f"Error al verificar stock bajo: {error}")
            raise
        finally:
            if conn and conn.open:
                cursor.close()
                conn.close()

    def registrar_movimiento(self, producto_id, cantidad, tipo_movimiento, usuario_id, proveedor_id=None, precio_unitario=None):
        conn = None
        try:
            conn = self.conexion.get_connection()
            cursor = conn.cursor()
            
            # Actualizar stock
            if tipo_movimiento == 'entrada':
                sql_update = "UPDATE productos SET cantidad_en_stock = cantidad_en_stock + %s WHERE id = %s"
                sql_mov = """INSERT INTO entradas_inventario 
                            (producto_id, cantidad, usuario_id, proveedor_id, precio_unitario) 
                            VALUES (%s, %s, %s, %s, %s)"""
                valores_mov = (producto_id, cantidad, usuario_id, proveedor_id, precio_unitario)
            else:
                sql_update = "UPDATE productos SET cantidad_en_stock = cantidad_en_stock - %s WHERE id = %s"
                sql_mov = """INSERT INTO salidas_inventario 
                            (producto_id, cantidad, usuario_id) 
                            VALUES (%s, %s, %s)"""
                valores_mov = (producto_id, cantidad, usuario_id)
            
            cursor.execute(sql_update, (cantidad, producto_id))
            cursor.execute(sql_mov, valores_mov)
            conn.commit()
        except pymysql.Error as error:
            print(f"Error al registrar movimiento: {error}")
            raise
        finally:
            if conn and conn.open:
                cursor.close()
                conn.close()

    def generar_reporte_movimientos(self, fecha_inicio, fecha_fin):
        conn = None
        try:
            conn = self.conexion.get_connection()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            sql = """
                SELECT p.nombre, c.nombre as categoria, p.descripcion,
                       (SELECT SUM(cantidad) FROM entradas_inventario 
                        WHERE producto_id = p.id AND fecha BETWEEN %s AND %s) as entradas,
                       (SELECT SUM(cantidad) FROM salidas_inventario 
                        WHERE producto_id = p.id AND fecha BETWEEN %s AND %s) as salidas,
                       p.cantidad_en_stock as stock_actual,
                       p.precio as precio_actual
                FROM productos p
                LEFT JOIN categorias_productos c ON p.categoria_id = c.id
            """
            cursor.execute(sql, (fecha_inicio, fecha_fin, fecha_inicio, fecha_fin))
            return cursor.fetchall()
        except pymysql.Error as error:
            print(f"Error al generar reporte: {error}")
            raise
        finally:
            if conn and conn.open:
                cursor.close()
                conn.close()

    def eliminar(self, id_producto):
        """Elimina un producto del sistema."""
        conn = None
        try:
            conn = self.conexion.get_connection()
            cursor = conn.cursor()
            
            # Verificar si el producto existe
            cursor.execute("SELECT id FROM productos WHERE id = %s", (id_producto,))
            if not cursor.fetchone():
                raise ValueError("Producto no encontrado")
            
            # Verificar si hay movimientos asociados
            cursor.execute("""
                SELECT COUNT(*) as total 
                FROM (
                    SELECT producto_id FROM entradas_inventario WHERE producto_id = %s
                    UNION ALL
                    SELECT producto_id FROM salidas_inventario WHERE producto_id = %s
                ) as movimientos
            """, (id_producto, id_producto))
            
            if cursor.fetchone()['total'] > 0:
                raise ValueError("No se puede eliminar el producto porque tiene movimientos asociados")
            
            # Eliminar el producto
            cursor.execute("DELETE FROM productos WHERE id = %s", (id_producto,))
            conn.commit()
            return True
            
        except pymysql.Error as error:
            if conn:
                conn.rollback()
            print(f"Error al eliminar producto: {error}")
            raise
        finally:
            if conn and conn.open:
                cursor.close()
                conn.close() 