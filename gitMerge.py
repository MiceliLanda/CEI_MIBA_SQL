# # """ 
# # S -> G B
# # G -> git merge
# # B -> L R | D R | E R
# # L -> a..z, A..Z
# # D -> 0..9
# # E -> / , _ , -
# # R -> L R | D R | E R | vacío
# # """
# # from tkinter import ttk
# # from tkinter import *

# # def S(entrada):
# #     comando = G(entrada)
# #     if comando:
# #         B(comando)
# #     else:
# #         message.config(text='[Error] : Bad command git')

# # def G(term):
# #     if len(term)>=3:
# #         if term.pop(0) == 'git' and term.pop(0) == 'merge':
# #             return list(term.pop())
# #         else: 
# #             return ''
# #     else:
# #         message.config(text='[Error] : Bad command git')

# # def B(name):
# #     E = ['/','_','-']   
# #     if name:
# #         if name[0].isalnum() or name[0] in E:
# #             name.pop(0)
# #             B(name)
# #         else : 
# #             message.config(text=f'[Error] : Invalid Character : {name[0]}')
# #     else:
# #         message.config(text='[OK] : Instrucción válida')

# # def run():
# #     root = Tk()
# #     root.title("Git Merge")
# #     root.geometry('1500x500')
# #     lbl = Label(root,text="Ingresa la instrucción",font=('Roboto 16 ') )
# #     lbl.pack(pady=(100,0))
# #     text=Entry(root, font = ('Roboto 15'),width=50)
# #     text.insert(END, "")
# #     text.pack(pady=30)

# #     def getvalues():
# #         linea = text.get()
# #         if linea:
# #             S(linea.strip().split(' '))
# #         else:
# #             message.config(text='Campos obligatorios')

# #     btn = Button(root,text='Analizar',bg='green',fg='white' ,padx=70,pady=8,command=getvalues)
# #     btn.pack(pady=30)
# #     global message
# #     message = Label(root,font=('Roboto 14 bold'), text="")
# #     message.pack()
# #     root.mainloop()

# # run()
import pymysql as sql
from configparser import ConfigParser
config = ConfigParser()
config.read("config.ini")
server = config["mysql"]


tokens = {'id':0 , 'tipo':0 , 'sep':0}
reservedBasic = ['supr-struct','new-db','supr-db','take']

def executar(valor):
    
    if valor[0] in reservedBasic:
        if valor[0] == 'new-db':
            ExecuteMiba(f'create database {valor[-1]};')

        if valor[0] == 'take':
            ExecuteMiba(f'use {valor[-1]};')

        if valor[0] == 'supr-struct':
            ExecuteMiba(f'drop table {valor[-1]};')

        if valor[0] == 'supr-db':
            ExecuteMiba(f'drop database {valor[-1]};')
    else: 
        print('ERROR NO EXISTE')

    """ QUEDA PENDIENTE EL DE CREAR TABLA PARA QUE SE CHEQUE CUANTOS ATRIBUTOS LLEVA, QUE SEA DINÁMICO """
    # if valor[0] == 'new-struct':
    #     ExecuteMiba(f'create table;')
    

def ExecuteMiba(valor):
    try:
        con = sql.connect(host = server['server'],user = server['username'],password = server['password'],database = server['database'])
        print(f'Conexion Ok')
        try:
            with con.cursor() as send:
                send.execute(valor)
            print('[OK] : Querie Ejecutada')
            con.commit()
        finally:
            """ Cerrar conexión """
            con.close()

    except (sql.err.OperationalError, sql.err.InternalError) as e:
        print(f'\nMIBA SQL Error : {e}')

executar(input('\n\nIngrese la sentencia MIBA Sql: ').lower().split(' '))

