from core.scanner.scanner import *
from core.scanner.tokens import *
from core.interpreter.context import *
from core.interpreter.symbolTable import *
from core.errors.errors import *
from core.errors.runtime import *

import math

##################################
# VALUES
##################################

# Para funcoes
class Value:
    def __init__(self):
        self.set_pos()
        self.set_context()

    # Metodo para armazenar a posicao do numero para caso haver algum erro sabermos onde encontra-lo
    def set_pos(self, pos_start=None, pos_end=None):
        self.pos_start = pos_start
        self.pos_end = pos_end
        return self
    
    def set_context(self, context=None):
        self.context = context
        return self
    
    def added_to(self, other):
        return None, self.illegal_operation(other)

    def subbed_by(self, other):
        return None, self.illegal_operation(other)
    
    def multed_by(self, other):
        return None, self.illegal_operation(other)
    
    def dived_by(self, other):
        return None, self.illegal_operation(other)
    
    def modded_by(self, other):
        return None, self.illegal_operation(other)
    
    def powed_by(self, other):
        return None, self.illegal_operation(other)
    
    def get_comparison_eq(self, other):
        return None, self.illegal_operation(other)
    
    def get_comparison_ne(self, other):
        return None, self.illegal_operation(other)
    
    def get_comparison_lt(self, other):
        return None, self.illegal_operation(other)
    
    def get_comparison_gt(self, other):
        return None, self.illegal_operation(other)
    
    def get_comparison_lte(self, other):
        return None, self.illegal_operation(other)
    
    def get_comparison_gte(self, other):
        return None, self.illegal_operation(other)

    def anded_by(self, other):
        return None, self.illegal_operation(other)
    
    def ored_by(self, other):
        return None, self.illegal_operation(other)
    
    def notted(self, other):
        return None, self.illegal_operation(other)    
    
    def execute(self, args):
        return RTResult().failure(self.illegal_operation())
    
    def copy(self):
        raise Exception('No copy method defined')   
    
    # Um valor e verdadeiro se nao for igual a zero    
    def is_true(self):
        return False
    
    def illegal_operation(self, other=None):
        if not other: other = self
        return RTError(
            self.pos_start, other.pos_end,
            'Illegal operation',
            self.context
        )
        
    def in_check(self, container):
        return None, self.illegal_operation(container)

