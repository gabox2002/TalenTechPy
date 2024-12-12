import sqlite3
from colorama import Fore, Style

# --------------------------------------------------------------------------------
def conectar_bd():
    """Función para establecer conexión con la base de datos y crea la tabla si no existe."""
    conn = sqlite3.connect("inventario.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            descripcion TEXT,
            cantidad INTEGER NOT NULL,
            precio REAL NOT NULL,
            categoria TEXT
        )
    """)
    conn.commit()
    return conn

# --------------------------------------------------------------------------------
def validar_numero(mensaje, tipo="float"):
    """Función para validar que el usuario ingrese un número válido (entero o decimal)."""
    while True:
        entrada = input(mensaje).strip()
        if entrada.replace('.', '', 1).replace('-', '', 1).isnumeric():
            if tipo == "int":
                return int(entrada)
            elif tipo == "float":
                return float(entrada)
        else:
            print("Por favor, ingrese un valor numérico válido.")

# --------------------------------------------------------------------------------
def validar_texto(mensaje):
    """Función para validar que el usuario ingrese un texto no vacío."""
    while True:
        texto = input(mensaje).strip()
        if texto:
            return texto
        print("Por favor, ingrese un texto válido.")

# --------------------------------------------------------------------------------
def agregar_producto(conn, nombre, descripcion, cantidad, precio, categoria):
    """Función para solicitar al usuario los datos de un producto y lo agrega al inventario tras validar las entradas."""
    print("\n--- Agregar Producto ---")
    
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO productos (nombre, descripcion, cantidad, precio, categoria)
        VALUES (?, ?, ?, ?, ?)
    """, (nombre, descripcion, cantidad, precio, categoria))
    conn.commit()
    print(Fore.GREEN + "Producto agregado con éxito." + Style.RESET_ALL)

# --------------------------------------------------------------------------------
def formatear_producto(producto):
    """Recibe un producto y devuelve una línea formateada para mostrarlo en una tabla."""
    id_prod = str(producto[0]).rjust(3)
    nombre = producto[1].ljust(18)
    descripcion = producto[2]
    if len(descripcion) > 40:
        descripcion = descripcion[:37] + "..."
    descripcion = descripcion.ljust(40)
    cantidad = str(producto[3]).rjust(8)
    precio = f"{producto[4]:.0f}".rjust(6)
    categoria = producto[5].ljust(9)

    return f"{id_prod} | {nombre} | {descripcion} | {cantidad} | {precio} | {categoria}"

# --------------------------------------------------------------------------------
def mostrar_productos(conn):
    """Función para mostrar todos los productos en el inventario en forma de tabla."""
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    if productos:
        # Encabezados de la tabla
        print("\n ID | Nombre             | Descripción                              | Cantidad | Precio | Categoría ")
        print("-" * 100)
        for prod in productos:
            print(formatear_producto(prod))
    else:
        print(Fore.YELLOW + "No hay productos en el inventario." + Style.RESET_ALL)

# --------------------------------------------------------------------------------
def actualizar_cantidad(conn, id_producto, nueva_cantidad):
    """Función para actualizar la cantidad de un producto específico."""
    cursor = conn.cursor()
    cursor.execute("UPDATE productos SET cantidad = ? WHERE id = ?", (nueva_cantidad, id_producto))
    if cursor.rowcount:
        conn.commit()
        print(Fore.GREEN + "Cantidad actualizada con éxito." + Style.RESET_ALL)
    else:
        print(Fore.RED + "Producto no encontrado." + Style.RESET_ALL)

# --------------------------------------------------------------------------------
def eliminar_producto(conn, id_producto):
    """Función para eliminar un producto por su ID."""
    cursor = conn.cursor()
    cursor.execute("DELETE FROM productos WHERE id = ?", (id_producto,))
    if cursor.rowcount:
        conn.commit()
        print(Fore.GREEN + "Producto eliminado con éxito." + Style.RESET_ALL)
    else:
        print(Fore.RED + "Producto no encontrado." + Style.RESET_ALL)

# --------------------------------------------------------------------------------
def buscar_producto(conn, id_producto):
    """Función para buscar un producto en el inventario por su ID."""
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos WHERE id = ?", (id_producto,))
    producto = cursor.fetchone()
    if producto:
        print("\n ID | Nombre             | Descripción                              | Cantidad | Precio | Categoría ")
        print("-" * 100)
        print(formatear_producto(producto))
    else:
        print(Fore.RED + "No se encontró el producto con el ID especificado." + Style.RESET_ALL)

# --------------------------------------------------------------------------------
def reporte_bajo_stock(conn, limite):
    """Función para generar un reporte de productos con stock igual o menor al límite."""
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos WHERE cantidad <= ?", (limite,))
    productos = cursor.fetchall()
    if productos:
        print("\nID  | Nombre           | Cantidad")
        print("-" * 36)
        for prod in productos:
            print(f"{prod[0]:<3} | {prod[1]:<16} | {prod[3]:<8}")
    else:
        print(Fore.YELLOW + "No hay productos con bajo stock." + Style.RESET_ALL)


# --------------------------------------------------------------------------------
def mostrar_menu():
    """Función para mostrar el menú principal."""
    print(Fore.LIGHTCYAN_EX + "\n" + "-" * 100)
    print("Menú Principal")
    print("-" * 100 + Style.RESET_ALL)    
    print("1. Agregar producto")
    print("2. Mostrar productos")
    print("3. Actualizar cantidad de producto")
    print("4. Eliminar producto")
    print("5. Buscar producto")
    print("6. Generar reporte de bajo stock")
    print("7. Salir""\n")

# --------------------------------------------------------------------------------
def main():
    conn = conectar_bd()
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            nombre = validar_texto("Ingrese el nombre del producto: ")
            descripcion = validar_texto("Ingrese una descripción: ")
            cantidad = validar_numero("Ingrese la cantidad: ", tipo="int")
            precio = validar_numero("Ingrese el precio: ", tipo="float")
            categoria = validar_texto("Ingrese la categoría: ")
            agregar_producto(conn, nombre, descripcion, cantidad, precio, categoria)
        elif opcion == "2":
            mostrar_productos(conn)
        elif opcion == "3":
            id_producto = validar_numero("Ingrese el ID del producto: ", tipo="int")
            nueva_cantidad = validar_numero("Ingrese la nueva cantidad: ", tipo="int")
            actualizar_cantidad(conn, id_producto, nueva_cantidad)
        elif opcion == "4":
            id_producto = validar_numero("Ingrese el ID del producto a eliminar: ", tipo="int")
            eliminar_producto(conn, id_producto)
        elif opcion == "5":
            id_producto = validar_numero("Ingrese el ID del producto a buscar: ", tipo="int")
            buscar_producto(conn, id_producto)
        elif opcion == "6":
            limite = validar_numero("Ingrese el límite de stock: ", tipo="int")
            reporte_bajo_stock(conn, limite)
        elif opcion == "7":
            print("Saliendo del programa...")
            break
        else:
            print(Fore.RED + "Opción no válida. Intente nuevamente." + Style.RESET_ALL)
    conn.close()

if __name__ == "__main__":
    main()