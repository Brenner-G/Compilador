# algoritimo de descida recursiva
# atenção a recursão a esquerda
from lex import tokenizar

def ler_arquivo(caminho):
    try:
        with open(caminho, 'r') as f:
            conteudo = f.read()
        return conteudo
    except FileNotFoundError:
        print("File not found!")

class ErroSintatico(Exception):
    pass

class Parser:
    def __init__(self,tokens):
        self.tokens = tokens
        self.pos = 0
    
    def peek(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        else:
            return None

    def avancar(self):
        tokens = self.peek()
        self.pos += 1
        return tokens
    
    def match(self,tipo_esperado,lexema_esperado=None):
        atual = self.peek()
        if atual is None:
            raise ErroSintatico(f"Fim inesperado do arquivo")
        tipo, lexema, linha = atual
        if tipo != tipo_esperado:
            raise ErroSintatico(f"Erro sintático na linha {linha}: esperava {tipo_esperado}, encontrado {tipo} ('{lexema}')")
        if lexema_esperado is not None and lexema != lexema_esperado:
            raise ErroSintatico(f"Erro sintático na linha {linha}: esperava {tipo_esperado}, encontrado {tipo} ('{lexema}')")
        return self.avancar()

    def parse_program(self):
        while self.peek() != None:
            self.parse_class()
            self.match("SEMI")

    def parse_class(self):
        self.match('palavra reservada', 'class')

        self.match('TYPE_ID')

        token_atual = self.peek()
        if token_atual is not None and token_atual[0] == 'palavra reservada' and token_atual[1] == 'inherits':
            self.match('palavra reservada','inherits')
            self.match('TYPE_ID')

        self.match('LBRACE')
        token_atual = self.peek()
        while token_atual is not None and token_atual[0] != 'RBRACE':
            self.parse_feature()
            self.match("SEMI")
            token_atual = self.peek()
        self.match('RBRACE')

    def parse_feature(self):
        self.match("OBJECT_ID")

        token_atual = self.peek()
        if token_atual is not None and token_atual[0] == 'LPAREN':
            self.match("LPAREN")
            token_atual = self.peek()
            while token_atual is not None and token_atual[0] != 'RPAREN':
                self.match("OBJECT_ID")
                self.match("COLON")
                self.match('TYPE_ID')
                token_atual = self.peek()
                if token_atual is not None and token_atual[0] == 'COMMA':
                    self.match('COMMA')
                    token_atual = self.peek()
            self.match("RPAREN")
            self.match("COLON")
            self.match("TYPE_ID")
            self.match("LBRACE")
            self.parse_expr()
            self.match("RBRACE")

        elif token_atual is not None and token_atual[0] == 'COLON':
            self.match("COLON")
            self.match("TYPE_ID")
            token_atual = self.peek()
            if token_atual is not None and token_atual[0] == 'ASSIGN':
                self.match("ASSIGN")
                self.parse_expr()

    def parse_expr(self):
        #provisorio
        return self.avancar()

    def parse_primary(self):
        token_atual = self.peek()
        if token_atual is None:
            raise ErroSintatico("Fim inesperado do arquivo, esperava uma expressão")
        tipo, lexema, linha = token_atual

        if tipo == 'Int':
            return self.match('Int')
        elif tipo == 'String':
            return self.match('String')
        elif tipo == 'Bool':
            return self.match('Bool')
        elif tipo == 'OBJECT_ID':
            self.match('OBJECT_ID')
            token_atual = self.peek()
            if token_atual is not None and token_atual[0] == 'LPAREN':
                self.match('LPAREN')
                token_atual = self.peek()
                while token_atual is not None and token_atual[0] != 'RPAREN':
                    self.parse_expr()
                    token_atual = self.peek()
                    if token_atual is not None and token_atual[0] == 'COMMA':
                        self.match('COMMA')
                        token_atual = self.peek()
                return self.match('RPAREN')
            else:
                #provisorio
                return True
        elif tipo == 'LPAREN':
            self.match('LPAREN')
            self.parse_expr()
            return self.match('RPAREN')
        else:
            raise ErroSintatico(f"Erro sintatico na linha {linha}: expressão inesperada, encontrado {tipo} ('{lexema}')")



codigo = ler_arquivo("helloWorld2.cl")
tamanho = len(codigo)
tokens = tokenizar(codigo, tamanho)
p = Parser(tokens)
p.parse_program()
print("Parse concluído com sucesso!")