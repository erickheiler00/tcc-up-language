##################################
# SYMBOL TABLE
##################################

# Na tabela de simbolos ficara armazenada as variaveis que foram atribuidas
class SymbolTable:
    def __init__(self, parent=None):
        self.symbols = {}       # Dicionario de simbolos
        self.parent = parent    # Essa tabela de simbolos de funcao tera um pai como tabela de simbolos
                                # e essa sera a tabela de simbolos global, de modo que tera todas as 
                                # variaveis globais no codigo. Entao, eles podem ser acessados em qualquer
                                # lugar no codigo. Por isso precisamos acompanhar a tabela de simbolos pai

    # Metodo para obter o valor de uma variavel a partir do seu nome
    def get(self, name):
        value = self.symbols.get(name, None)
        
        # Verificando se o valor e None e se temos pais 
        # porque a tabela de simbolos global nao tera nenhum pai
        # porque sera a tabela de simbolos raiz
        if value == None and self.parent:   
            return self.parent.get(name)    # Se nao tiver um pai, podemos retornar o pai de autoinicializacao
                                            # no get so com o nome da variavel
        return value                        # Caso contrario apenas retornamos o valor

    def set(self, name, value):
        self.symbols[name] = value          # Definindo o nome da chave e o valor
    
    def remove(self, name):
        del self.symbols[name]
