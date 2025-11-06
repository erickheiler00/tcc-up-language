def buscaReversa(dic, valor_buscado):
    chaves_encontradas = []
    
    for chave in dic:
        valor = dic.get(chave)
        if valor == valor_buscado:
            chaves_encontradas.append(chave)
    
    return chaves_encontradas

def main():
    dic = {}
    continuar = True

    while continuar:
        chave = input("Digite uma chave para ser armazenada no dicionário (enter para parar): ")
        if chave == "": 
            continuar = False
            break
        
        valor = input("Digite um valor para ser armazenado no dicionário (enter para parar): ")
        
        dic[chave] = valor
        
    valor_buscado = input("\nPor fim, digite um valor a ser buscado: ")
    
    chaves_encontradas = buscaReversa(dic, valor_buscado)
    print("\nChaves que possuem o valor buscado:")
    print(chaves_encontradas)
    
if __name__ == "__main__":
    main()