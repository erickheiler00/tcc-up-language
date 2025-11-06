a = int(input("Digite o primeiro número: "))
b = int(input("Digite o segundo número: "))
c = int(input("Digite o terceiro número: "))

if a <= b <= c:
    print("Números em ordem crescente:", a, b, c)

elif a <= c <= b:
    print("Números em ordem crescente:", a, c, b)

elif b <= c <= a:
    print("Números em ordem crescente:", b, c, a)

elif c <= a <= b:
    print("Números em ordem crescente:", c, a, b)
    
elif c <= b <= a:
    print("Números em ordem crescente:", c, b, a)

else:
    print("Números em ordem crescente:", b, a, c)