"""
Servicio de Reportes para el Sistema de Gestión de Inventario.
Proporciona funcionalidades para generar reportes en diferentes formatos.
"""

from datetime import datetime
from DAO.producto_dao import ProductoDAO

class ReporteService:
    def __init__(self):
        self.producto_dao = ProductoDAO()

    def _formatear_tabla(self, datos, formato='normal'):
        """Formatea los datos en una tabla con bordes."""
        if not datos:
            return "No hay datos para mostrar."

        # Definir anchos de columnas
        anchos = {
            'nombre': 25,
            'entradas': 10,
            'salidas': 10,
            'stock': 10,
            'valor': 12
        }

        # Crear líneas de la tabla
        linea_superior = "+" + "-"*(anchos['nombre']+2) + "+" + \
                        "-"*(anchos['entradas']+2) + "+" + \
                        "-"*(anchos['salidas']+2) + "+" + \
                        "-"*(anchos['stock']+2) + "+" + \
                        "-"*(anchos['valor']+2) + "+"

        # Crear encabezados
        headers = ["Producto", "Entradas", "Salidas", "Stock", "Valor Total"]
        header_row = "|" + headers[0].center(anchos['nombre']+2) + "|" + \
                    headers[1].center(anchos['entradas']+2) + "|" + \
                    headers[2].center(anchos['salidas']+2) + "|" + \
                    headers[3].center(anchos['stock']+2) + "|" + \
                    headers[4].center(anchos['valor']+2) + "|"

        # Formatear filas
        rows = []
        total_valor = 0
        for item in datos:
            nombre = item['nombre'][:anchos['nombre']]
            entradas = str(item['entradas'] or 0)
            salidas = str(item['salidas'] or 0)
            stock = str(item['stock_actual'])
            valor = item['stock_actual'] * item.get('precio', 0)
            total_valor += valor
            
            row = "|" + nombre.ljust(anchos['nombre']+2) + "|" + \
                  entradas.center(anchos['entradas']+2) + "|" + \
                  salidas.center(anchos['salidas']+2) + "|" + \
                  stock.center(anchos['stock']+2) + "|" + \
                  f"${valor:,.2f}".rjust(anchos['valor']+2) + "|"
            rows.append(row)

        # Agregar fila de totales
        total_row = "|" + "TOTAL".ljust(anchos['nombre']+2) + "|" + \
                   "".center(anchos['entradas']+2) + "|" + \
                   "".center(anchos['salidas']+2) + "|" + \
                   "".center(anchos['stock']+2) + "|" + \
                   f"${total_valor:,.2f}".rjust(anchos['valor']+2) + "|"

        # Unir todas las partes
        tabla = [
            linea_superior,
            header_row,
            linea_superior,
            *rows,
            linea_superior,
            total_row,
            linea_superior
        ]

        return "\n".join(tabla)

    def simular_reporte_excel(self, fecha_inicio, fecha_fin):
        """Simula la generación de un reporte en formato Excel."""
        try:
            datos = self.producto_dao.generar_reporte_movimientos(fecha_inicio, fecha_fin)
            
            print("\n=== REPORTE DE MOVIMIENTOS DE INVENTARIO ===")
            print(f"Formato: Excel")
            print(f"Fecha de generación: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"Período: {fecha_inicio} - {fecha_fin}")
            print("\n" + self._formatear_tabla(datos, 'excel'))
            print("\nSimulación de archivo Excel guardado exitosamente!")
            return True
        except Exception as e:
            print(f"Error al generar simulación de Excel: {e}")
            return False

    def simular_reporte_pdf(self, fecha_inicio, fecha_fin):
        """Simula la generación de un reporte en formato PDF."""
        try:
            datos = self.producto_dao.generar_reporte_movimientos(fecha_inicio, fecha_fin)
            
            print("\n=== REPORTE DE MOVIMIENTOS DE INVENTARIO ===")
            print(f"Formato: PDF")
            print(f"Fecha de generación: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"Período: {fecha_inicio} - {fecha_fin}")
            print("\n" + self._formatear_tabla(datos, 'pdf'))
            
            # Agregar pie de página
            print("\nNotas:")
            print("- Los valores están expresados en pesos.")
            print("- El stock actual representa el inventario al momento de la generación del reporte")
            print("- Las entradas y salidas corresponden al período especificado")
            
            print("\nSimulación de archivo PDF guardado exitosamente!")
            return True
        except Exception as e:
            print(f"Error al generar simulación de PDF: {e}")
            return False

    def generar_reporte_alertas(self):
        """Genera un reporte de productos con alertas de stock bajo."""
        try:
            productos_bajo_stock = self.producto_dao.verificar_stock_bajo()
            
            print("\n=== REPORTE DE ALERTAS DE STOCK ===")
            print(f"Fecha de generación: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            if not productos_bajo_stock:
                print("\nNo hay productos con alertas de stock bajo.")
                return True
            
            print("\nProductos que requieren reposición:")
            print("-" * 60)
            for p in productos_bajo_stock:
                print(f"Producto: {p['nombre']}")
                print(f"Stock actual: {p['cantidad_en_stock']}")
                print(f"Nivel de alerta: {p['nivel_alerta']}")
                print(f"Déficit: {p['nivel_alerta'] - p['cantidad_en_stock']}")
                print("-" * 60)
            
            return True
        except Exception as e:
            print(f"Error al generar reporte de alertas: {e}")
            return False 