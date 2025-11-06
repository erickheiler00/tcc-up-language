def main():
    n = int(input("Quantos números você deseja informar? "))

    numeros = []

    print("Digite os números:")
    for _ in range(n):
        numero = int(input())
        numeros.append(numero)

    print("\nOrdem inversa:")
    for i in range(n - 1, -1, -1):
        print(numeros[i])

if __name__ == "__main__":
    main()