# Classe numerica para armazenar numeros para depois operar sobre eles com outros numeros
class Number(Value):
    def __init__(self, value):
        super().__init__() # Number herda de Value
        self.value = value
    
    # Metodos para operar o numero: somar, subtrair, multiplicar, dividir, negar o numero, etc

    # Metodo para somar dois numeros
    def added_to(self, other):
        if isinstance(other, Number):                                                  # Verificar se é um numero, pois posteriormente trabalharemos tambem com strings
            return Number(self.value + other.value).set_context(self.context), None    # Adicionando o nosso valor ao outro valor
        else: # Porque nao faz sentido adicionar um Number a uma funcao
            return None, Value.illegal_operation(self, other)
        
    # Metodo para subtrair dois numeros
    def subbed_by(self, other):
        if isinstance(other, Number):                 
            return Number(self.value - other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)
    
    # Metodo para multiplicar dois numeros
    def multed_by(self, other):
        if isinstance(other, Number):                 
            return Number(self.value * other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)
    
    # Metodo para dividir dois numeros
    def dived_by(self, other):
        if isinstance(other, Number):             
            # Precisamos retornar um erro caso tenha divisao por zero    
            if other.value == 0:
                return None, RTError(
                    other.pos_start, other.pos_end,
                    'Division by zero',
                    self.context
                )
            
            return Number(self.value / other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)
        
    # Metodo para divisao inteira de dois numeros
    def intdiv_by(self, other):
        if isinstance(other, Number):             
            # Erro em caso de divisao por zero    
            if other.value == 0:
                return None, RTError(
                    other.pos_start, other.pos_end,
                    'Division by zero',
                    self.context
                )
            
            return Number(int(self.value // other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)
            
    # Metodo para calcular o resto da divisao de dois numeros
    def modded_by(self, other):
        if isinstance(other, Number):           
            
            # Erro em caso de divisao por zero    
            if other.value == 0:
                return None, RTError(
                    other.pos_start, other.pos_end,
                    'Division by zero',
                    self.context
                )
            
            return Number(self.value % other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)
        
    def powed_by(self, other):
        if isinstance(other, Number):                                                   # Verificando se o outro valor e um numero
            return Number(self.value ** other.value).set_context(self.context), None    # Se for retornamos um novo numero com o 
                                                                                        # valor ** (operador de potencia) pelo outro valor 
        else:
            return None, Value.illegal_operation(self, other)
    
    def get_comparison_eq(self, other):
        if isinstance(other, Number):
            return Boolean(1 if self.value == other.value else 0).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)
    
    def get_comparison_ne(self, other):
        if isinstance(other, Number):
            return Boolean(1 if self.value != other.value else 0).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)
        
    def get_comparison_lt(self, other):
        if isinstance(other, Number):
            return Boolean(1 if self.value < other.value else 0).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)
    
    def get_comparison_gt(self, other):
        if isinstance(other, Number):
            return Boolean(1 if self.value > other.value else 0).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)
    
    def get_comparison_lte(self, other):
        if isinstance(other, Number):
            return Boolean(1 if self.value <= other.value else 0).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)
        
    def get_comparison_gte(self, other):
        if isinstance(other, Number):
            return Boolean(1 if self.value >= other.value else 0).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)
    
    def anded_by(self, other):
        if isinstance(other, Number):
            return Boolean(1 if self.value and other.value else 0).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)
    
    def ored_by(self, other):
        if isinstance(other, Number):
            return Boolean(1 if self.value or other.value else 0).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)
    
    def notted(self):
        return Number(1 if self.value == 0 else 0).set_context(self.context), None
        
    def copy(self):
        copy = Number(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy    
    
    # Um valor e verdadeiro se nao for igual a zero    
    def is_true(self):
        return self.value != 0
    
    def __str__(self):
        return str(self.value)
    
    # Metodo de representacao

    def __repr__(self):
        return str(self.value)
    
    def in_check(self, container):
        if isinstance(container, List):
            # Verifica se o numero esta na lista
            for element in container.elements:
                if isinstance(element, Number) and element.value == self.value:
                    return Boolean(1).set_context(self.context), None
            return Boolean(0).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, container)

Number.null = Number(0)
Number.false = Number(0)
Number.true = Number(1)
Number.math_PI = Number(math.pi)

# Classe para valores booleanos
class Boolean(Value):
    def __init__(self, value):
        super().__init__()
        self.value = value  # 1 para true, 0 para false

    def added_to(self, other):
        return None, self.illegal_operation(other)

    def subbed_by(self, other):
        return None, self.illegal_operation(other)

    def multed_by(self, other):
        return None, self.illegal_operation(other)

    def dived_by(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_eq(self, other):
        if isinstance(other, Boolean):
            return Boolean(1 if self.value == other.value else 0).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def get_comparison_ne(self, other):
        if isinstance(other, Boolean):
            return Boolean(1 if self.value != other.value else 0).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def anded_by(self, other):
        if isinstance(other, Boolean):
            return Boolean(1 if self.value and other.value else 0).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def ored_by(self, other):
        if isinstance(other, Boolean):
            return Boolean(1 if self.value or other.value else 0).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def notted(self):
        return Boolean(1 if self.value == 0 else 0).set_context(self.context), None

    def is_true(self):
        return self.value != 0

    def copy(self):
        copy = Boolean(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def __str__(self):
        return "true" if self.value else "false"

    def __repr__(self):
        return "true" if self.value else "false"

class String(Value):
    def __init__(self, value):
        super().__init__()
        self.value = value
    
    # Concatenar strings
    def added_to(self, other):
        if isinstance(other, String):
            return String(self.value + other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)
    
    # Para repetir a string um determinado numero de vezes
    def multed_by(self, other):
        if isinstance(other, Number):
            return String(self.value * other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)
    
    def get_comparison_eq(self, other):
        if isinstance(other, String):
            return Boolean(1 if self.value == other.value else 0).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)
    
    def get_comparison_ne(self, other):
        if isinstance(other, String):
            return Boolean(1 if self.value != other.value else 0).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)
    
    # A string e considerada verdadeira se ela possui pelo menos um caracter
    def is_true(self):
        return len(self.value) > 0
    
    def copy(self):
        copy = String(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy
    
    def __str__(self):
        return self.value
    
    def __repr__(self):
        return f'"{self.value}"'
    
    def in_check(self, container):
        if isinstance(container, String):
            # Verifica se a string esta contida em outra string
            is_in = 1 if self.value in container.value else 0
            return Boolean(is_in).set_context(self.context), None
        elif isinstance(container, List):
            # Verifica se a string esta na lista
            for element in container.elements:
                if isinstance(element, String) and element.value == self.value:
                    return Boolean(1).set_context(self.context), None
            return Boolean(0).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, container)

