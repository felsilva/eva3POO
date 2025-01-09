-- Insertar categorías de productos tecnológicos
INSERT INTO `categorias_productos` (`nombre`, `descripcion`) VALUES
('Laptops', 'Computadoras portátiles y notebooks de última generación'),
('Smartphones', 'Teléfonos inteligentes y accesorios móviles'),
('Tablets', 'Tablets y dispositivos 2 en 1 convertibles'),
('Audio', 'Equipos de audio, audífonos y parlantes'),
('Gaming', 'Consolas y accesorios para videojuegos'),
('Computación', 'Componentes y accesorios de computación'),
('Monitores', 'Pantallas y monitores de alta resolución'),
('Almacenamiento', 'Dispositivos de almacenamiento y respaldo'),
('Redes', 'Equipos de conectividad y redes'),
('Smart Home', 'Dispositivos para el hogar inteligente');

-- Insertar proveedores tecnológicos
INSERT INTO `proveedores` (`nombre`, `contacto`, `direccion`) VALUES
('TechImport Chile', 'Roberto Méndez', 'Av. Providencia 1234, Santiago'),
('Distribuidora Samsung', 'Carolina Vera', 'Av. Las Condes 567, Santiago'),
('Apple Distribution', 'Andrés Torres', 'Av. Kennedy 890, Las Condes'),
('Gaming Pro', 'Valentina Soto', 'Av. Vicuña Mackenna 432, Santiago'),
('Global Electronics', 'Diego Ruiz', 'Av. Apoquindo 765, Las Condes'),
('Tech Mayorista', 'María José López', 'Av. Irarrázaval 2345, Ñuñoa'),
('PC Factory Direct', 'Felipe Herrera', 'Av. Libertador 543, Santiago'),
('Gaming World', 'Catalina Muñoz', 'Av. Matta 876, Santiago'),
('Smart Solutions', 'Jorge Pizarro', 'Av. La Florida 234, La Florida'),
('Digital Import', 'Paula Vargas', 'Av. Vitacura 432, Vitacura');

-- Insertar productos con especificaciones detalladas
INSERT INTO `productos` (`nombre`, `descripcion`, `precio`, `cantidad_en_stock`) VALUES
-- Laptops
('MacBook Pro 16', 'Apple MacBook Pro 16" M3 Pro, 32GB RAM, 1TB', 2499990.00, 15),
('Lenovo ThinkPad X1', 'ThinkPad X1 Carbon Gen 11, Intel i7, 16GB RAM', 1799990.00, 20),
('ASUS ROG Zephyrus', 'ROG Zephyrus G14 2024, Ryzen 9, RTX 4090', 2299990.00, 10),
('Dell XPS 13', 'Dell XPS 13 Plus, Intel i9, 32GB RAM, 1TB', 1999990.00, 12),
('HP Spectre x360', 'HP Spectre x360 14", Intel i7, 16GB RAM', 1699990.00, 18),

-- Smartphones
('iPhone 15 Pro Max', 'iPhone 15 Pro Max 1TB, Titanio Natural', 1899990.00, 25),
('Samsung S24 Ultra', 'Samsung Galaxy S24 Ultra 512GB 5G', 1599990.00, 30),
('Google Pixel 8 Pro', 'Google Pixel 8 Pro 256GB, 12GB RAM', 999990.00, 20),
('Xiaomi 14 Pro', 'Xiaomi 14 Pro 512GB, 12GB RAM', 899990.00, 25),
('Samsung Z Fold5', 'Samsung Galaxy Z Fold5 512GB', 1999990.00, 15),

-- Tablets
('iPad Pro 12.9', 'iPad Pro 12.9" M2, 256GB WiFi + 5G', 1299990.00, 20),
('Samsung Tab S9 Ultra', 'Galaxy Tab S9 Ultra 512GB, 16GB RAM', 1199990.00, 15),
('Microsoft Surface Pro 9', 'Surface Pro 9, Intel i7, 16GB RAM', 1399990.00, 12),
('Lenovo Tab P12 Pro', 'Tab P12 Pro 256GB, 8GB RAM', 699990.00, 18),
('iPad Air', 'iPad Air M1, 256GB WiFi', 899990.00, 25),

