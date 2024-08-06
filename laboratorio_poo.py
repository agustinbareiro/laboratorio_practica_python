'''
Desafío 1: Sistema de Gestión de Productos

Objetivo: Desarrollar un sistema para manejar productos en un inventario.

Requisitos:
    * Crear una clase base Producto con atributos como nombre, precio, cantidad en stock, etc.
    * Definir al menos 2 clases derivadas para diferentes categorías de productos
    (por ejemplo, ProductoElectronico, ProductoAlimenticio) con atributos y métodos específicos.
    * Implementar operaciones CRUD para gestionar productos del inventario.
    * Manejar errores con bloques try-except para validar entradas y gestionar excepciones.
    * Persistir los datos en archivo JSON.
'''
from datetime import datetime
import json

class Producto:
    def __init__(self, id_producto, nombre, descripcion, precio, stock):
        self.__id_producto = id_producto
        self.__nombre = nombre
        self.__descripcion = descripcion
        self.__precio = precio
        self.__stock = stock

    @property
    def id_producto(self):
        return self.__id_producto
    
    @property
    def nombre(self):
        return self.__nombre.capitalize()
    
    @property
    def descripcion(self):
        return self.__descripcion.capitalize()
    
    @property
    def precio(self):
        return self.__precio
    
    @property
    def stock(self):
        return self.__stock

    @id_producto.setter
    def id_producto(self, nuevo_id_producto):
        self.__id_producto = self.validar_id_producto(nuevo_id_producto)

    @nombre.setter
    def nombre(self, nombre):
        self.__nombre = nombre

    @descripcion.setter
    def descripcion(self, descripcion):
        self.__descripcion = descripcion

    @precio.setter
    def precio(self, nuevo_precio):
        self.__precio = self.validar_precio(nuevo_precio)

    @stock.setter
    def stock(self, nuevo_stock):
        self.__stock = self.validar_stock(nuevo_stock)

    def validar_id_producto(self, id_producto):
        try:
            id_producto_num = int(id_producto)
            if id_producto_num < 0:
                raise ValueError("El número de ID del producto no puede ser negativo.")
            return id_producto_num
        except ValueError:
            raise ValueError("El número de ID del producto debe ser un número entero.")

    def validar_precio(self, precio):
        try:
            precio_num = float(precio)
            if precio_num <= 0:
                raise ValueError("El precio debe ser un número positivo.")
            return precio_num
        except ValueError:
            raise ValueError("El precio debe ser un número válido.")
        
    def validar_stock(self, stock):
        try:
            stock_num = int(stock)
            if stock_num < 0:
                raise ValueError("El número de stock no puede ser negativo.")
            return stock_num
        except ValueError:
            raise ValueError("El número de stock debe ser un número entero.")

    def to_dict (self):
        return {
            "id_producto": self.id_producto,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "precio": self.precio,
            "stock": self.stock
        }
    
    def __str__(self):
        return f"{self.nombre} - {self.descripcion}"

class ProductoElectronico(Producto):
    def __init__(self, id_producto, nombre, descripcion, precio, stock, garantia):
        super().__init__(id_producto, nombre, descripcion, precio, stock)
        self.__garantia = garantia
        
    @property
    def garantia(self):
        return self.__garantia

    @garantia.setter
    def garantia(self, nueva_garantia):
        self.__garantia = self.validar_garantia(nueva_garantia)

    def validar_garantia(self, garantia):
        try:
            garantia_num = int(garantia)
            if garantia_num < 0:
                raise ValueError("La cantidad de meses de garantía no puede ser un número negativo.")
            return garantia_num
        except ValueError:
            raise ValueError("La cantidad de meses de garantía debe ser un número válido.")

    def to_dict (self):
        data = super().to_dict()
        data['garantia'] = self.garantia
        return data
    
    def __str__(self):
        return f"ProductoElectronico: ({self.nombre}, ${self.precio}, Stock:{self.stock}, {self.garantia} meses de garantía.)"

