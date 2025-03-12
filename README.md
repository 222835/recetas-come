#Recetas-COME# 
Sistema de Gestión de Recetas y Proyecciones - Comestibles Excelentes

Este proyecto es un sistema de gestión de recetas y proyecciones de ingredientes para la empresa Comestibles Excelentes. El objetivo principal del sistema es facilitar la creación, proyección y análisis de ingredientes necesarios para la preparación de productos alimenticios, optimizando la selección de proveedores y controlando los costos. El sistema estará basado en una arquitectura cliente-servidor y utilizará MariaDB para la base de datos.

## Características principales

- **Gestión de recetas**: Los usuarios pueden crear, modificar y eliminar recetas, con la capacidad de agregar ingredientes y cantidades.
- **Proyecciones de ingredientes**: Permite calcular la cantidad exacta de ingredientes necesarios según el número de comensales y ajustar las proyecciones de acuerdo a las necesidades de producción.
- **Historial de proyecciones**: Guarda un registro de todas las proyecciones realizadas, permitiendo su búsqueda y análisis posterior.
- **Comparación de costos de insumos**: Carga los costos de insumos de diferentes proveedores y permite compararlos para encontrar las mejores opciones de compra.
- **Gestión de usuarios**: El sistema contará con diferentes niveles de acceso, permitiendo a los administradores gestionar usuarios y contraseñas.

## Tecnología

- **Backend**: Aplicación nativa de escritorio para Windows.
- **Base de datos**: MariaDB para almacenar recetas, proyecciones y usuarios.
- **Lenguaje de programación**: Python.
- **Arquitectura**: Cliente-servidor.

## Roles y permisos de usuario

El sistema contará con los siguientes roles de usuario:

- **Administrador (Gerente de Operaciones)**: Acceso completo al sistema, incluyendo la gestión de usuarios y la administración de recetas, proyecciones e insumos.
- **Departamento de Compras**: Acceso limitado a la visualización de recetas, proyecciones e insumos, sin acceso a la gestión de usuarios o configuraciones del sistema.

## Instalación

1. Clona el repositorio:
    ```bash
    git clone https://github.com/222835/recetas-come.git
    ```
2. Navega al directorio del proyecto:
    ```bash
    cd recetas-come
    ```
3. Genera cambios y agregalos al proyecto
    ```bash 
    git add .
    git commit -m "Descripción de los cambios realizados"
    git push origin nombre_rama

4. Haz un pull request para hacer merge de los cambios 

