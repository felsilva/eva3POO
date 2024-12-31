import bcrypt

def generar_hash_password(password):
    """Genera un hash bcrypt para una contraseña."""
    salt = bcrypt.gensalt()
    password_hash = bcrypt.hashpw(password.encode('utf-8'), salt)
    return password_hash.decode('utf-8')

if __name__ == "__main__":
    password = "admin123"  # La contraseña que queremos hashear
    hash_resultado = generar_hash_password(password)
    print(f"Hash generado para '{password}':")
    print(hash_resultado)
    
    # Verificar que el hash funciona
    verificacion = bcrypt.checkpw(
        password.encode('utf-8'),
        hash_resultado.encode('utf-8')
    )
    print(f"\nVerificación exitosa: {verificacion}") 