class ProductoAlimenticio(Producto):
    def __init__(self, id_producto, nombre, descripcion, precio, stock, vencimiento):
        super().__init__(id_producto, nombre, descripcion, precio, stock)
        self.__vencimiento = vencimiento

    @property
    def vencimiento(self):
        return self.__vencimiento

    @vencimiento.setter
    def vencimiento(self, nuevo_vencimiento):
        self.__vencimiento = self.validar_vencimiento(nuevo_vencimiento)

    def validar_vencimiento(self, vencimiento): #No funciona
        try:
            vencimiento_fecha = datetime.strptime(vencimiento, "%d-%m-%Y")
            if vencimiento_fecha <= datetime.now():
                raise ValueError("La fecha de vencimiento no puede ser anterior a la carga del producto.")
            return vencimiento_fecha
        except ValueError:
            raise ValueError("El vencimiento debe ser una fecha válida.")
        
    def to_dict (self):
        data = super().to_dict()
        data['vencimiento'] = self.vencimiento
        return data
        
    def __str__(self):
        return f"ProductoAlimenticio: ({self.nombre}, ${self.precio}, Stock: {self.stock}, Vence el: {self.vencimiento}.)"

class GestionProductos:
    def __init__(self, archivo):
        self.archivo = archivo

    def leer_datos(self):
        try:
            with open(self.archivo, 'r') as file:
                datos = json.load(file)
        except FileNotFoundError:
            return {}
        except Exception as e:
            raise Exception (f"Error al leer datos del archivo: {e}")
        else:
            return datos

    def guardar_datos(self, datos):
        try:
            with open(self.archivo, 'w') as file:
                json.dump(datos, file, indent = 4)
        except IOError as e:
            print(f"Error al intentar guardar los datos en {self.archivo}: {e}")
        except Exception as e:
            print(f"Error inesperado: {e}")

    def nuevo_producto(self, producto):
        try:
            datos = self.leer_datos()
            id_producto = producto.id_producto
            if not str(id_producto) in datos.keys():
                datos[id_producto] = producto.to_dict()
                self.guardar_datos(datos)
                print(f"Producto: {producto.nombre}, ID: {id_producto} creado correctamente.")
            else:
                print (f"Ya existe un producto con el ID: {id_producto}.")
        except Exception as e:
            print(f"Error al cargar nuevo producto: {e}")
    
    def buscar_producto(self, id_producto):
        try:
            datos = self.leer_datos()
            if id_producto in datos.keys():
                producto_data = datos[id_producto]
                print(f"Producto encontrado con ID {id_producto}.")
                if "garantia" in producto_data:
                    print(f"Producto Electrónico: {producto_data['nombre']}, Precio: ${producto_data['precio']}, Stock: {producto_data['stock']}, Garantía: {producto_data['garantia']} meses.")
                else:
                    print(f"Producto Alimenticio: {producto_data['nombre']}, Precio: ${producto_data['precio']}, Stock: {producto_data['stock']}, Vencimiento: {producto_data['vencimiento']}.")
            else:
                print(f"Producto no encontrado con ID {id_producto}.")
        except Exception as e:
            print(f"Error al buscar producto: {e}")
    
    def actualizar_precio(self, id_producto, nuevo_precio):
        try:
            datos = self.leer_datos()
            if id_producto in datos.keys():
                datos[id_producto]['precio'] = nuevo_precio
                self.guardar_datos(datos)
                print(f"Precio del producto ID: {id_producto} actualizado correctamente.")
            else:
                print(f"Producto no encontrado con ID {id_producto}.")
        except Exception as e:
            print(f"Error al actualizar el precio del producto.")
    
    def eliminar_producto(self, id_producto):
        try:
            datos = self.leer_datos()
            if id_producto in datos.keys():
                del datos[id_producto]
                self.guardar_datos(datos)
                print(f"Producto ID: {id_producto} eliminado correctamente.")
            else:
                print(f"Producto no encontrado con ID {id_producto}.")
        except Exception as e:
            print(f"Error al eliminar el producto.")