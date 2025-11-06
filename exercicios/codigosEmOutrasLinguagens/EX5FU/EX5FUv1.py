# Primeiro número
num = int(input("Digite o 1º número inteiro positivo: "))
binario = []

if num == 0:
    print("Binário: 0")
else:
    while num > 0:
        binario.append(num % 2)
        num = num // 2
        
    print("Binário:", end=" ")
    
    for i in range(len(binario) - 1, -1, -1):
        print(binario[i], end="")
        
    print()

# Segundo número
num = int(input("Digite o 2º número inteiro positivo: "))
binario = []

if num == 0:
    print("Binário: 0")
else:
    while num > 0:
        binario.append(num % 2)
        num = num // 2
        
    print("Binário:", end=" ")
    
    for i in range(len(binario) - 1, -1, -1):
        print(binario[i], end="")
    
    print()

# Terceiro número
num = int(input("Digite o 3º número inteiro positivo: "))
binario = []

if num == 0:
    print("Binário: 0")
else:
    while num > 0:
        binario.append(num % 2)
        num = num // 2
    
    print("Binário:", end=" ")
    
    for i in range(len(binario) - 1, -1, -1):
        print(binario[i], end="")
    
    print()