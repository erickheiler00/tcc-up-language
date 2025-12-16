####################################
# IMPORTS 
####################################

from strings_with_arrows import *
from core.scanner.scanner import *
from core.parser.parser import *
from core.interpreter.interpreter import *
from core.interpreter.symbolTable import *
from core.errors.errors import *

import os

class BuiltInFunction(BaseFunction):
    def __init__(self, name):
        super().__init__(name)
    
    def execute(self, args):
        res = RTResult()
        exec_ctx = self.generate_new_context()
        
        method_name = f'execute_{self.name}'
        method = getattr(self, method_name, self.no_visit_method)
        
        # Armazena os argumentos para funcoes que aceitam quantidade variavel
        self.current_args = args
        
        # Se arg_names estiver vazio, aceita qualquer quantidade de argumentos
        if hasattr(method, 'arg_names') and len(method.arg_names) > 0:
            res.register(self.check_and_populate_args(method.arg_names, args, exec_ctx))
            if res.should_return(): return res
        
        return_value = res.register(method(exec_ctx))
        if res.should_return(): return res
        return res.success(return_value)
        
    def no_visit_method(self, exec_ctx):
        raise Exception(f'No execute_{self.name} method defined')
        
    def copy(self):
        copy = BuiltInFunction(self.name)
        copy.set_context(self.context)
        copy.set_pos(self.pos_start, self.pos_end)
        return copy

    def __repr__(self):
        return f"<built-in function {self.name}>"
    
    ##################################
    
    def execute_print(self, exec_ctx):
        # Aceita multiplos argumentos
        # Coleta todos os argumentos passados
        output = []
        for i in range(len(self.current_args)):
            output.append(str(self.current_args[i]))
        
        print(''.join(output))
        return RTResult().success(Number.null)
    execute_print.arg_names = []  # Aceita qualquer numero de argumentos
    
    def execute_print_ret(self, exec_ctx):
        # Em vez de retornar null queremos retornar o valor que estamos imprimindo
        return RTResult().success(String(str(exec_ctx.symbol_table.get('value'))))
    execute_print_ret.arg_names = ['value']
    
    def execute_print_inline(self, exec_ctx):
        # Print sem quebra de linha
        output = []
        for i in range(len(self.current_args)):
            output.append(str(self.current_args[i]))
        
        print(''.join(output), end='')
        return RTResult().success(Number.null)
    execute_print_inline.arg_names = []
    
    def execute_input(self, exec_ctx):
        prompt = ""
        if len(self.current_args) > 0:
            prompt = str(self.current_args[0])
        
        text = input(prompt)
        return RTResult().success(String(text))
    execute_input.arg_names = []
        
    def execute_input_int(self, exec_ctx):
        prompt = ""
        if len(self.current_args) > 0:
            prompt = str(self.current_args[0])
        
        while True:
            text = input(prompt)
            try:
                number = int(text)
                break
            except ValueError:
                print(f"'{text}' must be an integer. Try again!")
        return RTResult().success(Number(number))
    execute_input_int.arg_names = []
    
    def execute_input_float(self, exec_ctx):
        prompt = ""
        if len(self.current_args) > 0:
            prompt = str(self.current_args[0])
        
        while True:
            text = input(prompt)
            try:
                number = float(text)
                break
            except ValueError:
                print(f"'{text}' must be a float. Try again!")
        return RTResult().success(Number(number))
    execute_input_float.arg_names = []
    
    def execute_clear(self, exec_ctx):
        os.system('cls' if os.name == 'nt' else 'cls')
        return RTResult().success(Number.null)
    execute_clear.arg_names = []
    
    def execute_is_number(self, exec_ctx):
        is_number = isinstance(exec_ctx.symbol_table.get("value"), Number)
        return RTResult().success(Boolean(1) if is_number else Boolean(0))
    execute_is_number.arg_names = ["value"]

    def execute_is_string(self, exec_ctx):
        is_string = isinstance(exec_ctx.symbol_table.get("value"), String)
        return RTResult().success(Boolean(1) if is_string else Boolean(0))
    execute_is_string.arg_names = ["value"]

    def execute_is_list(self, exec_ctx):
        is_list = isinstance(exec_ctx.symbol_table.get("value"), List)
        return RTResult().success(Boolean(1) if is_list else Boolean(0))
    execute_is_list.arg_names = ["value"]

    def execute_is_function(self, exec_ctx):
        is_function = isinstance(exec_ctx.symbol_table.get("value"), BaseFunction)
        return RTResult().success(Boolean(1) if is_function else Boolean(0))
    execute_is_function.arg_names = ["value"]

    def execute_is_boolean(self, exec_ctx):
        is_boolean = isinstance(exec_ctx.symbol_table.get("value"), Boolean)
        return RTResult().success(Boolean(1) if is_boolean else Boolean(0))
    execute_is_boolean.arg_names = ["value"]
    
    def execute_is_digit(self, exec_ctx):
        text = exec_ctx.symbol_table.get("value")
        
        if not isinstance(text, String):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "Argument must be string",
                exec_ctx
            ))
        
        # Verifica se a string contem apenas digitos usando isdigit()
        return RTResult().success(Boolean(1) if text.value.isdigit() else Boolean(0))
    execute_is_digit.arg_names = ["value"]
    
    def execute_append(self, exec_ctx):
        list_ = exec_ctx.symbol_table.get("list")
        value = exec_ctx.symbol_table.get("value")
        
        if not isinstance(list_, List):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "First argument must be list",
                exec_ctx
            ))
        list_.elements.append(value)
        return RTResult().success(Number.null)
    execute_append.arg_names = ["list", "value"]
    
    def execute_pop(self, exec_ctx):
        list_ = exec_ctx.symbol_table.get("list")
        index = exec_ctx.symbol_table.get("index")
        
        if not isinstance(list_, List):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "First argument must be list",
                exec_ctx
            ))
            
        if not isinstance(index, Number):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "Second argument must be number", 
                exec_ctx
            ))
            
        try:
            element = list_.elements.pop(index.value)
        except:
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                'Element at this index could not be removed from list because index is out of bounds',
                exec_ctx
            ))
        return RTResult().success(element)
    execute_pop.arg_names = ["list", "index"]
    
    def execute_extend(self, exec_ctx):
        listA = exec_ctx.symbol_table.get("listA")
        listB = exec_ctx.symbol_table.get("listB")
        
        if not isinstance(listA, List):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "First argument must be list",
                exec_ctx
            ))
            
        if not isinstance(listB, List):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "Second argument must be list", 
                exec_ctx
            ))
        listA.elements.extend(listB.elements)
        return RTResult().success(Number.null)
    execute_extend.arg_names = ["listA", "listB"]
    
    # funcao para obter o comprimento de uma lista
    def execute_len(self, exec_ctx):
        list_ = exec_ctx.symbol_table.get("list")
        
        if not isinstance(list_, List):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "Argument must be string",
                exec_ctx
            ))
        return RTResult().success(Number(len(list_.elements)))
    execute_len.arg_names = ["list"]
    
    
    def execute_run(self, exec_ctx):
        # Variavel com o nome do arquivo, nome esse que foi acrescentado na tabela de simbolos
        fn = exec_ctx.symbol_table.get("fn")
        
        if not isinstance(fn, String):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "Argument must be string",
                exec_ctx
            ))

        fn = fn.value
        
        # Tentando abrir o arquivo e ler o seu conteudo
        try:
            with open(fn, "r", encoding="utf-8") as f:
                script = f.read()
        except Exception as e:
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                f"Failed to load script \"{fn}\"\n" + str(e),
                exec_ctx
            ))

        _, error = run(fn, script)
        
        if error:
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                f"Failed to finish executing script \"{fn}\"\n" + 
                error.as_string(),
                exec_ctx
            ))
        
        return RTResult().success(Number.null)
    execute_run.arg_names = ["fn"]     # Argumento = nome do arquivo que estamos executando
    
    def execute_log10(self, exec_ctx):
        number = exec_ctx.symbol_table.get("value")
        
        if not isinstance(number, Number):
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "Argument must be a number",
                exec_ctx
            ))
        
        if number.value <= 0:
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                "Logarithm undefined for non-positive numbers",
                exec_ctx
            ))
        
        return RTResult().success(Number(math.log10(number.value)).set_context(exec_ctx))

    execute_log10.arg_names = ['value']
    
