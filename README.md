# Proyecto evaluación 3 asignatura programación orientada a objetos segura 
## Integrantes:
- José González 
- Victor Mondaca
- Felipe Silva

# Tema 3: App para tienda de accesorios para mascotas Talca Pets

## Descripción
Aplicación computacional en Python para gestionar una tienda virtual de venta de productos para mascota llamada **Comercial Santa Clara**. Los usuarios pueden agregar, visualizar, actualizar y eliminar información sobre los accesorios para mascotas.

## Requisitos del Sistema
- Python 3.8 o superior
- MySQL 8.0 o superior
- Conexión a Internet (para obtener el precio del dólar)

## Instalación

1. Clonar el repositorio:
```bash
git clone [URL_DEL_REPOSITORIO]
cd [NOMBRE_DEL_DIRECTORIO]
```

2. Crear un entorno virtual e activarlo:
```bash
python -m venv venv
source venv/bin/activate  # En Linux/Mac
venv\Scripts\activate     # En Windows
```
# Dependencias Principales 

- **pymysql**: Para conexión con MySQL
- **bcrypt**: Para manejar encriptación de datos
- **requests**: Para realizar solicitudes HTTP y tener acceso a APIs
- **progressbar2**: Para simular barra de carga (NO ES OBLIGATORIA)

3. Instalar las dependencias:
```bash
pip install -r requirements.txt
```


4. Configurar la base de datos:
- Crear una base de datos MySQL
- Ejecutar el script `database.sql` para crear las tablas necesarias
- Modificar las credenciales de conexión en `DAO/conexion.py` según tu configuración

## Estructura del Proyecto

```
.
├── DAO/                    # Data Access Objects
│   ├── conexion.py        # Conexión a la base de datos
│   ├── accesorio_dao.py   # Operaciones CRUD para accesorios
│   ├── tipo_dao.py        # Operaciones CRUD para tipos
│   └── usuario_dao.py     # Operaciones CRUD para usuarios
├── DTO/                    # Data Transfer Objects
│   ├── accesorio_dto.py   # Modelo de accesorio
│   ├── tipo_dto.py        # Modelo de tipo
│   └── usuario_dto.py     # Modelo de usuario
├── database.sql           # Script de creación de base de datos
├── requirements.txt       # Dependencias del proyecto
└── main.py               # Punto de entrada de la aplicación
```

## Uso

1. Ejecutar la aplicación:
```bash
python main.py
```

2. Registrar un usuario nuevo o iniciar sesión si ya tiene una cuenta.

3. Una vez autenticado, podrá:
   - Ingresar nuevos accesorios
   - Mostrar accesorios existentes
   - Modificar accesorios
   - Eliminar accesorios

### Funcionalidades Principales

1. **Gestión de Usuarios**
   - Registro de nuevos usuarios
   - Inicio de sesión seguro con contraseñas hasheadas

2. **Gestión de Accesorios**
   - Agregar nuevos accesorios con conversión automática de precios (CLP a USD)
   - Visualizar todos los accesorios
   - Buscar accesorios por ID o nombre
   - Filtrar accesorios por rango de precio, stock o edad recomendada
   - Modificar información de accesorios existentes
   - Eliminar accesorios

3. **Características Especiales**
   - Conversión automática de precios de CLP a USD usando API de indicadores financieros
   - Interfaz de usuario amigable con menús claros
   - Validación de datos de entrada
   - Manejo seguro de contraseñas con bcrypt

## Tablas de la Base de Datos

### **tipo**
- `id_tipo` (PK)
- `nombre`
- `descripcion`

### **accesorio**
- `id_accesorio` (PK)
- `nombre`
- `precio_dolar`
- `especie`
- `descripcion`
- `stock`
- `peso`
- `edad_recomendada`
- `tipo_id` (FK)

### **usuarios**
- `id_usuario` (PK)
- `username` (UNIQUE)
- `password_hash`
- `nombres`
- `apellidos`
- `email`
- `tipo_usuario`
- `fecha_registro`

## Reglas de Negocio
- Un accesorio pertenece a un tipo
- Un tipo está asociado a muchos accesorios
- Los precios se ingresan en pesos chilenos y se convierten automáticamente a dólares
- Las contraseñas se almacenan de forma segura usando bcrypt

## Notas Importantes
- Los nombres de las tablas están en minúsculas y sin acentos
- El campo `password_hash` es VARCHAR(120) para almacenar el hash de la contraseña
- Se requiere conexión a Internet para obtener el precio del dólar en tiempo real


