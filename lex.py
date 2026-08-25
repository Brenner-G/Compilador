import time
def ler_arquivo(caminho):
    try:
        with open(caminho, 'r') as f:
            conteudo = f.read()
        return conteudo
    except FileNotFoundError:
        print("File not found!")

caracter = [':','<',';',',','=','+','-','*','/','"']
caracter_abertura = ['{','(']
caracter_fechamento = ['}',')']
reservada = ['class','inherits','if','then','else','while','loop','pool','let','in','case','of','esac','new','isvoid',]
booleano = ['true','false']

simbolos = {
            '{':	'LBRACE',
            '}':	'RBRACE',
            '(':	'LPAREN',
            ')':	'RPAREN',
            ':':	'COLON',
            ';':	'SEMI',
            ',':	'COMMA',
            '<-':   'ASSIGN',
            '<=':   'LE',
            '<':    'LT',
            '=':    'EQ',
            '+':    'PLUS',
            '-':    'MINUS',
            '*':    'TIMES',
            '/':    'DIVIDE',
            '@':    'AT'
}

def tipagem(lexema):
    tipo = None
    if lexema in booleano:
        tipo = 'Bool'
    elif lexema.lower() in reservada:
        tipo = 'palavra reservada'
    elif lexema.isdigit():
        tipo = 'Int'
    elif lexema[0].isupper():
        tipo = 'TYPE_ID'
    elif lexema[0].islower() or lexema[0] == '_':
        tipo = 'OBJECT_ID'
    elif lexema[0] == '"':
        tipo = 'String'
    elif lexema in simbolos:
        tipo = simbolos[lexema]      
    return tipo


def lex(codigo,pos,linha):
    while pos < tamanho and (codigo[pos].isspace() or (codigo[pos] == '-' and pos < tamanho-1 and codigo[pos+1] == "-") or (codigo[pos] == '(' and pos < tamanho-1 and codigo[pos+1] == '*')):
        if codigo[pos].isspace():
            if codigo[pos] == '\n':
                linha += 1
            pos +=1
        elif codigo[pos] == '-':
            pos = pos + 2
            while pos < tamanho and not codigo[pos] == '\n':
                pos += 1 
        else:
            pos = pos + 2
            while pos < tamanho-1 and (not codigo[pos] == '*' or not codigo[pos+1] == ')'):
                pos += 1
            pos +=2

    
    if pos >= tamanho:
        return None,None, pos, linha


    inicio = pos
    
    if codigo[pos] in caracter:
        if codigo[pos] == '"':
            pos += 1
            while pos < tamanho and not codigo[pos] == '"':
                pos += 1            
            if pos < tamanho:
                pos += 1
            elif pos == tamanho:
                print("String não finalizada, falta o fecha aspas")
        elif codigo[pos] == "<":
            if pos < tamanho-1 and (codigo[pos+1] == '-' or codigo[pos+1] == '=') :
                pos = pos + 2
            else:
                pos += 1
        else:
            pos += 1

    elif codigo[pos] in caracter_abertura:
        pos += 1

    elif codigo[pos] in caracter_fechamento:
        pos += 1


    elif codigo[pos].isdigit():
        while pos < tamanho and codigo[pos].isdigit():
            pos += 1
    elif codigo[pos].isalnum() or codigo[pos] == '_':
        while pos < tamanho and (codigo[pos].isalnum() or codigo[pos] == '_' ):
            pos += 1
    else:
        print(f"Lexema: {codigo[pos]} não encontrado")
        return None,None, pos, linha

    
    lexema = codigo[inicio:pos]
    if lexema:
        tipo = tipagem(lexema)
    return tipo,lexema, pos, linha



codigo = ler_arquivo("teste.cl")
pos = 0
linha = 1
tamanho = len(codigo)
i=0
tipo=""

while pos < tamanho:
    tipo,lexema,pos,linha = lex(codigo,pos,linha)
    print(f"Lexema: {lexema}, Tipo {tipo}, Linha: {linha}")
    if lexema == None:
        break

