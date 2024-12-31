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
            return bcrypt.hashpw(password.encode('utf-8'), salt)
        except Exception as e:
            logging.error(f"Error al hashear contraseña: {str(e)}")
            raise ValueError("Error al procesar la contraseña")

    def _verificar_password(self, password, password_hash):
        """Verifica si la contraseña coincide con el hash."""
        try:
            if not password or not password_hash:
                return False
            return bcrypt.checkpw(
                password.encode('utf-8'),
                password_hash.encode('utf-8') if isinstance(password_hash, str) else password_hash
            )
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
            
            sql = """INSERT INTO usuarios (username, password_hash, nombre, apellido, 
                     email, rol) VALUES (%s, %s, %s, %s, %s, %s)"""
            valores = (
                usuario_dto.username,
                password_hash.decode('utf-8'),
                usuario_dto.nombre,
                usuario_dto.apellido,
                usuario_dto.email,
                usuario_dto.rol
            )
            
            cursor.execute(sql, valores)
            conn.commit()
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
            return None

        conn = None
        try:
            conn = self.conexion.get_connection()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            
            sql = """SELECT id, username, password_hash, nombre, apellido, email, rol 
                     FROM usuarios WHERE username = %s"""
            cursor.execute(sql, (username,))
            usuario_data = cursor.fetchone()
            
            if not usuario_data:
                logging.warning(f"Usuario no encontrado: {username}")
                return None

            if not self._verificar_password(password, usuario_data['password_hash']):
                logging.warning(f"Contraseña incorrecta para usuario: {username}")
                return None

            # No enviamos el password_hash al DTO por seguridad
            usuario_data['password_hash'] = None
            return UsuarioDTO(**usuario_data)

        except pymysql.Error as error:
            logging.error(f"Error al validar credenciales: {str(error)}")
            raise
        except Exception as e:
            logging.error(f"Error inesperado al validar credenciales: {str(e)}")
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
            
            # Verificar la contraseña actual
            sql = "SELECT password_hash FROM usuarios WHERE id = %s"
            cursor.execute(sql, (id_usuario,))
            usuario_data = cursor.fetchone()
            
            if not usuario_data:
                raise ValueError("Usuario no encontrado")

            if not self._verificar_password(password_actual, usuario_data['password_hash']):
                raise ValueError("La contraseña actual es incorrecta")
            
            # Hashear y guardar la nueva contraseña
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
 