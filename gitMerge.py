""" 
S -> G B
G -> git merge
B -> L R | D R | E R
L -> a..z, A..Z
D -> 0..9
E -> / , _ , -
R -> L R | D R | E R | vacío
"""

def S(entrada):
    comando = G(entrada)
    if comando:
        B(comando)
    else:
        print('Error command git')

def G(term):
    if term.pop(0) == 'git' and term.pop(0) == 'merge':
        return list(term.pop())
    else: 
        return ''

def B(name):
    E = ['/','_','-']   
    for element in name:
        if element.isalpha() or element in E:
            pass
            # print('L|D|E : ',element)
        else : 
            print('Error Invalid Character : ',element)
            break
    print('OK')


S('git merge branch'.strip().split(' '))