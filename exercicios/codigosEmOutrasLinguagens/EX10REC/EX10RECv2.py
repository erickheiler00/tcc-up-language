def exibir_invertido(n):
    if n == 0:
        return
    
    numero = int(input())
    exibir_invertido(n - 1)
    print(numero)

def main():
    n = int(input("Quantos números você deseja informar? "))
    
    print("Digite os números e veja-os na ordem inversa:")
    exibir_invertido(n)

if __name__ == "__main__":
    main()