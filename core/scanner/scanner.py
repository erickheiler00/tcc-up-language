# Scanner
from strings_with_arrows import *
from core.scanner.tokens import *
from core.errors.errors import *

class Scanner:
    def __init__(self, fn, text):
        self.fn = fn
        self.text = text
        self.pos = Position(-1, 0, -1, fn, text)  # Posicao atual e coluna iniciam negativas porque o advance ira incrementa-las
        self.current_char = None        # Caractere atual
        self.advance()
    
    # Metodo para avancar a posicao e o caractere
    """
        Caractere atual recebe o caractere daquela posicao
        Somente podemos fazer isso se a posicao for menor que o comprimento do texto
        Se alcancarmos o final do texto definimos ele como nulo
    """
    def advance(self):
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.idx] if self.pos.idx < len(self.text) else None
    
    # Metodo para criar um token
    def make_tokens(self):
        tokens = []    # Lista vazia de tokens
        
        # Loop para percorrer cada caractere do texto
        """
            Se não for igual a nenhum caractere apenas o ignoramos
            Sendo assim, espacos em branco serao ignorados
            
            Se o caractere atual for igual a um simbolo adicionamos ele na lista
            junto com o tipo correspondente aquele token
        """
        while self.current_char != None:
            if self.current_char in ' \t':
                self.advance()
            elif self.current_char == '#':
                self.skip_comment()
            elif self.current_char in ';\n':
                tokens.append(Token(TT_NEWLINE, pos_start=self.pos))
                self.advance()
            elif self.current_char in DIGITS:
                tokens.append(self.make_number())
            elif self.current_char in LETTERS:                  # Se o caractere atual estiver em LETTERS significa que e um identificador
                tokens.append(self.make_identifier())
            elif self.current_char == '"':
                tokens.append(self.make_string())
            elif self.current_char == '+':
                tokens.append(Token(TT_PLUS, pos_start=self.pos))
                self.advance()
            elif self.current_char == '-':
                tokens.append(self.make_minus_or_arrow())
            elif self.current_char == '*':
                tokens.append(Token(TT_MUL, pos_start=self.pos))
                self.advance()
            elif self.current_char == '/':
                pos_start = self.pos.copy()
                self.advance()
                if self.current_char == '/':
                    self.advance()
                    tokens.append(Token(TT_INTDIV, pos_start=pos_start, pos_end=self.pos))
                else:
                    tokens.append(Token(TT_DIV, pos_start=pos_start, pos_end=self.pos))
            elif self.current_char == '%':
                tokens.append(Token(TT_MOD, pos_start=self.pos))
                self.advance()
            elif self.current_char == '^':
                tokens.append(Token(TT_POW, pos_start=self.pos))
                self.advance()
            elif self.current_char == '(':
                tokens.append(Token(TT_LPAREN, pos_start=self.pos))
                self.advance()
            elif self.current_char == ')':
                tokens.append(Token(TT_RPAREN, pos_start=self.pos))
                self.advance()
            elif self.current_char == '[':
                tokens.append(Token(TT_LSQUARE, pos_start=self.pos))
                self.advance()
            elif self.current_char == ']':
                tokens.append(Token(TT_RSQUARE, pos_start=self.pos))
                self.advance()
            elif self.current_char == '!':
                token, error = self.make_not_equals() # Para verificar se o caractere apos esse é um igual (=)
                if error: return [], error          # Se for diferente de igual ele criara um novo token, diferente de igual
                tokens.append(token)
            elif self.current_char == '=':
                tokens.append(self.make_equals())
            elif self.current_char == '<':
                tokens.append(self.make_less_than())
            elif self.current_char == '>':
                tokens.append(self.make_greater_than())
            elif self.current_char == ',':
                tokens.append(Token(TT_COMMA, pos_start=self.pos))
                self.advance()
            else:
                # Passar a posicao em que ocorreu o erro
                pos_start = self.pos.copy()                
                char = self.current_char
                self.advance()
                # Retornar erro de caractere ilegal passando o caractere como detalhes
                return [], IllegalCharError(pos_start, self.pos, "'" + char + "'")
        
        tokens.append(Token(TT_EOF, pos_start=self.pos))   # Token de fim de arquivo
        return tokens, None
    
    # Metodo para criar um numero
    def make_number(self):
        num_str = ''
        dot_count = 0                 # Ver se tem ponto para verificar se é float ou int
        pos_start = self.pos.copy()
        
        # Verificando se o caractere atual pertence a DIGITS ou se é um ponto
        """
            Se for um ponto incrementamos a variavel dot_count e adicionamos um ponto na string
            Se dot_count ja for igual a 1 paramos porque nao podemos ter dois pontos em um numero
            Se nao for nenhuma das opcoes anteriores apenas adicionamos o numero na string
        """
        while self.current_char != None and self.current_char in DIGITS + '.':
            if self.current_char == '.':
                if dot_count == 1: break
                dot_count += 1    
            num_str += self.current_char
            self.advance()
        
        """
        while self.current_char != None and self.current_char in DIGITS + '.':
            if self.current_char == '.':
                if dot_count == 1: break
                dot_count += 1
                num_str += '.'
            else:
                num_str += self.current_char
            self.advance()
        """
        
        """
            Se dot_count for 0 significa que e um numero inteiro:
                Entao, retornamos um token do tipo inteiro e 
                convertemos a string para o numero inteiro correspondente
            Caso contrario o numero e um float:
                Entao, fazemos o mesmo processo, porem com o tipo float
        """ 
        if dot_count == 0:
            return Token(TT_KEYWORD, int(num_str), pos_start, self.pos)
        else:
            return Token(TT_KEYWORD, float(num_str), pos_start, self.pos)

    def make_string(self):
        string = ''
        pos_start = self.pos.copy()
        escape_character = False
        self.advance()
        
        escape_characters = {
            'n': '\n',
            't': '\t'
        }
        
        while self.current_char != None and (self.current_char != '"' or escape_character):
            if escape_character:
                string += escape_characters.get(self.current_char, self.current_char)
                escape_character = False
            else:
                if self.current_char == '\\':
                    escape_character = True
                else:
                    string += self.current_char
            self.advance()
            
        self.advance()
        return Token(TT_KEYWORD, ('string_literal', string), pos_start, self.pos)
        
    # metodo para criar a string correspondente ao identificador
    def make_identifier(self):
        id_str = ''
        pos_start = self.pos.copy()
        
        # Enquanto for diferente de nulo e estiver em LETTERS, DIGITS ou for um '_'
        while self.current_char != None and self.current_char in LETTERS_DIGITS + '_':
            id_str += self.current_char
            self.advance()
        
        # O token sera definido como KEYWORD se estiver na lista de KEYWORDS (palavras-chave)
        # Caso contrario, sera definido como identificador  
        # if id_str == 'true':
        #     tok_type = TT_TRUE
        # elif id_str == 'false':
        #     tok_type = TT_FALSE
        # O token sera definido como KEYWORD se estiver na lista de KEYWORDS
    
        # if id_str in KEYWORDS:
        #     tok_type = TT_KEYWORD
        # else:
        #     tok_type = TT_IDENTIFIER
        
        tok_type = TT_KEYWORD if id_str in KEYWORDS else TT_IDENTIFIER
        
        return Token(tok_type, id_str, pos_start, self.pos)
    
    def make_minus_or_arrow(self):
        tok_type = TT_MINUS
        pos_start = self.pos.copy()
        self.advance()
        
        # Se o caractere depois de - e >, entao o token e uma seta (ARROW)
        if self.current_char == '>':
            self.advance()
            tok_type = TT_ARROW
        
        # Caso contrario, o token e o sinal de menos (MINUS)
        return Token(tok_type, pos_start=pos_start, pos_end=self.pos)
    
    def make_not_equals(self):
        pos_start = self.pos.copy()
        self.advance()
        
        # Verificando se o proximo caractere depois do ! e um sinal de igual (=)
        # Se for, avancamos e retornamos um novo token
        if self.current_char == '=':
            self.advance()             
            return Token(TT_NE, pos_start=pos_start, pos_end=self.pos), None
        
        # Caso contrario, retornamos um erro
        self.advance()
        return None, ExpectedCharError(pos_start, self.pos, "'=' (after '!')")
    
    def make_equals(self):
        # Por padrao, definimos o token como um igual simples
        tok_type = TT_EQ
        pos_start = self.pos.copy()
        self.advance()
        
        # Precisamos determinar se sera um token de somente um igual (=) ou de igual duplo (==)
        # Verificando se o proximo caractere depois do igual (=) é um outro igual (=)
        # Se for, avancamos e criamos um token do tipo double equal
        if self.current_char == '=':
            self.advance()
            tok_type = TT_EE
        
        # Retornando um novo token, junto com nossa posicao inicial e final
        return Token(tok_type, pos_start=pos_start, pos_end=self.pos)
    
    def make_less_than(self):
        tok_type = TT_LT
        pos_start = self.pos.copy()
        self.advance()
        
        if self.current_char == '=':
            self.advance()
            tok_type = TT_LTE
        
        return Token(tok_type, pos_start=pos_start, pos_end=self.pos)
    
    def make_greater_than(self):
        tok_type = TT_GT
        pos_start = self.pos.copy()
        self.advance()
        
        if self.current_char == '=':
            self.advance()
            tok_type = TT_GTE
        
        return Token(tok_type, pos_start=pos_start, pos_end=self.pos)    

    def skip_comment(self):
        self.advance()
        
        # Verificando enquanto o caractere atual nao e igual a uma nova linha
        while self.current_char != '\n':
            self.advance()
        
        self.advance()