def tokenizacao(expressao):
    lista_tokens = []
    nova_expressao = ""
    num = ""
    caractere_ant = ""
    
    for caractere in expressao:
        if caractere != " ":
            nova_expressao += caractere
            
    for caractere in nova_expressao:
        if caractere == "(" or caractere == ")" or caractere == "*" or caractere == "/" or caractere == "^":
            if num != "":
                lista_tokens.append(num)
                num = ""
            lista_tokens.append(caractere)
        elif (caractere == "+" or caractere == "-") and (caractere_ant.isdigit() or caractere_ant == ")"):
            if caractere_ant.isdigit() or caractere_ant == ")":
                if num != "":
                    lista_tokens.append(num)
                    num = ""
                lista_tokens.append(caractere)
        else:
            num += caractere
            
        caractere_ant = caractere
        
    if num !="":
        lista_tokens.append(num)
        
    return lista_tokens

def main():
    expressao = input("Digite uma expressão matemática: ")
    lista_tokens = tokenizacao(expressao)
    print(lista_tokens)

if __name__ == "__main__":
    main()