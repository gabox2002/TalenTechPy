====================================
GESTOR DE INVENTARIO - TIENDA
====================================

Esta es una aplicación en Python que permite gestionar el inventario de una pequeña tienda. 
La aplicación utiliza una base de datos SQLite para almacenar los datos de los productos y 
proporciona una interfaz basada en la terminal para interactuar con el inventario.

------------------------------------
CARACTERÍSTICAS
------------------------------------
- Registrar productos: Agrega nuevos productos al inventario.
- Mostrar productos: Lista todos los productos registrados en el inventario.
- Actualizar cantidad: Modifica la cantidad de un producto existente.
- Eliminar productos: Elimina productos del inventario por su ID.
- Buscar productos: Busca productos por su ID.
- Reporte de bajo stock: Genera un informe de productos con cantidades bajas según un límite especificado.

------------------------------------
REQUISITOS
------------------------------------
**Software**
- Python 3.7 o superior.
- Librería `colorama` (para mejorar la interfaz en la terminal).
- SQLite (incluido por defecto en Python).

**Instalación de dependencias**
Instala la librería `colorama` ejecutando el siguiente comando en tu terminal:

pip install colorama

------------------------------------
ESTRUCTURA DEL PROYECTO
------------------------------------
- `app.py`: Código principal de la aplicación.
- `inventario.db`: Base de datos SQLite que almacena los datos del inventario. 
  (Se genera automáticamente al ejecutar el programa por primera vez).

------------------------------------
CÓMO INTERACTUAR CON LA APLICACIÓN
------------------------------------
Sigue las instrucciones del menú principal para interactuar con la aplicación.

------------------------------------
MENÚ PRINCIPAL
------------------------------------
El programa mostrará el siguiente menú para seleccionar las opciones:

1. Agregar producto
2. Mostrar productos
3. Actualizar cantidad de producto
4. Eliminar producto
5. Buscar producto
6. Generar reporte de bajo stock
7. Salir

------------------------------------
BASE DE DATOS
------------------------------------
La aplicación crea automáticamente una base de datos llamada `inventario.db` en la misma carpeta 
donde se encuentra el archivo `app.py`. La tabla `productos` tiene la siguiente estructura:

| Campo         | Tipo     | Descripción                              |
|---------------|----------|------------------------------------------|
| `id`          | INTEGER  | Identificador único (clave primaria).    |
| `nombre`      | TEXT     | Nombre del producto (no nulo).           |
| `descripcion` | TEXT     | Descripción breve del producto.          |
| `cantidad`    | INTEGER  | Cantidad disponible (no nulo).           |
| `precio`      | REAL     | Precio del producto (no nulo).           |
| `categoria`   | TEXT     | Categoría a la que pertenece el producto.|

------------------------------------
REPORTE DE BAJO STOCK
------------------------------------
El programa genera un informe de productos cuyo stock sea igual o inferior a un límite especificado por el usuario.
