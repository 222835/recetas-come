## Sistema de Gestión de Recetas y Proyecciones - Comestibles Excelentes

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

1.  **Clonar el repositorio:**
    ```bash
    git clone [https://github.com/222835/recetas-come.git](https://github.com/222835/recetas-come.git)
    ```
2.  **Navegar al directorio del proyecto:**
    ```bash
    cd recetas-come
    ```
3.  **Crear un entorno virtual (recomendado):**
    ```bash
    python -m venv venv
    ```
    * **Activar el entorno virtual:**
        * **Windows:** `venv\Scripts\activate`
        * **macOS y Linux:** `source venv/bin/activate`
4.  **Instalar las dependencias:**
        ```bash
        pip install -r requirements.txt
        ```
5.  **Instalar MariaDB:**
    * Descarga e instala MariaDB desde [mariadb.com/downloads/](https://mariadb.com/downloads/). Sigue las instrucciones oficiales para tu sistema operativo.
    * Vídeo tutorial de instalación: [https://www.youtube.com/watch?v=syYStO\_BFgw](https://www.youtube.com/watch?v=syYStO_BFgw)
6.  **Configurar la base de datos:**
    * Copia el archivo `.env.example` a `.env`:
        ```bash
        cp .env.example .env
        ```
    * Edita el archivo `.env` con las credenciales y la dirección de tu base de datos MariaDB local. Ejemplo:
        ```
        DB_HOST="localhost"
        DB_USER="root"
        DB_PASSWORD="root"
        DB_DATABASE="test_db"
        ```
    * Crea la base de datos en MariaDB usando el nombre que especificaste en `.env`.
    * Cree la base de datos COME, usando el script sql que le fue proporcionado, de la siguiente manera, ya sea con algun GUI de mariadb, o con la linea de comandos:
    * **Usando la línea de comandos de MariaDB:**
        1.  Abre la línea de comandos de MariaDB.
        2.  Inicia sesión con tu usuario y contraseña:
            ```bash
            mysql -u tu_usuario -p
            ```
        3. Copia y pega el contenido del archivo .sql que se encuentra en la carpeta `src/database/db_init.sql`
7.  **Ejecutar el proyecto:**
    ```bash
    python main.py
    ```

### Tests

Los tests estan escritos para funcionar con el modulo ya integrado en python de `unittest`. Estos estan organizados en sus propios archivos de la siguiente manera: `test_[nombre del modulo a testear]_[archivo de ese modulo a testear].py`, Los tests se organizan en clases para mayor comodidad.


**Ejecutar un solo test:**

```bash

python -m unittest "[archivo a testear].py"

```


**Ejecutar todos los tests a la vez:**

```bash

python -m unittest discover -s tests -p "test_*.py"

``` 
