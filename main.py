"""
Sistema de Gestión de Inventario Santa Clara
------------------------------------------
Este sistema resuelve la gestión de inventarios mediante:
- Control en tiempo real del stock
- Automatización de procesos de entrada/salida
- Alertas de stock bajo
- Generación de reportes de movimientos
- Gestión completa de productos
- Autenticación segura de usuarios

Desarrollado utilizando el patrón DAO/DTO.
"""

from datetime import datetime
from servicios.reporte_service import ReporteService
from DAO.producto_dao import ProductoDAO
from DAO.usuario_dao import UsuarioDAO
from DTO.producto_dto import ProductoDTO
from DTO.usuario_dto import UsuarioDTO
import getpass
import re

def validar_entrada_numerica(prompt, tipo='float'):
    """Valida y obtiene una entrada numérica del usuario."""
    while True:
        try:
            valor = input(prompt)
            if not valor.strip():
                return None
            return int(valor) if tipo == 'int' else float(valor)
        except ValueError:
            print("Error: Por favor ingrese un valor numérico válido.")

def validar_fecha(fecha_str):
    """Valida el formato de fecha ingresado."""
    try:
        return datetime.strptime(fecha_str, '%Y-%m-%d').strftime('%Y-%m-%d')
    except ValueError:
        raise ValueError("Formato de fecha inválido. Use YYYY-MM-DD")

def mostrar_menu_autenticacion():
    """Muestra el menú de autenticación."""
    print("\n=== SISTEMA DE GESTIÓN DE INVENTARIO SANTA CLARA ===")
    print("1. Iniciar Sesión")
    print("2. Registrar Usuario")
    print("0. Salir")
    return input("Seleccione una opción: ")

def registrar_usuario(usuario_dao):
    """Registra un nuevo usuario en el sistema."""
    print("\n=== REGISTRO DE USUARIO ===")
    try:
        username = input("Nombre de usuario (mínimo 4 caracteres): ").strip()
        if len(username) < 4:
            print("El nombre de usuario debe tener al menos 4 caracteres.")
            return None

        # Usar getpass para ocultar la contraseña
        password = getpass.getpass("Contraseña (mínimo 8 caracteres): ")
        if len(password) < 8:
            print("La contraseña debe tener al menos 8 caracteres.")
            return None

        confirm_password = getpass.getpass("Confirme la contraseña: ")
        if password != confirm_password:
            print("Las contraseñas no coinciden.")
            return None

        nombre = input("Nombre: ").strip()
        apellido = input("Apellido: ").strip()
        
        email = input("Email: ").strip()
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            print("El email no tiene un formato válido.")
            return None

        print("\nSeleccione el rol:")
        print("1. Usuario")
        print("2. Administrador")
        rol_opcion = input("Opción (1/2): ").strip()
        
        rol = 'usuario' if rol_opcion == '1' else 'admin' if rol_opcion == '2' else None
        if not rol:
            print("Rol no válido.")
            return None

        usuario_dto = UsuarioDTO(
            username=username,
            password=password,
            nombre=nombre,
            apellido=apellido,
            email=email,
            rol=rol
        )

        usuario_dao.crear(usuario_dto)
        print("\nUsuario registrado exitosamente!")
        return True

    except ValueError as e:
        print(f"Error de validación: {str(e)}")
        return None
    except Exception as e:
        print(f"Error al registrar usuario: {str(e)}")
        return None

def iniciar_sesion(usuario_dao):
    """Inicia sesión en el sistema."""
    print("\n=== INICIO DE SESIÓN ===")
    try:
        username = input("Usuario: ").strip()
        password = getpass.getpass("Contraseña: ")

        usuario = usuario_dao.validar_credenciales(username, password)
        if usuario:
            print(f"\n¡Bienvenido {usuario.nombre} {usuario.apellido}!")
            return usuario
        else:
            print("Credenciales inválidas.")
            return None
    except Exception as e:
        print(f"Error al iniciar sesión: {str(e)}")
        return None

