import pymysql
import logging

class Conexion:
    def __init__(self):
        # Configuración de la base de datos
        self.host = 'localhost'
        self.user = 'root'
        self.password = 'Inacap@2024.'  # Asegúrate de que esta sea tu contraseña
        self.database = 'santa_clara_mantenedor_db'
        self.charset = 'utf8mb4'
        self.port = 3306
        self.connect_timeout = 5

    def get_connection(self):
        """Obtiene una conexión a la base de datos."""
        try:
            connection = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                charset=self.charset,
                port=self.port,
                connect_timeout=self.connect_timeout,
                cursorclass=pymysql.cursors.DictCursor,
                autocommit=True
            )
            return connection
        except pymysql.Error as e:
            error_msg = f"Error de conexión MySQL ({e.args[0]}): {e.args[1]}"
            logging.error(error_msg)
            raise Exception(error_msg)
        except Exception as e:
            error_msg = f"Error inesperado al conectar: {str(e)}"
            logging.error(error_msg)
            raise Exception(error_msg)

    def test_connection(self):
        """Prueba la conexión a la base de datos."""
        connection = None
        try:
            connection = self.get_connection()
            with connection.cursor() as cursor:
                cursor.execute("SELECT VERSION()")
                version = cursor.fetchone()
                print(f"\nConexión exitosa a MySQL:")
                print(f"Versión del servidor: {version['VERSION()']}")
                return True
        except Exception as e:
            print("\nError de conexión:")
            print(f"- Mensaje: {str(e)}")
            print("\nVerifique que:")
            print("1. El servidor MySQL esté en ejecución")
            print(f"2. El usuario '{self.user}' tenga acceso desde '{self.host}'")
            print(f"3. La base de datos '{self.database}' exista")
            print("4. La contraseña sea correcta")
            return False
        finally:
            if connection and connection.open:
                connection.close()

    def execute_query(self, query, params=None):
        """Ejecuta una consulta SQL y maneja los errores."""
        connection = None
        try:
            connection = self.get_connection()
            with connection.cursor() as cursor:
                cursor.execute(query, params)
                return cursor.fetchall()
        except pymysql.Error as e:
            error_msg = f"Error en la consulta ({e.args[0]}): {e.args[1]}\nQuery: {query}"
            logging.error(error_msg)
            raise Exception(error_msg)
        finally:
            if connection and connection.open:
                connection.close()

    def execute_update(self, query, params=None):
        """Ejecuta una actualización SQL y maneja los errores."""
        connection = None
        try:
            connection = self.get_connection()
            with connection.cursor() as cursor:
                cursor.execute(query, params)
                connection.commit()
                return cursor.rowcount
        except pymysql.Error as e:
            if connection:
                connection.rollback()
            error_msg = f"Error en la actualización ({e.args[0]}): {e.args[1]}\nQuery: {query}"
            logging.error(error_msg)
            raise Exception(error_msg)
        finally:
            if connection and connection.open:
                connection.close() 