from datetime import datetime
from DAO.producto_dao import ProductoDAO

class ReporteService:
    def __init__(self):
        self.producto_dao = ProductoDAO()

    def simular_reporte_excel(self, fecha_inicio, fecha_fin):
        try:
            datos = self.producto_dao.generar_reporte_movimientos(fecha_inicio, fecha_fin)
            print("\n=== SIMULACIÓN DE REPORTE EXCEL ===")
            print(f"Fecha de generación: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"Período: {fecha_inicio} - {fecha_fin}")
            print("\nProducto | Entradas | Salidas | Stock Actual")
            print("-" * 50)
            for item in datos:
                print(f"{item['nombre'][:20]:<20} | {item['entradas'] or 0:^8} | {item['salidas'] or 0:^7} | {item['stock_actual']:^12}")
            print("\nSimulación de archivo Excel guardado exitosamente!")
            return True
        except Exception as e:
            print(f"Error al generar simulación de Excel: {e}")
            return False

    def simular_reporte_pdf(self, fecha_inicio, fecha_fin):
        try:
            datos = self.producto_dao.generar_reporte_movimientos(fecha_inicio, fecha_fin)
            print("\n=== SIMULACIÓN DE REPORTE PDF ===")
            print("+" + "="*50 + "+")
            print("|" + "REPORTE DE MOVIMIENTOS DE INVENTARIO".center(50) + "|")
            print("|" + f"Período: {fecha_inicio} - {fecha_fin}".center(50) + "|")
            print("+" + "="*50 + "+")
            print("|" + "Producto".center(20) + "|" + "Entradas".center(9) + "|" + "Salidas".center(9) + "|" + "Stock".center(8) + "|")
            print("+" + "-"*50 + "+")
            
            for item in datos:
                nombre = item['nombre'][:18].ljust(20)
                entradas = str(item['entradas'] or 0).center(9)
                salidas = str(item['salidas'] or 0).center(9)
                stock = str(item['stock_actual']).center(8)
                print(f"|{nombre}|{entradas}|{salidas}|{stock}|")
            
            print("+" + "-"*50 + "+")
            print("\nSimulación de archivo PDF guardado exitosamente!")
            return True
        except Exception as e:
            print(f"Error al generar simulación de PDF: {e}")
            return False 