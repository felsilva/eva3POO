from DAO.conexion import Conexion
from DTO.tipo_dto import TipoDTO

class TipoDAO:
    def __init__(self):
        self.conexion = Conexion()

    def insertar(self, tipo_dto):
        try:
            connection = self.conexion.get_connection()
            with connection.cursor() as cursor:
                sql = "INSERT INTO tipo (nombre, descripcion) VALUES (%s, %s)"
                valores = (tipo_dto.nombre, tipo_dto.descripcion)
                cursor.execute(sql, valores)
                connection.commit()
                return cursor.lastrowid
        except Exception as e:
            print(f"Error al insertar tipo: {e}")
            return None

    def obtener_todos(self):
        try:
            connection = self.conexion.get_connection()
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM tipo")
                resultados = cursor.fetchall()
                return [TipoDTO(
                    id_tipo=row['id_tipo'],
                    nombre=row['nombre'],
                    descripcion=row['descripcion']
                ) for row in resultados]
        except Exception as e:
            print(f"Error al obtener tipos: {e}")
            return []

    def obtener_por_id(self, id_tipo):
        try:
            connection = self.conexion.get_connection()
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM tipo WHERE id_tipo = %s", (id_tipo,))
                row = cursor.fetchone()
                if row:
                    return TipoDTO(
                        id_tipo=row['id_tipo'],
                        nombre=row['nombre'],
                        descripcion=row['descripcion']
                    )
                return None
        except Exception as e:
            print(f"Error al obtener tipo: {e}")
            return None

    def actualizar(self, tipo_dto):
        try:
            connection = self.conexion.get_connection()
            with connection.cursor() as cursor:
                sql = "UPDATE tipo SET nombre = %s, descripcion = %s WHERE id_tipo = %s"
                valores = (tipo_dto.nombre, tipo_dto.descripcion, tipo_dto.id_tipo)
                cursor.execute(sql, valores)
                connection.commit()
                return True
        except Exception as e:
            print(f"Error al actualizar tipo: {e}")
            return False

    def eliminar(self, id_tipo):
        try:
            connection = self.conexion.get_connection()
            with connection.cursor() as cursor:
                sql = "DELETE FROM tipo WHERE id_tipo = %s"
                cursor.execute(sql, (id_tipo,))
                connection.commit()
                return True
        except Exception as e:
            print(f"Error al eliminar tipo: {e}")
            return False 