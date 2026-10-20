import sqlite3
from datetime import datetime

def conectar():
    return sqlite3.connect("inventario_ventas.db")

def inicializar_base_datos():
    conexion = conectar()
    cursor = conexion.cursor()
    # Crear tabla productos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            precio REAL NOT NULL,
            cantidad INTEGER NOT NULL
        )
    """)
    # Crear tabla ventas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ventas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            producto_id INTEGER,
            cantidad_vendida INTEGER NOT NULL,
            fecha TEXT NOT NULL,
            FOREIGN KEY (producto_id) REFERENCES productos(id)
        )
    """)
    conexion.commit()
    conexion.close()

def registrar_producto():
    nombre = input("Nombre del producto: ")
    precio = float(input("Precio del producto: "))
    cantidad = int(input("Cantidad disponible: "))
    
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("INSERT INTO productos (nombre, precio, cantidad) VALUES (?, ?, ?)", (nombre, precio, cantidad))
    conexion.commit()
    conexion.close()
    print("¡Producto registrado con éxito!")

def consultar_productos():
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    conexion.close()
    
    print("\n--- LISTA DE PRODUCTOS ---")
    for p in productos:
        print(f"ID: {p[0]} | Nombre: {p[1]} | Precio: ${p[2]:.2f} | Stock: {p[3]}")

def registrar_venta():
    consultar_productos()
    prod_id = int(input("Ingrese el ID del producto a vender: "))
    cantidad_venta = int(input("Ingrese la cantidad a vender: "))
    
    conexion = conectar()
    cursor = conexion.cursor()
    
    try:
        # Iniciar transacción implícita
        # 1. Verificar existencia y stock
        cursor.execute("SELECT cantidad FROM productos WHERE id = ?", (prod_id,))
        resultado = cursor.fetchone()
        
        if not resultado:
            raise Exception("El producto no existe.")
        
        stock_actual = resultado[0]
        if stock_actual < cantidad_venta:
            raise Exception("Stock insuficiente para realizar la venta.")
        
        # 2. Registrar la venta
        fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("INSERT INTO ventas (producto_id, cantidad_vendida, fecha) VALUES (?, ?, ?)", 
                       (prod_id, cantidad_venta, fecha_actual))
        
        # 3. Descontar del inventario
        cursor.execute("UPDATE productos SET cantidad = cantidad - ? WHERE id = ?", (cantidad_venta, prod_id))
        
        # 4. Confirmar transacción
        conexion.commit()
        print("¡Venta registrada y stock actualizado exitosamente!")
        
    except Exception as e:
        conexion.rollback()
        print(f"Error en la transacción, se aplicó rollback: {e}")
    finally:
        conexion.close()

def mostrar_historial_ventas():
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT v.id, p.nombre, v.cantidad_vendida, v.fecha 
        FROM ventas v
        JOIN productos p ON v.producto_id = p.id
    """)
    ventas = cursor.fetchall()
    conexion.close()
    
    print("\n--- HISTORIAL DE VENTAS (JOIN) ---")
    for v in ventas:
        print(f"Venta ID: {v[0]} | Producto: {v[1]} | Cantidad: {v[2]} | Fecha: {v[3]}")

def menu():
    inicializar_base_datos()
    while True:
        print("\n=== SISTEMA DE INVENTARIO Y VENTAS ===")
        print("1. Registrar producto")
        print("2. Consultar productos")
        print("3. Registrar venta")
        print("4. Mostrar historial de ventas")
        print("5. Salir")
        
        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            registrar_producto()
        elif opcion == "2":
            consultar_productos()
        elif opcion == "3":
            registrar_venta()
        elif opcion == "4":
            mostrar_historial_ventas()
        elif opcion == "5":
            print("Saliendo del sistema...")
            break
        else:
            print("Opción inválida. Intente de nuevo.")

if __name__ == "__main__":
    menu()