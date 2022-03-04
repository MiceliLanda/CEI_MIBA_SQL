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
    print('\nNombre de la tabla : ',''.join(reversed(nombre)))
    print('Pila gramática : ',pila,'\n')
    for i in reversed(nombre):
        if not i.isalnum():
            print('Caracter inválido crack  mira crack-> ',i)
            new = ''.join(reversed(nombre))
            entrada.append(new)
        else:
            nombre.pop(),pila.pop()
            print('Actual : ',' '.join(reversed(nombre)), '  - Verificando : ',i)
            print(pila)
            if pila.pop() == 'R':
                pila.extend(list('RL'))
                if not nombre:
                    pila.clear(),pila.extend(list('$)TRL('))
                    print('Pila gramática : ',pila,'\n')
                else: print('R - > L')
    # pila.pop(),pila.pop()
    # print('LO QUE SE VA AL firstParent -> ',entrada , pila)
    firstParent(entrada, pila)  

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
        pila.append('$'),entrada.append('$')
        print(f'Entrada end : {entrada} Pila end : {pila}')
    elif entrada[-1][-1] == ')':
        entrada.pop()
        entrada.append('$')
        pila.append('$')
        print('parentesisCierre suma \n Ejecución Ok')
        print(f'Entrada end : {entrada} Pila end2 : {pila}')
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
            print('Entrada Actual :',''.join(reversed(name)), '  - Verificando : ',i)
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

    print('Entrada chekSperador : ',entrada[-1], ' Pila check separador : ',pila)
    if len(entrada[-1]) > 1 and entrada[-1][-1] == ',': #CUANDO LLEGA CON TIPO DE DATO
        clean = entrada[-1][0:len(entrada[-1])-1]
        entrada.pop(),entrada.append(clean)
        print('SALI DE SEPARADOR PARA ENTRAR A CHECKDATO 1-> ',entrada)
        checkDato(entrada, pila)
    elif entrada[-1] == ',': #ESTE CASO ES CUANDO LLEGA LA COMA SOLA EJ. ','
        entrada.pop()
        print('SALI DE SEPARADOR PARA ENTRAR A CHECKDATO 2-> ',entrada)
        checkDato(entrada, pila)

def checkDato(entrada, pila): #int, algo bool)5 
    # print('entrada checkDato : ',entrada ,' checkdatoPila : ',pila)
    print('Antes del cualquier if de checkdato : ', entrada[-1],'\n')
    if ',' in entrada[-1]:
        print('Tiene coma pegado al tipo : ',entrada[-1])
        checkSeparador(entrada, pila)
    elif ')' in entrada[-1] and entrada[-1][0:len(entrada[-1])-1] in tiposDato:
        print('Tiene parentesis, es único : ',entrada[-1])
        endParentesis(entrada, pila)
    else:
        print('No tiene coma ni parentesis de cierre, se checa si es un dato válido : ',entrada[-1])
        # print('Size entrada: ',len(entrada))
        if len(entrada) > 1 and len(entrada) <4: # entrada = '$' ')' 'int'
            # print('Size entrada dentro del if de size: ',len(entrada))
            if entrada[-1] in tiposDato:
                print('Se encontró un tipo parecido = ',entrada[-1])
                entrada.pop(),pila.pop(),pila.extend(list('TRL'))
                print('size :',len(entrada), entrada)
                checkName(entrada,pila)
            else:
                print('No se encontró un tipo, eliminado y Termina')
        else:
            print('QUE ES ENTRADA ',entrada[-1])
            if entrada[-1] in tiposDato:
                entrada.pop(),pila.pop(),pila.extend(list('TRL'))
                print('Entra al else porque no es el ultimo : ',entrada,'\nPIla: ',pila)
                checkName(entrada,pila)
            else: 
                print('Tipo no valido: ' ,entrada[-1])

#""" ME QUEDÉ EN VERIFICAR SI EL ULTIMO ELEMENTO DE LA ENTRADA ES SOLO COMA IF 139 """

advanceSetence('new-struct Alumnos (atri1 int, atri2 bool, atri3 varchar, asd double)'.strip(' ').lower().split(' '))

