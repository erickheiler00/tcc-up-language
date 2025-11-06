from strings_with_arrows import *
from core.lexer.lexer import *
from core.parser.nodes import *
from core.parser.parseResult import *
from core.errors.errors import *

####################################
# PARSER (ANALISADOR SINTATICO)
####################################

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.tok_idx = -1          # indice do token atual
        self.advance()
        
    def advance(self):
        self.tok_idx += 1
        self.update_current_tok()
        return self.current_tok
    
    def reverse(self, amount=1):
        # Pegamos o valor que temos que reverter e subtrair esse valor do indice do token
        self.tok_idx -= amount
        # Entao, tudo o que fazemos e apenas chamar update_current_tok() que atualiza a variavel do token atual
        self.update_current_tok()
        return self.current_tok
    
    def update_current_tok(self):
        if self.tok_idx >= 0 and self.tok_idx < len(self.tokens):
            self.current_tok = self.tokens[self.tok_idx]
    
    def parse(self):
        # Procurando por multiplas instrucoes
        res = self.statements()
        if not res.error and self.current_tok.type != TT_EOF:           # Verificando se nao houve erro e se nao chegou no fim do arquivo
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Token cannot appear after previous tokens"
            ))
        return res
    
    ###############################
    
    
    def statements(self):
        res = ParseResult()
        statements = []
        pos_start = self.current_tok.pos_start.copy()

        # Queremos pular qualquer numero de linhas no comeco
        while self.current_tok.type == TT_NEWLINE:
            res.register_advancement()
            self.advance()
        
        
        # Pegamos a primeira expressao e adicionamos ele na lista de instrucoes
        # Atualizacao = agora estamos procurando uma instrucao/statement ao invez de uma expressao
        statement = res.register(self.statement())
        if res.error: return res
        statements.append(statement)

        more_statements = True

        # Procurando novas expressoes separadas por novas linhas
        while True:
            newline_count = 0
            # Se o token for uma nova linha, pulamos essa nova linha
            while self.current_tok.type == TT_NEWLINE:
                res.register_advancement()
                self.advance()
                newline_count += 1
            # Precisamos de no minimo uma nova linha, por isso essa verificacao
            if newline_count == 0:
                more_statements = False

            # Se nao houver mais uma nova linha, sabemos que procuramos todas as instrucoes
            if not more_statements: break
            
            # Se chegou ao fim do arquivo, para
            if self.current_tok.type == TT_EOF:
                break
                
            statement = res.try_register(self.statement())
            # Verificando se a instrucao nao existe
            if not statement:
                # Se nao existir usamos o metodo reverse() -> contagem reversa que esta no resultado
                # Estamos fazendo isso porque queremos chamar esse metodo de expressao e o metodo de expressao
                # teria avancado algumas vezes, entao precisamos obter essa contagem reversa e reverter por essa quantia
                self.reverse(res.to_reverse_count)
                more_statements = False
                continue
            statements.append(statement)
        
        return res.success(ListNode(
            statements,
            pos_start,
            self.current_tok.pos_end.copy()
        ))
                
    def statement(self):
        res = ParseResult()
        pos_start = self.current_tok.pos_start.copy()
        
        if self.current_tok.matches(TT_KEYWORD, 'return'):
            res.register_advancement()
            self.advance()
            
            # Verificando se ha uma expressao apos o return
            expr = res.try_register(self.expr())
            if not expr:
                self.reverse(res.to_reverse_count)
            return res.success(ReturnNode(expr, pos_start, self.current_tok.pos_start.copy()))

        if self.current_tok.matches(TT_KEYWORD, 'continue'):
            res.register_advancement()
            self.advance()
            return res.success(ContinueNode(pos_start, self.current_tok.pos_start.copy()))
    
        if self.current_tok.matches(TT_KEYWORD, 'break'):
            res.register_advancement()
            self.advance()
            return res.success(BreakNode(pos_start, self.current_tok.pos_start.copy()))
    
        # Se nao encontrarmos nenhuma dessas palavras-chave estamos procurando por uma expressao normal
        expr = res.register(self.expr())
        if res.error:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected 'return', 'continue', 'break', 'if', 'for', 'while', 'fun', int, float, string, boolean, list, identifier, '+', '-', '(', '[' or 'not'"
            ))
        return res.success(expr)
    
    def expr(self):
        res = ParseResult()
        # Lista de tipos suportados
        TYPES = ['int', 'float', 'string', 'boolean', 'list']
        from core.lexer.tokens import TT_KEYWORD
        
        # Verificar se e uma declaracao tipada (tipo + identificador + =)
        if (self.current_tok.type == TT_KEYWORD and self.current_tok.value in TYPES and
            self.tok_idx + 1 < len(self.tokens) and 
            self.tokens[self.tok_idx + 1].type == TT_IDENTIFIER and
            self.tok_idx + 2 < len(self.tokens) and
            self.tokens[self.tok_idx + 2].type == TT_EQ):
            
            var_type = self.current_tok.value
            res.register_advancement()
            self.advance()
            
            var_name = self.current_tok
            res.register_advancement()
            self.advance()

            # O proximo token deve ser o sinal de igual (=)
            res.register_advancement()
            self.advance()

            # Captura o valor atribuido
            expr = res.register(self.expr())
            if res.error: return res
            
            # Verificacao de tipo
            expr_type = self.get_expr_type(expr)
            
            if expr_type == 'function_result':
                # Se for uma chamada de funcao, verificamos no runtime
                # Criamos um no especial que fara a verificacao durante a execucao
                return res.success(TypedVarAssignNode(var_name, expr, var_type))
            
            if not self.is_type_compatible(var_type, expr_type):
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    f"Type mismatch: cannot assign {expr_type} to {var_type}"
                ))
            return res.success(TypedVarAssignNode(var_name, expr, var_type))
        
        # Permitir reatribuicao para variaveis existentes (identificador + =)
        elif (self.current_tok.type == TT_IDENTIFIER and
            self.tok_idx + 1 < len(self.tokens) and
            self.tokens[self.tok_idx + 1].type == TT_EQ):
            
            var_name = self.current_tok
            res.register_advancement()
            self.advance()
            
            res.register_advancement()
            self.advance()
            
            expr = res.register(self.expr())
            if res.error: return res
            
            return res.success(VarAssignNode(var_name, expr))

        node = res.register(self.bin_op(self.comp_expr, ((TT_KEYWORD, 'and'), (TT_KEYWORD, 'or'))))
        if res.error:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected 'if', 'for', 'while', 'fun', int, float, list, identifier, '+', '-', '(', '[' or 'not'"
            ))
        return res.success(node)
    
    # Funcao para determinar o tipo de uma expressao
    def get_expr_type(self, node):
        from core.lexer.tokens import TT_KEYWORD
        from core.lexer.tokens import TT_EE, TT_NE, TT_LT, TT_GT, TT_LTE, TT_GTE, TT_PLUS, TT_MINUS
        from core.parser.nodes import VarAccessNode, IfNode, ForNode, WhileNode, CallNode, ListNode, FuncDefNode
        
        # Se for um token direto (NumberNode, StringNode, etc.)
        if hasattr(node, 'tok'):
            if node.tok.type == TT_KEYWORD:
                if isinstance(node.tok.value, int):
                    return 'int'
                elif isinstance(node.tok.value, float):
                    return 'float'
                elif isinstance(node.tok.value, tuple) and node.tok.value[0] == 'string_literal':
                    return 'string'
                elif node.tok.value in ['true', 'false']:
                    return 'boolean'
        
        # Se for acesso a variavel (VarAccessNode)
        elif isinstance(node, VarAccessNode):
            return 'variable'
        
        # Se for uma atribuicao tipada (TypedVarAssignNode)
        elif isinstance(node, TypedVarAssignNode):
            return node.var_type
        
        # Se for uma expressao if-then-else (IfNode)
        elif isinstance(node, IfNode):
            # Para if multi-linha, pega o tipo do primeiro bloco then
            if node.cases and len(node.cases) > 0:
                _, then_expr, _ = node.cases[0]
                then_type = self.get_expr_type(then_expr)
                # Se tem else, verifica se os tipos sao compativeis
                if node.else_case:
                    else_expr, _ = node.else_case
                    else_type = self.get_expr_type(else_expr)
                    # Se ambos sao do mesmo tipo, retorna esse tipo
                    if then_type == else_type:
                        return then_type
                    # Se envolve variaveis, deixa para o runtime
                    elif then_type == 'variable' or else_type == 'variable':
                        return 'variable'
                return then_type
            return 'unknown'
        
        # Se for um loop (ForNode, WhileNode) - retornam listas
        elif isinstance(node, (ForNode, WhileNode)):
            return 'list'
        
        # Se for uma chamada de funcao (CallNode)
        elif isinstance(node, CallNode):
            if isinstance(node.node_to_call, VarAccessNode):
                # Precisariamos acessar a tabela de simbolos aqui, o que e complicado no parser
                # Por isso, deixamos para o runtime
                return 'function_result'
            return 'function_result'  # Nao podemos determinar o tipo no parsing
        
        # Se for uma lista (ListNode)
        elif isinstance(node, ListNode):
            return 'list'
        
        # Se for uma definicao de funcao (FuncDefNode)
        elif isinstance(node, FuncDefNode):
            return 'function'
            # return node.return_type
        
        # Se for uma operacao binaria
        elif hasattr(node, 'op_tok') and hasattr(node, 'left_node'):
            # Operacoes de comparacao sempre retornam boolean
            if node.op_tok.type in [TT_EE, TT_NE, TT_LT, TT_GT, TT_LTE, TT_GTE]:
                return 'boolean'
            # Operacoes logicas (and, or) sempre retornam boolean
            elif node.op_tok.matches(TT_KEYWORD, 'and') or node.op_tok.matches(TT_KEYWORD, 'or'):
                return 'boolean'
            # Para outras operacoes (+, -, *, /, ^), o tipo depende dos operandos
            else:
                left_type = self.get_expr_type(node.left_node)
                right_type = self.get_expr_type(node.right_node)
                # Se qualquer operando for float, o resultado é float
                if left_type == 'float' or right_type == 'float':
                    return 'float'
                # Se ambos forem int, o resultado é int
                elif left_type == 'int' and right_type == 'int':
                    return 'int'
                # Para string + string = string
                elif left_type == 'string' and right_type == 'string' and node.op_tok.type == TT_PLUS:
                    return 'string'
                # Se envolve variaveis, não podemos determinar o tipo exato no parsing
                elif left_type == 'variable' or right_type == 'variable':
                    return 'variable'
        
        # Se for uma operacao unaria
        elif hasattr(node, 'op_tok') and hasattr(node, 'node'):
            # Operacao 'not' sempre retorna boolean
            if node.op_tok.matches(TT_KEYWORD, 'not'):
                return 'boolean'
            # Operacao de negativo mantem o tipo
            elif node.op_tok.type == TT_MINUS:
                return self.get_expr_type(node.node)
        
        # Para outros tipos de nós
        return 'unknown'

    # Verifica se um tipo de expressao e compativel com o tipo da variavel
    def is_type_compatible(self, var_type, expr_type):
        if var_type == 'boolean' and expr_type == 'boolean':
            return True
        #elif var_type == 'int' and expr_type in ['int', 'boolean']:  # int pode receber boolean
        elif var_type == 'int' and expr_type == 'int':  # int NAO pode receber boolean
            return True
        elif var_type == 'float' and expr_type == 'float':
            return True
        elif var_type == 'string' and expr_type == 'string':
            return True
        elif var_type == 'list' and expr_type == 'list':
            return True
        elif var_type == 'function' and expr_type == 'function':
            return True
        # Permitir atribuicao de variaveis e resultados de funcoes (verificacao no runtime)
        elif expr_type in ['variable', 'function_result']:
            return True
        return False
    
    def comp_expr(self):
        res = ParseResult()
    
        # Verificando se o token atual possui o valor 'not'
        # Se for, atribuiremos o token atual a uma variavel
        if self.current_tok.matches(TT_KEYWORD, 'not'):
            op_tok = self.current_tok
            res.register_advancement()                  # Avancamos
            self.advance()
            
            node = res.register(self.comp_expr())       # Expressao de comparacao completamente nova
            if res.error: return res
            return res.success(UnaryOpNode(op_tok, node))

        # Tenta fazer parse de uma expressao in primeiro
        node = res.register(self.in_expr())

        if res.error:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected int, float, identifier, '+', '-', '(', '[', 'if', 'for', 'while', 'fun' or 'not'"
            ))
        
        return res.success(node)
    
    def in_expr(self):
        res = ParseResult()
    
        # Parse da expressao aritmetica
        node = res.register(self.bin_op(self.arith_expr, (TT_EE, TT_NE, TT_LT, TT_GT, TT_LTE, TT_GTE)))
        if res.error: return res
        
        # Verifica se ha a palavra-chave 'in'
        if self.current_tok.matches(TT_KEYWORD, 'in'):
            res.register_advancement()
            self.advance()
            
            # Parse do container (lista ou string)
            container = res.register(self.arith_expr())
            if res.error: return res
            
            # Retorna um InNode
            return res.success(InNode(node, container))
        
        return res.success(node)
    
    def arith_expr(self):
        return self.bin_op(self.term, (TT_PLUS, TT_MINUS))
    
    def term(self):
        return self.bin_op(self.factor, (TT_MUL, TT_DIV, TT_INTDIV, TT_MOD))
    
    def factor(self):
        res = ParseResult()                  # Nova instancia do ParseResult
        tok = self.current_tok               # Token atual que sera analisado
        
        # Para casos em que comecarmos com -5, por exemplo
        if tok.type in (TT_PLUS, TT_MINUS):
            res.register_advancement()
            self.advance()            # Sempre que chamarmos advance() vamos envolve-lo no metodo register()
            factor = res.register(self.factor())    # factor() é chamado para analisar a expressao que segue o operador (+ ou -), 
                                                    # queremos pegar o numero depois do sinal
            if res.error: return res
            return res.success(UnaryOpNode(tok, factor))    # Se a analise foi bem-sucedida, um no de operador unario é criado 
                                                            # Com o operador atual (tok) e o fator analisado (factor)
        return self.power()
    
    def power(self):
        return self.bin_op(self.call, (TT_POW, ), self.factor)
    
    def call(self):
        res = ParseResult()
        # Pegando o atom
        atom = res.register(self.atom())
        if res.error: return res
        
        # Procurando por um parenteses esquerdo
        if self.current_tok.type == TT_LPAREN:
            res.register_advancement()
            self.advance()
            arg_nodes = []
            
            # Verificando se ha um parenteses direito
            if self.current_tok.type == TT_RPAREN:
                res.register_advancement()
                self.advance()
            # Se nao houver, procuramos uma expressao 
            else:
                arg_nodes.append(res.register(self.expr()))
                if res.error:   
                    return res.failure(InvalidSyntaxError(
                        self.current_tok.pos_start, self.current_tok.pos_end,
                        "Expected ')', 'if', 'for', 'while', 'fun', int, float, string, boolean, list, identifier, '+', '-', '(', '[' or 'not'"
                    ))
                
                # Verificando se ha uma virgula depois da expressao
                while self.current_tok.type == TT_COMMA:
                    res.register_advancement()
                    self.advance()
                    
                    arg_nodes.append(res.register(self.expr()))
                    if res.error: return res
                
                # Procurando por um parenteses direito
                if self.current_tok.type != TT_RPAREN:
                    return res.failure(InvalidSyntaxError(
                        self.current_tok.pos_start, self.current_tok.pos_end,
                        f"Expected ',' or ')'"
                    ))
                
                res.register_advancement()
                self.advance()
            return res.success(CallNode(atom, arg_nodes))
        return res.success(atom)
    
    def atom(self):
        res = ParseResult()
        tok = self.current_tok
        
        if tok.type in TT_KEYWORD and isinstance(tok.value, (int, float)):      # Verificando se e INT ou FLOAT
            res.register_advancement()
            self.advance()
            return res.success(NumberNode(tok))   # Tambem retornamos um no numerico desse token

        elif tok.type == TT_KEYWORD and isinstance(tok.value, tuple) and tok.value[0] == 'string_literal':
            res.register_advancement()
            self.advance()
            return res.success(StringNode(tok))   

        elif tok.type == TT_IDENTIFIER:
            res.register_advancement()
            self.advance()            # Se for um identificador podemos avancar para o proximo token
            return res.success(VarAccessNode(tok))  # Retornamos um no de variavel desse token

        elif tok.matches(TT_KEYWORD, 'true') or tok.matches(TT_KEYWORD, 'false'):      # Tratamento para booleanos
            res.register_advancement()
            self.advance()
            return res.success(BooleanNode(tok))  

        # Para casos em que mudamos a ordem das operacoes
        elif tok.type == TT_LPAREN:
            res.register_advancement()
            self.advance()             # Avancamos
            expr = res.register(self.expr())         # Pegamos uma nova expressao
            if res.error: return res
            if self.current_tok.type == TT_RPAREN:   # Precisamos procurar um parenteses direito
                res.register_advancement()
                self.advance()
                return res.success(expr)
            else:
                return res.failure(InvalidSyntaxError(
					self.current_tok.pos_start, self.current_tok.pos_end,
					"Expected ')'"
				))

        elif tok.type == TT_LSQUARE:
            list_expr = res.register(self.list_expr())
            if res.error: return res
            return res.success(list_expr)

        elif tok.matches(TT_KEYWORD, 'if'):
            if_expr = res.register(self.if_expr())
            if res.error: return res
            return res.success(if_expr)
        
        elif tok.matches(TT_KEYWORD, 'for'):
            for_expr = res.register(self.for_expr())
            if res.error: return res
            return res.success(for_expr)

        elif tok.matches(TT_KEYWORD, 'while'):
            while_expr = res.register(self.while_expr())
            if res.error: return res
            return res.success(while_expr)

        elif tok.matches(TT_KEYWORD, 'fun'):
            func_def = res.register(self.func_def())
            if res.error: return res
            return res.success(func_def)

        return res.failure(InvalidSyntaxError(
            tok.pos_start, tok.pos_end,
            "Expected int, float, identifier, '+', '-', '(', '[', 'if', 'for', 'while', 'fun'"
        ))
    
    def list_expr(self):
        res = ParseResult()
        element_nodes = []
        pos_start = self.current_tok.pos_start.copy()
        
        # Procurando por um colchete esquerdo
        if self.current_tok.type != TT_LSQUARE:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                f"Expected '['"
            ))
            
        res.register_advancement()
        self.advance()
        
        # Procurando por um colchete direito -> para o caso de lista vazia
        if self.current_tok.type == TT_RSQUARE:
            res.register_advancement()
            self.advance()
        # Se nao houver, procuramos uma expressao
        else:
            element_nodes.append(res.register(self.expr()))
            if res.error:   
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected ']', 'if', 'for', 'while', 'fun', int, float, string, boolean, list, identifier, '+', '-', '(', '[' or 'not'"
                ))
                
            # Verificando se ha uma virgula depois da expressao
            while self.current_tok.type == TT_COMMA:
                res.register_advancement()
                self.advance()
                
                element_nodes.append(res.register(self.expr()))
                if res.error: return res
            
            # Procurando por um parenteses direito
            if self.current_tok.type != TT_RSQUARE:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    f"Expected ',' or ']'"
                ))
            
            res.register_advancement()
            self.advance()
        
        return res.success(ListNode(
            element_nodes, 
            pos_start,
            self.current_tok.pos_end.copy()
        ))

    def if_expr(self):
        res = ParseResult()
        all_cases = res.register(self.if_expr_cases('if'))
        if res.error: return res
        cases, else_case = all_cases
        return res.success(IfNode(cases, else_case))

    def if_expr_b(self):
        return self.if_expr_cases('elif')
    
    def if_expr_c(self):
        res = ParseResult()
        else_case = None
        
        # Verificando se ha a palavra-chave else
        if self.current_tok.matches(TT_KEYWORD, 'else'):
            res.register_advancement()
            self.advance()
            
            # Verificando se ha uma nova linha
            if self.current_tok.type == TT_NEWLINE:
                res.register_advancement()
                self.advance()
                
                # Se houver, procuramos as declaracoes
                statements = res.register(self.statements())
                if res.error: return res
                else_case = (statements, True)

                # Procurando a palavra-chave endif
                if self.current_tok.matches(TT_KEYWORD, 'endif'):
                    res.register_advancement()
                    self.advance()
                else:
                    return res.failure(InvalidSyntaxError(
                        self.current_tok.pos_start, self.current_tok.pos_end,
                        "Expected 'endif'"
                    ))
            # Caso nao haja uma nova linha, fazemos como antes
            else:
                # Obtemos uma expressao unica, verificamos se ha erro e atribuimos essa expressao ao else_case
                expr = res.register(self.statement())
                if res.error: return res
                else_case = (expr, False)
            
        return res.success(else_case)

    def if_expr_b_or_c(self):
        res = ParseResult()
        cases, else_case = [], None
        
        # Verificando se existe um elif (expr_b)
        if self.current_tok.matches(TT_KEYWORD, 'elif'):
            all_cases = res.register(self.if_expr_b())
            if res.error: return res
            cases, else_case = all_cases
        # Caso contrario, e um else (expr_c)
        else:
            else_case = res.register(self.if_expr_c())
            if res.error: return res
            
        return res.success((cases, else_case))

    def if_expr_cases(self, case_keyword):
        res = ParseResult()
        cases = []
        
        # Verifica palavra-chave (if/elif)
        if not self.current_tok.matches(TT_KEYWORD, case_keyword):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                f"Expected '{case_keyword}'"
            ))
        
        res.register_advancement()
        self.advance()
        
        # Parse da condicao
        condition = res.register(self.expr())
        if res.error: return res
        
        # Verifica 'then'
        if not self.current_tok.matches(TT_KEYWORD, 'then'):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected 'then'"
            ))
        
        res.register_advancement()
        self.advance()
        
        # Decisao baseada em quebra de linha
        if self.current_tok.type == TT_NEWLINE:
            return self._handle_multiline_if(res, condition, cases)
        else:
            return self._handle_inline_if(res, condition, cases)

    # Processa if com quebras de linha e blocos
    def _handle_multiline_if(self, res, condition, cases):
        res.register_advancement()
        self.advance()
        
        # Parse do bloco de statements
        statements = res.register(self.statements())
        if res.error: return res
        cases.append((condition, statements, True))
        
        # Inicializa else_case como None
        else_case = None
        
        # Processa else/elif/endif
        while True:
            if self.current_tok.matches(TT_KEYWORD, 'endif'):
                res.register_advancement()
                self.advance()
                break
            elif self.current_tok.matches(TT_KEYWORD, 'else'):
                else_case = self._parse_else_block(res)
                if res.error: return res
                # Apos else multilinha, deve vir endif
                if else_case and else_case[1]:  # Se for multilinha (True)
                    if not self.current_tok.matches(TT_KEYWORD, 'endif'):
                        return res.failure(InvalidSyntaxError(
                            self.current_tok.pos_start, self.current_tok.pos_end,
                            "Expected 'endif' after multiline else block"
                        ))
                    res.register_advancement()
                    self.advance()
                break
            elif self.current_tok.matches(TT_KEYWORD, 'elif'):
                # Recursao para processar elif
                all_cases = res.register(self.if_expr_cases('elif'))
                if res.error: return res
                new_cases, new_else = all_cases
                cases.extend(new_cases)
                if new_else:
                    else_case = new_else
                break
            else:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected 'else', 'elif' or 'endif'"
                ))
        
        return res.success((cases, else_case))

    # Processa if inline (sem quebras de linha)
    def _handle_inline_if(self, res, condition, cases):
        # Parse da expressao unica
        expr = res.register(self.statement())
        if res.error: return res
        cases.append((condition, expr, False))
        
        # Verifica se ha endif opcional
        if self.current_tok.matches(TT_KEYWORD, 'endif'):
            res.register_advancement()
            self.advance()
            return res.success((cases, None))
        
        # Caso contrario, usa a logica original para else/elif
        all_cases = res.register(self.if_expr_b_or_c())
        if res.error: return res
        new_cases, else_case = all_cases
        cases.extend(new_cases)
        
        return res.success((cases, else_case))

    # Helper para processar bloco else
    def _parse_else_block(self, res):
        res.register_advancement()
        self.advance()
        
        if self.current_tok.type == TT_NEWLINE:
            res.register_advancement()
            self.advance()
            else_statements = res.register(self.statements())
            if res.error: return None
            return (else_statements, True)
        else:
            else_expr = res.register(self.statement())
            if res.error: return None
            return (else_expr, False)
    
    def for_expr(self):
        res = ParseResult()
        
        # Se nao encontrarmos a palavra-chave for, retornamos um erro
        if not self.current_tok.matches(TT_KEYWORD, 'for'):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end, 
                f"Expected 'for'"
            ))
        
        # Se encontrarmos, avancamos
        res.register_advancement()
        self.advance()

        # Procuramos um identificador
        if self.current_tok.type != TT_IDENTIFIER:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                f"Expected identifier"
            ))
        
        # Se encontrarmos, o atribuiremos ao nome da variavel e, em seguida, avancamos
        var_name = self.current_tok
        res.register_advancement()
        self.advance()

        if self.current_tok.matches(TT_KEYWORD, 'in'):
            # For-in loop (iterar sobre string/lista)
            res.register_advancement()
            self.advance()
            
            iterable = res.register(self.expr())
            if res.error: return res
            
            if not self.current_tok.matches(TT_KEYWORD, 'do'):
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    f"Expected 'do'"
                ))
            
            res.register_advancement()
            self.advance()
            
            if self.current_tok.type == TT_NEWLINE:
                res.register_advancement()
                self.advance()
                
                body = res.register(self.statements())
                if res.error: return res
                
                if not self.current_tok.matches(TT_KEYWORD, 'endfor'):
                    return res.failure(InvalidSyntaxError(
                        self.current_tok.pos_start, self.current_tok.pos_end,
                        f"Expected 'endfor'"
                    ))
            
                res.register_advancement()
                self.advance()
                
                return res.success(ForInNode(var_name, iterable, body, True))
            
            body = res.register(self.statement())
            if res.error: return res
            
            return res.success(ForInNode(var_name, iterable, body, False))

        # Procuramos um sinal de igual
        if self.current_tok.type != TT_EQ:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                f"Expected '='"
            ))
        
        # Avancamos
        res.register_advancement()
        self.advance()
        
        # Obtemos o nosso valor inicial do contador do for
        start_value = res.register(self.expr())
        if res.error: return res
        
        # Procuramos pela palavra-chave to
        if not self.current_tok.matches(TT_KEYWORD, 'to'):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                f"Expected 'to'"
            ))
        
        # Avancamos
        res.register_advancement()
        self.advance()
        
        # Obtermos o valor final do contador do for
        end_value = res.register(self.expr())
        if res.error: return res
        
        # Procuramos pela palavra-chave step
        if self.current_tok.matches(TT_KEYWORD, 'step'):
            # Se houver, avancamos
            res.register_advancement()
            self.advance()
            
            # Entao, obtemos o valor do step
            step_value = res.register(self.expr())
            if res.error: return res
        else:
            step_value = None
        
        # Procuramos pela palavra chave do
        if not self.current_tok.matches(TT_KEYWORD, 'do'):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                f"Expected 'do'"
            ))
        
        # Avancamos
        res.register_advancement()
        self.advance()
        
        # Verificando se ha uma nova linha
        if self.current_tok.type == TT_NEWLINE:
            res.register_advancement()
            self.advance()
            
            body = res.register(self.statements())
            if res.error: return res
            
            if not self.current_tok.matches(TT_KEYWORD, 'endfor'):
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    f"Expected 'endfor'"
                ))
        
            res.register_advancement()
            self.advance()
            
            return res.success(ForNode(var_name, start_value, end_value, step_value, body, True))
        
        body = res.register(self.statement())
        if res.error: return res

        return res.success(ForNode(var_name, start_value, end_value, step_value, body, False))
        
    def while_expr(self):
        res = ParseResult()
        
        # Procuramos a palavra-chave while
        if not self.current_tok.matches(TT_KEYWORD, 'while'):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                f"Expected 'while'"
            ))
            
        # Se encontrarmos, avancamos
        res.register_advancement()
        self.advance()
        
        # Obtemos a condicao do while
        condition = res.register(self.expr())
        if res.error: return res
        
        # Procuramos a palavra-chave do
        if not self.current_tok.matches(TT_KEYWORD, 'do'):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                f"Expected 'do'"
            ))
    
        # Avancamos
        res.register_advancement()
        self.advance()
        
        # Verificando se ha uma nova linha
        if self.current_tok.type == TT_NEWLINE:
            res.register_advancement()
            self.advance()

            body = res.register(self.statements())
            if res.error: return res

            if not self.current_tok.matches(TT_KEYWORD, 'endwhile'):
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    f"Expected 'endwhile'"
                ))

            res.register_advancement()
            self.advance()

            return res.success(WhileNode(condition, body, True))
        
        body = res.register(self.statement())
        if res.error: return res

        return res.success(WhileNode(condition, body, False))
    
    def func_def(self):
        res = ParseResult()
    
        # Procuramos a palavra-chave fun
        if not self.current_tok.matches(TT_KEYWORD, 'fun'):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                f"Expected 'fun'"
            ))
        
        # Avancamos
        res.register_advancement()
        self.advance()
        
        # Procuramos um identificador (nome da funcao) ou colocamos None para funcao anonima
        if self.current_tok.type == TT_IDENTIFIER:
            var_name_tok = self.current_tok
            res.register_advancement()
            self.advance()
        else:
            var_name_tok = None  # funcao anonima
        
        # Procuramos um parenteses esquerdo para os parametros
        if self.current_tok.type != TT_LPAREN:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                f"Expected '('"
            ))
        
        # Avancamos
        res.register_advancement()
        self.advance()
        
        # Lista de nomes e tipos de argumentos
        arg_name_toks = []
        arg_types = []
        
        # Parse parametros: tipo nome, tipo nome, ...
        if self.current_tok.type == TT_KEYWORD and self.current_tok.value in ['int', 'float', 'string', 'boolean', 'list', 'function']:
            # Primeiro tipo
            arg_types.append(self.current_tok.value)
            res.register_advancement()
            self.advance()
            
            # Nome do parametro
            if self.current_tok.type != TT_IDENTIFIER:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    f"Expected parameter name"
                ))
            arg_name_toks.append(self.current_tok)
            res.register_advancement()
            self.advance()
            
            # Outros parametros
            while self.current_tok.type == TT_COMMA:
                res.register_advancement()
                self.advance()
                
                # Tipo
                if not (self.current_tok.type == TT_KEYWORD and 
                        self.current_tok.value in ['int', 'float', 'string', 'boolean', 'list', 'function']):
                    return res.failure(InvalidSyntaxError(
                        self.current_tok.pos_start, self.current_tok.pos_end,
                        f"Expected parameter type"
                    ))
                arg_types.append(self.current_tok.value)
                res.register_advancement()
                self.advance()
                
                # Nome
                if self.current_tok.type != TT_IDENTIFIER:
                    return res.failure(InvalidSyntaxError(
                        self.current_tok.pos_start, self.current_tok.pos_end,
                        f"Expected parameter name"
                    ))
                arg_name_toks.append(self.current_tok)
                res.register_advancement()
                self.advance()
        
        # Procuramos parenteses direito
        if self.current_tok.type != TT_RPAREN:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                f"Expected ')'"
            ))
        
        # Avancamos
        res.register_advancement()
        self.advance()
        
        # Procuramos seta obrigatoria '->'
        if self.current_tok.type != TT_ARROW:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                f"Expected '->'"
            ))
        
        # Avancamos
        res.register_advancement()
        self.advance()
        
        # Tipo de retorno
        if not (self.current_tok.type == TT_KEYWORD and 
                self.current_tok.value in ['int', 'float', 'string', 'boolean', 'list', 'void']):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                f"Expected return type"
            ))
        
        return_type = self.current_tok.value
        res.register_advancement()
        self.advance()
        
        # Verificar se e inline ou multilinhas
        if self.current_tok.type == TT_NEWLINE:
            # Multilinhas
            res.register_advancement()
            self.advance()
            
            body = res.register(self.statements())
            if res.error: return res
            
            # Procuramos 'endfun'
            if not self.current_tok.matches(TT_KEYWORD, 'endfun'):
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    f"Expected 'endfun'"
                ))
            
            res.register_advancement()
            self.advance()
            
            return res.success(FuncDefNode(var_name_tok, arg_name_toks, arg_types, return_type, body, False))
        else:
            # Inline - deve ter return explicito
            if not self.current_tok.matches(TT_KEYWORD, 'return'):
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    f"Expected 'return' for inline function"
                ))
            
            res.register_advancement()
            self.advance()
            
            body = res.register(self.expr())
            if res.error: return res
            
            return res.success(FuncDefNode(var_name_tok, arg_name_toks, arg_types, return_type, body, True))

    ###############################
    
    """
        Diferencas entre as funcoes term e expr: 
        
        Em uma eu procuro um termo e na outra um fator
        Em uma eu procuro por mais ou menos e na outra por multiplicacao ou divisao
        
        Entao, criamos a funcao bin_op para resolver ambos os problemas de uma vez
    """
    def bin_op(self, func_a, ops, func_b=None):                    # func = funcao, ops = operacoes
        if func_b == None:
            func_b = func_a
    
        res = ParseResult()                                       # Nova instancia do ParseResult
        left = res.register(func_a())                               # Pegando fator da esquerda
        if res.error: return res
        
        while self.current_tok.type in ops or (self.current_tok.type, self.current_tok.value) in ops:
            op_tok = self.current_tok
            res.register_advancement()
            self.advance()
            right = res.register(func_b())
            if res.error: return res
            left = BinOpNode(left, op_tok, right)                # Fator da esquerda, token da operacao, fator da direita
        
        return res.success(left)                                 # Left agora e um no de operacao binaria