-- Audio
('Sony WH-1000XM5', 'Audífonos Bluetooth noise cancelling', 399990.00, 30),
('AirPods Pro 2', 'AirPods Pro 2da gen con cancelación', 249990.00, 40),
('JBL Boombox 3', 'Parlante Bluetooth portátil resistente agua', 299990.00, 20),
('Samsung Buds3 Pro', 'Audífonos TWS con cancelación activa', 179990.00, 35),
('Bose 700', 'Audífonos premium noise cancelling', 449990.00, 25),

-- Gaming
('PS5 Digital', 'PlayStation 5 versión digital 1TB', 499990.00, 20),
('Xbox Series X', 'Xbox Series X 1TB', 599990.00, 18),
('Nintendo Switch OLED', 'Nintendo Switch modelo OLED', 349990.00, 25),
('Steam Deck', 'Steam Deck 512GB', 699990.00, 15),
('PS5 Pro', 'PlayStation 5 Pro 2TB', 699990.00, 12),

-- Computación
('AMD Ryzen 9 7950X', 'Procesador AMD Ryzen 9 7950X', 699990.00, 15),
('NVIDIA RTX 4090', 'Tarjeta gráfica NVIDIA GeForce RTX 4090', 1999990.00, 8),
('Corsair 32GB RAM', 'Kit RAM Corsair 32GB DDR5 6000MHz', 299990.00, 30),
('ASUS ROG STRIX Z790', 'Placa madre ASUS ROG STRIX Z790-E', 499990.00, 20),
('Lian Li PC-O11', 'Gabinete Lian Li PC-O11 Dynamic', 199990.00, 25),

-- Monitores
('LG 27GP950', 'Monitor Gaming LG 27" 4K 144Hz', 799990.00, 15),
('Samsung Odyssey G9', 'Monitor curvo 49" 240Hz', 1499990.00, 10),
('ASUS ProArt PA32UCG', 'Monitor profesional 32" 4K HDR', 1999990.00, 8),
('Dell U2723QE', 'Monitor Dell 27" 4K USB-C', 699990.00, 20),
('BenQ EX2780Q', 'Monitor gaming 27" 144Hz IPS', 499990.00, 25),

-- Almacenamiento
('Samsung 990 Pro 2TB', 'SSD NVMe Samsung 990 Pro 2TB', 299990.00, 30),
('WD Black 8TB', 'Disco duro WD Black 8TB 7200RPM', 399990.00, 20),
('Crucial P5 Plus 1TB', 'SSD NVMe Crucial P5 Plus 1TB', 159990.00, 35),
('Seagate IronWolf 16TB', 'Disco duro NAS Seagate 16TB', 599990.00, 15),
('Kingston KC3000 2TB', 'SSD NVMe Kingston KC3000 2TB', 279990.00, 25),

-- Redes
('ASUS ROG Rapture', 'Router gaming WiFi 6E', 399990.00, 15),
('UniFi Dream Router', 'Router UniFi Dream Machine Pro', 499990.00, 12),
('TP-Link Deco XE75', 'Sistema mesh WiFi 6E', 299990.00, 20),
('Netgear Orbi 960', 'Sistema mesh WiFi 6E premium', 899990.00, 10),
('Synology RT6600ax', 'Router Synology WiFi 6', 299990.00, 18),

-- Smart Home
('Echo Show 15', 'Pantalla inteligente Alexa 15.6"', 299990.00, 20),
('Nest Hub Max', 'Pantalla inteligente Google 10"', 199990.00, 25),
('Philips Hue Kit', 'Kit inicial Philips Hue', 149990.00, 30),
('Ring Doorbell Pro', 'Timbre inteligente con cámara', 179990.00, 25),
('NVIDIA Shield TV Pro', 'Media player Android TV', 199990.00, 20);

-- Insertar 100 pedidos con fechas del último año
INSERT INTO `pedidos` (`proveedor_id`, `fecha_pedido`, `estado`)
SELECT 
    FLOOR(1 + RAND() * 10) as proveedor_id,
    DATE_SUB(NOW(), INTERVAL FLOOR(RAND() * 365) DAY) as fecha_pedido,
    ELT(FLOOR(1 + RAND() * 4), 'pendiente', 'en_proceso', 'entregado', 'cancelado') as estado
