import re
import requests
from DTO.usuario_dto import UsuarioDTO
from DTO.accesorio_dto import AccesorioDTO
from DTO.tipo_dto import TipoDTO
from DAO.usuario_dao import UsuarioDAO
from DAO.accesorio_dao import AccesorioDAO
from DAO.tipo_dao import TipoDAO

def validar_email(email):
    return '@' in email and '.' in email

def validar_password(password):
    return len(password) >= 8

def validar_campos_vacios(*campos):
    return all(campo.strip() for campo in campos)

def mostrar_menu_principal():
    print("="*60)
    print("MENÚ USUARIOS - TALCA PETS".center(60))
    print("="*60)
    print("1.- INICIAR SESIÓN")
    print("2.- REGISTRAR USUARIO")
    print("3.- SALIR")
    print("="*60)

def mostrar_menu_mantenedor():
    print("="*60)
    print("MANTENEDOR DE ACCESORIOS PARA MASCOTA".center(60))
    print("="*60)
    print("1.- (I) INGRESAR ACCESORIO")
    print("2.- (R) MOSTRAR ACCESORIOS")
    print("3.- (U) MODIFICAR ACCESORIO")
    print("4.- (D) ELIMINAR ACCESORIO")
    print("5.- (C) GESTIONAR CATEGORÍAS DE ACCESORIOS")
    print("6.- (E) SALIR")
    print("="*60)

def mostrar_menu_mostrar():
    print("="*40)
    print("MENÚ MOSTRAR".center(40))
    print("="*40)
    print("1.- MOSTRAR LOS ACCESORIOS")
    print("2.- MOSTRAR UN ACCESORIO")
    print("3.- MOSTRAR PARCIAL")
    print("4.- VOLVER")
    print("="*40)

def obtener_precio_dolar():
    try:
        response = requests.get('https://mindicador.cl/api')
        if response.status_code == 200:
            data = response.json()
            return data['dolar']['valor']
        return None
    except Exception as e:
        print(f"Error al obtener el precio del dólar: {e}")
        return None

def convertir_a_dolares(pesos):
    valor_dolar = obtener_precio_dolar()
    if valor_dolar:
        return round(pesos / valor_dolar, 2)
    return None

def registrar_usuario():
    try:
        print("\nREGISTRO DE USUARIO")
        print("="*30)
        username = input("Ingrese nombre de usuario: ")
        password = input("Ingrese contraseña: ")
        nombres = input("Ingrese nombres: ")
        apellidos = input("Ingrese apellidos: ")
        email = input("Ingrese email: ")
        
        print("\nTipo de usuario:")
        print("1.- Cliente")
        print("2.- Administrador")
        tipo_opcion = input("Seleccione (1/2): ")
        
        if not validar_campos_vacios(username, password, nombres, apellidos, email):
            print("Todos los campos son obligatorios")
            return False
            
        if not validar_email(email):
            print("El email debe contener '@' y '.'")
            return False
            
        if not validar_password(password):
            print("La contraseña debe tener al menos 8 caracteres")
            return False
        
        tipo_usuario = 'cliente' if tipo_opcion == '1' else 'admin'
        
        nuevo_usuario = UsuarioDTO(
            username=username,
            password_hash=password,
            nombres=nombres,
            apellidos=apellidos,
            email=email,
            tipo_usuario=tipo_usuario
        )
        
        usuario_dao = UsuarioDAO()
        if usuario_dao.registrar(nuevo_usuario):
            print(f"\nUsuario registrado exitosamente como {tipo_usuario}")
            return True
        else:
            print("\nError al registrar usuario")
            return False
            
    except Exception as e:
        print(f"\nError en el registro: {e}")
        return False

def iniciar_sesion():
    username = input("Ingrese su nombre de usuario: ")
    password = input("Ingrese su contraseña: ")
    
    usuario_dao = UsuarioDAO()
    usuario = usuario_dao.validar_credenciales(username, password)
    
    if usuario:
        print(f"\nBienvenido {usuario.nombres} {usuario.apellidos}")
        print(f"Tipo de usuario: '{usuario.tipo_usuario}'")
        
        if usuario.tipo_usuario.lower() != 'admin':
            print("No tiene permisos de administrador para acceder al mantenedor.")
            return None
        return usuario
    else:
        print("\nCredenciales inválidas")
        return None

