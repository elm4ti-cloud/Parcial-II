# Parcial-II
1. Entidades y Atributos
Tabla productos: Almacena la información del inventario.

id (INTEGER, Primary Key, Auto-increment)

nombre (TEXT, Not Null)

precio (REAL, Not Null)

cantidad (INTEGER, Not Null)

Tabla ventas: Registra cada transacción de venta realizada.

id (INTEGER, Primary Key, Auto-increment)

producto_id (INTEGER, Foreign Key referenciando a productos(id))

cantidad_vendida (INTEGER, Not Null)

fecha (TEXT, Not Null — se puede usar la fecha actual del sistema)

2. Relación de la Base de Datos
Relación de Uno a Muchos (1:N): Un producto puede estar presente en muchas ventas, pero cada registro de venta pertenece a un único producto.

3. Operaciones al registrar una venta
Verificar que el ID del producto ingresado exista en la base de datos.   


Consultar la cantidad disponible actual en stock.   


Validar que la cantidad solicitada sea menor o igual al stock disponible.   


Insertar el registro correspondiente en la tabla ventas.

Actualizar (restar) la cantidad del producto en la tabla productos.   

Aplicar commit() para confirmar los cambios o rollback() si ocurre algún fallo.   

EVIDENCIAS DEL FUNCIONAMIENTO

<img width="980" height="878" alt="image" src="https://github.com/user-attachments/assets/68ded2f4-71d8-4c82-9562-0ba43f38c901" />

<img width="980" height="514" alt="image" src="https://github.com/user-attachments/assets/748666a7-73c7-4299-a8cb-b9965f4f525e" />

ROLLBACK

<img width="980" height="586" alt="image" src="https://github.com/user-attachments/assets/2968a44b-7091-450b-9d3a-462f72dd94a5" />

