from email.mime import audio
from tkinter import ttk
from tkinter import *
L = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','ñ','o','p','q','r','s','t','u','v','w','x','y','z']
D = [0,1,2,3,4,5,6,7,8,9]
tokens = { 'reserved': 0 ,'identificadores' : 0, 'parentesisApertura': 0, 'parentesisCierre': 0, 'signo':0, 'separador':0, 'tipoDato': 0 }
reservedBasic = ['supr-struct','new-db','supr-db','take']
reservedAdvance = ['new-struct','supr-struct','upd', '>','f']
tiposDato = ['int','varchar', 'bool', 'double']

def deleteValuesToken():
    for i,clave in enumerate(tokens):
        if tokens.get(clave) > 0:
            tokens[clave] = 0
def waiting():
    message.config(text='Waiting for MIBA sentence')

def outputMessageError():
    message.config(text='[ERROR] : Check your MIBA Syntax')

def outputSuccessMessage():
    message.config(text='[OK] : MIBA Sintax Correct')

def showTokens():
    tokensCount.config(text=f'{tokens}')

def principal(sentence):
    aux = sentence.strip().split(' ')
    aux.reverse()
    sentencia = aux
    if sentencia[-1] in reservedBasic:
        BasicSentences(sentencia)
    elif sentencia[-1] in reservedAdvance:
        advanceSetence(sentencia)
    else:
        outputMessageError()
        showTokens()

def BasicSentences(sentencia):
    pila = ['$','R','L']
    verify = False
    bandera = True
    # print(f'Pila entrada: {sentencia} \nPila gramática: {pila}\n')
    # entrada = list(sentencia)
    # entrada.reverse()
    if sentencia[-1] in reservedBasic:
        print('Palabra reservada: ',sentencia.pop(),'\n')
        tokens['reserved']+=1
    else: 
        outputMessageError()
        print('ERROR : No se encuentra palabra reservada')
        showTokens()
        bandera = False
    
    if bandera and len(sentencia)>=1:
        sentence = sentencia
        name = list(sentence.pop())
        # print('Entrada : ',' '.join(name))
        name.reverse()
        print(pila)
        for i in reversed(name):
            # if not i in L or i in D:
            if not i.isalnum():
                print('Error : Caracter no válido (',i,')')
                new = ''.join(reversed(name))
                sentence.append(new)
                verify = False
                break
            else:
                name.pop()
                pila.pop()
                print('Entrada Actual : ',' '.join(reversed(name)), '  - Verificando : ',i)
                print(pila)
                if pila.pop() == 'R':
                    pila.extend(list('RL'))
                    print(pila)
            verify = True
        if verify:
            tokens['identificadores'] += 1
            pila.clear(),pila.append('$'),sentence.append('$')
            outputSuccessMessage()
            showTokens()
            print('\nEntrada Final : ',sentence,' Pila : ',pila,'\nTokens : ',tokens)
        else:
            outputMessageError()
            showTokens()
            print('\nEntrada Final : ',sentence,' Pila : ',pila,'\nTokens : ',tokens)
    else: 
        outputMessageError()
        showTokens()

def advanceSetence(sentencia):
    bandera = True
    verify = False
    pila = ['$',')','T','R','L','(','R','L']
    # entrada = list(sentencia)
    # entrada.reverse()
    print('\n########################## SENTENCIA MIBA ###############################\n')
    if sentencia[-1] in reservedAdvance:
        tokens['reserved'] +=1
        print('Palabra reservada: ',sentencia.pop(), ' [OK]')
    else: 
        print('ERROR : No se encuentra palabra reservada')
        bandera = False

    # print('ENTRADA ADVANCE ', entrada)
    #
    if bandera: 
        nombre = list(sentencia.pop())
        nombre.reverse()
        print('\nNombre de la tabla : ',''.join(reversed(nombre)))
        # print('Pila gramática : ',pila,'\n')
        for i in reversed(nombre):
            if not i.isalnum():
                print('Caracter inválido -> ',i)
                new = ''.join(reversed(nombre))
                sentencia.append(new)
                break
            else:
                nombre.pop(),pila.pop()
                print('Actual : ',''.join(reversed(nombre)), '  - Verificando : ',i,'  [OK]')
                # print('Pila en función : ',pila)
                if pila.pop() == 'R':
                    pila.extend(list('RL'))
                    if not nombre:
                        pila.clear(),pila.extend(list('$)TRL('))
                        # print('Pila gramática : ',pila,'\n')
                        verify = True
                    else:
                        print(f' R - > L R')
        if verify:
            tokens['identificadores']+=1
            firstParent(sentencia, pila) 
        else:
            print('Error Sintaxis inválida')
            print(pila)
            outputMessageError()
            showTokens()

