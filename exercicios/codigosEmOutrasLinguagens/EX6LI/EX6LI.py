def divisores(num):
    lista_divisores = []
    for i in range(1,num+1):    
        if num % i == 0:
            lista_divisores.append(i)
    return lista_divisores

def main():
    num = int(input("Digite um número para saber seus divisores: "))
    
    lista_divisores = divisores(num)
    print(f"Os divisores do número {num} são: {lista_divisores}")
    
if __name__ == "__main__":
    main()