class List(Value):
    def __init__(self, elements):
        super().__init__()
        self.elements = elements

    # Metodo para adicionar um novo elemento na lista
    def added_to(self, other):
        new_list = self.copy()
        new_list.elements.append(other)
        return new_list, None
    
    # Metodo para remover um elemento da lista
    def subbed_by(self, other):
        # Verificando se o elemento e um numero, porque esse numero sera o indice do elemento que estamos removendo
        if isinstance(other, Number):
            new_list = self.copy()
            try:
                new_list.elements.pop(other.value)
                return new_list, None
            # Erro caso o indice a ser removido nao exista
            except:
                return None, RTError(
                    other.pos_start, other.pos_end,
                    'Element at this index could not be removed from list because index is out of bounds',
                    self.context
                )
        else:
            return None, Value.illegal_operation(self, other)
    
    # Operacao para concatenar listas
    def multed_by(self, other):
        # Verificando se o elemento que vamos concatenar e uma lista
        if isinstance(other, List):
            new_list = self.copy()
            new_list.elements.extend(other.elements)
            return new_list, None
        else:
            return None, Value.illegal_operation(self, other)

    # Metodo para obter um elemento da lista
    def dived_by(self, other):
        if isinstance(other, Number):
            try:
                return self.elements[other.value], None
            except:
                return None, RTError(
                    other.pos_start, other.pos_end,
                    'Element at this index could not be retrieved from list because index is out of bounds',
                    self.context
                )
        else:
            return None, Value.illegal_operation(self, other)
    
    def copy(self):
        copy = List(self.elements)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy
    
    def __str__(self):
        return ", ".join([str(x) for x in self.elements])
    
    def __repr__(self):
        return f'[{", ".join([repr(x) for x in self.elements])}]'

class BaseFunction(Value):
    def __init__(self, name):
        super().__init__()
        self.name = name or "<anonymous>"
        
    def generate_new_context(self):
        new_context = Context(self.name, self.context, self.pos_start)
        new_context.symbol_table = SymbolTable(new_context.parent.symbol_table)
        return new_context

    def check_args(self, arg_names, args):
        res = RTResult()
        
        # Verificando se o numero de argumentos passados na funcao esta correto
        if len(args) > len(arg_names):
            return res.failure(RTError(
                self.pos_start, self.pos_end,
                f"{len(args) - len(arg_names)} too many args passed into {self}",
                self.context
            ))
        
        if len(args) < len(arg_names):
            return res.failure(RTError(
                self.pos_start, self.pos_end,
                f"{len(arg_names) - len(args)} too few args passed into {self}",
                self.context
            ))
        return res.success(None)

    # Colocando os argumentos na tabela de simbolo
    def populate_args(self, arg_names, args, exec_ctx):
        # Iterando sobre cada argumento
        for i in range(len(args)):
            # Obtemos o nome e o valor do argumento
            arg_name = arg_names[i]
            arg_value = args[i]
            arg_value.set_context(exec_ctx)                    # Atualizamos o contexto
            exec_ctx.symbol_table.set(arg_name, arg_value)     # Adicionamos esse valor na tabela de simbolos
    
    def check_and_populate_args(self, arg_names, args, exec_ctx):
        res = RTResult()
        res.register(self.check_args(arg_names, args))
        if res.should_return(): return res
        self.populate_args(arg_names, args, exec_ctx)
        return res.success(None)

