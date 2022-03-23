
identificadores = ['new-struct Alumnos (b varchar','edad varchar','matricula bool)'] #separado por comas

def processNS(sentencia):
    check = len(sentencia)
    i = 0
    entrada = []
    for elemento in sentencia:
        i+=1
        elemento = elemento.strip(' ')
        # print(f'vali {i} {check}')
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
            final = "".join((elemento,' '))
            entrada.append(final)
        else:
            entrada.append(elemento)
        
    entrada = ''.join(entrada)
    # print('1er -> ',entrada)
    entrada = entrada.split(' ')
    executar(entrada)

def executar(valor):
    # final = []
    valor.pop(0) #ELIMI
    script = f'create table {valor.pop(0)}'
    valor.reverse()
    size = round((len(valor)/2))
    # print('size:',size,len(valor),valor)
    if len(valor)==2:
        script += (f'{valor.pop()} {valor.pop()};')
    if len(valor) > 3:    
        for atri in range(size):
            # print(atri,size-1,len(valor)-1,valor)
            if atri == size-1:
                # print('if atri == len(valor)-1')
                script +=(f' {valor.pop()} {valor.pop()};')
                # break
            else:
                # print('else atri == len(valor)-1')
                script +=(f' {valor.pop()} {valor.pop()},')
                # break
    if len(valor) > 2:
        script += (f' {valor.pop()} {valor.pop()}{valor.pop()};')
    # else:
        # script += (f'{valor.pop()} {valor.pop()};')
    print('Sentencia final : ',script)

# entrada = input().split(',')
processNS(identificadores)


