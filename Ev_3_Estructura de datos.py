#EVIDENCIA 3
import datetime
import os
import sys
import sqlite3
from sqlite3 import Error
#
SEPARADOR = ("*" * 20) + "\n"
#
try:
    with sqlite3.connect("Tienda.db") as conn:
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS foliov (Folio INTEGER PRIMARY KEY, Fecha TEXT NOT NULL);")
        c.execute('''CREATE TABLE IF NOT EXISTS articulosv (Descripcion TEXT NOT NULL, Cantidad INTEGER NOT NULL,
                    Precio INTEGER NOT NULL, Total REAL NOT NULL, Foliov INTEGER NOT NULL,
                    FOREIGN KEY(Foliov) REFERENCES Foliov(Folio));''')
        print("Tabla creada exitosamente")
    while True:  
    #  
        print("\nMENÚ")
        print("1) Agregar venta")
        print("2) Busqueda especifica")
        print("3) Busqueda de ventas por fecha")
        print("4) Salir")
#  
        respuesta = int(input("Elija una opción: "))
#   
#    
        if respuesta == 1:
            while True:
                folio = int(input('\nIngrese el folio: '))
                with sqlite3.connect("Tienda.db") as conn:
                    c = conn.cursor()
                    efolio = {"folio": folio}
                    c.execute("SELECT * FROM foliov WHERE Folio = :folio", efolio)
                    fol = c.fetchall()
                    if fol:
                        print("El folio ya existe. Ingrese uno nuevamente")
                    else:
                        break     
            while True:
                fecha_capturada= input('Introduce una fecha (dd/mm/yyyy): ')
                fecha = datetime.datetime.strptime(fecha_capturada, "%d/%m/%Y").date()
                c.execute("INSERT INTO foliov (Folio, Fecha)VALUES(?,?)", (folio, fecha))
                print("Venta agregada exitosamente")
                conn.commit()
                agregarArticulo =1
                while agregarArticulo==1:  
                    descripcion= input('Introduce un articulo: ')
                    precio=int(input('Introduce el precio del articulo: '))
                    cantidad = int(input('Introduce la cantidad: '))
                    total = precio * cantidad    
                    c.execute('''INSERT INTO articulosv (Descripcion, Cantidad, Precio,
                                Total, Foliov)VALUES(?,?,?,?,?)''', (descripcion, cantidad, precio, total, folio))
                    print("Regristro agregado exitosamente")
                    conn.commit()                
#              
                    agregarArticulo=int(input('¿Desea añadir más articulos? \n1)Si \n2)No: '))
                    
                    suma_montos = 0
                    if agregarArticulo == 2:
                        efolio = {"folio": folio}
                        suma_montos = 0
                        c.execute('''SELECT foliov.Folio, foliov.Fecha, articulosv.Descripcion, articulosv.Cantidad, articulosv.Precio, articulosv.Total \
                                 FROM foliov \
                                 INNER JOIN articulosv ON articulosv.Foliov = foliov.Folio WHERE Folio = :folio''',efolio)
                        fec = c.fetchall()
                        if fec:
                            print("Folio\tFecha\t\tDescripcion\tCantidad\t\tPrecio\t\tTotal")
                        for Folio, Fecha, Descripcion, Cantidad, Precio, Total in fec:
                            print(f"{Folio}\t{Fecha}\t{Descripcion}\t\t{Cantidad}\t\t{Precio}\t\t{Total}")
                            suma_montos+= Total
                        print(SEPARADOR)
                        print("*******************")
                        print(f'Subtotal: ${suma_montos}')
                        iva = suma_montos * .16
                        totaliva = suma_montos + iva
                        print(f'Total + IVA: ${totaliva}')
                        
                break
         
#    
        elif respuesta == 2:
            folio_busqueda = int(input('\nIngrese el folio a buscar: '))
            efolio = {"folio": folio_busqueda}
            c.execute('''SELECT foliov.Folio, foliov.Fecha, articulosv.Descripcion, articulosv.Cantidad, articulosv.Precio \
                         FROM foliov \
                         INNER JOIN articulosv ON articulosv.Foliov = foliov.Folio WHERE Folio = :folio''', efolio)
            fol = c.fetchall()
            if fol:
                print("Folio\tFecha\t\tDescripcion\t\tCantidad\t\tPrecio")
                for Folio, Fecha, Descripcion, Cantidad, Precio in fol:
                    print(f"{Folio}\t{Fecha}\t{Descripcion}\t\t\t{Cantidad}\t\t\t{Precio}")
            else:
                print("El folio que ingreso no existe")
                        
    #          
        elif respuesta == 3:
            fecha_i = input('\nIngrese la fecha a buscar: ')
            fecha_busqueda = datetime.datetime.strptime(fecha_i, "%d/%m/%Y").date()
            suma_montos = 0
            efecha = {"folio": fecha_busqueda}
            c.execute('''SELECT foliov.Folio, foliov.Fecha, articulosv.Descripcion, articulosv.Cantidad, articulosv.Precio, articulosv.Total \
                         FROM foliov \
                         INNER JOIN articulosv ON articulosv.Foliov = foliov.Folio WHERE Fecha = :folio''', efecha)
            fec = c.fetchall()
            if fec:
                print("Folio\tFecha\t\tDescripcion\tCantidad\tPrecio\t\tTotal")
                for Folio, Fecha, Descripcion, Cantidad, Precio, Total in fec:
                    print(f"{Folio}\t{Fecha}\t{Descripcion}\t\t{Cantidad}\t\t{Precio}\t\t{Total}")
                    suma_montos+= Total
                print(SEPARADOR)
                print(f'Ventas {fecha_busqueda}')
                print("*******************")
                print(f'Subtotal: ${suma_montos}')
                iva = suma_montos * .16
                totaliva = suma_montos + iva
                print(f'Total + IVA: ${totaliva}')
            else:
                print("La fecha que ingreso no existe")
    #               
        elif respuesta == 4:
            print("Gracias por su compra, buen día")
            break                  
#
except Error as e:
    print (e)
except Exception:
    print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
finally:
    if conn:   
        conn.close()