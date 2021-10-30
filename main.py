from tkinter import *
from tkinter import ttk
from tkinter import messagebox

from smtplib import *

import tkinter

import mysql.connector

cnx = mysql.connector.connect(user='root', password='lucas123',
                                host='127.0.0.1',
                                port='3306',
                                charset='utf8',
                                database='productos')

class Login:
   
    def __init__(self, window):
        self.wind = window
        self.wind.geometry("400x400")
        self.wind.title('Registro e inicio de sesión')
        

        frame = LabelFrame(self.wind, text = 'Inicio de sesión', height = 200)
        frame.grid(row = 0, column = 0, columnspan = 3, pady = 50, padx = 50)
        
        
        userverify = StringVar()
        passwordverify = StringVar()
        
        # Usuario
        Label(frame, text = 'Usuario: ').grid(row = 1, column = 0, pady = 10)
        self.user = Entry(frame, textvariable = userverify)
        self.user.focus()
        self.user.grid(row = 1, column = 1)

        # Contraseña
        Label(frame, text = 'Contraseña: ').grid(row = 2, column = 0, pady = 5)
        self.password = Entry(frame, textvariable = passwordverify, show = '*')
        self.password.focus()
        self.password.grid(row = 2, column = 1)

        # Botones
        ttk.Button(frame, text = 'Iniciar sesión', command = lambda: self.iniciar_sesion(userverify, passwordverify)).grid(row = 3, columnspan = 2, sticky = W + E, pady = 5)
        ttk.Button(frame, text = 'Crear cuenta', command = self.crear_cuenta).grid(row = 4, columnspan = 2, sticky = W + E, pady = 5)
        ttk.Button(frame, text = 'Recuperar contraseña', command = self.recuperar_contrasenia).grid(row = 5, columnspan = 2, sticky = W + E, pady = 5)
        


    # Recuperar contraseña
    def recuperar_contrasenia (self):
        
        messagebox.showinfo(title="Contraseña", message="Se le ha enviado su contraseña por email")

    # Creación cuenta
    def crear_cuenta (self): 
        self.crearcuenta = Toplevel()
        self.crearcuenta.title = 'Editar producto'
        self.crearcuenta.geometry("400x400")
        
        header = Label(self.crearcuenta, text = "Pantalla de registro")
        header.grid(row = 0, column = 0 , columnspan = 4)
        
        frame = LabelFrame(self.crearcuenta, height = 500)
        frame.grid(row = 0, column = 0, columnspan = 4, pady = 50, padx = 50, sticky = N + S)


        user = StringVar()
        contra = StringVar()
        email = StringVar()

        # Usuario
        Label(frame, text = 'Usuario: ').grid(row = 1, column = 0, pady = 10)
        self.user = Entry(frame, textvariable = user)
        self.user.focus()
        self.user.grid(row = 1, column = 1)

        # Email
        Label(frame, text = 'Email: ').grid(row = 2, column = 0, pady = 10)
        self.mail = Entry(frame, textvariable = email)
        self.mail.focus()
        self.mail.grid(row = 2, column = 1)

        # Contraseña
        Label(frame, text = 'Contraseña: ').grid(row = 3, column = 0, pady = 5)
        self.password = Entry(frame, show ="*", textvariable = contra)
        self.password.focus()
        self.password.grid(row = 3, column = 1)

        ttk.Button(self.crearcuenta, text = 'Registrarse', command = lambda: self.insertar_usuarios()).grid(row = 10, column = 2, sticky = W + E)
        self.crearcuenta.mainloop()

    def validacion(self):
        if '@' and '.com' in self.mail.get():
            return len(self.user.get()) != 0 and len(self.password.get()) != 0
        
        else:
            messagebox.showinfo(message="El email ingresado no es correcto")
        
   
    def insertar_usuarios(self):
        if self.validacion():
            query = """INSERT INTO usuarios (iduser, nombreuser, mail, contraseña) VALUES (NULL,%s,%s,%s)"""
            parametros =  (self.user.get(), self.mail.get(), self.password.get())
            self.consultar(query, parametros)
            messagebox.showinfo(message="Registro exitoso")           
            self.user.delete(0, END)
            self.mail.delete(0, END)
            self.password.delete(0, END)
        else:
            messagebox.showinfo(message="Los datos ingresados no son correctos. Por favor, verifique que todos los campos estén completos")



    def consultar(self, query, parametros = ()):
        cursor = cnx.cursor(buffered=True)
        try:
            query = cursor.execute(query, parametros)
            cnx.commit()
            cursor.close()
        except Exception as error:
            print(error)
        return query

    # Inicio de sesión
    def iniciar_sesion (self, userverify, passwordverify):
        
        cursor = cnx.cursor(buffered=True)
        
        query = "SELECT contrasena, iduser FROM usuarios WHERE nombreuser = %s and contrasena = %s "
        parametros = (userverify.get(), passwordverify.get())
        cursor.execute(query, parametros)
        cnx.commit()
        resultado = cursor.fetchall()
        if resultado == []:
            messagebox.showwarning(message="Usuario o contraseña incorrecta")
        else:
            messagebox.showinfo(message="Inicio de sesión correcta")
            iduser = resultado[0][1]
            self.wind.destroy()
            Product()

        
        



       
    

