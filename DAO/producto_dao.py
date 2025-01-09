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
                SELECT 
                    p.nombre,
                    p.descripcion,
                    p.cantidad_en_stock as stock_actual,
                    p.precio as precio_actual,
                    COALESCE(e.total_entradas, 0) as entradas,
                    COALESCE(s.total_salidas, 0) as salidas,
                    cp.nombre as categoria,
                    COALESCE(e.total_entradas * p.precio, 0) as valor_entradas,
                    COALESCE(s.total_salidas * p.precio, 0) as valor_salidas,
                    (p.cantidad_en_stock * p.precio) as valor_total_inventario
                FROM productos p
                LEFT JOIN categorias_productos cp ON p.categoria_id = cp.id
                LEFT JOIN (
                    SELECT producto_id, SUM(cantidad) as total_entradas
                    FROM entradas_inventario
                    WHERE DATE(fecha) BETWEEN DATE(%s) AND DATE(%s)
                    GROUP BY producto_id
                ) e ON p.id = e.producto_id
                LEFT JOIN (
                    SELECT producto_id, SUM(cantidad) as total_salidas
                    FROM salidas_inventario
                    WHERE DATE(fecha) BETWEEN DATE(%s) AND DATE(%s)
                    GROUP BY producto_id
                ) s ON p.id = s.producto_id
                WHERE e.total_entradas > 0 OR s.total_salidas > 0
                ORDER BY p.nombre
            """
            cursor.execute(sql, (fecha_inicio, fecha_fin, fecha_inicio, fecha_fin))
            resultados = cursor.fetchall()
            
            # Asegurar que los valores numéricos sean float y calcular totales
            for resultado in resultados:
                resultado['precio_actual'] = float(resultado['precio_actual'])
                resultado['stock_actual'] = int(resultado['stock_actual'])
                resultado['entradas'] = int(resultado['entradas'])
                resultado['salidas'] = int(resultado['salidas'])
                resultado['valor_entradas'] = float(resultado['valor_entradas'])
                resultado['valor_salidas'] = float(resultado['valor_salidas'])
                resultado['valor_total'] = float(resultado['valor_total_inventario'])
            
            return resultados
        except pymysql.Error as error:
            print(f"Error al generar reporte: {error}")
            raise
        finally:
            if conn and conn.open:
                cursor.close()
                conn.close()

    def tiene_movimientos(self, producto_id):
        conn = None
        try:
            conn = self.conexion.get_connection()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            
            # Verificar entradas
            cursor.execute("""
                SELECT 
                    (SELECT COUNT(*) FROM entradas_inventario WHERE producto_id = %s) +
                    (SELECT COUNT(*) FROM salidas_inventario WHERE producto_id = %s) +
                    (SELECT COUNT(*) FROM detalles_pedidos WHERE producto_id = %s) as total
            """, (producto_id, producto_id, producto_id))
            
            resultado = cursor.fetchone()
            return resultado['total'] > 0
            
        except pymysql.Error as error:
            print(f"Error al verificar movimientos: {error}")
            raise
        finally:
            if conn and conn.open:
                cursor.close()
                conn.close()

    def eliminar_movimientos(self, producto_id):
        conn = None
        try:
            conn = self.conexion.get_connection()
            cursor = conn.cursor()
            
            # Primero eliminamos el historial de precios
            cursor.execute("""
                DELETE FROM historial_precios 
                WHERE producto_id = %s
            """, (producto_id,))
            
            # Luego eliminamos las alertas de inventario
            cursor.execute("""
                DELETE FROM alertas_inventario 
                WHERE producto_id = %s
            """, (producto_id,))
            
            # Eliminamos los detalles de pedidos
            cursor.execute("""
                DELETE FROM detalles_pedidos 
                WHERE producto_id = %s
            """, (producto_id,))
            
            # Eliminamos las entradas
            cursor.execute("""
                DELETE FROM entradas_inventario 
                WHERE producto_id = %s
            """, (producto_id,))
            
            # Eliminamos las salidas
            cursor.execute("""
                DELETE FROM salidas_inventario 
                WHERE producto_id = %s
            """, (producto_id,))
            
            conn.commit()
            return True
        except pymysql.Error as error:
            if conn:
                conn.rollback()
            print(f"Error al eliminar movimientos: {error}")
            raise
        finally:
            if conn and conn.open:
                cursor.close()
                conn.close()

    def eliminar(self, producto_id):
        conn = None
        try:
            conn = self.conexion.get_connection()
            cursor = conn.cursor()
            
            # Primero verificamos si el producto existe
            cursor.execute("SELECT id FROM productos WHERE id = %s", (producto_id,))
            if not cursor.fetchone():
                raise Exception("El producto no existe")
            
            # Eliminamos primero todos los registros relacionados
            self.eliminar_movimientos(producto_id)
            
            # Finalmente eliminamos el producto
            cursor.execute("DELETE FROM productos WHERE id = %s", (producto_id,))
            conn.commit()
            return True
            
        except pymysql.Error as error:
            if conn:
                conn.rollback()
            print(f"Error en la base de datos: {error}")
            raise Exception(f"Error al eliminar el producto: {str(error)}")
        except Exception as e:
            if conn:
                conn.rollback()
            raise e
        finally:
            if conn and conn.open:
                cursor.close()
                conn.close()

    def verificar_fechas_movimientos(self):
        conn = None
        try:
            conn = self.conexion.get_connection()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            
            cursor.execute("""
                SELECT 
                    MIN(fecha) as primera_fecha,
                    MAX(fecha) as ultima_fecha
                FROM (
                    SELECT fecha FROM entradas_inventario
                    UNION ALL
                    SELECT fecha FROM salidas_inventario
                ) as todas_fechas
                WHERE fecha IS NOT NULL
            """)
            
            resultado = cursor.fetchone()
            if resultado['primera_fecha'] is None or resultado['ultima_fecha'] is None:
                # Si no hay movimientos, usar el último mes
                from datetime import datetime, timedelta
                fecha_actual = datetime.now()
                resultado = {
                    'primera_fecha': fecha_actual - timedelta(days=30),
                    'ultima_fecha': fecha_actual
                }
            return resultado
            
        except pymysql.Error as error:
            print(f"Error al verificar fechas: {error}")
            raise
        finally:
            if conn and conn.open:
                cursor.close()
                conn.close()

    def listar_categorias(self):
        """Lista todas las categorías disponibles."""
        conn = None
        try:
            conn = self.conexion.get_connection()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute("SELECT id, nombre FROM categorias_productos ORDER BY nombre")
            return cursor.fetchall()
        except pymysql.Error as error:
            print(f"Error al listar categorías: {error}")
            raise
        finally:
            if conn and conn.open:
                cursor.close()
                conn.close() 