def ingresar_accesorio():
    accesorio_dao = AccesorioDAO()
    tipo_dao = TipoDAO()
    
    # Primero mostramos los tipos disponibles
    print("\nCategorías de accesorios disponibles:")
    print("-" * 40)
    tipos = tipo_dao.obtener_todos()
    if not tipos:
        print("No hay categorías de accesorios registradas. Debe registrar al menos una categoría primero.")
        return
    
    for tipo in tipos:
        print(f"ID: {tipo.id_tipo} - {tipo.nombre}")
    print("-" * 40)
    
    print("\nINGRESO DE ACCESORIO")
    print("-" * 20)
    
    nombre = input("Nombre del accesorio: ")
    
    while True:
        try:
            precio_pesos = float(input("Precio en pesos chilenos: "))
            break
        except ValueError:
            print("Por favor, ingrese un número válido")
    
    precio_dolar = convertir_a_dolares(precio_pesos)
    if not precio_dolar:
        print("Error al convertir el precio. Intente más tarde.")
        return
    
    especie = input("Especie: ")
    descripcion = input("Descripción: ")
    
    while True:
        try:
            stock = int(input("Stock: "))
            break
        except ValueError:
            print("Por favor, ingrese un número entero válido")
    
    while True:
        try:
            peso = float(input("Peso: "))
            break
        except ValueError:
            print("Por favor, ingrese un número válido")
    
    edad_recomendada = input("Edad recomendada: ")
    
    # Validación del tipo_id
    while True:
        try:
            tipo_id = int(input("ID de la categoría (de la lista mostrada arriba): "))
            # Verificar si el tipo existe
            tipo_seleccionado = tipo_dao.obtener_por_id(tipo_id)
            if tipo_seleccionado:
                break
            else:
                print("El ID de categoría seleccionado no existe. Por favor, elija uno de la lista.")
        except ValueError:
            print("Por favor, ingrese un número válido")
    
    accesorio = AccesorioDTO(
        id_accesorio=None,
        nombre=nombre,
        precio_dolar=precio_dolar,
        especie=especie,
        descripcion=descripcion,
        stock=stock,
        peso=peso,
        edad_recomendada=edad_recomendada,
        tipo_id=tipo_id
    )
    
    if accesorio_dao.insertar(accesorio):
        print("\nAccesorio registrado exitosamente.")
    else:
        print("\nError al registrar accesorio.")

def mostrar_accesorios():
    while True:
        mostrar_menu_mostrar()
        opcion = input("Ingrese una opción: ")
        accesorio_dao = AccesorioDAO()
        
        if opcion == "1":
            accesorios = accesorio_dao.obtener_todos()
            if accesorios:
                print("\nListado de Accesorios:")
                print("=" * 60)
                print("ID  |  Nombre  |  Precio USD  |  Stock")
                print("=" * 60)
                for accesorio in accesorios:
                    print(f"{accesorio.id_accesorio}  |  {accesorio.nombre}  |  ${accesorio.precio_dolar}  |  {accesorio.stock}")
                print("=" * 60)
            else:
                print("No hay accesorios registrados.")
                
        elif opcion == "2":
            buscar = input("Buscar por (1-ID, 2-Nombre): ")
            if buscar == "1":
                try:
                    id_accesorio = int(input("ID del accesorio: "))
                    accesorio = accesorio_dao.obtener_por_id(id_accesorio)
                except ValueError:
                    print("Por favor, ingrese un número válido")
                    continue
            else:
                nombre = input("Nombre del accesorio: ")
                accesorio = accesorio_dao.obtener_por_nombre(nombre)
                
            if accesorio:
                print("\nDetalles del accesorio:")
                print("=" * 60)
                print(f"ID: {accesorio.id_accesorio}")
                print(f"Nombre: {accesorio.nombre}")
                print(f"Precio USD: ${accesorio.precio_dolar}")
                print(f"Especie: {accesorio.especie}")
                print(f"Descripción: {accesorio.descripcion}")
                print(f"Stock: {accesorio.stock}")
                print(f"Peso: {accesorio.peso}")
                print(f"Edad recomendada: {accesorio.edad_recomendada}")
                print("=" * 60)
            else:
                print("Accesorio no encontrado.")
                
        elif opcion == "3":
            print("\nFiltrar por:")
            print("-" * 20)
            print("1.- Precio")
            print("2.- Stock")
            print("3.- Edad recomendada")
            print("-" * 20)
            filtro = input("Seleccione: ")
            
            campos = {
                "1": "precio_dolar",
                "2": "stock",
                "3": "edad_recomendada"
            }
            
            if filtro in campos:
                try:
                    min_val = float(input("Valor mínimo: "))
                    max_val = float(input("Valor máximo: "))
                    accesorios = accesorio_dao.obtener_por_rango(campos[filtro], min_val, max_val)
                    
                    if accesorios:
                        print("\nAccesorios encontrados:")
                        print("=" * 60)
                        print("ID  |  Nombre  |  Precio USD  |  Stock")
                        print("=" * 60)
                        for accesorio in accesorios:
                            print(f"{accesorio.id_accesorio}  |  {accesorio.nombre}  |  ${accesorio.precio_dolar}  |  {accesorio.stock}")
                        print("=" * 60)
                    else:
                        print("No se encontraron accesorios en ese rango.")
                except ValueError:
                    print("Por favor, ingrese valores numéricos válidos")
            else:
                print("Opción no válida.")
                
        elif opcion == "4":
            break
        else:
            print("Opción no válida.")

