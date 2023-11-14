import sqlite3
from sqlite3 import Error
import sys
from datetime import datetime
import re # Librería para el manejo de expresiones regulares para validación

def Crear_tablas():
    try:
        #Conexion a la base de datos "PIA.db"
        with sqlite3.connect("PIA.db") as conn:
            mi_cursor = conn.cursor()
            #Se crean las tablas con sus atributos
            mi_cursor.execute("CREATE TABLE IF NOT EXISTS Sucursal (IDSucursal INTEGER PRIMARY KEY, Nombre TEXT NOT NULL, Direccion TEXT NOT NULL, CodigoPostal TEXT NOT NULL, Telefono TEXT NOT NULL);")
            mi_cursor.execute("CREATE TABLE IF NOT EXISTS Producto (IDProducto INTEGER PRIMARY KEY, Nombre TEXT NOT NULL, Descripcion TEXT, Precio DECIMAL(10, 2) NOT NULL, Disponibles INTEGER NOT NULL);")
            mi_cursor.execute("CREATE TABLE IF NOT EXISTS Venta (IDVenta INTEGER PRIMARY KEY, FechaVenta DATE, Sucursal INTEGER, Producto INTEGER, Cantidad INTEGER, PrecioUnitario DECIMAL(10, 2), TotalVenta DECIMAL(10, 2), FOREIGN KEY (Sucursal) REFERENCES Sucursal(IDSucursal), FOREIGN KEY (Producto) REFERENCES Producto(IDProducto));")
            print("___Tablas creadas___")
    except Error as e:
        print(e)
    except:
        print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
    finally:
        conn.close()

def Agregar_sucursal(nombre, direccion, codigo_postal, telefono):
    try:
        #Conexion con la base de datos
        with sqlite3.connect("PIA.db") as conn:
            mi_cursor = conn.cursor()
            #Se insertan los datos de la funcion a la tabla "Sucursal"
            mi_cursor.execute("INSERT INTO Sucursal (Nombre, Direccion, CodigoPostal, Telefono) VALUES (?, ?, ?, ?);", (nombre, direccion, codigo_postal, telefono))
            print("___Sucursal agregada___")
    except Error as e:
        print(e)
    except:
        print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
    finally:
        conn.close()

def Agregar_producto(nombre, descripcion, precio, disponibles):
    try:
        #Conexion con la base de datos
        with sqlite3.connect("PIA.db") as conn:
            mi_cursor = conn.cursor()
            #Ejecutamos un codigo SQL para comprobar si el "nombre" existe dentro de mi tabla
            mi_cursor.execute("SELECT * FROM Producto WHERE Nombre = ?;", (nombre,))
            #Guardamos el dato si es que existe
            producto_existente = mi_cursor.fetchone()

            if producto_existente: #Si el producto existe solo se modificara la descripcion y el precio
                #Guardamos los datos del id y de la cantidad existente, ignorando los otros datos
                id_producto_existente, _, _, _, disponibles_existente = producto_existente
                #A las cantidades disponibles le sumamos las que ya teniamos mas la nuevas cantidades
                nuevas_disponibles = disponibles_existente + disponibles
                #Actualizamos los datos de la tabla
                mi_cursor.execute("UPDATE Producto SET Descripcion = ?, Precio = ?, Disponibles = ? WHERE IDProducto = ?;", (descripcion, precio, nuevas_disponibles, id_producto_existente))
                print(f"Se han actualizado los datos de {nombre}. Ahora hay un total de {nuevas_disponibles} disponibles.")
            else: #Si no existe el producto entonces lo crearemos
                mi_cursor.execute("INSERT INTO Producto (Nombre, Descripcion, Precio, Disponibles) VALUES (?, ?, ?, ?);", (nombre, descripcion, precio, disponibles))
                print("___Producto agregado___")
    except Error as e:
        print(e)
    except Exception as ex:
        print(f"Se produjo el siguiente error: {ex}")
    finally:
        conn.close()