def mostrar_menu():
    """Muestra el menú principal del sistema."""
    print("\n=== SISTEMA DE GESTIÓN DE INVENTARIO SANTA CLARA ===")
    print("1. Gestionar Productos")
    print("2. Registrar Entrada de Inventario")
    print("3. Registrar Salida de Inventario")
    print("4. Verificar Stock Bajo")
    print("5. Generar Reportes")
    print("6. Cambiar Contraseña")
    print("0. Cerrar Sesión")
    return input("Seleccione una opción: ")

def cambiar_password(usuario_dao, usuario_actual):
    """Permite al usuario cambiar su contraseña."""
    print("\n=== CAMBIO DE CONTRASEÑA ===")
    try:
        password_actual = getpass.getpass("Contraseña actual: ")
        nueva_password = getpass.getpass("Nueva contraseña (mínimo 8 caracteres): ")
        
        if len(nueva_password) < 8:
            print("La nueva contraseña debe tener al menos 8 caracteres.")
            return False
            
        confirmar_password = getpass.getpass("Confirme la nueva contraseña: ")
        
        if nueva_password != confirmar_password:
            print("Las contraseñas no coinciden.")
            return False
            
        if usuario_dao.cambiar_password(usuario_actual.id, password_actual, nueva_password):
            print("Contraseña cambiada exitosamente!")
            return True
        return False
    except ValueError as e:
        print(f"Error: {str(e)}")
        return False
    except Exception as e:
        print(f"Error al cambiar la contraseña: {str(e)}")
        return False

def menu_productos(producto_dao):
    """Gestiona las operaciones relacionadas con productos."""
    while True:
        try:
            print("\n=== GESTIÓN DE PRODUCTOS ===")
            print("1. Listar productos")
            print("2. Agregar producto")
            print("3. Actualizar producto")
            print("4. Volver al menú principal")
            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                productos = producto_dao.listar_todos()
                if not productos:
                    print("No hay productos registrados.")
                    continue
                print("\n=== LISTA DE PRODUCTOS ===")
                print("ID | Nombre | Stock | Precio")
                print("-" * 50)
                for p in productos:
                    print(f"{p.id:2d} | {p.nombre[:20]:20} | {p.cantidad_en_stock:5d} | ${p.precio:8.2f}")
            
            elif opcion == "2":
                nombre = input("Nombre del producto: ").strip()
                if not nombre:
                    print("El nombre es obligatorio.")
                    continue
                descripcion = input("Descripción: ")
                precio = validar_entrada_numerica("Precio: ")
                if precio is None or precio <= 0:
                    print("El precio debe ser mayor que 0.")
                    continue
                stock = validar_entrada_numerica("Stock inicial: ", 'int')
                if stock is None or stock < 0:
                    print("El stock no puede ser negativo.")
                    continue
                
                producto_dto = ProductoDTO(
                    nombre=nombre,
                    descripcion=descripcion,
                    precio=precio,
                    cantidad_en_stock=stock
                )
                producto_dao.crear(producto_dto)
                print("Producto creado exitosamente!")
            
            elif opcion == "3":
                id_producto = validar_entrada_numerica("ID del producto a actualizar: ", 'int')
                if id_producto is None:
                    continue
                producto = producto_dao.obtener_por_id(id_producto)
                if producto:
                    nombre = input(f"Nombre ({producto.nombre}): ").strip()
                    if nombre:
                        producto.nombre = nombre
                    descripcion = input(f"Descripción ({producto.descripcion}): ")
                    if descripcion:
                        producto.descripcion = descripcion
                    precio = validar_entrada_numerica(f"Precio ({producto.precio}): ")
                    if precio is not None and precio > 0:
                        producto.precio = precio
                    producto_dao.actualizar(producto)
                    print("Producto actualizado exitosamente!")
                else:
                    print("Producto no encontrado!")
            
            elif opcion == "4":
                break
                
        except Exception as e:
            print(f"Error: {str(e)}")
            print("Por favor, intente nuevamente.")

