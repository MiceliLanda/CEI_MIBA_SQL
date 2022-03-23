from tkinter import ttk
from tkinter import *
import pymysql as sql
from configparser import ConfigParser
config = ConfigParser()
config.read("config.ini")
server = config["mysql"]

tokens = { 'reserved': 0 ,'identificadores' : 0, 'parentesisApertura': 0, 'parentesisCierre': 0, 'signo':0, 'separador':0, 'tipoDato': 0 }
reservedBasic = ['supr-struct','new-db','supr-db','take']
reservedAdvance = ['new-struct']
tiposDato = ['int','varchar', 'bool', 'double']

def processNS(sentencia):
    check = len(sentencia)
    i=0
    entrada = []
    for elemento in sentencia:
        i+=1
        elemento = elemento.strip(' ')

        if len(sentencia) < 2:
            if 'varchar' in elemento or 'bool' in elemento:
                elemento = elemento.replace('varchar','varchar(255)')
                elemento = elemento.replace('bool','bit')
        else: 
            if check == i:
                elemento = elemento.replace('varchar','varchar(255)')
                elemento = elemento.replace('bool','bit')
            else:   
                elemento = elemento.replace('bool','bit')
                elemento = elemento.replace('varchar','varchar(255) ')

        if not ')' in elemento:
            print(elemento,'en el parentesis del not')
            final = "".join((elemento,' '))
            entrada.append(final)
        else:
            # print(elemento,'en el else parentesis del not')
            entrada.append(elemento)

    entrada = ''.join(entrada)
    entrada = entrada.split(' ')
    entrada.pop(0) #ELIMI
    print(entrada,' despues del split')
    script = f'create table {entrada.pop(0)}'
    entrada.reverse()
    size = round((len(entrada)/2))
    print(size,len(entrada))
    if len(entrada)==2:
        script += (f' {entrada.pop()} {entrada.pop()};')
    if len(entrada) > 3:    
        for atri in range(size):
            # print(atri,size-1,len(entrada)-1,entrada)
            if atri == size-1:
                # print('if atri == len(entrada)-1')
                script +=(f' {entrada.pop()} {entrada.pop()};')
                # break
            else:
                # print('else atri == len(entrada)-1')
                script +=(f' {entrada.pop()} {entrada.pop()},')
                # break
    if len(entrada) > 2:
        script += (f' {entrada.pop()} {entrada.pop()}{entrada.pop()};')

    executar(script)

def executar(valor):
    print(valor,' valor')
    if valor[0] in reservedBasic:
        if valor[0] == 'new-db':
            print(f'create database {valor[-1]}')
            ExecuteMiba(f'create database {valor[-1]};')

        if valor[0] == 'take':
            ExecuteMiba(f'use {valor[-1]};')

        if valor[0] == 'supr-struct':
            ExecuteMiba(f'drop table {valor[-1]};')

        if valor[0] == 'supr-db':
            ExecuteMiba(f'drop database {valor[-1]};')
    else:
        ExecuteMiba(valor)

def ExecuteMiba(query):
    try:
        con = sql.connect(host = server['server'],user = server['username'],password = server['password'],database = server['database'])
        print(f'Conexion Ok')
        try:
            with con.cursor() as send:
                send.execute(query)
            con.commit()
        finally:
            """ Cerrar conexión """
            con.close()
            showExecutedMIBA('[OK] : MIBA Query Executed Successfully')

    except (sql.err.OperationalError, sql.err.InternalError, sql.err.ProgrammingError, sql.err.Error, sql.err.DatabaseError,sql.err.MySQLError) as e:
        showExecutedMIBA(f'[ERROR] : MIBA SQL: {e}')

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

def showExecutedMIBA(result):
    mibaMessage.config(text=result)

def showTokens():
    token = f"""    \n      Tokens:\n
                Palabras reservadas : {tokens.get('reserved')}\n
                Identificadores : {tokens.get('identificadores')}\n
                Parentesís de Apertura : {tokens.get('parentesisApertura')}\n
                Separador : {tokens.get('separador')}\n
                Tipo de Dato : {tokens.get('tipoDato')}\n
                Parentesís de Cierre : {tokens.get('parentesisCierre')}"""
    lblToken.insert(END,token)

