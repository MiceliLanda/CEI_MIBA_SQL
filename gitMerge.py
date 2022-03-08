""" 
S -> G B
G -> git merge
B -> L R | D R | E R
L -> a..z, A..Z
D -> 0..9
E -> / , _ , -
R -> L R | D R | E R | vacío
"""
from tkinter import ttk
from tkinter import *

def S(entrada):
    comando = G(entrada)
    if comando:
        B(comando)
    else:
        message.config(text='[Error] : Bad command git')

def G(term):
    if len(term)>=3:
        if term.pop(0) == 'git' and term.pop(0) == 'merge':
            return list(term.pop())
        else: 
            return ''
    else:
        message.config(text='[Error] : Bad command git')

def B(name):
    E = ['/','_','-']   
    if name:
        if name[0].isalnum() or name[0] in E:
            name.pop(0)
            B(name)
        else : 
            message.config(text=f'[Error] : Invalid Character : {name[0]}')
    else:
        message.config(text='[OK] : Instrucción válida')

def run():
    root = Tk()
    root.title("Git Merge")
    root.geometry('1500x500')
    lbl = Label(root,text="Ingresa la instrucción",font=('Roboto 16 ') )
    lbl.pack(pady=(100,0))
    text=Entry(root, font = ('Roboto 15'),width=50)
    text.insert(END, "")
    text.pack(pady=30)

    def getvalues():
        linea = text.get()
        if linea:
            S(linea.strip().split(' '))
        else:
            message.config(text='Campos obligatorios')

    btn = Button(root,text='Analizar',bg='green',fg='white' ,padx=70,pady=8,command=getvalues)
    btn.pack(pady=30)
    global message
    message = Label(root,font=('Roboto 14 bold'), text="")
    message.pack()
    root.mainloop()

run()