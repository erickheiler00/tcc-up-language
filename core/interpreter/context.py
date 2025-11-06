##################################
# CONTEXT
##################################

# Classe que ira conter o contexto atual do programa
# Se um erro aconteceu na funcao /0, por exemplo, ele nos mostrara o rastreamento voltando por todas as funcoes anteriores
class Context:
    # Parent seria o contexto inteiro e parent_entry_pos seria uma posicao especifica onde o contexto mudou para fazer algo - funcao /0
    def __init__(self, display_name, parent=None, parent_entry_pos=None):
        self.display_name = display_name
        self.parent = parent
        self.parent_entry_pos = parent_entry_pos
        self.symbol_table = None
