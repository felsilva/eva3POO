import bcrypt
from DAO.conexion import Conexion
from DTO.usuario_dto import UsuarioDTO

class UsuarioDAO:
    def __init__(self):
        self.conexion = Conexion()

    def registrar(self, usuario_dto):
        try:
            connection = self.conexion.get_connection()
            with connection.cursor() as cursor:
                # Verificar si el usuario ya existe
                cursor.execute("SELECT username FROM usuarios WHERE username = %s", (usuario_dto.username,))
                if cursor.fetchone():
                    print("El nombre de usuario ya existe")
                    return None

                # Generar hash de la contraseña
                salt = bcrypt.gensalt()
                password_hash = bcrypt.hashpw(usuario_dto.password_hash.encode('utf-8'), salt)
                
                sql = """INSERT INTO usuarios (username, password_hash, nombres, apellidos, 
                         email, tipo_usuario) VALUES (%s, %s, %s, %s, %s, %s)"""
                valores = (usuario_dto.username, password_hash.decode('utf-8'),
                          usuario_dto.nombres, usuario_dto.apellidos,
                          usuario_dto.email, usuario_dto.tipo_usuario.lower())
                cursor.execute(sql, valores)
                connection.commit()
                return cursor.lastrowid
        except Exception as e:
            print(f"Error al registrar usuario: {e}")
            return None

    def validar_credenciales(self, username, password):
        try:
            connection = self.conexion.get_connection()
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM usuarios WHERE username = %s", (username,))
                row = cursor.fetchone()
                
                if row:
                    stored_password = row['password_hash'].encode('utf-8')
                    if bcrypt.checkpw(password.encode('utf-8'), stored_password):
                        # Imprimir para debug
                        print(f"Tipo de usuario en la base de datos: '{row['tipo_usuario']}'")
                        
                        return UsuarioDTO(
                            username=row['username'],
                            password_hash=None,
                            nombres=row['nombres'],
                            apellidos=row['apellidos'],
                            email=row['email'],
                            tipo_usuario=row['tipo_usuario'].lower()
                        )
                return None
        except Exception as e:
            print(f"Error al validar credenciales: {e}")
            return None

    def obtener_por_username(self, username):
        try:
            connection = self.conexion.get_connection()
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM usuarios WHERE username = %s", (username,))
                row = cursor.fetchone()
                if row:
                    return UsuarioDTO(
                        username=row['username'],
                        password_hash=None,
                        nombres=row['nombres'],
                        apellidos=row['apellidos'],
                        email=row['email'],
                        tipo_usuario=row['tipo_usuario'].lower()
                    )
                return None
        except Exception as e:
            print(f"Error al obtener usuario: {e}")
            return None
 