def menu_reportes(reporte_service):
    """Gestiona la generación de reportes."""
    while True:
        try:
            print("\n=== GENERACIÓN DE REPORTES ===")
            print("1. Simular Reporte Excel")
            print("2. Simular Reporte PDF")
            print("3. Volver al menú principal")
            opcion = input("Seleccione una opción: ")

            if opcion in ["1", "2"]:
                fecha_inicio = input("Fecha inicio (YYYY-MM-DD): ")
                fecha_fin = input("Fecha fin (YYYY-MM-DD): ")
                
                fecha_inicio = validar_fecha(fecha_inicio)
                fecha_fin = validar_fecha(fecha_fin)
                
                if datetime.strptime(fecha_inicio, '%Y-%m-%d') > datetime.strptime(fecha_fin, '%Y-%m-%d'):
                    print("La fecha de inicio debe ser anterior a la fecha fin.")
                    continue
                
                if opcion == "1":
                    reporte_service.simular_reporte_excel(fecha_inicio, fecha_fin)
                else:
                    reporte_service.simular_reporte_pdf(fecha_inicio, fecha_fin)
            
            elif opcion == "3":
                break
                
        except ValueError as ve:
            print(f"Error: {str(ve)}")
        except Exception as e:
            print(f"Error inesperado: {str(e)}")

def main():
    """Función principal que inicia el sistema."""
    usuario_dao = UsuarioDAO()
    producto_dao = ProductoDAO()
    reporte_service = ReporteService()
    
    while True:
        opcion = mostrar_menu_autenticacion()
        
        if opcion == "1":
            usuario_actual = iniciar_sesion(usuario_dao)
            if usuario_actual:
                # Menú principal
                while True:
                    try:
                        opcion = mostrar_menu()
                        
                        if opcion == "1":
                            menu_productos(producto_dao)
                        
                        elif opcion == "2":
                            id_producto = validar_entrada_numerica("ID del producto: ", 'int')
                            if id_producto is None:
                                continue
                            cantidad = validar_entrada_numerica("Cantidad a ingresar: ", 'int')
                            if cantidad is None or cantidad <= 0:
                                print("La cantidad debe ser mayor que 0.")
                                continue
                            producto_dao.registrar_movimiento(id_producto, cantidad, "entrada")
                            print("Entrada registrada exitosamente!")
                        
                        elif opcion == "3":
                            id_producto = validar_entrada_numerica("ID del producto: ", 'int')
                            if id_producto is None:
                                continue
                            cantidad = validar_entrada_numerica("Cantidad a retirar: ", 'int')
                            if cantidad is None or cantidad <= 0:
                                print("La cantidad debe ser mayor que 0.")
                                continue
                            producto_dao.registrar_movimiento(id_producto, cantidad, "salida")
                            print("Salida registrada exitosamente!")
                        
                        elif opcion == "4":
                            productos_bajo_stock = producto_dao.verificar_stock_bajo()
                            if not productos_bajo_stock:
                                print("\nNo hay productos con stock bajo.")
                                continue
                            print("\n=== PRODUCTOS CON STOCK BAJO ===")
                            print("Producto | Stock Actual | Nivel de Alerta")
                            print("-" * 50)
                            for p in productos_bajo_stock:
                                print(f"{p['nombre'][:20]:20} | {p['cantidad_en_stock']:12d} | {p['nivel_alerta']:14d}")
                        
                        elif opcion == "5":
                            menu_reportes(reporte_service)
                        
                        elif opcion == "6":
                            cambiar_password(usuario_dao, usuario_actual)
                        
                        elif opcion == "0":
                            print("Sesión cerrada.")
                            break
                        
                        else:
                            print("Opción no válida. Por favor, intente nuevamente.")
                    
                    except Exception as e:
                        print(f"Error inesperado: {str(e)}")
                        print("Por favor, intente nuevamente.")
        
        elif opcion == "2":
            registrar_usuario(usuario_dao)
        
        elif opcion == "0":
            print("¡Gracias por usar el sistema!")
            break
        
        else:
            print("Opción no válida. Por favor, intente nuevamente.")

if __name__ == "__main__":
    main() 