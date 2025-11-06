def decimalParaBinario(num):
    binario = []

    if num == 0:
        print("Binário: 0")
        return

    while num > 0:
        binario.append(num % 2)
        num = num // 2

    print("Binário:", end=" ")
    
    for i in range(len(binario) - 1, -1, -1):
        print(binario[i], end="")
        
    print()

num = int(input("Digite o 1º número inteiro positivo: "))
decimalParaBinario(num)

num = int(input("Digite o 2º número inteiro positivo: "))
decimalParaBinario(num)

num = int(input("Digite o 3º número inteiro positivo: "))
decimalParaBinario(num)