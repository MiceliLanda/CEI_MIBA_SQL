
L = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','ñ','o','p','q','r','s','t','u','v','w','x','y','z']
D = [0,1,2,3,4,5,6,7,8,9]
tokens = { 'reserved': 0 ,'identificadores' : 0, 'parentesisApertura': 0, 'parentesisCierre': 0, 'signo':0, 'separador':0, 'tipoDato': 0 }
reservedBasic = ['supr-struct','new-db','supr-db','take']
reservedAdvance = ['new-struct','supr-struct','upd', '>']
tiposDato = ['int','varchar', 'bool', 'double']

def BasicSentences(sentencia):
    pila = ['$','R','L']
    verify = False
    bandera = True
    entrada = list(sentencia)
    entrada.reverse()
    if entrada.pop() in reservedBasic:
        tokens['reserved']+=1
    else: 
        print('ERROR : No se encuentra palabra reservada')
        bandera = False
    
    if bandera:
        sentence = entrada
        name = list(sentence.pop())
        print('Entrada : ',' '.join(name))
        name.reverse()
        print(pila)
        for i in reversed(name):
            if not i in L or i in D:
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
            pila.clear(),pila.append('$')
        else: tokens['identificadores'] = 0
        print('\nEntrada Final : ',sentence,' Pila : ',pila,'\nTokens : ',tokens)

def advanceSetence(sentencia):
    bandera = True
    verify = False
    pila = ['$',')','T','R','L','(','R','L']
    entrada = list(sentencia)
    entrada.reverse()
    print('\n########################## SENTENCIA MIBA ###############################\n')
    if entrada[-1] in 'new-struct':
        tokens['reserved'] +=1
        print('Palabra reservada: ',entrada.pop(), ' [OK]')
    else: 
        print('ERROR : No se encuentra palabra reservada')
        bandera = False

    # print('ENTRADA ADVANCE ', entrada)
    #
    if bandera: 
        nombre = list(entrada.pop())
        nombre.reverse()
        print('\nNombre de la tabla : ',''.join(reversed(nombre)))
        # print('Pila gramática : ',pila,'\n')
        for i in reversed(nombre):
            if not i.isalnum():
                print('Caracter inválido -> ',i)
                new = ''.join(reversed(nombre))
                entrada.append(new)
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
            firstParent(entrada, pila) 
        else:
            print('Error Sintaxis inválida')
            print(pila)
            print(tokens)

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
        print(pila)
        print(f'{tokens}')

def endParentesis(entrada,pila):
    print('###################################################################################')
    print('Parentesis Cierre: ',entrada[-1])
    pila.clear()
    # print('final',entrada[-1][-1])
    if entrada[-1] == ')':
        # print('parentesisCierre suma \n Ejecución Ok')
        tokens['parentesisCierre']+=1
        entrada.pop()
        pila.append('$'),entrada.append('$')
        # print(f'Entrada end : {entrada} Pila end : {pila}')
        print(tokens)
    elif entrada[-1][-1] == ')':
        tokens['parentesisCierre']+=1
        entrada.pop()
        entrada.append('$')
        pila.append('$')
        print(tokens)
        # print('parentesisCierre suma \n Ejecución Ok')
        # print(f'Entrada end : {entrada} Pila end2 : {pila}')
    else: 
        pila.append('$')
        print(pila)
        print('\nERROR : Se espera un parenteis de cierre\n',tokens)

def checkName(entrada, pila): # atri int, algo bool)
    print('######################################## Name ##########################################')
    sentence = entrada
    name = list(sentence.pop())
    print('Entrada : ',''.join(name))
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
            else: 
                tokens['tipoDato']+=1
                endParentesis(entrada,pila)
# BasicSentences(('take nombre $'.strip(' ').lower().split(' ')))

advanceSetence('new-struct b (nombre bool)'.lower().strip().split(' '))