FROM 
    (SELECT X.N + Y.N * 10 AS num
     FROM 
        (SELECT 0 AS N UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9) X,
        (SELECT 0 AS N UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9) Y
     LIMIT 100) numbers;

-- Insertar 100 detalles de pedidos
INSERT INTO `detalles_pedidos` (`pedido_id`, `producto_id`, `cantidad`, `precio_unitario`)
SELECT 
    p.id as pedido_id,
    prod.id as producto_id,
    FLOOR(1 + RAND() * 10) as cantidad,
    prod.precio as precio_unitario
FROM 
    pedidos p
    CROSS JOIN (SELECT 1 as n UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5) numbers
    JOIN productos prod ON prod.id = FLOOR(1 + RAND() * 50)
LIMIT 100;

-- Insertar 100 entradas de inventario
INSERT INTO `entradas_inventario` (`producto_id`, `cantidad`, `fecha`, `usuario_id`)
SELECT 
    FLOOR(1 + RAND() * 50) as producto_id,
    FLOOR(5 + RAND() * 46) as cantidad,
    DATE_SUB(NOW(), INTERVAL FLOOR(RAND() * 365) DAY) as fecha,
    1 as usuario_id  -- ID del usuario administrador
FROM 
    (SELECT X.N + Y.N * 10 AS num
     FROM 
        (SELECT 0 AS N UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9) X,
        (SELECT 0 AS N UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9) Y
     LIMIT 100) numbers;

-- Insertar 100 salidas de inventario
INSERT INTO `salidas_inventario` (`producto_id`, `cantidad`, `fecha`, `usuario_id`)
SELECT 
    FLOOR(1 + RAND() * 50) as producto_id,
    FLOOR(1 + RAND() * 11) as cantidad,
    DATE_SUB(NOW(), INTERVAL FLOOR(RAND() * 365) DAY) as fecha,
    1 as usuario_id  -- ID del usuario administrador
FROM 
    (SELECT X.N + Y.N * 10 AS num
     FROM 
        (SELECT 0 AS N UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9) X,
        (SELECT 0 AS N UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9) Y
     LIMIT 100) numbers;

-- Insertar 100 registros de historial de precios
INSERT INTO `historial_precios` (`producto_id`, `precio_anterior`, `precio_nuevo`, `fecha_cambio`, `usuario_id`)
SELECT 
    prod.id as producto_id,
    prod.precio as precio_anterior,
    ROUND(prod.precio * (0.85 + (RAND() * 0.3)), 2) as precio_nuevo,
    DATE_SUB(NOW(), INTERVAL FLOOR(RAND() * 365) DAY) as fecha_cambio,
    1 as usuario_id
FROM 
    productos prod,
    (SELECT X.N + Y.N * 10 AS num
     FROM 
        (SELECT 0 AS N UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9) X,
        (SELECT 0 AS N UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9) Y
     LIMIT 100) numbers
WHERE prod.id = FLOOR(1 + RAND() * 50);

-- Insertar 100 alertas de inventario
INSERT INTO `alertas_inventario` (`producto_id`, `nivel_alerta`, `fecha`)
SELECT 
    FLOOR(1 + RAND() * 50) as producto_id,
    FLOOR(3 + RAND() * 13) as nivel_alerta,
    DATE_SUB(NOW(), INTERVAL FLOOR(RAND() * 365) DAY) as fecha
FROM 
   (SELECT X.N + Y.N * 10 AS num
     FROM 
        (SELECT 0 AS N UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9) X,
        (SELECT 0 AS N UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9) Y
     LIMIT 100) numbers;

-- Actualizar los niveles de stock basados en las entradas y salidas
UPDATE productos p 
SET cantidad_en_stock = (
    SELECT GREATEST(0, p.cantidad_en_stock + 
        COALESCE((SELECT SUM(cantidad) FROM entradas_inventario WHERE producto_id = p.id), 0) -
        COALESCE((SELECT SUM(cantidad) FROM salidas_inventario WHERE producto_id = p.id), 0)
    )
);

-- Verificar la integridad de los datos
SELECT 
    'Categorías' as tabla, COUNT(*) as registros FROM categorias_productos
