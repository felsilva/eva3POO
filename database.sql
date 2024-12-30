CREATE TABLE productos (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(255) NOT NULL,
  descripcion TEXT,
  precio DECIMAL(10, 2) NOT NULL,
  cantidad_en_stock INT NOT NULL
);

CREATE TABLE entradas_inventario (
  id INT AUTO_INCREMENT PRIMARY KEY,
  producto_id INT,
  cantidad INT NOT NULL,
  fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (producto_id) REFERENCES productos(id)
);

CREATE TABLE salidas_inventario (
  id BIGINT AUTO_INCREMENT PRIMARY KEY,
  producto_id BIGINT,
  cantidad INT NOT NULL,
  fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (producto_id) REFERENCES productos(id)
);

CREATE TABLE usuarios (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nombre_usuario VARCHAR(255) UNIQUE NOT NULL,
  contrasena VARCHAR(255) NOT NULL,
  rol VARCHAR(50) NOT NULL
);

CREATE TABLE roles_permisos (
  id INT AUTO_INCREMENT PRIMARY KEY,
  rol VARCHAR(50) NOT NULL,
  permiso VARCHAR(50) NOT NULL
);

CREATE TABLE alertas_inventario (
  id INT AUTO_INCREMENT PRIMARY KEY,
  producto_id INT,
  nivel_alerta INT NOT NULL,
  fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (producto_id) REFERENCES productos(id)
);

CREATE TABLE proveedores (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(255) NOT NULL,
  contacto VARCHAR(255),
  direccion TEXT
);

CREATE TABLE categorias_productos (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(255) NOT NULL,
  descripcion TEXT
);

CREATE TABLE historial_precios (
  id INT AUTO_INCREMENT PRIMARY KEY,
  producto_id INT,
  precio DECIMAL(10, 2) NOT NULL,
  fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (producto_id) REFERENCES productos(id)
);

CREATE TABLE pedidos (
  id INT AUTO_INCREMENT PRIMARY KEY,
  proveedor_id INT,
  fecha_pedido TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  estado VARCHAR(50) NOT NULL,
  FOREIGN KEY (proveedor_id) REFERENCES proveedores(id)
);

CREATE TABLE detalles_pedidos (
  id INT AUTO_INCREMENT PRIMARY KEY,
  pedido_id INT,
  producto_id INT,
  cantidad INT NOT NULL,
  precio_unitario DECIMAL(10, 2) NOT NULL,
  FOREIGN KEY (pedido_id) REFERENCES pedidos(id),
  FOREIGN KEY (producto_id) REFERENCES productos(id)
);