from datetime import datetime
from servicios.reporte_service import ReporteService
from DAO.producto_dao import ProductoDAO
from DTO.producto_dto import ProductoDTO

def mostrar_menu():
    print("\n=== SISTEMA DE GESTIÓN DE INVENTARIO SANTA CLARA ===")
    print("1. Gestionar Productos")
    print("2. Registrar Entrada de Inventario")
    print("3. Registrar Salida de Inventario")
    print("4. Verificar Stock Bajo")
    print("5. Generar Reportes")
    print("0. Salir")
    return input("Seleccione una opción: ")

def menu_productos(producto_dao):
    while True:
        print("\n=== GESTIÓN DE PRODUCTOS ===")
        print("1. Listar productos")
        print("2. Agregar producto")
        print("3. Actualizar producto")
        print("4. Volver al menú principal")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            productos = producto_dao.listar_todos()
            print("\n=== LISTA DE PRODUCTOS ===")
            for p in productos:
                print(f"ID: {p.id} | Nombre: {p.nombre} | Stock: {p.cantidad_en_stock} | Precio: ${p.precio}")
        
        elif opcion == "2":
            nombre = input("Nombre del producto: ")
            descripcion = input("Descripción: ")
            precio = float(input("Precio: "))
            stock = int(input("Stock inicial: "))
            producto_dto = ProductoDTO(nombre=nombre, descripcion=descripcion, 
                                    precio=precio, cantidad_en_stock=stock)
            producto_dao.crear(producto_dto)
            print("Producto creado exitosamente!")
        
        elif opcion == "3":
            id_producto = int(input("ID del producto a actualizar: "))
            producto = producto_dao.obtener_por_id(id_producto)
            if producto:
                producto.nombre = input(f"Nombre ({producto.nombre}): ") or producto.nombre
                producto.descripcion = input(f"Descripción ({producto.descripcion}): ") or producto.descripcion
                producto.precio = float(input(f"Precio ({producto.precio}): ") or producto.precio)
                producto_dao.actualizar(producto)
                print("Producto actualizado exitosamente!")
            else:
                print("Producto no encontrado!")
        
        elif opcion == "4":
            break

def menu_reportes(reporte_service):
    while True:
        print("\n=== GENERACIÓN DE REPORTES ===")
        print("1. Simular Reporte Excel")
        print("2. Simular Reporte PDF")
        print("3. Volver al menú principal")
        opcion = input("Seleccione una opción: ")

        if opcion in ["1", "2"]:
            fecha_inicio = input("Fecha inicio (YYYY-MM-DD): ")
            fecha_fin = input("Fecha fin (YYYY-MM-DD): ")
            
            if opcion == "1":
                reporte_service.simular_reporte_excel(fecha_inicio, fecha_fin)
            else:
                reporte_service.simular_reporte_pdf(fecha_inicio, fecha_fin)
        
        elif opcion == "3":
            break

def main():
    producto_dao = ProductoDAO()
    reporte_service = ReporteService()

    while True:
        opcion = mostrar_menu()
        
        if opcion == "1":
            menu_productos(producto_dao)
        
        elif opcion == "2":
            id_producto = int(input("ID del producto: "))
            cantidad = int(input("Cantidad a ingresar: "))
            producto_dao.registrar_movimiento(id_producto, cantidad, "entrada")
            print("Entrada registrada exitosamente!")
        
        elif opcion == "3":
            id_producto = int(input("ID del producto: "))
            cantidad = int(input("Cantidad a retirar: "))
            producto_dao.registrar_movimiento(id_producto, cantidad, "salida")
            print("Salida registrada exitosamente!")
        
        elif opcion == "4":
            productos_bajo_stock = producto_dao.verificar_stock_bajo()
            print("\n=== PRODUCTOS CON STOCK BAJO ===")
            for p in productos_bajo_stock:
                print(f"Producto: {p['nombre']} | Stock actual: {p['cantidad_en_stock']} | Nivel de alerta: {p['nivel_alerta']}")
        
        elif opcion == "5":
            menu_reportes(reporte_service)
        
        elif opcion == "0":
            print("¡Gracias por usar el sistema!")
            break

if __name__ == "__main__":
    main() 