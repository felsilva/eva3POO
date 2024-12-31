# Sistema de Gestión de Inventario Santa Clara

## Descripción
Sistema de gestión de inventario desarrollado para automatizar y optimizar el control de stock, movimientos de productos y generación de reportes. Implementa una arquitectura DAO/DTO con autenticación segura y manejo eficiente de datos.

## Características Principales
- Control en tiempo real del inventario
- Gestión de entradas y salidas de productos
- Sistema de alertas para stock bajo
- Generación de reportes en múltiples formatos
- Autenticación segura con bcrypt
- Control de acceso basado en roles
- Interfaz de consola intuitiva

## Requisitos del Sistema
- Python 3.8 o superior
- MySQL 5.7 o superior
- Dependencias Python (ver requirements.txt)

## Instalación

1. Clonar el repositorio:
```bash
git clone [URL_DEL_REPOSITORIO]
cd sistema-inventario
```

2. Crear y activar entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Configurar la base de datos:
- Crear una base de datos MySQL
- Ejecutar el script `database.sql`
- Configurar las credenciales en el archivo de conexión

## Estructura del Proyecto
```
sistema-inventario/
├── DAO/                    # Capa de acceso a datos
│   ├── conexion.py        # Gestión de conexiones a BD
│   ├── producto_dao.py    # Operaciones CRUD productos
│   └── usuario_dao.py     # Gestión de usuarios
├── DTO/                    # Objetos de transferencia de datos
│   ├── producto_dto.py    # DTO de productos
│   └── usuario_dto.py     # DTO de usuarios
├── servicios/             # Lógica de negocio
│   └── reporte_service.py # Generación de reportes
├── database.sql           # Esquema de la base de datos
├── main.py               # Punto de entrada
└── requirements.txt      # Dependencias del proyecto
```

## Funcionalidades

### Gestión de Usuarios
- Registro de nuevos usuarios
- Autenticación segura con contraseñas hasheadas
- Roles de usuario (admin/usuario)
- Cambio de contraseñas
- Validaciones de datos

### Gestión de Productos
- Alta, baja y modificación de productos
- Control de stock
- Registro de entradas y salidas
- Historial de movimientos
- Alertas de stock bajo

### Reportes
- Generación de reportes de movimientos
- Exportación simulada a Excel y PDF
- Filtros por fecha
- Totales y resúmenes

## Seguridad
- Contraseñas hasheadas con bcrypt
- Validación de datos de entrada
- Control de acceso por roles
- Protección contra SQL injection
- Manejo seguro de sesiones

## Base de Datos
El sistema utiliza MySQL con las siguientes tablas principales:
- usuarios: Gestión de usuarios y autenticación
- productos: Catálogo de productos
- entradas_inventario: Registro de entradas
- salidas_inventario: Registro de salidas
- alertas_inventario: Configuración de alertas

## Uso del Sistema

### Inicio de Sesión
```bash
python main.py
```
1. Seleccionar "Iniciar Sesión"
2. Ingresar credenciales

### Registro de Usuario
1. Seleccionar "Registrar Usuario"
2. Completar información requerida:
   - Nombre de usuario (mín. 4 caracteres)
   - Contraseña (mín. 8 caracteres)
   - Datos personales
   - Rol (admin/usuario)

### Operaciones Principales
1. Gestión de Productos
   - Listar productos
   - Agregar producto
   - Actualizar producto
2. Movimientos de Inventario
   - Registrar entradas
   - Registrar salidas
3. Control de Stock
   - Verificar stock bajo
   - Alertas automáticas
4. Reportes
   - Generar reportes por período
   - Visualizar en diferentes formatos

## Contribución
Para contribuir al proyecto:
1. Fork del repositorio
2. Crear rama para nueva funcionalidad
3. Commit con mensajes descriptivos
4. Push a la rama
5. Crear Pull Request

## Licencia
Este proyecto está bajo la Licencia MIT. Ver archivo LICENSE para más detalles.


