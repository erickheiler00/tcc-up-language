####################################
# PARSE RESULT
####################################

# Classe para verificar se ha algum erro e monitorar o no
# Para nao precisar retornar um no em cada funcao 
class ParseResult:
    def __init__(self):
        self.error = None
        self.node = None
        self.last_registered_advance_count = 0
        self.advance_count = 0      # Contar quantas vezes avancamos nessa funcao especifica
        self.to_reverse_count = 0

    # Metodo para registrar avanco        
    def register_advancement(self):
        self.last_registered_advance_count = 1
        self.advance_count += 1
    
    def register(self, res):
        self.last_registered_advance_count = res.advance_count
        self.advance_count += res.advance_count
        if res.error: self.error = res.error   # Verificando se tem um erro
        return res.node                        # Retornando o resultado como um no

    def try_register(self, res):
        if res.error:
            self.to_reverse_count = res.advance_count
            return None
        return self.register(res)

    def success(self, node):
        self.node = node
        return self
    
    def failure(self, error):
        if not self.error or self.last_registered_advance_count == 0:  # Se deu erro ou se nao avancamos desde entao
            self.error = error
        return self
