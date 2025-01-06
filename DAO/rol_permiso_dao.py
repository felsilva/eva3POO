from .conexion import Conexion
import pymysql

class RolPermisoDAO:
    def __init__(self):
        self.conexion = Conexion()

    def obtener_permisos_por_rol(self, rol):
        """Obtiene todos los permisos asociados a un rol."""
        conn = None
        try:
            conn = self.conexion.get_connection()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            sql = """SELECT permiso, descripcion 
                     FROM roles_permisos 
                     WHERE rol = %s"""
            cursor.execute(sql, (rol,))
            return cursor.fetchall()
        except pymysql.Error as error:
            print(f"Error al obtener permisos: {error}")
            raise
        finally:
            if conn and conn.open:
                cursor.close()
                conn.close()

    def verificar_permiso(self, rol, permiso):
        """Verifica si un rol tiene un permiso específico."""
        conn = None
        try:
            conn = self.conexion.get_connection()
            cursor = conn.cursor()
            sql = """SELECT COUNT(*) 
                     FROM roles_permisos 
                     WHERE rol = %s AND permiso = %s"""
            cursor.execute(sql, (rol, permiso))
            resultado = cursor.fetchone()
            return resultado[0] > 0
        except pymysql.Error as error:
            print(f"Error al verificar permiso: {error}")
            raise
        finally:
            if conn and conn.open:
                cursor.close()
                conn.close()

    def agregar_permiso(self, rol, permiso, descripcion=None):
        """Agrega un nuevo permiso a un rol."""
        conn = None
        try:
            conn = self.conexion.get_connection()
            cursor = conn.cursor()
            sql = """INSERT INTO roles_permisos (rol, permiso, descripcion) 
                     VALUES (%s, %s, %s)"""
            cursor.execute(sql, (rol, permiso, descripcion))
            conn.commit()
        except pymysql.Error as error:
            print(f"Error al agregar permiso: {error}")
            raise
        finally:
            if conn and conn.open:
                cursor.close()
                conn.close()

    def eliminar_permiso(self, rol, permiso):
        """Elimina un permiso de un rol."""
        conn = None
        try:
            conn = self.conexion.get_connection()
            cursor = conn.cursor()
            sql = "DELETE FROM roles_permisos WHERE rol = %s AND permiso = %s"
            cursor.execute(sql, (rol, permiso))
            conn.commit()
        except pymysql.Error as error:
            print(f"Error al eliminar permiso: {error}")
            raise
        finally:
            if conn and conn.open:
                cursor.close()
                conn.close()

    def listar_todos_permisos(self):
        """Lista todos los permisos existentes agrupados por rol."""
        conn = None
        try:
            conn = self.conexion.get_connection()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            sql = """SELECT rol, GROUP_CONCAT(permiso) as permisos 
                     FROM roles_permisos 
                     GROUP BY rol"""
            cursor.execute(sql)
            return cursor.fetchall()
        except pymysql.Error as error:
            print(f"Error al listar permisos: {error}")
            raise
        finally:
            if conn and conn.open:
                cursor.close()
                conn.close() 