def Registrar_venta(sucursal_id, producto_id, cantidad):
    try:
        #Conexion a la base de datos
        with sqlite3.connect("PIA.db") as conn:
            mi_cursor = conn.cursor()
            #Buscamos primero si el producto existe
            mi_cursor.execute("SELECT Nombre, Precio, Disponibles FROM Producto WHERE IDProducto = ?;", (producto_id,))
            resultado_producto = mi_cursor.fetchone()
            if resultado_producto: #Si existe entonces empezamos a registrar la venta
                #Obtenemos los datos del producto
                nombre_producto, precio_unitario, disponibles = resultado_producto
                if disponibles >= cantidad: #Comprobamos si hay existencias del producto
                    total_venta = precio_unitario * cantidad
                    fecha_venta = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    mi_cursor.execute("INSERT INTO Venta (FechaVenta, Sucursal, Producto, Cantidad, PrecioUnitario, TotalVenta) VALUES (?, ?, ?, ?, ?, ?);", (fecha_venta, sucursal_id, producto_id, cantidad, precio_unitario, total_venta))
                    mi_cursor.execute("UPDATE Producto SET Disponibles = Disponibles - ? WHERE IDProducto = ?;", (cantidad, producto_id))
                    print(f"Venta registrada exitosamente: {cantidad} unidades de {nombre_producto} por un total de ${total_venta}")
                else:
                    print("___No hay suficientes productos disponibles___")
            else:
                print("___Producto no encontrado___")
    except Error as e:
        print(e)
    except Exception as ex:
        print(f"Se produjo el siguiente error: {ex}")
    finally:
        conn.close()

def Ver_sucursales():
    try:
        with sqlite3.connect("PIA.db") as conn:
            mi_cursor = conn.cursor()
            mi_cursor.execute("SELECT * FROM Sucursal;") #Consulta de SQL para mostrar todas las sucursales existentes
            sucursales = mi_cursor.fetchall()
            print("___Sucursales___")
            for sucursal in sucursales:
                print(sucursal)
    except Error as e:
        print(e)
    except:
        print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
    finally:
        conn.close()

def Ver_productos():
    try:
        with sqlite3.connect("PIA.db") as conn:
            mi_cursor = conn.cursor()
            mi_cursor.execute("SELECT * FROM Producto;") #Consulta de SQL para mostrar todos los productos existentes
            productos = mi_cursor.fetchall()
            print("___Productos___")
            for producto in productos:
                print(producto)
    except Error as e:
        print(e)
    except:
        print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
    finally:
        conn.close()

def Ver_ventas():
    try:
        with sqlite3.connect("PIA.db") as conn:
            mi_cursor = conn.cursor()
            mi_cursor.execute("SELECT * FROM Venta;") #Consulta de SQL para mostrar todas las ventas existentes
            ventas = mi_cursor.fetchall()
            print("___Ventas___")
            for venta in ventas:
                print(venta)
    except Error as e:
        print(e)
    except:
        print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
    finally:
        conn.close()


def Eliminar_sucursal(sucursal_id):
    try:
        #Conexion a la base de datos
        with sqlite3.connect("PIA.db") as conn:
            mi_cursor = conn.cursor()
            #Eliminamos los datos de la tabla donde el ID de la sucursal sea la misma que la funcion
            mi_cursor.execute("DELETE FROM Sucursal WHERE IDSucursal = ?;", (sucursal_id,))
            print(f"Sucursal con ID {sucursal_id} eliminada exitosamente.")
    except Error as e:
        print(e)
    except:
        print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
    finally:
        conn.close()

def Eliminar_producto(producto_id):
    try:    
        with sqlite3.connect("PIA.db") as conn:
            mi_cursor = conn.cursor()
            #Eliminamos los datos de la tabla donde el ID del producto sea la misma que la funcion
            mi_cursor.execute("DELETE FROM Producto WHERE IDProducto = ?;", (producto_id,))
            print(f"Producto con ID {producto_id} eliminado exitosamente.")
    except Error as e:
        print(e)
    except:
        print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
    finally:
        conn.close()

