L = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','ñ','o','p','q','r','s','t','u','v','w','x','y','z']
D = [0,1,2,3,4,5,6,7,8,9]
tokens = { 'reserved': 0 ,'identificadores' : 0 }
reservedBasic = ['supr-struct','new-db','supr-db','take']

def BasicSentences(sentencia):
    pila = ['$','R','L']
    verify = False
    entrada = list(sentencia)
    entrada.reverse()
    if entrada.pop() in reservedBasic:
        tokens['reserved']+=1
    else: 
        print('ERROR : No se encuentra palabra reservada')

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
        else :
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
BasicSentences(('take nombre $'.strip(' ').lower().split(' ')))