class Function(BaseFunction):
    def __init__(self, name, body_node, arg_names, arg_types, return_type, should_auto_return):
        super().__init__(name)
        self.body_node = body_node
        self.arg_names = arg_names
        self.arg_types = arg_types          # ['int', 'int'] for somar(int a, int b)
        self.return_type = return_type      # 'int' for -> int
        self.should_auto_return = should_auto_return  # Deve retornar nulo
        
    def execute(self, args):
        res = RTResult()
        interpreter = Interpreter()
        exec_ctx = self.generate_new_context()
        
        res.register(self.check_and_populate_args(self.arg_names, args, exec_ctx))
        if res.should_return(): return res
        
        # Validacao de tipos dos argumentos
        res.register(self.check_arg_types(args))
        if res.should_return(): return res
        
        # Chamando o interpretador
        value = res.register(interpreter.visit(self.body_node, exec_ctx))
        if res.should_return() and res.func_return_value == None: return res
    
        ret_value = (value if self.should_auto_return else None) or res.func_return_value or Number.null
        return res.success(ret_value)
    
    # Metodo que copia a funcao, entao, cria uma nova funcao e passa todas as variaveis 
    # e define o contexto e a posicao da nova funcao e, entao, apenas a retorna
    def copy(self):
        copy = Function(self.name, self.body_node, self.arg_names, self.arg_types, self.return_type, self.should_auto_return)
        copy.set_context(self.context)
        copy.set_pos(self.pos_start, self.pos_end)
        return copy
    
    # Metodo de representacao para vermos a string de funcao
    def __repr__(self):
        return f"<function {self.name}>"
    
    def check_arg_types(self, args):
        res = RTResult()
        
        # Verificacao de tipos dos argumentos
        for i in range(len(args)):
            expected_type = self.arg_types[i]
            actual_arg = args[i]
            
            # Determinar o tipo atual do argumento
            if isinstance(actual_arg, Number):
                # Para Number, verificamos se e int ou float baseado no valor
                if isinstance(actual_arg.value, int):
                    actual_type = 'int'
                else:
                    actual_type = 'float'
            elif isinstance(actual_arg, String):
                actual_type = 'string'
            elif isinstance(actual_arg, List):
                actual_type = 'list'
            elif isinstance(actual_arg, Function):
                actual_type = 'function'
            else:
                actual_type = 'unknown'
            
            # Verificar compatibilidade de tipos
            if expected_type != actual_type:
                # Permitir int quando esperamos boolean (1/0 para true/false)
                if not (expected_type == 'boolean' and actual_type == 'int'):
                    return res.failure(RTError(
                        self.pos_start, self.pos_end,
                        f"Argument {i+1} expected {expected_type} but got {actual_type}",
                        self.context
                    ))
        
        return res.success(None)

##################################
# INTERPRETER
##################################