UNION ALL
SELECT 'Productos', COUNT(*) FROM productos
UNION ALL
SELECT 'Proveedores', COUNT(*) FROM proveedores
UNION ALL
SELECT 'Pedidos', COUNT(*) FROM pedidos
UNION ALL
SELECT 'Detalles de Pedidos', COUNT(*) FROM detalles_pedidos
UNION ALL
SELECT 'Entradas Inventario', COUNT(*) FROM entradas_inventario
UNION ALL
SELECT 'Salidas Inventario', COUNT(*) FROM salidas_inventario
UNION ALL
SELECT 'Historial Precios', COUNT(*) FROM historial_precios
UNION ALL
SELECT 'Alertas Inventario', COUNT(*) FROM alertas_inventario;

-- Insertar movimientos de inventario para los últimos 3 meses
-- Entradas de inventario recientes
INSERT INTO entradas_inventario (producto_id, cantidad, fecha, usuario_id, proveedor_id, precio_unitario) VALUES
-- MacBook Pro 16 (ID: 1)
(1, 20, DATE_SUB(NOW(), INTERVAL 2 MONTH), 1, 1, 2499990),
(1, 15, DATE_SUB(NOW(), INTERVAL 1 MONTH), 1, 1, 2499990),
(1, 10, DATE_SUB(NOW(), INTERVAL 15 DAY), 1, 1, 2499990),

-- iPhone 15 Pro Max (ID: 6)
(6, 30, DATE_SUB(NOW(), INTERVAL 2 MONTH), 1, 2, 1899990),
(6, 25, DATE_SUB(NOW(), INTERVAL 1 MONTH), 1, 2, 1899990),
(6, 20, DATE_SUB(NOW(), INTERVAL 10 DAY), 1, 2, 1899990),

-- Samsung S24 Ultra (ID: 7)
(7, 25, DATE_SUB(NOW(), INTERVAL 2 MONTH), 1, 2, 1599990),
(7, 20, DATE_SUB(NOW(), INTERVAL 1 MONTH), 1, 2, 1599990),
(7, 15, DATE_SUB(NOW(), INTERVAL 5 DAY), 1, 2, 1599990);

-- Salidas de inventario recientes
INSERT INTO salidas_inventario (producto_id, cantidad, fecha, usuario_id) VALUES
-- MacBook Pro 16 (ID: 1)
(1, 15, DATE_SUB(NOW(), INTERVAL 45 DAY), 1),
(1, 12, DATE_SUB(NOW(), INTERVAL 30 DAY), 1),
(1, 8, DATE_SUB(NOW(), INTERVAL 15 DAY), 1),
(1, 5, DATE_SUB(NOW(), INTERVAL 5 DAY), 1),

-- iPhone 15 Pro Max (ID: 6)
(6, 20, DATE_SUB(NOW(), INTERVAL 40 DAY), 1),
(6, 18, DATE_SUB(NOW(), INTERVAL 25 DAY), 1),
(6, 15, DATE_SUB(NOW(), INTERVAL 10 DAY), 1),
(6, 10, DATE_SUB(NOW(), INTERVAL 2 DAY), 1),

-- Samsung S24 Ultra (ID: 7)
(7, 15, DATE_SUB(NOW(), INTERVAL 35 DAY), 1),
(7, 12, DATE_SUB(NOW(), INTERVAL 20 DAY), 1),
(7, 10, DATE_SUB(NOW(), INTERVAL 8 DAY), 1),
(7, 8, DATE_SUB(NOW(), INTERVAL 1 DAY), 1);

-- Configurar alertas de inventario
INSERT INTO alertas_inventario (producto_id, nivel_alerta, fecha) VALUES
(1, 15, NOW()),  -- MacBook Pro 16
(6, 20, NOW()),  -- iPhone 15 Pro Max
(7, 18, NOW()),  -- Samsung S24 Ultra
(11, 12, NOW()), -- iPad Pro
(16, 25, NOW()), -- Sony WH-1000XM5
(21, 15, NOW()), -- PS5 Digital
(26, 10, NOW()), -- AMD Ryzen 9
(31, 8, NOW()),  -- LG 27GP950
(36, 20, NOW()), -- Samsung 990 Pro
(41, 10, NOW()); -- ASUS ROG Rapture