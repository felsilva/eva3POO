from DTO.producto_dto import ProductoDTO
from .conexion import Conexion
import mysql.connector
from datetime import datetime

class ProductoDAO:
    def __init__(self):
        self.conexion = Conexion()

    def crear(self, producto_dto):
        try:
            conn = self.conexion.get_conexion()
            cursor = conn.cursor()
            sql = """INSERT INTO productos (nombre, descripcion, precio, cantidad_en_stock, categoria_id) 
                     VALUES (%s, %s, %s, %s, %s)"""
            valores = (producto_dto.nombre, producto_dto.descripcion, producto_dto.precio,
                      producto_dto.cantidad_en_stock, producto_dto.categoria_id)
            cursor.execute(sql, valores)
            conn.commit()
            return cursor.lastrowid
        except mysql.connector.Error as error:
            print(f"Error al crear producto: {error}")
            raise
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    def actualizar(self, producto_dto):
        try:
            conn = self.conexion.get_conexion()
            cursor = conn.cursor()
            sql = """UPDATE productos 
                     SET nombre = %s, descripcion = %s, precio = %s, 
                         cantidad_en_stock = %s, categoria_id = %s 
                     WHERE id = %s"""
            valores = (producto_dto.nombre, producto_dto.descripcion, producto_dto.precio,
                      producto_dto.cantidad_en_stock, producto_dto.categoria_id, producto_dto.id)
            cursor.execute(sql, valores)
            conn.commit()
        except mysql.connector.Error as error:
            print(f"Error al actualizar producto: {error}")
            raise
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    def obtener_por_id(self, id):
        try:
            conn = self.conexion.get_conexion()
            cursor = conn.cursor(dictionary=True)
            sql = "SELECT * FROM productos WHERE id = %s"
            cursor.execute(sql, (id,))
            resultado = cursor.fetchone()
            if resultado:
                return ProductoDTO(**resultado)
            return None
        except mysql.connector.Error as error:
            print(f"Error al obtener producto: {error}")
            raise
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    def listar_todos(self):
        try:
            conn = self.conexion.get_conexion()
            cursor = conn.cursor(dictionary=True)
            sql = "SELECT * FROM productos"
            cursor.execute(sql)
            resultados = cursor.fetchall()
            return [ProductoDTO(**producto) for producto in resultados]
        except mysql.connector.Error as error:
            print(f"Error al listar productos: {error}")
            raise
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    def verificar_stock_bajo(self):
        try:
            conn = self.conexion.get_conexion()
            cursor = conn.cursor(dictionary=True)
            sql = """SELECT p.*, a.nivel_alerta 
                     FROM productos p 
                     JOIN alertas_inventario a ON p.id = a.producto_id 
                     WHERE p.cantidad_en_stock <= a.nivel_alerta"""
            cursor.execute(sql)
            resultados = cursor.fetchall()
            return resultados
        except mysql.connector.Error as error:
            print(f"Error al verificar stock bajo: {error}")
            raise
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    def registrar_movimiento(self, producto_id, cantidad, tipo_movimiento):
        try:
            conn = self.conexion.get_conexion()
            cursor = conn.cursor()
            
            # Actualizar stock
            if tipo_movimiento == 'entrada':
                sql_update = "UPDATE productos SET cantidad_en_stock = cantidad_en_stock + %s WHERE id = %s"
                sql_mov = "INSERT INTO entradas_inventario (producto_id, cantidad) VALUES (%s, %s)"
            else:
                sql_update = "UPDATE productos SET cantidad_en_stock = cantidad_en_stock - %s WHERE id = %s"
                sql_mov = "INSERT INTO salidas_inventario (producto_id, cantidad) VALUES (%s, %s)"
            
            cursor.execute(sql_update, (cantidad, producto_id))
            cursor.execute(sql_mov, (producto_id, cantidad))
            conn.commit()
        except mysql.connector.Error as error:
            print(f"Error al registrar movimiento: {error}")
            raise
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    def generar_reporte_movimientos(self, fecha_inicio, fecha_fin):
        try:
            conn = self.conexion.get_conexion()
            cursor = conn.cursor(dictionary=True)
            sql = """
                SELECT p.nombre, p.descripcion,
                       (SELECT SUM(cantidad) FROM entradas_inventario 
                        WHERE producto_id = p.id AND fecha BETWEEN %s AND %s) as entradas,
                       (SELECT SUM(cantidad) FROM salidas_inventario 
                        WHERE producto_id = p.id AND fecha BETWEEN %s AND %s) as salidas,
                       p.cantidad_en_stock as stock_actual
                FROM productos p
            """
            cursor.execute(sql, (fecha_inicio, fecha_fin, fecha_inicio, fecha_fin))
            return cursor.fetchall()
        except mysql.connector.Error as error:
            print(f"Error al generar reporte: {error}")
            raise
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close() 