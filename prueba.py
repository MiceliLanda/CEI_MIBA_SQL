tiposDato = ['int','varchar', 'bool', 'double']

def advanceSetence(sentencia):
    pila = ['$',')','T','R','L','(','R','L']
    entrada = list(sentencia)
    entrada.reverse()
    if entrada.pop() in 'new-struct':
        print('Reserved : 1')
    else: 
        print('ERROR : No se encuentra palabra reservada')

    print('ENTRADA ADVANCE ', entrada)
    #
    nombre = list(entrada.pop())
    nombre.reverse()
    for i in reversed(nombre):
        if not i.isalnum():
            print('Caracter inválido crack  mira crack-> ',i)
            new = ''.join(reversed(nombre))
            entrada.append(new)
        else:
            nombre.pop(),pila.pop()
            print('Entrada Actual : ',' '.join(reversed(nombre)), '  - Verificando : ',i)
            print(pila)
            if pila.pop() == 'R':
                pila.extend(list('RL'))
                print(pila)
    pila.pop(),pila.pop()
    # print('LO QUE SE VA AL firstParent -> ',entrada , pila)
    firstParent(entrada, pila)  
        
    # print(new)
# advanceSetence(('new nombre (atri int) $'.strip(' ').lower().split(' ')))
""" advanceSetence(('new nombre (atri int, atri2 varchar) $'.strip(' ').lower().split(' ')))
pila = ['$',',',')','td','name','(']
entrada = ['varchar)','atri2','int,','atri','(']
entrada = ['varchar)','atri2','int,','(atri'] """


def firstParent(entrada,pila):
    if  len(entrada[-1]) > 1 and pila[-1] == entrada[-1][0]:
        clean = entrada[-1][1::]
        entrada.pop()
        pila.pop()
        entrada.append(clean)
        print('if 1 : ',entrada)
        checkName(entrada, pila)
    elif '(' == entrada[-1]:
        pila.pop(),entrada.pop()
        print('if 2: ',entrada)
        checkName(entrada, pila)
    else: 
        print('ERROR: Se fue alv todo, naah mentira crack , solo no pusiste parentesis')

def endParentesis(entrada,pila):
    pila.clear()
    print('final',entrada[-1][-1])
    if entrada[-1] == ')':
        print('parentesisCierre suma \n Ejecución Ok')
        entrada.pop()
        pila.append('$')
    elif entrada[-1][-1] == ')':
        entrada.pop()
        entrada.append('$')
        print('parentesisCierre suma \n Ejecución Ok')
    else: print('ERROR : Se espera un parenteis de cierre')

def checkName(entrada, pila): # atri int, algo bool)
    sentence = entrada
    name = list(sentence.pop())
    print('Entrada : ',''.join(name))
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
        # tokens['identificadores'] += 1
        print('Indentificador 1')
        pila.pop(),pila.pop()
        print('\nEntrada Name eliminado : ',sentence,' Pila Name: ',pila)
        # return entrada, pila
        checkDato(entrada, pila)
    else: print('Indentificador 0')
        
    # else: tokens['identificadores'] = 0
def checkSeparador(entrada,pila):
    """ CHECAR QUE AUMENTE EL CONTADOR DE SEPARADOR EN EL DE TOKENS """

    print('Entrada chekSperador : ',entrada, ' Pila check separador : ',pila)
    if len(entrada[-1]) > 1 and entrada[-1][-1] == ',': #CUANDO LLEGA CON TIPO DE DATO
        clean = entrada[-1][0:len(entrada[-1])-1]
        entrada.pop(),entrada.append(clean)
        print('SALI DE SEPARADOR PARA ENTRAR A CHECKDATO -> ',entrada)
        checkDato(entrada, pila)
    elif entrada[-1] == ',': #ESTE CASO ES CUANDO LLEGA LA COMA SOLA EJ. ','
        entrada.pop()
        print('SALI DE SEPARADOR PARA ENTRAR A CHECKDATO -> ',entrada)
        checkDato(entrada, pila)

def checkDato(entrada, pila): #int, algo bool)
    # print('entrada checkDato : ',entrada ,' checkdatoPila : ',pila)
    print('130 ',entrada[-1][-1::])
    if (entrada[0] and entrada[0][-1::]) == ')' and len(entrada) <=1:
        if entrada[-1] in tiposDato:
            print('eliminarlo nomás -> ', entrada[-1])# TIENE PARENTESIS SOLO EN ENTRADADA.POP
            entrada.pop(),pila.pop(),endParentesis(entrada, pila)
        elif entrada[-1][0:len(entrada[-1])-1] in tiposDato: # TIENE PARENTESIS PEGADO AL TIPO DE DATO
            tipo = entrada[-1][-1::]
            print('Elif 113 pegado al tipo -> ',entrada[-1])
            # new = entrada[-1][0:len(entrada[-1])-1
            endParentesis(entrada, pila)
        else: 
            print('No existe el tipo de dato ',entrada[-1][0:len(entrada[-1])-1])
    elif (entrada[-1] and entrada[-1][-1::]) == ',':    
        """ CHECAR QUE SE ELIMINE LA PILA TAQMBIÉN """
        checkSeparador(entrada, pila)
    elif entrada[-1] in tiposDato:
        entrada.pop(),pila.pop()
        print('Nueva entrada despues de check separador -> ',entrada,'  PIla -> ',pila)
        if (entrada[-1] or entrada[-1][-1::]) == ',':
            checkSeparador(entrada, pila)
        else: 
            pila.extend(list('TRL'))
            checkName(entrada, pila)
    elif entrada[-1].isalnum():
        pila.extend(list('TRL'))
        checkName(entrada, pila)
    else: 
        print('ERROR: No tiene parentesis de cierre')

advanceSetence('new-struct nombre (a int , b double, c varchar )'.strip(' ').lower().split(' '))

""" pila, entrada , value = firstParent(['double)','atri3','varchar','atri2','int,','(atri'],['$',',)','T','R','L','('])
checkName(entrada,pila) """