class Product:
    def __init__(self):
        # Arranca 
        self.wind = Tk()
        self.wind.title('Control de productos')

        # Contenedor
        frame = LabelFrame(self.wind, text = 'Añadir producto')
        frame.grid(row = 2, column = 0, columnspan = 4, pady = 20)

        # Entrada de nombre
        Label(frame, text = 'Nombre: ').grid(row = 1, column = 0, pady = 5)
        self.name = Entry(frame)
        self.name.focus()
        self.name.grid(row = 1, column = 1)

        # Entrada de precio
        Label(frame, text = 'Precio: ').grid(row = 2, column = 0, pady = 5)
        self.price = Entry(frame)
        self.price.grid(row = 2, column = 1)

        # Entrada de stock
        Label(frame, text = 'Stock: ').grid(row = 3, column = 0, pady = 5)
        self.stock = Entry(frame)
        self.stock.grid(row = 3, column = 1)

        # Boton añadir producto
        ttk.Button(frame, text = 'Agregar producto', command = self.anadir_producto).grid(row = 5, columnspan = 2, sticky = W + E, pady = 5)

        # Mensajes de salida
        self.message = Label(text = '', fg = 'green')
        self.message.grid(row = 4, column = 0, columnspan = 2, sticky = W + E)

        # Tabla
        self.tree = ttk.Treeview(height = 8, columns = ('#0', '#1', '#2'))
        self.tree.grid(row = 3, column = 0, columnspan = 2)
        self.tree.heading('#0', text = 'Id', anchor = CENTER)
        self.tree.heading('#1', text = 'Nombre', anchor = CENTER)
        self.tree.heading('#2', text = 'Precio', anchor = CENTER)
        self.tree.heading('#3', text = 'Stock', anchor = CENTER)

        # Botones
        ttk.Button(text = 'ELIMINAR', command = self.eliminar_producto).grid(row = 5, column = 0, sticky = W + E)
        ttk.Button(text = 'EDITAR', command = self.editar_producto).grid(row = 5, column = 1, sticky = W + E)

        # Llenar filas
        self.obtener_productos()

    # Funcion que ejecuta consultas
    def consultar(self, query, parametros = ()):
        cursor = cnx.cursor(buffered=True)
        try:
            query = cursor.execute(query, parametros)
            cnx.commit()
            cursor.close()
        except Exception as error:
            print(error)
        return query

    # Obtener productos de la base de datos
    def obtener_productos(self):
        # limpiar tabla
        records = self.tree.get_children()
        cursor = cnx.cursor(buffered=True)
        for element in records:
            self.tree.delete(element)
        # obtener data
        query = "SELECT id,nombre,precio,stock FROM productos ORDER BY id DESC"
        cursor.execute(query)
        db_rows = cursor.fetchall()
        # llenando data
        if db_rows != None:
            for row in db_rows:
                self.tree.insert('', 0, text = row[0], values = [row[1], row[2], row [3]])

    # Validacion
    def validacion(self):
        return len(self.name.get()) != 0 and len(self.price.get()) != 0

    def anadir_producto(self):
        if self.validacion():
            query = "INSERT INTO productos (id,nombre,precio,stock) VALUES (NULL,%s,%s,%s)"
            parametros =  (self.name.get(), self.price.get(), self.stock.get())
            self.consultar(query, parametros)
            self.message['text'] = 'Producto {} añadido'.format(self.name.get())
            self.name.delete(0, END)
            self.price.delete(0, END)
            self.stock.delete(0, END)
        else:
            self.message['text'] = 'Se requiere un precio, nombre y stock'
        self.obtener_productos()

    def eliminar_producto(self):
        self.message['text'] = ''
        if self.tree.item(self.tree.selection()) == None:
                self.message['text'] = 'Por favor elija un producto'
        else:
            self.message['text'] = ''
            id = self.tree.item(self.tree.selection())["text"]
            query = f'DELETE FROM productos WHERE id = {id}'
            cursor = cnx.cursor(buffered=True)
            cursor.execute(query)
            cnx.commit()
            self.obtener_productos()

    def editar_producto(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['values'][0]
        except IndexError as e:
            self.message['text'] = 'Por favor elija un producto'
            return
        name = self.tree.item(self.tree.selection())['values'][0]
        old_price = self.tree.item(self.tree.selection())['values'][1]
        self.edit_wind = Toplevel()
        self.edit_wind.title = 'Editar producto'
        # Nombre viejo
        Label(self.edit_wind, text = 'Nombre antigüo:').grid(row = 0, column = 1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = name), state = 'readonly').grid(row = 0, column = 2)
        # Nombre nuevo
        Label(self.edit_wind, text = 'Nombre nuevo:').grid(row = 1, column = 1)
        new_name = Entry(self.edit_wind)
        new_name.grid(row = 1, column = 2)

        # precio viejo 
        Label(self.edit_wind, text = 'Precio antigüo:').grid(row = 2, column = 1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = old_price), state = 'readonly').grid(row = 2, column = 2)
        # precio nuevo
        Label(self.edit_wind, text = 'Precio nuevo:').grid(row = 3, column = 1)
        new_price= Entry(self.edit_wind)
        new_price.grid(row = 3, column = 2)

        Button(self.edit_wind, text = 'Actualizar', command = lambda: self.editar_productos(new_name.get(), name, new_price.get(), old_price)).grid(row = 4, column = 2, sticky = W)
        self.edit_wind.mainloop()

    def editar_productos(self, new_name, name, new_price, old_price):
        query = """UPDATE productos SET nombre = %s, precio = %s WHERE nombre = %s AND precio = %s"""
        parametros = (new_name, new_price, name, old_price)
        self.consultar(query, parametros)
        self.edit_wind.destroy()
        self.message['text'] = 'Producto {} actualizado'.format(name)
        self.obtener_productos()

if __name__ == '__main__':
    window = Tk()
    application = Login(window)
    window.mainloop()

cnx.close()