BuiltInFunction.print         = BuiltInFunction("print")
BuiltInFunction.print_ret     = BuiltInFunction("print_ret")
BuiltInFunction.print_inline = BuiltInFunction("print_inline")
BuiltInFunction.input         = BuiltInFunction("input")
BuiltInFunction.input_int     = BuiltInFunction("input_int")
BuiltInFunction.input_float   = BuiltInFunction("input_float")
BuiltInFunction.clear         = BuiltInFunction("clear")
BuiltInFunction.is_number     = BuiltInFunction("is_number")
BuiltInFunction.is_string     = BuiltInFunction("is_string")
BuiltInFunction.is_list       = BuiltInFunction("is_list")
BuiltInFunction.is_function   = BuiltInFunction("is_function")
BuiltInFunction.isdigit       = BuiltInFunction("is_digit")
BuiltInFunction.is_boolean    = BuiltInFunction("is_boolean")
BuiltInFunction.append        = BuiltInFunction("append")
BuiltInFunction.pop           = BuiltInFunction("pop")
BuiltInFunction.extend        = BuiltInFunction("extend")
BuiltInFunction.len           = BuiltInFunction("len")
BuiltInFunction.run           = BuiltInFunction("run")
BuiltInFunction.log10         = BuiltInFunction("log10")

