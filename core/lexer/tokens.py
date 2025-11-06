# Tokens
import string

####################################
# CONSTANTS
####################################

DIGITS = '0123456789'
LETTERS = string.ascii_letters
LETTERS_DIGITS = LETTERS + DIGITS

####################################
# TOKENS
####################################

TT_IDENTIFIER = 'IDENTIFIER'      
TT_KEYWORD    = 'KEYWORD'
TT_PLUS       = 'PLUS'
TT_MINUS      = 'MINUS'
TT_MUL        = 'MUL'
TT_DIV        = 'DIV'
TT_INTDIV     = 'INTDIV'    # Divisao inteira
TT_MOD        = 'MOD'       # Modulo - Resto da divisao
TT_POW        = 'POW'
TT_LPAREN     = 'LPAREN'
TT_RPAREN     = 'RPAREN'
TT_LSQUARE    = 'LSQUARE'  # [
TT_RSQUARE    = 'RSQUARE'  # ]   
TT_EQ         = 'EQ'
TT_EE         = 'EE'       # Double equals
TT_NE         = 'NE'       # Not equals
TT_LT         = 'LT'       # Less than - Menor que
TT_GT         = 'GT'       # Greater than - Maior que
TT_LTE        = 'LTE'      # Less than or equal - Menor ou igual a
TT_GTE        = 'GTE'      # Greater than or equal - Maior ou igual a
TT_COMMA      = 'COMMA'    # Virgula
TT_ARROW      = 'ARROW'    # Seta ->
TT_NEWLINE    = 'NEWLINE'
TT_EOF        = 'EOF'

KEYWORDS = [
    'int',
    'float',
    'string',
    'boolean',
    'void',
    'list',
    'function',
    'true',
    'false',
    'and',
    'or',
    'not',
    'if',
    'elif',
    'else',
    'for',
    'in',
    'to',
    'step',
    'while',
    'fun',
    'then',
    'do',
    'endif',
    'endfor',
    'endwhile',
    'endfun',
    'return',
    'continue',
    'break'
]

class Token:
    # Metodo para inicializar as variaveis
    def __init__(self, type_, value=None, pos_start=None, pos_end=None):
        self.type = type_
        self.value = value
        
        if pos_start:                           # Se ha uma pos_start
            self.pos_start = pos_start.copy()
            self.pos_end = pos_start.copy()
            self.pos_end.advance()              # pos_end = pos_start + 1
            
        if pos_end:                             # Se ha uma pos_end
            self.pos_end = pos_end.copy()
    
    # Verifica se o token corresponde ao tipo e valor fornecido
    def matches(self, type_, value):
        return self.type == type_ and self.value == value
    
    # Metodo de representacao para imprimir corretamente na tela
    """ 
        Representa um objeto como uma string
        Se o token tiver um valor ele imprimira o tipo e o valor
        Se ele não tiver um valor ele imprimira apenas o tipo
    """
    def __repr__(self): 
        if self.value: return f'{self.type}:{self.value}'
        return f'{self.type}'