def modificar_accesorio():
    accesorio_dao = AccesorioDAO()
    
    id_accesorio = int(input("ID del accesorio a modificar: "))
    accesorio = accesorio_dao.obtener_por_id(id_accesorio)
    
    if not accesorio:
        print("Accesorio no encontrado.")
        return
    
    print("\nDeje en blanco para mantener el valor actual")
    
    nombre = input(f"Nombre [{accesorio.nombre}]: ") or accesorio.nombre
    
    precio_actual_pesos = accesorio.precio_dolar * obtener_precio_dolar()
    precio_str = input(f"Precio en pesos [{precio_actual_pesos}]: ")
    if precio_str:
        precio_dolar = convertir_a_dolares(float(precio_str))
    else:
        precio_dolar = accesorio.precio_dolar
    
    especie = input(f"Especie [{accesorio.especie}]: ") or accesorio.especie
    descripcion = input(f"Descripción [{accesorio.descripcion}]: ") or accesorio.descripcion
    stock_str = input(f"Stock [{accesorio.stock}]: ")
    stock = int(stock_str) if stock_str else accesorio.stock
    peso_str = input(f"Peso [{accesorio.peso}]: ")
    peso = float(peso_str) if peso_str else accesorio.peso
    edad = input(f"Edad recomendada [{accesorio.edad_recomendada}]: ") or accesorio.edad_recomendada
    
    accesorio_actualizado = AccesorioDTO(
        id_accesorio, nombre, precio_dolar, especie, descripcion,
        stock, peso, edad, accesorio.tipo_id
    )
    
    if accesorio_dao.actualizar(accesorio_actualizado):
        print("Accesorio actualizado exitosamente.")
    else:
        print("Error al actualizar accesorio.")

def eliminar_accesorio():
    accesorio_dao = AccesorioDAO()
    
    # Mostrar accesorios disponibles
    accesorios = accesorio_dao.obtener_todos()
    if not accesorios:
        print("No hay accesorios registrados para eliminar.")
        return
        
    print("\nAccesorios disponibles:")
    print("=" * 60)
    print("ID  |  Nombre  |  Precio USD  |  Stock")
    print("=" * 60)
    for accesorio in accesorios:
        print(f"{accesorio.id_accesorio}  |  {accesorio.nombre}  |  ${accesorio.precio_dolar}  |  {accesorio.stock}")
    print("=" * 60)
    
    try:
        id_accesorio = int(input("\nID del accesorio a eliminar: "))
        accesorio = accesorio_dao.obtener_por_id(id_accesorio)
        
        if not accesorio:
            print("Accesorio no encontrado.")
            return
        
        print("\nDatos del accesorio a eliminar:")
        print("-" * 40)
        print(f"Nombre: {accesorio.nombre}")
        print(f"Precio USD: ${accesorio.precio_dolar}")
        print(f"Stock: {accesorio.stock}")
        print("-" * 40)
        
        confirmacion = input("¿Está seguro de eliminar este accesorio? (s/n): ")
        if confirmacion.lower() == 's':
            if accesorio_dao.eliminar(id_accesorio):
                print("Accesorio eliminado exitosamente.")
            else:
                print("Error al eliminar accesorio.")
        else:
            print("Operación cancelada.")
    except ValueError:
        print("Por favor, ingrese un ID válido.")

def mostrar_menu_tipos():
    print("="*60)
    print("GESTIÓN DE CATEGORÍAS DE ACCESORIOS".center(60))
    print("="*60)
    print("1.- AGREGAR CATEGORÍA")
    print("2.- MOSTRAR CATEGORÍAS")
    print("3.- ACTUALIZAR CATEGORÍA")
    print("4.- ELIMINAR CATEGORÍA")
    print("5.- VOLVER")
    print("="*60)

def ingresar_tipo():
    print("\nINGRESO DE TIPO")
    print("-" * 20)
    
    nombre = input("Nombre del tipo: ")
    descripcion = input("Descripción: ")
    
    tipo_dto = TipoDTO(
        id_tipo=None,
        nombre=nombre,
        descripcion=descripcion
    )
    
    tipo_dao = TipoDAO()
    if tipo_dao.insertar(tipo_dto):
        print("\nTipo registrado exitosamente.")
    else:
        print("\nError al registrar tipo.")