def firstParent(entrada,pila):
    print('###################################################################################')
    print(f'ParentesisApertura : ',entrada[-1],'\n')
    if  len(entrada[-1]) > 1 and pila[-1] == entrada[-1][0]:
        clean = entrada[-1][1::]
        entrada.pop()
        pila.pop()
        entrada.append(clean)
        print('Nueva Entrada : ',entrada)
        tokens['parentesisApertura']+=1
        checkName(entrada, pila)
    elif '(' == entrada[-1]:
        pila.pop(),entrada.pop()
        print('Nueva Entrada : ',entrada)
        tokens['parentesisApertura']+=1
        checkName(entrada, pila)
    else: 
        print('ERROR: Se espera parentesis de apertura ',entrada)
        outputMessageError()
        showTokens()
        print(pila)
        print(f'{tokens}')

def endParentesis(entrada,pila):
    print('###################################################################################')
    print('Parentesis Cierre')
    pila.clear()
    # print('final',entrada[-1][-1])
    if entrada[-1] == ')':
        tokens['parentesisCierre']+=1
        entrada.pop()
        pila.insert(0,'$'),entrada.append('$')
        print(tokens)
        outputSuccessMessage()
        showTokens()
        print()
    elif entrada[-1][-1] == ')':
        tokens['parentesisCierre']+=1
        entrada.pop()
        entrada.append('$')
        pila.append('$')
        outputSuccessMessage()
        showTokens()
        print('\nEntrada Final : ',entrada,' Pila : ',pila,'\n')
        # print('parentesisCierre suma \n Ejecución Ok')j
        # print(f'Entrada end : {entrada} Pila end2 : {pila}')
    else: 
        pila.append(')'),pila.insert(0,'$')
        entrada.pop()
        entrada.insert(0,'$')
        print('\nEntrada Final : ',entrada,' Pila : ',pila,'\n')
        print('\nERROR : Se espera un parenteis de cierre\n')
        outputMessageError()
        showTokens()

def checkName(entrada, pila): # atri int, algo bool)
    if '=' in entrada[-1]:
        pila.clear(),pila.extend(list('$)RL=RL>RL=RL'))
        checknameFix(entrada,pila)
    else:
        print('######################################## Name ##########################################')
        sentence = entrada
        name = list(sentence.pop())
        print('Entrada :',''.join(name))
        name.reverse()
        print(pila)
        for i in reversed(name):
            if not i.isalnum():
                print('Error : Caracter no válido (',i,')')
                new = ''.join(reversed(name))
                sentence.append(new)
                verify = False
                break
            else:
                pila.pop()
                name.pop()
                print('Actual :',''.join(reversed(name)), '  - Verificando : ',i,' [OK]')
                # print('Pila en función : ',pila)
                if pila.pop() == 'R':
                    pila.extend(list('RL'))
                    # print('Pila Gramática : ',pila)
            verify = True
        if verify:
            tokens['identificadores'] += 1
            pila.pop(),pila.pop()
            # print('\nEntrada Name eliminado : ',sentence,' Pila Name: ',pila)
            # return entrada, pila
            checkDato(entrada, pila)
        else: 
            print('Error : Nombre inválido')
            outputMessageError()
            showTokens()
            print(pila)
            print(tokens)
    # else: tokens['identificadores'] = 0

def checknameFix(entrada, pila):
    if '=' in entrada[-1]:
        checkSigno(entrada,pila)
    else:
        print('_########## ##################################### Name Fix-Struct ###############################################')
        # print('entrada',pila)
        sentence = entrada
        name = list(entrada.pop())
        name.reverse()
        for i in reversed(name):
            if not i.isalnum():
                print('Error : Caracter no válido (',i,')')
                new = ''.join(reversed(name))
                sentence.append(new)
                verify = False
                break
            else:
                pila.pop()
                name.pop()
                print('Actual :',''.join(reversed(name)), '  - Verificando : ',i,' [OK]')
                # print('Pila en función : ',pila)
                if pila.pop() == 'R':
                    pila.extend(list('RL'))
                        # print('Pila Gramática
            verify = True
        if verify:
            tokens['identificadores'] += 1
            pila.pop(),pila.pop()
            # print('\nEntrada Name eliminado : ',sentence,' Pila Name: ',pila)
            # return entrada, pila
            # checkDato(entrada, pila)
            checkSigno(entrada,pila)
        else: 
            print('Error : Nombre inválido')
            outputMessageError()
            showTokens()
            print(pila)
            print(tokens)
        print('entrada despues del proceso ',sentence,'  ',entrada )



""" fix-struct nombre (name=valor)  -> fix-struct nombre upd ( nombre = valor )"""