def Menu():
    #Menu con ciclo infinito
    while True:
        print("__Bienvenido___")
        print("1. Registrar Sucursal")
        print("2. Registrar Producto")
        print("3. Registrar Venta")
        print("4. Ver Sucursales")
        print("5. Ver Productos")
        print("6. Ver Ventas")
        print("7. Eliminar Sucursal")
        print("8. Eliminar Producto")
        print("9. Salir")
        print("______________")
        opcion = input("Seleccione una opción (1-9): ")
        print("______________")
        if opcion == "1":
            # Creacion de Sucursal
            while True: #Agregar Nombre
                _nombre=input("- Ingresa el nombre de la sucursal: ")
                _nombre=_nombre.upper()
                if _nombre=="":
                    print(" Error, el nombre no puede omitirse intenta de nuevo")
                    continue
                if (not bool(re.match("^[A-Z ÑÁÉÍÓÚÜ]{1,30}$",_nombre))):
                    print(" Error, el nombre no cumple con el patron, no puedes agregar numeros (1-30 caracteres), intenta de nuevo")
                    continue
                nombre=_nombre
                break
            
            while True: #Ingresar Direccion
                _direccion=input("- Ingresa la direccion de la sucursal:")
                _direccion=_direccion.upper()
                if _direccion=="":
                    print(" Error, la direccion no puede omitirse intenta de nuevo")
                    continue
                if (not bool(re.match("^[A-Z ÑÁÉÍÓÚÜ]{1,30}$",_direccion))):
                    print(" Error, la direccion no cumple con el patron, no puedes agregar numeros (1-30 caracteres), intenta de nuevo")
                    continue
                direccion=_direccion
                break

            while True: #Ingresar Codigo Postal
                _codigo_postal=input("- Ingresa el codigo postal de la sucursal:")
                if _codigo_postal=="":
                    print(" Error, el dato no puede omitirse intenta de nuevo")
                    continue
                if (not bool(re.match("^[0-9]{5}$",_codigo_postal))):
                    print(" Error, el codigo postal no cumple con el patron, deben contener 5 digitos, intenta de nuevo")
                    continue
                codigo_postal=_codigo_postal
                break

            while True: #Ingresar Telefono
                _telefono=input("- Ingresa el telefono de la sucursal:")
                if _telefono=="":
                    print(" Error, el telefono no puede omitirse intenta de nuevo")
                    continue
                if (not bool(re.match("^[0-9]{10}$",_telefono))):
                    print(" Error, el telefono no cumple con el patron, debe contener 10 digitos, intenta de nuevo")
                    continue
                telefono=_telefono
                break
            #Se crea la suscursal
            Agregar_sucursal(nombre, direccion, codigo_postal, telefono)

        elif opcion == "2":
            #Creacion del Producto
            while True: #Ingresar Nombre
                _nombre=input("- Ingresa el nombre del producto: ")
                _nombre=_nombre.upper()
                if _nombre=="":
                    print(" Error, el nombre no puede omitirse intenta de nuevo")
                    continue
                if (not bool(re.match("^[A-Z ÑÁÉÍÓÚÜ]{1,30}$",_nombre))):
                    print(" Error, el nombre no cumple con el patron, no puedes agregar numeros (1-30 caracteres), intenta de nuevo")
                    continue
                nombre=_nombre
                break

            while True: #Ingresar Descripcion
                _descripcion=input("- Ingresa la descripcion: ")
                _descripcion=_descripcion.upper()
                if _descripcion=="":
                    print(" Error, la descripcion no puede omitirse intenta de nuevo")
                    continue
                if (not bool(re.match("^[A-Z ÑÁÉÍÓÚÜ]{1,30}$",_descripcion))):
                    print(" Error, la descripcion no cumple con el patron, no puedes agregar numeros (1-30 caracteres), intenta de nuevo")
                    continue
                descripcion=_descripcion
                break

            while True: #Ingresar Precio
                _precio=(input("-Ingrese el precio de venta del producto: "))
                if _precio=="":
                    print(" Error, el precio no puede omitirse intenta de nuevo")
                    continue
                if (not bool(re.match("[0-9]{1,15}[.][0-9]{1,15}$",_precio))):
                    print(" Error, el precio no cumple con el patron,(XX.XX),intenta de nuevo")
                    continue
                precio=float(_precio)
                break

            while True: #Ingresar Disponibilidad
                _disponibles=(input("Ingrese la cantidad disponibles del producto: "))
                if _disponibles=="":
                    print(" Error, la cantidad diponible no puede omitirse intenta de nuevo")
                    continue
                if (not bool(re.match(r"^\d+$",_disponibles))):
                    print(" Error, la cantidad debe ser un numero,intenta de nuevo")
                    continue
                disponibles=int(_disponibles)
                break
        
                # Se crea el producto
            Agregar_producto(nombre, descripcion, precio, disponibles)

        elif opcion == "3":
            #Creacion de la Venta
            #ID sucursal
            while True:
                _sucursal_id=(input("Ingrese el ID de la sucursal: "))
                if _sucursal_id=="":
                    print(" Error, el ID no puede omitirse intenta de nuevo")
                    continue
                if (not bool(re.match(r"^\d+$",_sucursal_id))):
                    print(" Error, el ID debe ser un numero,intenta de nuevo")
                    continue
                sucursal_id=int(_sucursal_id)
                break
            
            #ID producto
            while True:
                _producto_id=(input("Ingrese el ID del producto: "))
                if _producto_id=="":
                    print(" Error, El ID no puede omitirse intenta de nuevo")
                    continue
                if (not bool(re.match(r"^\d+$",_producto_id))):
                    print(" Error, el ID debe ser un numero,intenta de nuevo")
                    continue
                producto_id=int(_producto_id)
                break
    
            #Cantidad Vendida
            while True:
                _cantidad=(input("Ingrese la cantidad vendida del producto: "))
                if _cantidad=="":
                    print(" Error, la cantidad vendida no puede omitirse intenta de nuevo")
                    continue
                if (not bool(re.match(r"^\d+$",_cantidad))):
                    print(" Error, la cantidad debe ser un numero,intenta de nuevo")
                    continue
                cantidad=int(_cantidad)
                break
 
            Registrar_venta(sucursal_id, producto_id, cantidad)

        elif opcion == "4":
            #visualización de las sucursales
            Ver_sucursales()

        elif opcion == "5":
            #visualización de los productos
            Ver_productos()

        elif opcion == "6":
            #visualización de las ventas
            Ver_ventas()

        elif opcion == "7":
            #Eliminar Sucursal
            while True:
                _sucursal_id=(input("Ingrese el ID de la sucursal a eliminar: "))
                if _sucursal_id=="":
                    print(" Error, el ID no puede omitirse intenta de nuevo")
                    continue
                if (not bool(re.match(r"^\d+$",_sucursal_id))):
                    print(" Error, el ID debe ser un numero,intenta de nuevo")
                    continue
                sucursal_id=int(_sucursal_id)
                break
            #Sucursal eliminada
            Eliminar_sucursal(sucursal_id)


        elif opcion == "8":
            #Eliminar Producto
            while True:
                _producto_id=(input("Ingrese el ID del producto a eliminar: "))
                if _producto_id=="":
                    print(" Error, el ID no puede omitirse intenta de nuevo")
                    continue
                if (not bool(re.match(r"^\d+$",_producto_id))):
                    print(" Error, el ID debe ser un numero,intenta de nuevo")
                    continue
                producto_id=int(_producto_id)
                break
            #Producto Eliminado
            Eliminar_producto(producto_id)


        elif opcion == "9":
            #Salida del menu
            print("Adiós!")
            break
        else:
            #Validacion si ingresa otro dato
            print("Opción no válida, seleccione una opción del 1 al 9.")

#Creacion de las tablas SQL
Crear_tablas()
#Creacion del Menu
Menu()
