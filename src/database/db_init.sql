CREATE DATABASE COME;

USE COME;

CREATE TABLE Usuarios (
    numero_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nombre_completo VARCHAR(100) NOT NULL,
    nombre_usuario VARCHAR(50) NOT NULL,
    contrasenia VARCHAR(150),
    rol VARCHAR(20)  
);

CREATE TABLE Proveedores (
    id_proveedor INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    categoria VARCHAR(50)
);


CREATE TABLE Ingredientes (
    id_ingrediente INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    clasificacion VARCHAR(50),
    unidad_medida VARCHAR(20)
);


CREATE TABLE Recetas (
    id_receta INT AUTO_INCREMENT PRIMARY KEY,
    nombre_receta VARCHAR(100) NOT NULL,
    clasificacion VARCHAR(50),
    periodo VARCHAR(50) NOT NULL,                       
    comensales_base INT NOT NULL,
    estatus boolean NOT NULL,
    fecha_eliminado DATE
);

CREATE TABLE Receta_Ingredientes(
    id_receta INT NOT NULL,
    id_ingrediente INT NOT NULL,
    cantidad DECIMAL(10,2) NOT NULL,
    PRIMARY KEY (id_receta, id_ingrediente),
    FOREIGN KEY (id_receta) REFERENCES Recetas(id_receta),
    FOREIGN KEY (id_ingrediente) REFERENCES Ingredientes(id_ingrediente)
);

CREATE TABLE Costos (
    id_costo INT AUTO_INCREMENT PRIMARY KEY,
    id_proveedor INT NOT NULL,
    nombre_ingrediente VARCHAR(100) NOT NULL,
    precio DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (id_proveedor) REFERENCES Proveedores(id_proveedor)
);

CREATE TABLE Proyecciones (
    id_proyeccion INT  AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    periodo VARCHAR(50),
    comensales INT NOT NULL,
    fecha DATE NOT NULL,
    estatus BOOLEAN NOT NULL,
    fecha_eliminado DATE
);

CREATE TABLE Proyeccion_Recetas (
    id_proyeccion INT NOT NULL,
    id_receta INT NOT NULL,
    porcentaje DECIMAL(5,2),
    PRIMARY KEY (id_proyeccion, id_receta),
    FOREIGN KEY (id_proyeccion) REFERENCES Proyecciones(id_proyeccion),
    FOREIGN KEY (id_receta) REFERENCES Recetas(id_receta)
);
