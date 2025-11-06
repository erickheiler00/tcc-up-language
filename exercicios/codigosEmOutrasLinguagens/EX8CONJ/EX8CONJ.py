def letras_unicas(palavra):
    conjunto = set()
    
    for caractere in palavra:
        if caractere not in conjunto:
            conjunto.add(caractere)
        else:
            return False
        
    return True        

def main():
    palavra = input("Digite uma palavra: ")

    print(letras_unicas(palavra))

if __name__ == "__main__":
    main()