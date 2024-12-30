from DAO.conexion import Conexion
from DTO.accesorio_dto import AccesorioDTO

class AccesorioDAO:
    def __init__(self):
        self.conexion = Conexion()

    def insertar(self, accesorio_dto):
        try:
            connection = self.conexion.get_connection()
            with connection.cursor() as cursor:
                sql = """INSERT INTO accesorio (nombre, precio_dolar, especie, descripcion, 
                         stock, peso, edad_recomendada, tipo_id) 
                         VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
                valores = (accesorio_dto.nombre, accesorio_dto.precio_dolar, 
                          accesorio_dto.especie, accesorio_dto.descripcion,
                          accesorio_dto.stock, accesorio_dto.peso, 
                          accesorio_dto.edad_recomendada, accesorio_dto.tipo_id)
                cursor.execute(sql, valores)
                connection.commit()
                return cursor.lastrowid
        except Exception as e:
            print(f"Error al insertar accesorio: {e}")
            return None

    def obtener_todos(self):
        try:
            connection = self.conexion.get_connection()
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM accesorio")
                resultados = cursor.fetchall()
                return [AccesorioDTO(
                    id_accesorio=row['id_accesorio'],
                    nombre=row['nombre'],
                    precio_dolar=row['precio_dolar'],
                    especie=row['especie'],
                    descripcion=row['descripcion'],
                    stock=row['stock'],
                    peso=row['peso'],
                    edad_recomendada=row['edad_recomendada'],
                    tipo_id=row['tipo_id']
                ) for row in resultados]
        except Exception as e:
            print(f"Error al obtener accesorios: {e}")
            return []

    def obtener_por_id(self, id_accesorio):
        try:
            connection = self.conexion.get_connection()
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM accesorio WHERE id_accesorio = %s", (id_accesorio,))
                row = cursor.fetchone()
                if row:
                    return AccesorioDTO(
                        id_accesorio=row['id_accesorio'],
                        nombre=row['nombre'],
                        precio_dolar=row['precio_dolar'],
                        especie=row['especie'],
                        descripcion=row['descripcion'],
                        stock=row['stock'],
                        peso=row['peso'],
                        edad_recomendada=row['edad_recomendada'],
                        tipo_id=row['tipo_id']
                    )
                return None
        except Exception as e:
            print(f"Error al obtener accesorio: {e}")
            return None

    def obtener_por_nombre(self, nombre):
        try:
            connection = self.conexion.get_connection()
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM accesorio WHERE nombre LIKE %s", (f"%{nombre}%",))
                row = cursor.fetchone()
                if row:
                    return AccesorioDTO(
                        id_accesorio=row['id_accesorio'],
                        nombre=row['nombre'],
                        precio_dolar=row['precio_dolar'],
                        especie=row['especie'],
                        descripcion=row['descripcion'],
                        stock=row['stock'],
                        peso=row['peso'],
                        edad_recomendada=row['edad_recomendada'],
                        tipo_id=row['tipo_id']
                    )
                return None
        except Exception as e:
            print(f"Error al obtener accesorio por nombre: {e}")
            return None

    def obtener_por_rango(self, campo, valor_min, valor_max):
        try:
            connection = self.conexion.get_connection()
            with connection.cursor() as cursor:
                sql = f"SELECT * FROM accesorio WHERE {campo} BETWEEN %s AND %s"
                cursor.execute(sql, (valor_min, valor_max))
                resultados = cursor.fetchall()
                return [AccesorioDTO(
                    id_accesorio=row['id_accesorio'],
                    nombre=row['nombre'],
                    precio_dolar=row['precio_dolar'],
                    especie=row['especie'],
                    descripcion=row['descripcion'],
                    stock=row['stock'],
                    peso=row['peso'],
                    edad_recomendada=row['edad_recomendada'],
                    tipo_id=row['tipo_id']
                ) for row in resultados]
        except Exception as e:
            print(f"Error al obtener accesorios por rango: {e}")
            return []

    def actualizar(self, accesorio_dto):
        try:
            connection = self.conexion.get_connection()
            with connection.cursor() as cursor:
                sql = """UPDATE accesorio SET nombre = %s, precio_dolar = %s, 
                         especie = %s, descripcion = %s, stock = %s, 
                         peso = %s, edad_recomendada = %s, tipo_id = %s 
                         WHERE id_accesorio = %s"""
                valores = (accesorio_dto.nombre, accesorio_dto.precio_dolar,
                          accesorio_dto.especie, accesorio_dto.descripcion,
                          accesorio_dto.stock, accesorio_dto.peso,
                          accesorio_dto.edad_recomendada, accesorio_dto.tipo_id,
                          accesorio_dto.id_accesorio)
                cursor.execute(sql, valores)
                connection.commit()
                return True
        except Exception as e:
            print(f"Error al actualizar accesorio: {e}")
            return False

    def eliminar(self, id_accesorio):
        try:
            connection = self.conexion.get_connection()
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM accesorio WHERE id_accesorio = %s", (id_accesorio,))
                connection.commit()
                return True
        except Exception as e:
            print(f"Error al eliminar accesorio: {e}")
            return False