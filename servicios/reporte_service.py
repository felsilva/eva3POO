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
            return "No hay datos para mostrar en el período seleccionado."

        # Definir anchos de columnas
        anchos = {
            'nombre': 25,
            'categoria': 15,
            'entradas': 10,
            'salidas': 10,
            'stock': 10,
            'precio': 15,
            'valor_mov': 20,
            'valor': 20
        }

        # Crear líneas de la tabla
        linea = "+" + "-"*(anchos['nombre']+2) + "+" + \
                "-"*(anchos['categoria']+2) + "+" + \
                "-"*(anchos['entradas']+2) + "+" + \
                "-"*(anchos['salidas']+2) + "+" + \
                "-"*(anchos['stock']+2) + "+" + \
                "-"*(anchos['precio']+2) + "+" + \
                "-"*(anchos['valor_mov']+2) + "+" + \
                "-"*(anchos['valor']+2) + "+"

        # Crear encabezados
        headers = ["Producto", "Categoría", "Entradas", "Salidas", "Stock", "Precio Unit.", "Valor Movs.", "Valor Total"]
        header_row = "|" + headers[0].center(anchos['nombre']+2) + "|" + \
                    headers[1].center(anchos['categoria']+2) + "|" + \
                    headers[2].center(anchos['entradas']+2) + "|" + \
                    headers[3].center(anchos['salidas']+2) + "|" + \
                    headers[4].center(anchos['stock']+2) + "|" + \
                    headers[5].center(anchos['precio']+2) + "|" + \
                    headers[6].center(anchos['valor_mov']+2) + "|" + \
                    headers[7].center(anchos['valor']+2) + "|"

        # Formatear filas
        rows = []
        total_valor = 0
        total_movimientos = 0
        for item in datos:
            nombre = item['nombre'][:anchos['nombre']]
            categoria = (item['categoria'] or 'Sin categoría')[:anchos['categoria']]
            entradas = str(item['entradas'])
            salidas = str(item['salidas'])
            stock = int(item['stock_actual'])
            precio = float(item['precio_actual'])
            valor_movimientos = float(item['valor_entradas']) + float(item['valor_salidas'])
            # Calcular el valor total como stock * precio
            valor_total = stock * precio
            
            total_valor += valor_total
            total_movimientos += valor_movimientos
            
            row = "|" + nombre.ljust(anchos['nombre']+2) + "|" + \
                  categoria.center(anchos['categoria']+2) + "|" + \
                  entradas.center(anchos['entradas']+2) + "|" + \
                  salidas.center(anchos['salidas']+2) + "|" + \
                  str(stock).center(anchos['stock']+2) + "|" + \
                  f"${precio:,.0f}".rjust(anchos['precio']+2) + "|" + \
                  f"${valor_movimientos:,.0f}".rjust(anchos['valor_mov']+2) + "|" + \
                  f"${valor_total:,.0f}".rjust(anchos['valor']+2) + "|"
            rows.append(row)

        # Agregar fila de totales
        total_row = "|" + "TOTAL INVENTARIO".ljust(anchos['nombre']+2) + "|" + \
                   "".center(anchos['categoria']+2) + "|" + \
                   "".center(anchos['entradas']+2) + "|" + \
                   "".center(anchos['salidas']+2) + "|" + \
                   "".center(anchos['stock']+2) + "|" + \
                   "".center(anchos['precio']+2) + "|" + \
                   f"${total_movimientos:,.0f}".rjust(anchos['valor_mov']+2) + "|" + \
                   f"${total_valor:,.0f}".rjust(anchos['valor']+2) + "|"

        # Agregar resumen
        resumen = [
            "",
            "Resumen del reporte:",
            f"- Valor total de movimientos: ${total_movimientos:,.0f}",
            f"- Valor total del inventario: ${total_valor:,.0f}"
        ]

        # Unir todas las partes
        tabla = [
            linea,
            header_row,
            linea,
            *rows,
            linea,
            total_row,
            linea,
            *resumen
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

    def verificar_fechas_disponibles(self):
        """Verifica las fechas disponibles para reportes."""
        try:
            fechas = self.producto_dao.verificar_fechas_movimientos()
            print("\n=== FECHAS DISPONIBLES PARA REPORTES ===")
            print(f"Primera fecha de movimiento: {fechas['primera_fecha']}")
            print(f"Última fecha de movimiento: {fechas['ultima_fecha']}")
            print("\nUse estas fechas como referencia para generar sus reportes.")
            return fechas
        except Exception as e:
            print(f"Error al verificar fechas disponibles: {e}")
            return None 