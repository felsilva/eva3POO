"""
DTO para la entidad Usuario.
Implementa validaciones y métodos de utilidad para el manejo de usuarios.
"""

import re

class UsuarioDTO:
    def __init__(self, id=None, username=None, password=None, nombre=None, 
                 apellido=None, email=None, rol=None, password_hash=None):
        self._id = id
        self._username = username
        self._password = password
        self._nombre = nombre
        self._apellido = apellido
        self._email = email
        self._rol = rol
        self._password_hash = password_hash
        self.validar()

    @property
    def id(self):
        return self._id

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, valor):
        if not valor or not valor.strip():
            raise ValueError("El nombre de usuario no puede estar vacío")
        if len(valor) < 4:
            raise ValueError("El nombre de usuario debe tener al menos 4 caracteres")
        self._username = valor.strip()

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, valor):
        if valor and len(valor) < 8:
            raise ValueError("La contraseña debe tener al menos 8 caracteres")
        self._password = valor

    @property
    def password_hash(self):
        return self._password_hash

    @password_hash.setter
    def password_hash(self, valor):
        self._password_hash = valor

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        if valor and not valor.strip():
            raise ValueError("El nombre no puede estar vacío")
        self._nombre = valor.strip() if valor else None

    @property
    def apellido(self):
        return self._apellido

    @apellido.setter
    def apellido(self, valor):
        if valor and not valor.strip():
            raise ValueError("El apellido no puede estar vacío")
        self._apellido = valor.strip() if valor else None

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, valor):
        if valor:
            if not re.match(r"[^@]+@[^@]+\.[^@]+", valor.strip()):
                raise ValueError("El email no tiene un formato válido")
            self._email = valor.strip()
        else:
            self._email = None

    @property
    def rol(self):
        return self._rol

    @rol.setter
    def rol(self, valor):
        roles_validos = ['admin', 'usuario']
        if valor and valor.lower() not in roles_validos:
            raise ValueError(f"Rol no válido. Debe ser uno de: {', '.join(roles_validos)}")
        self._rol = valor.lower() if valor else None

    def validar(self):
        """Valida que los datos del usuario sean correctos."""
        if self._username is not None:
            self.username = self._username
        if self._password is not None:
            self.password = self._password
        if self._nombre is not None:
            self.nombre = self._nombre
        if self._apellido is not None:
            self.apellido = self._apellido
        if self._email is not None:
            self.email = self._email
        if self._rol is not None:
            self.rol = self._rol

    def to_dict(self):
        """Convierte el DTO a un diccionario."""
        return {
            'id': self._id,
            'username': self._username,
            'nombre': self._nombre,
            'apellido': self._apellido,
            'email': self._email,
            'rol': self._rol,
            'password_hash': self._password_hash
        }

    def __str__(self):
        """Representación en string del usuario."""
        return f"Usuario(id={self._id}, username='{self._username}', nombre='{self._nombre}', rol='{self._rol}')" 