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

CREATE TABLE productos (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    descripcion TEXT,
    precio DECIMAL(10, 2) NOT NULL,
    cantidad_en_stock INT NOT NULL DEFAULT 0
) ENGINE=InnoDB;

CREATE TABLE proveedores (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    contacto VARCHAR(255),
    direccion TEXT
) ENGINE=InnoDB;

CREATE TABLE categorias_productos (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    descripcion TEXT
) ENGINE=InnoDB;

-- Tablas con dependencias
CREATE TABLE entradas_inventario (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    producto_id BIGINT NOT NULL,
    cantidad INT NOT NULL,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usuario_id BIGINT NOT NULL,
    CONSTRAINT fk_entrada_producto FOREIGN KEY (producto_id) 
        REFERENCES productos(id) ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_entrada_usuario FOREIGN KEY (usuario_id) 
        REFERENCES usuarios(id) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE salidas_inventario (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    producto_id BIGINT NOT NULL,
    cantidad INT NOT NULL,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usuario_id BIGINT NOT NULL,
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
    CONSTRAINT fk_alerta_producto FOREIGN KEY (producto_id) 
        REFERENCES productos(id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE historial_precios (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    producto_id BIGINT NOT NULL,
    precio DECIMAL(10, 2) NOT NULL,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_historial_producto FOREIGN KEY (producto_id) 
        REFERENCES productos(id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE pedidos (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    proveedor_id BIGINT NOT NULL,
    fecha_pedido TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado VARCHAR(50) NOT NULL,
    CONSTRAINT fk_pedido_proveedor FOREIGN KEY (proveedor_id) 
        REFERENCES proveedores(id) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE detalles_pedidos (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    pedido_id BIGINT NOT NULL,
    producto_id BIGINT NOT NULL,
    cantidad INT NOT NULL,
    precio_unitario DECIMAL(10, 2) NOT NULL,
    CONSTRAINT fk_detalle_pedido FOREIGN KEY (pedido_id) 
        REFERENCES pedidos(id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_detalle_producto FOREIGN KEY (producto_id) 
        REFERENCES productos(id) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE roles_permisos (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    rol VARCHAR(50) NOT NULL,
    permiso VARCHAR(50) NOT NULL
) ENGINE=InnoDB;

-- Índices para optimizar consultas
CREATE INDEX idx_usuarios_username ON usuarios(username);
CREATE INDEX idx_usuarios_email ON usuarios(email);
CREATE INDEX idx_productos_nombre ON productos(nombre);
CREATE INDEX idx_entradas_fecha ON entradas_inventario(fecha);
CREATE INDEX idx_salidas_fecha ON salidas_inventario(fecha);
CREATE INDEX idx_pedidos_fecha ON pedidos(fecha_pedido);
CREATE INDEX idx_historial_precios_fecha ON historial_precios(fecha);

-- Insertar roles y permisos básicos
INSERT INTO roles_permisos (rol, permiso) VALUES
('admin', 'gestionar_usuarios'),
('admin', 'gestionar_productos'),
('admin', 'gestionar_inventario'),
('admin', 'generar_reportes'),
('usuario', 'ver_productos'),
('usuario', 'registrar_movimientos'),
('usuario', 'ver_reportes');

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