""" HACER UNA COMPARACION PARA VER SU SE MANDA A CHECAR DATO O A VERIFICAR EL VALOR DEL NAME DESPUES DEL IGUAL """
def checkSeparador(entrada,pila):
    # print('Entrada chekSperador : ',entrada[-1], ' Pila check separador : ',pila)
    if len(entrada[-1]) > 1 and entrada[-1][-1] == ',': #CUANDO LLEGA CON TIPO DE DATO
        clean = entrada[-1][0:len(entrada[-1])-1]
        tokens['separador']+=1
        entrada.pop(),entrada.append(clean)
        # print('SALI DE SEPARADOR PARA ENTRAR A CHECKDATO 1-> ',entrada)
        checkDato(entrada, pila)
    elif entrada[-1] == ',':
        tokens['separador']+=1 #ESTE CASO ES CUANDO LLEGA LA COMA SOLA EJ. ','
        entrada.pop()
        # print('SALI DE SEPARADOR PARA ENTRAR A CHECKDATO 2-> ',entrada)
        checkDato(entrada, pila)

""" Función que debe evaluar si tiene signo = """

def checkSigno(entrada, pila):
    if entrada[-1] == '=':
        tokens['signo']+=1
        # checkName(entrada,pila)
    else:
        aux = []
        aux.extend(entrada.pop().split('='))
        aux.insert(1,'='),entrada.extend(aux)
        entrada.reverse()
        checknameFix(entrada,pila)

""" Función que debe evaluar si tiene > en la sentencia """
def checkCondicion(entrada, pila):
    pass

def checkDato(entrada, pila): #int, algo bool)5 
    # print('entrada checkDato : ',entrada ,' checkdatoPila : ',pila)
    # print('Antes del cualquier if de checkdato : ', entrada[-1],'\n')
    if ',' in entrada[-1]:
        # print('Tiene coma pegado al tipo : ',entrada[-1])
        # tokens['tipoDato']+=1
        checkSeparador(entrada, pila)
    elif ')' in entrada[-1] and entrada[-1][0:len(entrada[-1])-1] in tiposDato:
        # print('Tiene parentesis, es único : ',entrada[-1])
        tokens['tipoDato']+=1
        endParentesis(entrada, pila)
    else:
        # print('No tiene coma ni parentesis de cierre, se checa si es un dato válido : ',entrada[-1])
        # print('Size entrada: ',len(entrada))
        if len(entrada) > 1 and len(entrada) <4: # entrada = '$' ')' 'int'
            # print('Size entrada dentro del if de size: ',len(entrada))
            if entrada[-1] in tiposDato:
                # print('Se encontró un tipo parecido = ',entrada[-1])
                tokens['tipoDato'] += 1
                entrada.pop(),pila.pop(),pila.extend(list('TRL'))
                # print('size :',len(entrada), entrada)
                checkName(entrada,pila)
            else:
                print('No se encontró un tipo')
                outputMessageError()
                showTokens()
                print(pila)
                print(tokens)
        else:
            # print('QUE ES ENTRADA ',entrada[-1])
            if not len(entrada)< 2:
                if entrada[-1] in tiposDato:
                    tokens['tipoDato']+=1
                    entrada.pop(),pila.pop(),pila.extend(list('TRL'))
                    # print('Entra al else porque no es el ultimo : ',entrada,'\nPIla: ',pila)
                    checkName(entrada,pila)
                else: 
                    print('Tipo no valido: ' ,entrada[-1])
                    print(pila)
                    print(tokens)
                    outputMessageError()
                    showTokens()
            else: 
                tokens['tipoDato']+=1
                endParentesis(entrada,pila)


def run():
    root = Tk()
    root.title("MIBA SQL Analizador")
    root.geometry('1500x500')

    lbl = Label(root,text="Ingresa la sentencia de MIBA",font=('Roboto 16 ') )
    lbl.pack(pady=(100,0))
    text=Entry(root, font = ('Roboto 15'),width=50)
    text.insert(END, "")
    text.pack(pady=30)
    message2 = Label(root,font=('Roboto 14 bold'), text="Waiting for MIBA sentence...")
    message2.pack()


    def getValues():
        message2.config(text='')
        deleteValuesToken()
        sentence = text.get()
        aux = sentence.split(' ')
        if not len(aux) == 1:
            principal(sentence)
        else: 
            # deleteValuesToken()
            outputMessageError()
            showTokens()

    btn = Button(root,text='Analizar',bg='green',fg='white' ,padx=70,pady=8,command=getValues)
    btn.pack(pady=30)
    global message
    global tokensCount
    message = Label(root,font=('Roboto 14 bold'), text="")
    message.pack()
    tokensCount = Label(root,font=('Roboto 14 bold'), text='')
    tokensCount.pack()
    root.mainloop()

run()


