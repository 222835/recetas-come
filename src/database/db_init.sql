CREATE DATABASE COME;

USE COME;

CREATE TABLE Usuarios (
    numero_usuario INT PRIMARY KEY,
    nombre_completo VARCHAR(100) NOT NULL,
    nombre_usuario VARCHAR(50) NOT NULL,
    contrasenia VARCHAR(50),
    rol VARCHAR(20)  
);


CREATE TABLE Gestion_Usuarios (
    id_usuario INT PRIMARY KEY,
    numero_usuario INT NOT NULL,  
    nombre_completo VARCHAR(100),
    contrasenia VARCHAR(50),
    rol VARCHAR(20),  
    FOREIGN KEY (numero_usuario) REFERENCES Usuarios(numero_usuario)
);


CREATE TABLE Proveedores (
    id_proveedor INT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    categoria VARCHAR(50)
);


CREATE TABLE Ingredientes (
    id_ingrediente INT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    clasificacion VARCHAR(50),
    unidad_medida VARCHAR(20)
);


CREATE TABLE Recetas (
    id_receta INT PRIMARY KEY,
    nombre_receta VARCHAR(100) NOT NULL,
    clasificacion VARCHAR(50),
    periodo VARCHAR(50) NOT NULL,                       
    comensales_base INT NOT NULL,                   
);

CREATE TABLE Receta_Ingredientes (
    id_receta INT NOT NULL,
    id_ingrediente INT NOT NULL,
    cantidad DECIMAL(10,2) NOT NULL,
    unidad_medida VARCHAR(20) NOT NULL,  
    PRIMARY KEY (id_receta, id_ingrediente),
    FOREIGN KEY (id_receta) REFERENCES Recetas(id_receta),
    FOREIGN KEY (id_ingrediente) REFERENCES Ingredientes(id_ingrediente)
);


CREATE TABLE Costos (
    id_ingrediente INT PRIMARY KEY,
    id_proveedor INT NOT NULL,
    precio DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (id_ingrediente) REFERENCES Ingredientes(id_ingrediente),
    FOREIGN KEY (id_proveedor) REFERENCES Proveedores(id_proveedor)
);


CREATE TABLE basurero (
    id_basurero INT PRIMARY KEY,
    tipo VARCHAR(20) NOT NULL,      
    id_elemento INT NOT NULL,         
    id_usuario INT NOT NULL,
    FOREIGN KEY (id_usuario) REFERENCES Usuarios(numero_usuario)
);


CREATE TABLE Usuario_Recetas (
    numero_usuario INT NOT NULL,
    id_receta INT NOT NULL,
    rol VARCHAR(20) NOT NULL,         
    PRIMARY KEY (numero_usuario, id_receta),
    FOREIGN KEY (numero_usuario) REFERENCES Usuarios(numero_usuario),
    FOREIGN KEY (id_receta) REFERENCES Recetas(id_receta)
);


CREATE TABLE Proyecciones (
    id_proyeccion INT PRIMARY KEY,
    numero_usuario INT NOT NULL,
    nombre VARCHAR(100),
    periodo VARCHAR(50),
    comensales INT,
    FOREIGN KEY (numero_usuario) REFERENCES Usuarios(numero_usuario)
);


CREATE TABLE Historial_Proyecciones (
    id_cambio INT PRIMARY KEY,
    id_proyeccion INT NOT NULL,
    id_usuario INT NOT NULL,
    FOREIGN KEY (id_proyeccion) REFERENCES Proyecciones(id_proyeccion),
    FOREIGN KEY (id_usuario) REFERENCES Usuarios(numero_usuario)
);


CREATE TABLE Reportes (
    id_reporte INT PRIMARY KEY,
    id_proyeccion INT NOT NULL,
    fecha DATE,
    formato VARCHAR(10) NOT NULL,   
    contenido TEXT,                 
    FOREIGN KEY (id_proyeccion) REFERENCES Proyecciones(id_proyeccion)
);


CREATE TABLE Proyeccion_Recetas (
    id_proyeccion INT NOT NULL,
    id_receta INT NOT NULL,
    porcentaje DECIMAL(5,2),
    PRIMARY KEY (id_proyeccion, id_receta),
    FOREIGN KEY (id_proyeccion) REFERENCES Proyecciones(id_proyeccion),
    FOREIGN KEY (id_receta) REFERENCES Recetas(id_receta)
);
