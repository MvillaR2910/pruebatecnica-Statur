PRAGMA foreign_keys = OFF;

DROP TABLE IF EXISTS clientes;
DROP TABLE IF EXISTS ciudades;
DROP TABLE IF EXISTS departamentos;
DROP TABLE IF EXISTS usuarios;

CREATE TABLE usuarios (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    usuario VARCHAR(100) NOT NULL UNIQUE,
    contrasena_hash VARCHAR(255) NOT NULL
);

CREATE TABLE departamentos (
    codigo_departamento INTEGER NOT NULL PRIMARY KEY,
    nombre_departamento VARCHAR(100) NOT NULL
);

CREATE TABLE ciudades (
    codigo_ciudad INTEGER NOT NULL PRIMARY KEY,
    nombre_ciudad VARCHAR(100) NOT NULL,
    departamento_id INTEGER NOT NULL,
    FOREIGN KEY (departamento_id) REFERENCES departamentos (codigo_departamento)
);

CREATE TABLE clientes (
    documento_identidad VARCHAR(20) NOT NULL PRIMARY KEY,
    nombres VARCHAR(100) NOT NULL,
    apellidos VARCHAR(100) NOT NULL,
    departamento_id INTEGER NOT NULL,
    ciudad_id INTEGER NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    telefono VARCHAR(30) NOT NULL UNIQUE,
    creado_por_id INTEGER NOT NULL,
    FOREIGN KEY (departamento_id) REFERENCES departamentos (codigo_departamento),
    FOREIGN KEY (ciudad_id) REFERENCES ciudades (codigo_ciudad),
    FOREIGN KEY (creado_por_id) REFERENCES usuarios (id)
);

INSERT INTO usuarios (id, usuario, contrasena_hash) VALUES
(1, 'admin', 'scrypt:32768:8:1$2UrEULZUSSxcYiyN$51421d6392265128753d53fca1a68da381fbdf60a7726afb72bee2d34a61d52a4254802afca6c0effd33179ffc6db1c27de13112dbfc1b64f74edf1c3803e977');

INSERT INTO departamentos (codigo_departamento, nombre_departamento) VALUES
(5, 'Antioquia'),
(8, 'Atlántico'),
(11, 'Bogotá D.C.'),
(68, 'Santander'),
(76, 'Valle del Cauca');

INSERT INTO ciudades (codigo_ciudad, nombre_ciudad, departamento_id) VALUES
(5001, 'Medellín', 5),
(5002, 'Bello', 5),
(5004, 'Turbo', 5),
(8001, 'Barranquilla', 8),
(8078, 'Baranoa', 8),
(8088, 'Malambo', 8),
(11001, 'Bogotá D.C.', 11),
(68001, 'Bucaramanga', 68),
(68077, 'Barbosa', 68),
(68679, 'San Gil', 68),
(76001, 'Cali', 76),
(76109, 'Buenaventura', 76),
(76834, 'Tuluá', 76);

PRAGMA foreign_keys = ON;