def mostrar_tipos():
    tipo_dao = TipoDAO()
    tipos = tipo_dao.obtener_todos()
    
    if tipos:
        print("\nTipos registrados:")
        print("-" * 40)
        for tipo in tipos:
            print(f"ID: {tipo.id_tipo}")
            print(f"Nombre: {tipo.nombre}")
            print(f"Descripción: {tipo.descripcion}")
            print("-" * 40)
    else:
        print("No hay tipos registrados.")

def gestionar_tipos():
    tipo_dao = TipoDAO()
    while True:
        mostrar_menu_tipos()
        opcion = input("Ingrese una opción: ")
        
        if opcion == "1":
            nombre = input("Nombre de la categoría: ")
            descripcion = input("Descripción: ")
            
            if not validar_campos_vacios(nombre, descripcion):
                print("Los campos no pueden estar vacíos")
                continue
                
            tipo = TipoDTO(None, nombre, descripcion)
            if tipo_dao.insertar(tipo):
                print("Categoría agregada exitosamente")
            else:
                print("Error al agregar categoría")
                
        elif opcion == "2":
            tipos = tipo_dao.obtener_todos()
            if tipos:
                print("\nCategorías disponibles:")
                print("-" * 40)
                for tipo in tipos:
                    print(f"ID: {tipo.id_tipo} - Nombre: {tipo.nombre}")
                    print(f"Descripción: {tipo.descripcion}")
                    print("-" * 40)
            else:
                print("No hay categorías registradas")
                
        elif opcion == "3":
            tipos = tipo_dao.obtener_todos()
            if not tipos:
                print("No hay categorías registradas para actualizar.")
                continue
                
            print("\nCategorías disponibles:")
            print("-" * 40)
            for tipo in tipos:
                print(f"ID: {tipo.id_tipo} - Nombre: {tipo.nombre}")
            print("-" * 40)
            
            try:
                id_tipo = int(input("ID de la categoría a actualizar: "))
                tipo = tipo_dao.obtener_por_id(id_tipo)
                if tipo:
                    nombre = input("Nuevo nombre (Enter para mantener actual): ")
                    descripcion = input("Nueva descripción (Enter para mantener actual): ")
                    
                    if nombre.strip():
                        tipo.nombre = nombre
                    if descripcion.strip():
                        tipo.descripcion = descripcion
                        
                    if tipo_dao.actualizar(tipo):
                        print("Categoría actualizada exitosamente")
                    else:
                        print("Error al actualizar categoría")
                else:
                    print("Categoría no encontrada")
            except ValueError:
                print("ID inválido")
                
        elif opcion == "4":
            tipos = tipo_dao.obtener_todos()
            if not tipos:
                print("No hay categorías registradas para eliminar.")
                continue
                
            print("\nCategorías disponibles:")
            print("-" * 40)
            for tipo in tipos:
                print(f"ID: {tipo.id_tipo} - Nombre: {tipo.nombre}")
            print("-" * 40)
            
            try:
                id_tipo = int(input("ID de la categoría a eliminar: "))
                tipo = tipo_dao.obtener_por_id(id_tipo)
                
                if not tipo:
                    print("Categoría no encontrada.")
                    continue
                    
                print("\nDatos de la categoría a eliminar:")
                print("-" * 40)
                print(f"Nombre: {tipo.nombre}")
                print(f"Descripción: {tipo.descripcion}")
                print("-" * 40)
                
                confirmacion = input("¿Está seguro de eliminar esta categoría? (s/n): ")
                if confirmacion.lower() == 's':
                    if tipo_dao.eliminar(id_tipo):
                        print("Categoría eliminada exitosamente")
                    else:
                        print("Error al eliminar categoría")
                else:
                    print("Operación cancelada")
            except ValueError:
                print("ID inválido")
                
        elif opcion == "5":
            break
        else:
            print("Opción inválida")

def menu_mantenedor():
    while True:
        mostrar_menu_mantenedor()
        opcion = input("Ingrese una opción: ")
        
        if opcion == "1":
            ingresar_accesorio()
        elif opcion == "2":
            mostrar_accesorios()
        elif opcion == "3":
            modificar_accesorio()
        elif opcion == "4":
            eliminar_accesorio()
        elif opcion == "5":
            gestionar_tipos()
        elif opcion == "6":
            break
        else:
            print("Opción no válida.")

def main():
    while True:
        mostrar_menu_principal()
        opcion = input("Ingrese una opción: ")
        
        if opcion == "1":
            usuario = iniciar_sesion()
            if usuario and usuario.tipo_usuario.lower() == 'admin':
                menu_mantenedor()
                
        elif opcion == "2":
            registrar_usuario()
            
        elif opcion == "3":
            print("\nGracias por usar el sistema")
            break
        else:
            print("\nOpción inválida")

if __name__ == "__main__":
    main() 