-- Insertar datos en la tabla de productos
INSERT INTO productos (nombre, descripcion, precio, cantidad_en_stock)
VALUES
('iPhone 14', 'Smartphone de alta gama con cámara de 48MP y pantalla OLED', 999.99, 50),
('Samsung Galaxy S23', 'Smartphone premium con cámara de 50MP y pantalla AMOLED', 899.99, 80),
('MacBook Pro 16"', 'Laptop profesional con chip M1 Max, pantalla Retina y 64GB de RAM', 2599.99, 30),
('Sony WH-1000XM5', 'Auriculares inalámbricos con cancelación de ruido', 349.99, 200),
('Nintendo Switch OLED', 'Consola portátil híbrida con pantalla OLED y 64GB de almacenamiento', 349.00, 150),
('Amazon Echo Dot', 'Altavoz inteligente con Alexa', 49.99, 500);

-- Insertar datos en la tabla de entradas de inventario
INSERT INTO entradas_inventario (producto_id, cantidad)
VALUES
(1, 30),  -- iPhone 14
(2, 40),  -- Samsung Galaxy S23
(3, 15),  -- MacBook Pro 16"
(4, 100), -- Sony WH-1000XM5
(5, 60),  -- Nintendo Switch OLED
(6, 150); -- Amazon Echo Dot

-- Insertar datos en la tabla de salidas de inventario
INSERT INTO salidas_inventario (producto_id, cantidad)
VALUES
(1, 10),  -- iPhone 14
(2, 5),   -- Samsung Galaxy S23
(3, 5),   -- MacBook Pro 16"
(4, 20),  -- Sony WH-1000XM5
(5, 25),  -- Nintendo Switch OLED
(6, 50);  -- Amazon Echo Dot

-- Insertar datos en la tabla de usuarios
INSERT INTO usuarios (nombre_usuario, contrasena, rol)
VALUES
('admin', 'admin1234', 'Administrador'),
('juanperez', 'juan2024', 'Vendedor'),
('mariafernandez', 'maria2024', 'Vendedor'),
('luisgomez', 'luis2024', 'Vendedor');

-- Insertar datos en la tabla de roles_permisos
INSERT INTO roles_permisos (rol, permiso)
VALUES
('Administrador', 'Ver inventario'),
('Administrador', 'Editar productos'),
('Administrador', 'Gestionar usuarios'),
('Vendedor', 'Ver inventario'),
('Vendedor', 'Registrar salidas de inventario');

-- Insertar datos en la tabla de alertas de inventario
INSERT INTO alertas_inventario (producto_id, nivel_alerta)
VALUES
(1, 10),  -- iPhone 14
(2, 15),  -- Samsung Galaxy S23
(3, 5),   -- MacBook Pro 16"
(4, 50),  -- Sony WH-1000XM5
(5, 30),  -- Nintendo Switch OLED
(6, 100); -- Amazon Echo Dot

-- Insertar datos en la tabla de proveedores
INSERT INTO proveedores (nombre, contacto, direccion)
VALUES
('Apple Inc.', 'ventas@apple.com', '1 Infinite Loop, Cupertino, CA 95014, USA'),
('Samsung Electronics', 'contacto@samsung.com', '129 Samsung-ro, Suwon-si, Gyeonggi-do, Corea del Sur'),
('Sony Corporation', 'soporte@sony.com', '1-7-1 Konan, Minato-ku, Tokyo, Japón'),
('Nintendo Co. Ltd.', 'contacto@nintendo.com', '11-1 Kamitoba, Minami-ku, Kyoto, Japón'),
('Amazon', 'soporte@amazon.com', '410 Terry Ave N, Seattle, WA 98109, USA');

-- Insertar datos en la tabla de categorías de productos
INSERT INTO categorias_productos (nombre, descripcion)
VALUES
('Electrónica', 'Dispositivos electrónicos como smartphones, computadoras, y más.'),
('Audio', 'Productos relacionados con audio como auriculares, altavoces, etc.'),
('Juguetes y Videojuegos', 'Consolas y juegos para todo público.'),
('Hogar', 'Electrodomésticos y productos para el hogar.'),
('Tecnología', 'Todo lo relacionado con computadoras, gadgets, y más.');

-- Insertar datos en la tabla de historial de precios
INSERT INTO historial_precios (producto_id, precio)
VALUES
(1, 999.99),  -- iPhone 14
(2, 899.99),  -- Samsung Galaxy S23
(3, 2599.99), -- MacBook Pro 16"
(4, 349.99),  -- Sony WH-1000XM5
(5, 349.00),  -- Nintendo Switch OLED
(6, 49.99);   -- Amazon Echo Dot

-- Insertar datos en la tabla de pedidos
INSERT INTO pedidos (proveedor_id, estado)
VALUES
(1, 'Pendiente'),  -- Pedido a Apple
(2, 'Enviado'),    -- Pedido a Samsung
(3, 'Pendiente'),  -- Pedido a Sony
(4, 'Enviado'),    -- Pedido a Nintendo
(5, 'Pendiente');  -- Pedido a Amazon

-- Insertar datos en la tabla de detalles de pedidos
INSERT INTO detalles_pedidos (pedido_id, producto_id, cantidad, precio_unitario)
VALUES
(1, 1, 20, 999.99),  -- Pedido 1: 20 iPhone 14
(2, 2, 30, 899.99),  -- Pedido 2: 30 Samsung Galaxy S23
(3, 3, 15, 2599.99), -- Pedido 3: 15 MacBook Pro 16"
(4, 5, 50, 349.00),  -- Pedido 4: 50 Nintendo Switch OLED
(5, 6, 100, 49.99);  -- Pedido 5: 100 Amazon Echo Dot
