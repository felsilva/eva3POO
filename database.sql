-- Crear la base de datos
DROP DATABASE IF EXISTS santa_clara_mantenedor_db;
CREATE DATABASE santa_clara_mantenedor_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE santa_clara_mantenedor_db;

-- Tablas base (sin dependencias)
CREATE TABLE usuarios (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    nombre VARCHAR(100),
    apellido VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    rol ENUM('admin', 'usuario') NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

CREATE TABLE roles_permisos (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    rol VARCHAR(50) NOT NULL,
    permiso VARCHAR(100) NOT NULL,
    descripcion TEXT,
    UNIQUE KEY uk_rol_permiso (rol, permiso)
) ENGINE=InnoDB;

CREATE TABLE categorias_productos (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    descripcion TEXT
) ENGINE=InnoDB;

CREATE TABLE productos (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    descripcion TEXT,
    precio DECIMAL(10, 2) NOT NULL,
    cantidad_en_stock INT NOT NULL DEFAULT 0,
    categoria_id BIGINT,
    CONSTRAINT fk_producto_categoria 
    FOREIGN KEY (categoria_id) REFERENCES categorias_productos(id)
    ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE proveedores (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    contacto VARCHAR(255),
    direccion TEXT,
    telefono VARCHAR(20),
    email VARCHAR(100)
) ENGINE=InnoDB;

-- Tablas con dependencias
CREATE TABLE entradas_inventario (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    producto_id BIGINT NOT NULL,
    cantidad INT NOT NULL,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usuario_id BIGINT NOT NULL,
    proveedor_id BIGINT,
    precio_unitario DECIMAL(10, 2),
    CONSTRAINT fk_entrada_producto FOREIGN KEY (producto_id) 
        REFERENCES productos(id) ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_entrada_usuario FOREIGN KEY (usuario_id) 
        REFERENCES usuarios(id) ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_entrada_proveedor FOREIGN KEY (proveedor_id)
        REFERENCES proveedores(id) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE salidas_inventario (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    producto_id BIGINT NOT NULL,
    cantidad INT NOT NULL,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usuario_id BIGINT NOT NULL,
    motivo VARCHAR(255),
    CONSTRAINT fk_salida_producto FOREIGN KEY (producto_id) 
        REFERENCES productos(id) ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_salida_usuario FOREIGN KEY (usuario_id) 
        REFERENCES usuarios(id) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE alertas_inventario (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    producto_id BIGINT NOT NULL,
    nivel_alerta INT NOT NULL,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usuario_id BIGINT,
    CONSTRAINT fk_alerta_producto FOREIGN KEY (producto_id) 
        REFERENCES productos(id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_alerta_usuario FOREIGN KEY (usuario_id)
        REFERENCES usuarios(id) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE historial_precios (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    producto_id BIGINT NOT NULL,
    precio_anterior DECIMAL(10, 2) NOT NULL,
    precio_nuevo DECIMAL(10, 2) NOT NULL,
    fecha_cambio TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usuario_id BIGINT,
    CONSTRAINT fk_historial_producto FOREIGN KEY (producto_id) 
        REFERENCES productos(id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_historial_usuario FOREIGN KEY (usuario_id)
        REFERENCES usuarios(id) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE pedidos (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    proveedor_id BIGINT NOT NULL,
    fecha_pedido TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_entrega_estimada DATE,
    estado ENUM('pendiente', 'en_proceso', 'entregado', 'cancelado') NOT NULL DEFAULT 'pendiente',
    usuario_id BIGINT,
    CONSTRAINT fk_pedido_proveedor FOREIGN KEY (proveedor_id) 
        REFERENCES proveedores(id) ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_pedido_usuario FOREIGN KEY (usuario_id)
        REFERENCES usuarios(id) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE detalles_pedidos (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    pedido_id BIGINT NOT NULL,
    producto_id BIGINT NOT NULL,
    cantidad INT NOT NULL,
    precio_unitario DECIMAL(10, 2) NOT NULL,
    estado ENUM('pendiente', 'recibido', 'cancelado') NOT NULL DEFAULT 'pendiente',
    CONSTRAINT fk_detalle_pedido FOREIGN KEY (pedido_id) 
        REFERENCES pedidos(id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_detalle_producto FOREIGN KEY (producto_id) 
        REFERENCES productos(id) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB;

-- Índices para optimizar consultas
CREATE INDEX idx_usuarios_username ON usuarios(username);
CREATE INDEX idx_usuarios_email ON usuarios(email);
CREATE INDEX idx_productos_nombre ON productos(nombre);
CREATE INDEX idx_productos_categoria ON productos(categoria_id);
CREATE INDEX idx_proveedores_nombre ON proveedores(nombre);
CREATE INDEX idx_categorias_nombre ON categorias_productos(nombre);
CREATE INDEX idx_entradas_fecha ON entradas_inventario(fecha);
CREATE INDEX idx_salidas_fecha ON salidas_inventario(fecha);
CREATE INDEX idx_pedidos_fecha ON pedidos(fecha_pedido);
CREATE INDEX idx_pedidos_estado ON pedidos(estado);
CREATE INDEX idx_historial_fecha ON historial_precios(fecha_cambio);

-- Insertar roles y permisos básicos
INSERT INTO roles_permisos (rol, permiso, descripcion) VALUES
('admin', 'gestionar_usuarios', 'Permite crear, modificar y gestionar usuarios del sistema'),
('admin', 'gestionar_productos', 'Permite la gestión completa del catálogo de productos'),
('admin', 'gestionar_inventario', 'Permite gestionar el inventario y sus movimientos'),
('admin', 'gestionar_proveedores', 'Permite administrar proveedores y pedidos'),
('admin', 'generar_reportes', 'Permite generar todos los tipos de reportes'),
('admin', 'configurar_sistema', 'Permite modificar configuraciones del sistema'),
('usuario', 'ver_productos', 'Permite ver el catálogo de productos'),
('usuario', 'registrar_movimientos', 'Permite registrar entradas y salidas de inventario'),
('usuario', 'ver_reportes', 'Permite ver reportes básicos del sistema'),
('usuario', 'ver_proveedores', 'Permite consultar información de proveedores');

-- Insertar categorías predefinidas
INSERT INTO categorias_productos (nombre, descripcion) VALUES
('General', 'Categoría general de productos'),
('Materiales', 'Materiales y suministros'),
('Herramientas', 'Herramientas y equipos');

-- Crear usuario administrador por defecto
-- Contraseña: admin123
INSERT INTO usuarios (username, password_hash, nombre, apellido, email, rol)
VALUES (
    'admin', 
    '$2b$12$1xxxxxxxxxxxxxxxxxxxxuZLbwxnpY0o58unSvIPxddLxGystU.O', 
    'Administrador', 
    'Sistema', 
    'admin@santaclara.com', 
    'admin'
);