##################################
# RUN
##################################

# Criando uma tabela de simbolos global
global_symbol_table = SymbolTable()
global_symbol_table.set("null", Number.null)
global_symbol_table.set("false", Number.false)
global_symbol_table.set("true", Number.true)
global_symbol_table.set("math_pi", Number.math_PI)
global_symbol_table.set("print", BuiltInFunction.print)
global_symbol_table.set("print_ret", BuiltInFunction.print_ret)
global_symbol_table.set("print_inline", BuiltInFunction.print_inline)
global_symbol_table.set("input", BuiltInFunction.input)
global_symbol_table.set("input_int", BuiltInFunction.input_int)
global_symbol_table.set("input_float", BuiltInFunction.input_float)
global_symbol_table.set("clear", BuiltInFunction.clear)
global_symbol_table.set("cls", BuiltInFunction.clear)
global_symbol_table.set("is_num", BuiltInFunction.is_number)
global_symbol_table.set("is_str", BuiltInFunction.is_string)
global_symbol_table.set("is_list", BuiltInFunction.is_list)
global_symbol_table.set("is_fun", BuiltInFunction.is_function)
global_symbol_table.set("is_digit", BuiltInFunction.isdigit)
global_symbol_table.set("is_boolean", BuiltInFunction.is_boolean)
global_symbol_table.set("append", BuiltInFunction.append)
global_symbol_table.set("pop", BuiltInFunction.pop)
global_symbol_table.set("extend", BuiltInFunction.extend)
global_symbol_table.set("len", BuiltInFunction.len)
global_symbol_table.set("run", BuiltInFunction.run)
global_symbol_table.set("log10", BuiltInFunction.log10)

# Funcao de execucao
def run(fn, text):
    # Gerando os tokens
    scanner = Scanner(fn, text)                        # Nova instancia do analisador lexico
    tokens, error = scanner.make_tokens()
    if error: return None, error                   # Verificando se houve algum erro antes de gerarmos a AST
    
    # Gerando a AST (Arvore Sintatica Abstrata)
    parser = Parser(tokens)                        # Criando um novo parser e passando os tokens
    ast = parser.parse()                           # Chamando o metodo parse()
    if ast.error: return None, ast.error           # Verificando se houve algum erro
    
    # Rodando o programa
    interpreter = Interpreter()                    # Nova instancia do interpretador
    context = Context('<program>')
    context.symbol_table = global_symbol_table
    result = interpreter.visit(ast.node, context)                    # Passando um no da AST
    
    return result.value, result.error              # Retornando a AST 