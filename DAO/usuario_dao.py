"""
DAO para la entidad Usuario.
Implementa operaciones de base de datos y seguridad para usuarios.
"""

import bcrypt
from .conexion import Conexion
import pymysql
from DTO.usuario_dto import UsuarioDTO
import logging

class UsuarioDAO:
    def __init__(self):
        self.conexion = Conexion()

    def _hashear_password(self, password):
        """Genera un hash seguro para la contraseña."""
        try:
            salt = bcrypt.gensalt()
            password_bytes = password.encode('utf-8')
            hashed = bcrypt.hashpw(password_bytes, salt)
            logging.debug(f"Password hasheado exitosamente")
            return hashed
        except Exception as e:
            logging.error(f"Error al hashear contraseña: {str(e)}")
            raise ValueError("Error al procesar la contraseña")

    def _verificar_password(self, password_plano, password_hash):
        """Verifica si la contraseña coincide con el hash."""
        try:
            # Asegurar que ambos sean strings antes de codificar
            if not isinstance(password_plano, str) or not isinstance(password_hash, str):
                logging.error("Tipo de dato incorrecto para password o hash")
                return False

            # Convertir a bytes
            password_bytes = password_plano.encode('utf-8')
            hash_bytes = password_hash.encode('utf-8')

            logging.debug(f"Verificando contraseña...")
            resultado = bcrypt.checkpw(password_bytes, hash_bytes)
            logging.debug(f"Resultado de verificación: {resultado}")
            
            return resultado
        except Exception as e:
            logging.error(f"Error al verificar contraseña: {str(e)}")
            return False

    def crear(self, usuario_dto):
        """Crea un nuevo usuario en la base de datos."""
        if not usuario_dto.password:
            raise ValueError("La contraseña es obligatoria")

        conn = None
        try:
            conn = self.conexion.get_connection()
            cursor = conn.cursor()
            
            # Verificar si el usuario ya existe
            cursor.execute(
                "SELECT id FROM usuarios WHERE username = %s OR email = %s", 
                (usuario_dto.username, usuario_dto.email)
            )
            if cursor.fetchone():
                raise ValueError("El nombre de usuario o email ya está en uso")

            # Hashear la contraseña
            password_hash = self._hashear_password(usuario_dto.password)
            hash_str = password_hash.decode('utf-8')
            
            logging.debug(f"Hash generado para nuevo usuario: {hash_str}")
            
            # Insertar el nuevo usuario
            sql = """INSERT INTO usuarios (username, password_hash, nombre, apellido, 
                     email, rol) VALUES (%s, %s, %s, %s, %s, %s)"""
            valores = (
                usuario_dto.username,
                hash_str,
                usuario_dto.nombre,
                usuario_dto.apellido,
                usuario_dto.email,
                usuario_dto.rol
            )
            
            cursor.execute(sql, valores)
            conn.commit()
            
            logging.info(f"Usuario creado exitosamente: {usuario_dto.username}")
            return cursor.lastrowid
        except pymysql.Error as error:
            logging.error(f"Error al crear usuario: {str(error)}")
            raise
        finally:
            if conn and conn.open:
                cursor.close()
                conn.close()

    def validar_credenciales(self, username, password):
        """Valida las credenciales del usuario."""
        if not username or not password:
            logging.warning("Username o password vacíos")
            return None

        conn = None
        try:
            conn = self.conexion.get_connection()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            
            # Obtener el usuario por username
            sql = """SELECT id, username, password_hash, nombre, apellido, email, rol 
                     FROM usuarios WHERE username = %s"""
            cursor.execute(sql, (username,))
            usuario_data = cursor.fetchone()
            
            if not usuario_data:
                logging.warning(f"Usuario no encontrado: {username}")
                return None

            logging.debug(f"Usuario encontrado: {username}")
            logging.debug(f"Hash almacenado: {usuario_data['password_hash']}")

            # Verificar la contraseña
            es_valida = self._verificar_password(password, usuario_data['password_hash'])
            
            if not es_valida:
                logging.warning(f"Contraseña incorrecta para usuario: {username}")
                return None

            logging.info(f"Login exitoso para usuario: {username}")
            
            # No enviamos el password_hash al DTO por seguridad
            usuario_data['password_hash'] = None
            return UsuarioDTO(**usuario_data)

        except pymysql.Error as error:
            logging.error(f"Error al validar credenciales: {str(error)}")
            raise
        finally:
            if conn and conn.open:
                cursor.close()
                conn.close()

    def obtener_por_id(self, id_usuario):
        """Obtiene un usuario por su ID."""
        conn = None
        try:
            conn = self.conexion.get_connection()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            
            sql = """SELECT id, username, nombre, apellido, email, rol 
                     FROM usuarios WHERE id = %s"""
            cursor.execute(sql, (id_usuario,))
            usuario_data = cursor.fetchone()
            
            return UsuarioDTO(**usuario_data) if usuario_data else None
        except pymysql.Error as error:
            logging.error(f"Error al obtener usuario: {str(error)}")
            raise
        finally:
            if conn and conn.open:
                cursor.close()
                conn.close()

    def cambiar_password(self, id_usuario, password_actual, nueva_password):
        """Cambia la contraseña de un usuario."""
        conn = None
        try:
            conn = self.conexion.get_connection()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            
            # Obtener el hash actual
            sql = "SELECT password_hash FROM usuarios WHERE id = %s"
            cursor.execute(sql, (id_usuario,))
            usuario_data = cursor.fetchone()
            
            if not usuario_data:
                raise ValueError("Usuario no encontrado")

            # Verificar la contraseña actual
            if not self._verificar_password(password_actual, usuario_data['password_hash']):
                return False
            
            # Generar el nuevo hash y actualizar
            nuevo_hash = self._hashear_password(nueva_password)
            sql_update = "UPDATE usuarios SET password_hash = %s WHERE id = %s"
            cursor.execute(sql_update, (nuevo_hash.decode('utf-8'), id_usuario))
            conn.commit()
            return True
        except pymysql.Error as error:
            logging.error(f"Error al cambiar contraseña: {str(error)}")
            raise
        finally:
            if conn and conn.open:
                cursor.close()
                conn.close()
 