class Interpreter:
    # O metodo visit() levara a um no e a mensagem de visita processar esse no
    # e entao visitara todos os nos filhos
    def visit(self, node, context):
        method_name = f'visit_{type(node).__name__}'                # Obter tipo do no e o nome
        method = getattr(self, method_name, self.no_visit_method)   # Obter o metodo real que sera chamado
                                                                    # Sera passado o nome do metodo e o metodo padrao 
                                                                    # para o caso em que nenhum metodo for encontrado 
        return method(node, context)

    # metodo para gerar uma excecao
    def no_visit_method(self, node):
        raise Exception(f'No visit_{type(node).__name__} method defined')  # Nenhum metodo de visita foi definido

    ##################################
    # Definindo o metodo de visita para cada tipo de no
    
    # No numerico
    def visit_NumberNode(self, node, context):
        return RTResult().success(
            # Retornamos uma nova instancia de numero e para o valor vamos pegar o no, vamos pegar o seu token e depois pegar o seu valor 
            # Tambem queremos setar (definir) a posicao desse numero, entao vamos passar a sua posicao inicial e final
            Number(node.tok.value).set_context(context).set_pos(node.pos_start, node.pos_end)
        )

    def visit_BooleanNode(self, node, context):
        value = 1 if node.tok.value == 'true' else 0
        return RTResult().success(
            Boolean(value).set_context(context).set_pos(node.pos_start, node.pos_end)
        )
    
    def visit_StringNode(self, node, context):
        string_value = node.tok.value[1] if isinstance(node.tok.value, tuple) else node.tok.value
        return RTResult().success(
            String(string_value).set_context(context).set_pos(node.pos_start, node.pos_end)
        )
        
    def visit_ListNode(self, node, context):
        res = RTResult()
        elements = []
        
        # Percorrendo todos os elementos e adicionando-os a lista
        for element_node in node.element_nodes:
            elements.append(res.register(self.visit(element_node, context)))
            if res.should_return(): return res
        
        # Retornando uma nova lista   
        return res.success(
            List(elements).set_context(context).set_pos(node.pos_start, node.pos_end)
        ) 
        
    def visit_VarAccessNode(self, node, context):
        res = RTResult()                               # Novo resultado de tempo de execucao
        var_name = node.var_name_tok.value             # Obtendo o nome da variavel
        value = context.symbol_table.get(var_name)     # Obtendo o valor da variavel
        
        # Verificando se a variavel ainda nao foi definida
        # if not value:
        if value is None:
            return res.failure(RTError(
                node.pos_start, node.pos_end,
                f"'{var_name}' is not defined",
                context 
            ))
        
        value = value.copy().set_pos(node.pos_start, node.pos_end).set_context(context)   
        # Caso contrario, retornamos sucesso e passamos o valor da variavel
        return res.success(value)
    
    def visit_VarAssignNode(self, node, context):
        res = RTResult()
        var_name = node.var_name_tok.value
        value = res.register(self.visit(node.value_node, context))
        if res.should_return(): return res

        # Verificar se a variavel ja existe para permitir reatribuicao  
        existing_value = context.symbol_table.get(var_name)
        if existing_value is None:
            return res.failure(RTError(
                node.pos_start, node.pos_end,
                f"Variable '{var_name}' must be declared with type first. Use: type {var_name} = value",
                context
            ))
        
        # Verificacao de tipo para reatribuicao
        if isinstance(existing_value, Number) and not isinstance(value, Number):
            return res.failure(RTError(
                node.pos_start, node.pos_end,
                f"Cannot assign {type(value).__name__} to numeric variable '{var_name}'",
                context
            ))
        elif isinstance(existing_value, String) and not isinstance(value, String):
            return res.failure(RTError(
                node.pos_start, node.pos_end,
                f"Cannot assign {type(value).__name__} to string variable '{var_name}'",
                context
            ))
        elif isinstance(existing_value, List) and not isinstance(value, List):
            return res.failure(RTError(
            node.pos_start, node.pos_end,
            f"Cannot assign {type(value).__name__} to list variable '{var_name}'",
            context
        ))
                
        # Se nao der erro chamamos o metodo set para definir a variavel com o seu nome e valor
        context.symbol_table.set(var_name, value)
        return res.success(value)
            
    # No operador binario    
    def visit_BinOpNode(self, node, context): 
        res = RTResult()
        left = res.register(self.visit(node.left_node, context))              # Quando encontrarmos um operador binario precisamos 
        if res.should_return(): return res
        right = res.register(self.visit(node.right_node, context))             # visitar o no esquerdo e direito desse no
        if res.should_return(): return res

        # Verificando o token do operador para determinar qual funcao precisa ser chamada 
        if node.op_tok.type == TT_PLUS:
            result, error = left.added_to(right)
        elif node.op_tok.type == TT_MINUS:
            result, error = left.subbed_by(right)
        elif node.op_tok.type == TT_MUL:
            result, error = left.multed_by(right)
        elif node.op_tok.type == TT_DIV:
            result, error = left.dived_by(right)
        elif node.op_tok.type == TT_INTDIV:
            result, error = left.intdiv_by(right)
        elif node.op_tok.type == TT_MOD:
            result, error = left.modded_by(right)
        elif node.op_tok.type == TT_POW:
            result, error = left.powed_by(right)
        elif node.op_tok.type == TT_EE:
            result, error = left.get_comparison_eq(right)
        elif node.op_tok.type == TT_NE:
            result, error = left.get_comparison_ne(right)
        elif node.op_tok.type == TT_LT:
            result, error = left.get_comparison_lt(right)
        elif node.op_tok.type == TT_GT:
            result, error = left.get_comparison_gt(right)
        elif node.op_tok.type == TT_LTE:
            result, error = left.get_comparison_lte(right)
        elif node.op_tok.type == TT_GTE:
            result, error = left.get_comparison_gte(right)
        elif node.op_tok.matches(TT_KEYWORD, 'and'):
            result, error = left.anded_by(right)
        elif node.op_tok.matches(TT_KEYWORD, 'or'):
            result, error = left.ored_by(right)
        
        if error:
            return res.failure(error)
        else:
            return res.success(result.set_pos(node.pos_start, node.pos_end))

    # No operador unario
    def visit_UnaryOpNode(self, node, context):
        res = RTResult()
        number = res.register(self.visit(node.node, context))                   # Visitando o no filho, parecido com o que ocorre na operacao binaria
        if res.should_return(): return res
        
        error = None
        
        # Se o operador for o de menos, multiplicamos o numero por -1
        if node.op_tok.type == TT_MINUS:
            number, error = number.multed_by(Number(-1))
        elif node.op_tok.matches(TT_KEYWORD, 'not'):
            number, error = number.notted()
        
        if error:
            return res.failure(error)
        else:
            return res.success(number.set_pos(node.pos_start, node.pos_end))
    
    def visit_IfNode(self, node, context):
        res = RTResult()
        
        # Para cada par de condicoes e expressoes nos casos dos nos: 
        for condition, expr, should_return_null in node.cases:
            # Visitamos essa condicao e obtemos um valor de condicao
            condition_value = res.register(self.visit(condition, context))
            if res.should_return(): return res
            
            # Verificando se o valor de condicao e verdadeiro
            if condition_value.is_true():
                # Se for, avaliamos a expressao
                expr_value = res.register(self.visit(expr, context))
                if res.should_return(): return res
                return res.success(Number.null if should_return_null else expr_value)
        
        # Verificando se o no tem um caso else
        if node.else_case:
            expr, should_return_null = node.else_case
            # Se tiver, apenas avaliamos a expressao
            expr_value = res.register(self.visit(expr, context))
            if res.should_return(): return res
            return res.success(Number.null if should_return_null else expr_value)
        
        return res.success(Number.null)
    
    def visit_ForNode(self, node, context):
        res = RTResult()
        elements = []
        
        # Valor inicial do contador do for
        start_value = res.register(self.visit(node.start_value_node, context))
        if res.should_return(): return res
        
        # Valor final do contador do for
        end_value = res.register(self.visit(node.end_value_node, context))
        if res.should_return(): return res
        
        # Valor do step do for, se houver
        if node.step_value_node:
            step_value = res.register(self.visit(node.step_value_node, context))
            if res.should_return(): return res
        else:
            step_value = Number(1) # Valor padrao do step é 1
        
        i = start_value.value
        
        # Função lambda que verifica se i é menor/maior que o valor final end_value.value
        # Isso significa que o loop continuara enquanto i for menor que o valor final
        if step_value.value >= 0:
            condition = lambda: i < end_value.value  # Incrementando o valor
        else:
            condition = lambda: i > end_value.value  # Decrementando o valor
        
        while condition():
            # Atualiza o valor de uma variavel no contexto atual com o valor atual de i
            context.symbol_table.set(node.var_name_tok.value, Number(i))
            #  Incrementa ou decrementa i, dependendo do valor de step_value.value
            i += step_value.value

            value = res.register(self.visit(node.body_node, context))
            if res.should_return() and res.loop_should_continue == False and res.loop_should_break == False: return res
        
            if res.loop_should_continue:
                continue
            
            if res.loop_should_break:
                break
            
            elements.append(value)
        
        # return res.success(None)
        
        # for agora retorna uma lista de elementos    
        return res.success(
            Number.null if node.should_return_null else
            List(elements).set_context(context).set_pos(node.pos_start, node.pos_end)
        )

    def visit_ForInNode(self, node, context):
        res = RTResult()
        elements = []
        
        # Avaliar o iteravel (string ou lista)
        iterable = res.register(self.visit(node.iterable_node, context))
        if res.should_return(): return res
        
        # Determinar os elementos a iterar
        if isinstance(iterable, String):
            items = list(iterable.value)  # Converter string em lista de caracteres
        elif isinstance(iterable, List):
            items = iterable.elements
        else:
            return res.failure(RTError(
                node.pos_start, node.pos_end,
                "Can only iterate over strings and lists",
                context
            ))
        
        # Iterar sobre cada elemento
        for item in items:
            # Converter caractere em String se for iteracao de string
            if isinstance(iterable, String):
                item = String(item)
            
            # Atualizar variavel de iteracao no contexto
            context.symbol_table.set(node.var_name_tok.value, item)
            
            # Executar corpo do loop
            value = res.register(self.visit(node.body_node, context))
            if res.should_return() and res.loop_should_continue == False and res.loop_should_break == False:
                return res
            
            if res.loop_should_continue:
                continue
            
            if res.loop_should_break:
                break
            
            elements.append(value)
        
        return res.success(
            Number.null if node.should_return_null else
            List(elements).set_context(context).set_pos(node.pos_start, node.pos_end)
        )

    def visit_WhileNode(self, node, context):
        res = RTResult()
        elements = []
        
        while True:
            condition = res.register(self.visit(node.condition_node, context))
            if res.should_return(): return res
            
            # Se a condicao nao for verdadeira, saimos do while
            if not condition.is_true(): 
                break
            
            value = res.register(self.visit(node.body_node, context))
            if res.should_return() and res.loop_should_continue == False and res.loop_should_break == False: return res
        
            if res.loop_should_continue:
                continue
            
            if res.loop_should_break:
                break
        
            elements.append(value)
        # return res.success(None)
        
        # while agora retorna uma lista de elementos    
        
        return res.success(
            Number.null if node.should_return_null else
            List(elements).set_context(context).set_pos(node.pos_start, node.pos_end)
        )
    
    def visit_FuncDefNode(self, node, context):
        res = RTResult()
        
        func_name = node.var_name_tok.value if node.var_name_tok else None
        body_node = node.body_node
        arg_names = [arg_name.value for arg_name in node.arg_name_toks]
        arg_types = node.arg_types
        return_type = node.return_type
        func_value = Function(func_name, body_node, arg_names, arg_types, return_type, node.should_auto_return).set_context(context).set_pos(node.pos_start, node.pos_end)
        
        # Se a funcao tiver um nome, devemos adiciona-lo na tabela de simbolos para podermos chamar a funcao pelo nome
        if node.var_name_tok:
            context.symbol_table.set(func_name, func_value)
        
        return res.success(func_value)
    
    def visit_CallNode(self, node, context):
        res = RTResult()
        args = []
        
        value_to_call = res.register(self.visit(node.node_to_call, context))
        if res.should_return(): return res
        # Criando uma copia do valor da funcao para que, em caso de erro, possamos ver onde estamos chamando a funcao em vez de onde ela foi definida
        value_to_call = value_to_call.copy().set_pos(node.pos_start, node.pos_end)
        
        # Construindo uma lista de valores de argumentos
        for arg_node in node.arg_nodes:
            args.append(res.register(self.visit(arg_node, context)))
            if res.should_return(): return res
        
        # Agora, vamos de fato executar a funcao
        return_value = res.register(value_to_call.execute(args))
        if res.should_return(): return res
        return_value = return_value.copy().set_pos(node.pos_start, node.pos_end).set_context(context)
        return res.success(return_value)
    
    def visit_ReturnNode(self, node, context):
        res = RTResult()
        
        # Verificando se ha um no para retornar
        if node.node_to_return:
            # Se existir, visitamos esse no
            value = res.register(self.visit(node.node_to_return, context))
            if res.should_return(): return res
        else:
            value = Number.null

        return res.success_return(value)
    
    def visit_ContinueNode(self, node, context):
        return RTResult().success_continue()
    
    def visit_BreakNode(self, node, context):
        return RTResult().success_break()
    
    def visit_TypedVarAssignNode(self, node, context):
        res = RTResult()
        var_name = node.var_name_tok.value
        declared_type = node.var_type
        value = res.register(self.visit(node.value_node, context))
        if res.should_return(): return res

        # Verificacao de tipo no runtime
        if isinstance(value, Function):
            actual_type = value.return_type
        elif isinstance(value, Boolean):
            actual_type = 'boolean'
        elif isinstance(value, Number):
            actual_type = 'int' if isinstance(value.value, int) else 'float'
        elif isinstance(value, String):
            actual_type = 'string'
        elif isinstance(value, List):
            actual_type = 'list'
        else:
            actual_type = 'unknown'
        
        if declared_type != actual_type:
            return res.failure(RTError(
                node.pos_start, node.pos_end,
                f"Type mismatch: cannot assign {actual_type} to variable of type {declared_type}",
                context
            ))

        context.symbol_table.set(var_name, value)
        return res.success(value)
        
    def visit_InNode(self, node, context):
        res = RTResult()
        element = res.register(self.visit(node.element_node, context))
        if res.should_return(): return res
        
        container = res.register(self.visit(node.container_node, context))
        if res.should_return(): return res
        
        result, error = element.in_check(container)
        
        if error:
            return res.failure(error)
        else:
            return res.success(result.set_pos(node.pos_start, node.pos_end))