def runSentence(aux):
    sentencia = aux
    if sentencia[-1] in reservedBasic:
        BasicSentences(sentencia)
    elif sentencia[-1] in reservedAdvance:
        advanceSetence(sentencia)
    else:
        tokens['identificadores']+=2
        outputMessageError()
        showTokens()

def principal(sentence):
    aux = sentence.strip().split(' ')
    if ')' in aux:
        aux.pop()
        aux.insert(len(aux),f'{aux[-1]})')
        aux.pop(-2)
        aux.reverse()
        runSentence(aux)
    else:
        aux.reverse()
        runSentence(aux)
        
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
        tokens['identificadores']+=1
        showTokens()
        bandera = False
    
    if bandera and len(sentencia)>=1:
        sentence = sentencia
        name = list(sentence.pop())
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
            executar(identificadores)
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
        # print(f'{tokens}')

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
        # print(identificadores,' en endparentesis')
        # executar(identificadores)
        processNS(identificadores)
    elif entrada[-1][-1] == ')':
        tokens['parentesisCierre']+=1
        entrada.pop()
        entrada.append('$')
        pila.append('$')
        outputSuccessMessage()
        showTokens()
        print('\nEntrada Final : ',entrada,' Pila : ',pila,'\n')
        # print(identificadores,' en endparentesis')
        processNS(identificadores)
        # executar(identificadores)
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
        # checknameFix(entrada,pila)
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

def checkDato(entrada, pila): #int, algo bool)5 
    # print('entrada checkDato : ',entrada ,' checkdatoPila : ',pila)
    print('Antes del cualquier if de checkdato : ', entrada[-1],'\n')
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
                tokens['identificadores']+=1
                outputMessageError()
                showTokens()
                print(pila)
                # print(tokens)
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
                    tokens['identificadores']+=1
                    # print(tokens)
                    outputMessageError()
                    showTokens()
            else: 
                if entrada[-1] in tiposDato:
                    tokens['tipoDato']+=1
                    endParentesis(entrada,pila)
                    outputSuccessMessage()
                    showTokens()
                else: 
                    tokens['identificadores']+=1
                    outputMessageError()
                    showTokens()

def run():
    root = Tk()
    root.title("MIBA SQL Analizador")
    root.geometry('1100x900')

    lbl = Label(root,text="Ingresa la sentencia de MIBA",font=('Roboto 16 ') )
    lbl.place(x=400,y=20)
    # lbl.pack(pady=(100,0))
    text=Entry(root,font = ('Roboto 15'),width=60)
    text.place(x=150,y=70)
    message2 = Label(root,font=('Roboto 14 bold'), text="Waiting for MIBA sentence...")
    message2.place(x=400,y=130)
    
    def getValues():
        aux = []
        message2.config(text='')
        message.config(text='')
        lblToken.delete(1.0,END)
        mibaMessage.config(text='')
        deleteValuesToken()
        identificadores.clear()
        sentence = text.get()

        """ CHECAR IF """

        if '(' in sentence or ')' in sentence or ',' in sentence:
            print('tiene signos ',aux)
            identificadores.extend(sentence.split(','))
        else:
            aux = sentence.split(' ')
            print('llena el identificador ',aux)
            identificadores.extend(aux)


        if not len(aux) == 1:
            principal(sentence)
        else: 
            outputMessageError()
            showTokens()

    btn = Button(root,text='Analizar',bg='green',fg='white' ,height=2, padx=70,pady=8,command=getValues)
    btn.place(x=450,y=800)
    # btn.pack(pady=30)
    global message
    global identificadores
    global mibaMessage
    global lblToken
    identificadores = []
    lblToken = Text(root,font = ('Roboto 15 bold'),height=15,width=40)
    lblToken.place(x=250,y=170)
    lblToken.insert(END,'\n     Tokens:')
    message = Label(root,font=('Roboto 16 bold'), text="")
    message.place(x=350,y=580)
    message.config(text='       Sintáctico:')
    mibaMessage = Label(root,font=('Roboto 16 bold'), text="        Semántico :")
    mibaMessage.place(x=350,y=650)
    root.mainloop()

run()


